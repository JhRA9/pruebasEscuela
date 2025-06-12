from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

# Un contador global para asegurar nombres de materias únicos a través de todas las instancias de Locust
global_materia_unique_id_perf = 0

class EliminarMateriaPerformanceTest(HttpUser):
    # Tiempo de espera entre tareas (simula pausas de usuario)
    wait_time = between(1, 3)

    host = "http://localhost/proyectoEscuela"

    # Credenciales de admin
    ADMIN_EMAIL = "admin@admin.com"
    ADMIN_PASSWORD = "123"

    def on_start(self):
        """ Se ejecuta al inicio de cada usuario virtual """
        self.login()

    def login(self):
        """ Tarea para iniciar sesión. """
        login_page_response = self.client.get("/index.php", name="/login_page_load")
        
        soup = BeautifulSoup(login_page_response.text, 'html.parser')
        form_data = {}
        for input_tag in soup.find_all('input', type='hidden'):
            if input_tag.get('name') and input_tag.get('value'):
                form_data[input_tag.get('name')] = input_tag.get('value')

        form_data["email"] = self.ADMIN_EMAIL
        form_data["password"] = self.ADMIN_PASSWORD

        login_process_response = self.client.post(
            "/controler_login.php",
            data=form_data,
            name="/login_process",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if "admin" not in login_process_response.url:
            print(f"Fallo en el login para {self.ADMIN_EMAIL}. Status: {login_process_response.status_code}, URL: {login_process_response.url}")
            self.environment.runner.quit() 
        else:
            print(f"Login exitoso como {self.ADMIN_EMAIL}.")

    @task(1) # Cada tarea simula un flujo completo de creación-eliminación
    def create_and_delete_materia_performance(self):
        """ Simula la creación de una materia y su posterior eliminación, midiendo el rendimiento. """
        
        global global_materia_unique_id_perf
        global_materia_unique_id_perf += 1
        
        materia_name = f"MateriaPerf_{global_materia_unique_id_perf}_{int(time.time())}"
        materia_description = f"Descripción para {materia_name}"

        # --- 1. GET el formulario de creación de materia ---
        # Envuelve en try-except para capturar fallos aquí
        try:
            create_materia_form_response = self.client.get("/admin/materias/create.php", name="/admin/materias/create_form_load")
            create_materia_form_response.raise_for_status() # Lanza excepción si el status no es 2xx
        except Exception as e:
            print(f"ERROR: Fallo al cargar el formulario de creación de materia: {e}")
            return # Detener el flujo si falla esta parte
        
        soup_create = BeautifulSoup(create_materia_form_response.text, 'html.parser')
        
        create_form_data = {}
        for input_tag in soup_create.find_all(['input', 'textarea', 'select']):
            name = input_tag.get('name')
            value = input_tag.get('value')
            if name:
                if input_tag.name == 'select':
                    selected_option = input_tag.find('option', selected=True)
                    if selected_option:
                        create_form_data[name] = selected_option.get('value')
                    elif input_tag.find('option'):
                         create_form_data[name] = input_tag.find('option').get('value')
                else:
                    create_form_data[name] = value if value is not None else ''

        create_form_data["nombre_materia"] = materia_name
        create_form_data["descripcion"] = materia_description
        
        # --- 2. POST la solicitud para crear la materia ---
        try:
            create_post_response = self.client.post("/config/controllers/materias/create.php",
                                                     data=create_form_data,
                                                     name="/admin/materias/create_post",
                                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
            create_post_response.raise_for_status() # Lanza excepción si el status no es 2xx
        except Exception as e:
            print(f"ERROR: Fallo al crear la materia '{materia_name}': {e}")
            return # Detener el flujo si falla esta parte

        # --- 3. Eliminar la materia recién creada ---
        # Ir al listado de materias para encontrar el ID de la materia creada
        try:
            list_materias_response = self.client.get("/admin/materias/index.php", name="/admin/materias/list_for_delete")
            list_materias_response.raise_for_status() # Lanza excepción si el status no es 2xx
        except Exception as e:
            print(f"ERROR: Fallo al cargar la lista de materias para eliminación: {e}")
            return # Detener el flujo si falla esta parte
        
        # AUMENTAR EL TIEMPO DE ESPERA AQUÍ A UN VALOR MAYOR PARA DATATABLES EN CARGA ALTA
        # Probaremos con 5 segundos, ya que 3 fue insuficiente.
        time.sleep(5) 

        soup_list = BeautifulSoup(list_materias_response.text, 'html.parser')
        
        materia_id_to_delete = None
        
        # Búsqueda más específica y robusta de la fila por su ID o por su contenido
        materia_name_stripped_lower = materia_name.strip().lower()

        found_row = None
        for row in soup_list.find_all('tr'):
            materia_cell = row.find_all('td')
            if len(materia_cell) > 1:
                cell_text = materia_cell[1].get_text(strip=True).lower()
                if materia_name_stripped_lower == cell_text:
                    found_row = row
                    break
        
        if found_row:
            id_input = found_row.find('input', {'name': 'id_materia'})
            if id_input and id_input.get('value'):
                materia_id_to_delete = id_input.get('value')
                # print(f"DEBUG: ID de materia '{materia_name}' encontrado: {materia_id_to_delete}") # Puedes descomentar para depurar
            else:
                print(f"ADVERTENCIA: Fila para '{materia_name}' encontrada, pero no se encontró el input 'id_materia'.")
        else:
            print(f"ADVERTENCIA: Fila para '{materia_name}' NO encontrada en el HTML después de la espera de 5 segundos.")

        if materia_id_to_delete:
            try:
                delete_response = self.client.post("/config/controllers/materias/delete.php",
                                                     data={"id_materia": materia_id_to_delete},
                                                     name="/admin/materias/delete_post_performance",
                                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
                delete_response.raise_for_status() # Lanza excepción si el status no es 2xx
            except Exception as e:
                print(f"ERROR: Fallo al eliminar la materia '{materia_name}' (ID: {materia_id_to_delete}): {e}")
        else:
            print(f"Usuario {self.environment.runner.user_count}: No se pudo eliminar la materia '{materia_name}' porque no se encontró su ID o la fila.")
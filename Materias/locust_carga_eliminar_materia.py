from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

# Un contador global para asegurar nombres de materias únicos a través de todas las instancias de Locust
global_materia_unique_id = 0

class EliminarMateriaStressTest(HttpUser):
    # Tiempo de espera entre tareas (simula pausas de usuario)
    wait_time = between(1, 3) # Espera entre 1 y 3 segundos entre cada acción

    host = "http://localhost/proyectoEscuela" # URL base de tu aplicación

    # Credenciales de admin
    ADMIN_EMAIL = "admin@admin.com"
    ADMIN_PASSWORD = "123"

    def on_start(self):
        """ Se ejecuta al inicio de cada usuario virtual """
        self.login()

    def login(self):
        """ Tarea para iniciar sesión. """
        # Paso 1: GET la página de login para obtener el formulario y cualquier token CSRF
        login_page_response = self.client.get("/index.php", name="/login_page_load")
        
        # Paso 2: Parsear el HTML para encontrar el token CSRF (si existe) y otros campos ocultos
        soup = BeautifulSoup(login_page_response.text, 'html.parser')
        
        form_data = {}
        for input_tag in soup.find_all('input', type='hidden'):
            if input_tag.get('name') and input_tag.get('value'):
                form_data[input_tag.get('name')] = input_tag.get('value')

        form_data["email"] = self.ADMIN_EMAIL
        form_data["password"] = self.ADMIN_PASSWORD

        # Paso 3: POST la solicitud de login al script de procesamiento
        login_process_response = self.client.post(
            "/controler_login.php",
            data=form_data,
            name="/login_process",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Paso 4: Verificar el éxito del login
        if "admin" not in login_process_response.url:
            print(f"Fallo en el login para {self.ADMIN_EMAIL}. Status: {login_process_response.status_code}, URL: {login_process_response.url}")
            self.environment.runner.quit() 
        else:
            print(f"Login exitoso como {self.ADMIN_EMAIL}.")

    @task(1) # Ponderación 1, ya que es un flujo completo de creación-eliminación
    def create_and_delete_materia(self):
        """ Simula la creación de una materia y su posterior eliminación. """
        
        global global_materia_unique_id
        global_materia_unique_id += 1
        
        # --- 1. Crear una materia de prueba ---
        materia_name = f"Materia_Eliminar_{global_materia_unique_id}_{int(time.time())}"
        materia_description = f"Descripción para {materia_name}"

        # GET el formulario de creación de materia
        create_materia_form_response = self.client.get("/admin/materias/create.php", name="/admin/materias/create_form_load")
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
                    elif input_tag.find('option'): # Tomar la primera opción si ninguna está seleccionada
                         create_form_data[name] = input_tag.find('option').get('value')
                else:
                    create_form_data[name] = value if value is not None else ''

        create_form_data["nombre_materia"] = materia_name
        create_form_data["descripcion"] = materia_description
        
        self.client.post("/config/controllers/materias/create.php",
                         data=create_form_data,
                         name="/admin/materias/create_post",
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

        print(f"Usuario {self.environment.runner.user_count}: Materia '{materia_name}' creada.")

        # --- 2. Eliminar la materia recién creada ---
        # Ir al listado de materias para encontrar el ID de la materia creada
        self.client.get("/admin/materias/index.php", name="/admin/materias/list_for_delete")
        
        # Dar un tiempo extra para que la tabla de DataTables se actualice
        time.sleep(1) 

        # Encontrar la fila de la materia por su nombre y obtener su ID para la eliminación.
        soup_list = BeautifulSoup(self.client.last_response.text, 'html.parser')
        
        # Buscar la fila de la materia por el texto del nombre de la materia
        # Usamos string=lambda para buscar el texto dentro de cualquier elemento hijo
        materia_row = soup_list.find('tr', recursive=True, string=lambda text: text and materia_name in text)

        materia_id_to_delete = None
        if materia_row:
            # Dentro de la fila, buscar el input hidden con name="id_materia"
            id_input = materia_row.find('input', {'name': 'id_materia'})
            if id_input and id_input.get('value'):
                materia_id_to_delete = id_input.get('value')
            else:
                print(f"ADVERTENCIA: No se encontró el input 'id_materia' en la fila de '{materia_name}'.")
        else:
            print(f"ADVERTENCIA: No se encontró la fila de la materia '{materia_name}' para eliminar.")

        if materia_id_to_delete:
            # Simulamos el POST directo al controlador de delete, ya que Locust no renderiza JS (SweetAlert2)
            self.client.post("/config/controllers/materias/delete.php",
                             data={"id_materia": materia_id_to_delete},
                             name="/admin/materias/delete_post",
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
            print(f"Usuario {self.environment.runner.user_count}: Materia '{materia_name}' (ID: {materia_id_to_delete}) eliminada.")
        else:
            print(f"Usuario {self.environment.runner.user_count}: No se pudo eliminar la materia '{materia_name}' porque no se encontró su ID.")
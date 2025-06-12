from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

# Un contador global para asegurar títulos de tareas únicos a través de todas las instancias de Locust
global_task_unique_id_perf = 0

class EliminarTareaPerformanceTest(HttpUser):
    # Tiempo de espera entre tareas (simula pausas de usuario)
    wait_time = between(1, 3)

    host = "http://localhost/proyectoEscuela"

    # Credenciales de admin
    ADMIN_EMAIL = "admin@admin.com"
    ADMIN_PASSWORD = "123"

    # ID de materia válido, se obtendrá dinámicamente al inicio
    valid_materia_id = None

    def on_start(self):
        """ Se ejecuta al inicio de cada usuario virtual """
        self.login()
        # Intentar obtener un ID de materia válido una vez por usuario virtual
        self.valid_materia_id = self._get_valid_materia_id()
        if not self.valid_materia_id:
            print(f"[{self.environment.runner.user_count}] ERROR: No se pudo obtener un ID de materia válido. Este usuario virtual se detendrá.")
            self.environment.runner.quit() # Detener este usuario virtual si no hay materia

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

    def _get_valid_materia_id(self):
        """ Obtiene el ID de una materia existente para poder crear tareas. """
        try:
            # Ir al listado de materias
            materias_list_response = self.client.get("/admin/materias/index.php", name="/admin/materias/list_for_id")
            soup = BeautifulSoup(materias_list_response.text, 'html.parser')
            
            # Buscar el primer botón de edición de materia para extraer un ID válido
            edit_button = soup.find('a', href=lambda href: href and 'edit.php?id=' in href)
            
            if edit_button:
                materia_id = edit_button['href'].split('id=')[1]
                return materia_id
            else:
                print("ADVERTENCIA: No se encontró ninguna materia para obtener un ID válido.")
                return None
        except Exception as e:
            print(f"ERROR al obtener ID de materia: {e}")
            return None


    @task(1) # Cada tarea simula un flujo completo de creación-eliminación
    def create_and_delete_task_performance(self):
        """ Simula la creación de una tarea y su posterior eliminación, midiendo el rendimiento. """
        
        # Asegurarse de que tenemos un ID de materia
        if not self.valid_materia_id:
            print(f"[{self.environment.runner.user_count}] Saltando creación/eliminación de tarea: No hay ID de materia válido.")
            return

        global global_task_unique_id_perf
        global_task_unique_id_perf += 1
        
        # --- 1. Crear una tarea de prueba ---
        task_title = f"Tarea_Perf_{global_task_unique_id_perf}_{int(time.time())}"
        task_description = f"Descripción para {task_title}"
        task_date = "2025-12-31"
        task_time = "23:59"

        # GET el formulario de creación de tarea
        # ALMACENAR LA RESPUESTA EN UNA VARIABLE: create_task_form_response
        create_task_form_response = self.client.get("/admin/tareas/create.php", name="/admin/tareas/create_form_load")
        soup_create = BeautifulSoup(create_task_form_response.text, 'html.parser') # Usar la variable aquí
        
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

        create_form_data["titulo"] = task_title
        create_form_data["descripcion"] = task_description
        create_form_data["fecha_entrega"] = task_date
        create_form_data["hora_entrega"] = task_time
        create_form_data["id_materia"] = str(self.valid_materia_id)
        
        self.client.post("/config/controllers/tareas/create.php",
                         data=create_form_data,
                         name="/admin/tareas/create_post",
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

        # --- 2. Eliminar la tarea recién creada ---
        # GET el listado de tareas (esta es la respuesta que queremos analizar)
        # ALMACENAR LA RESPUESTA EN UNA VARIABLE: list_tasks_response
        list_tasks_response = self.client.get("/admin/tareas/index.php", name="/admin/tareas/list_for_delete")
        time.sleep(1) # Dar un tiempo extra para que la tabla se actualice

        # Usar la variable que contiene la respuesta del GET a la lista
        soup_list = BeautifulSoup(list_tasks_response.text, 'html.parser') 
        task_row = soup_list.find('tr', recursive=True, string=lambda text: text and task_title in text)

        task_id_to_delete = None
        if task_row:
            id_input = task_row.find('input', {'name': 'id_tarea'})
            if id_input and id_input.get('value'):
                task_id_to_delete = id_input.get('value')
            else:
                print(f"ADVERTENCIA: No se encontró el input 'id_tarea' en la fila de '{task_title}'.")
        else:
            print(f"ADVERTENCIA: No se encontró la fila de la tarea '{task_title}' para eliminar.")

        if task_id_to_delete:
            self.client.post("/config/controllers/tareas/delete.php",
                             data={"id_tarea": task_id_to_delete},
                             name="/admin/tareas/delete_post_performance",
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
        else:
            print(f"Usuario {self.environment.runner.user_count}: No se pudo eliminar la tarea '{task_title}' porque no se encontró su ID.")
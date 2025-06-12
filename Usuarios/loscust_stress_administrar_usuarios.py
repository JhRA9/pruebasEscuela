from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

# Un contador global para asegurar nombres de usuario/email únicos a través de todas las instancias de Locust
global_user_unique_id = 0

class AdminUserBehavior(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost/proyectoEscuela"

    ADMIN_EMAIL = "admin@admin.com"
    ADMIN_PASSWORD = "123"

    def on_start(self):
        """ Se ejecuta al inicio de cada usuario virtual """
        self.login()

    def login(self):
        """ Tarea para iniciar sesión, incluyendo la extracción de un posible token CSRF. """
        # Paso 1: GET la página de login para obtener el formulario y cualquier token CSRF
        login_page_response = self.client.get("/index.php", name="/login_page_load")
        
        # Paso 2: Parsear el HTML para encontrar el token CSRF (si existe) y otros campos ocultos
        soup = BeautifulSoup(login_page_response.text, 'html.parser')
        
        # Asumiendo que el token CSRF está en un campo oculto
        form_data = {}
        for input_tag in soup.find_all('input', type='hidden'):
            if input_tag.get('name') and input_tag.get('value'):
                form_data[input_tag.get('name')] = input_tag.get('value')

        # Añadir las credenciales al diccionario de datos del formulario
        form_data["email"] = self.ADMIN_EMAIL
        form_data["password"] = self.ADMIN_PASSWORD

        # CORRECCIÓN CLAVE: RUTA DEL POST DE LOGIN
        # Ahora sabemos que el controlador de login está al mismo nivel que index.php
        # y se llama 'controler_login.php'
        login_process_response = self.client.post(
            "/controler_login.php", # ¡RUTA FINALMENTE CORREGIDA!
            data=form_data,
            name="/login_process",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Paso 4: Verificar el éxito del login
        # Un login exitoso debería redirigir a una URL que contenga "admin"
        if "admin" not in login_process_response.url:
            print(f"Fallo en el login para {self.ADMIN_EMAIL}. Status: {login_process_response.status_code}, URL: {login_process_response.url}")
            # Si el login falla, el usuario virtual no puede continuar con las tareas de admin
            self.environment.runner.quit() 
        else:
            print(f"Login exitoso como {self.ADMIN_EMAIL}. Redirigido a: {login_process_response.url}")

    @task(3) # Ponderación 3
    def view_users_list(self):
        """ Prioridad 1: Visualizar el listado de usuarios """
        self.client.get("/admin/usuarios/", name="/admin/usuarios/list")

    @task(2) # Ponderación 2
    def edit_user(self):
        """ Prioridad 2: Editar un usuario existente. """
        # Asumiremos que el ID 2 (ej. el admin) siempre existe y es editable.
        user_id_to_edit = 2 
        
        global global_user_unique_id
        global_user_unique_id += 1
        new_username = f"EditedUser_{int(time.time())}_{global_user_unique_id}"
        
        # Paso 1: GET la página de edición para obtener los datos actuales del usuario y el token CSRF (si aplica)
        edit_form_response = self.client.get(f"/admin/usuarios/edit.php?id={user_id_to_edit}", name="/admin/usuarios/edit_form_load")
        
        soup = BeautifulSoup(edit_form_response.text, 'html.parser')
        
        edit_form_data = {}
        for input_tag in soup.find_all(['input', 'textarea', 'select']):
            name = input_tag.get('name')
            value = input_tag.get('value')
            if name:
                if input_tag.name == 'select':
                    selected_option = input_tag.find('option', selected=True)
                    if selected_option:
                        edit_form_data[name] = selected_option.get('value')
                    elif input_tag.find('option'):
                         edit_form_data[name] = input_tag.find('option').get('value')
                else:
                    edit_form_data[name] = value if value is not None else ''

        edit_form_data["nombres"] = new_username
        
        self.client.post(f"/config/controllers/usuarios/update.php", 
                         data=edit_form_data,
                         name="/admin/usuarios/update",
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

    @task(1) # Ponderación 1
    def create_user(self):
        """ Prioridad 3: Crear un nuevo usuario """
        global global_user_unique_id
        global_user_unique_id += 1
        new_user_email = f"testuser_{int(time.time())}_{global_user_unique_id}@test.com"
        new_user_name = f"TestUser {int(time.time())}_{global_user_unique_id}"
        new_user_password = "password123"

        create_form_response = self.client.get("/admin/usuarios/create.php", name="/admin/usuarios/create_form_load")
        
        soup = BeautifulSoup(create_form_response.text, 'html.parser')
        create_form_data = {}
        for input_tag in soup.find_all(['input', 'textarea', 'select']):
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

        create_form_data["rol_id"] = "3"
        create_form_data["nombres"] = new_user_name
        create_form_data["email"] = new_user_email
        create_form_data["password"] = new_user_password
        create_form_data["password_repeat"] = new_user_password

        self.client.post("/config/controllers/usuarios/create.php", 
                         data=create_form_data,
                         name="/admin/usuarios/create",
                         headers={"Content-Type": "application/x-www-form-urlencoded"})
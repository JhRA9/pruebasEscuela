from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

# Un contador global para asegurar emails/nombres de usuarios únicos
global_user_register_unique_id = 0

class RegistrarUsuariosPerformanceTest(HttpUser):
    # Tiempo de espera entre tareas (simula pausas de usuario)
    wait_time = between(1, 3) # Espera entre 1 y 3 segundos entre cada acción

    host = "http://localhost/proyectoEscuela" # URL base de tu aplicación

    # Credenciales de admin para el login inicial
    ADMIN_EMAIL = "admin@admin.com"
    ADMIN_PASSWORD = "123"
    
    # ID de rol válido, se obtendrá dinámicamente al inicio
    # para asegurar que siempre usamos un rol existente.
    valid_rol_id = None 

    def on_start(self):
        """ Se ejecuta al inicio de cada usuario virtual """
        self.login()
        # Intentar obtener un ID de rol válido una vez por usuario virtual
        self.valid_rol_id = self._get_valid_rol_id()
        if not self.valid_rol_id:
            print(f"[{self.environment.runner.user_count}] ERROR: No se pudo obtener un ID de rol válido. Este usuario virtual se detendrá.")
            self.environment.runner.quit() # Detener este usuario virtual si no hay rol

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

    def _get_valid_rol_id(self):
        """ Obtiene el ID de un rol existente para poder crear usuarios. """
        try:
            # Ir al listado de roles
            roles_list_response = self.client.get("/admin/roles/index.php", name="/admin/roles/list_for_id")
            soup = BeautifulSoup(roles_list_response.text, 'html.parser')
            
            # Buscar el primer botón de edición de rol para extraer un ID válido
            edit_button = soup.find('a', href=lambda href: href and 'edit.php?id=' in href)
            
            if edit_button:
                rol_id = edit_button['href'].split('id=')[1]
                return rol_id
            else:
                print("ADVERTENCIA: No se encontró ningún rol para obtener un ID válido.")
                return None
        except Exception as e:
            print(f"ERROR al obtener ID de rol: {e}")
            return None


    @task(1) # Cada tarea simula un registro completo
    def register_user(self):
        """ Simula el flujo de registro de un nuevo usuario. """
        
        # Asegurarse de que tenemos un ID de rol
        if not self.valid_rol_id:
            print(f"[{self.environment.runner.user_count}] Saltando registro de usuario: No hay ID de rol válido.")
            return

        global global_user_register_unique_id
        global_user_register_unique_id += 1
        
        # Generar datos únicos para el nuevo usuario
        user_name = f"UserPerf_{global_user_register_unique_id}_{int(time.time())}"
        user_email = f"userperf_{global_user_register_unique_id}_{int(time.time())}@test.com"
        user_password = "password123" # Puedes usar una contraseña genérica

        # --- 1. GET el formulario de creación de usuario ---
        # Simula la carga de la página del formulario
        create_user_form_response = self.client.get("/admin/usuarios/create.php", name="/admin/usuarios/create_form_load")
        
        # Parsear el HTML para obtener campos ocultos/seleccionados (ej. token CSRF si existiera, o valor de rol por defecto)
        soup_create = BeautifulSoup(create_user_form_response.text, 'html.parser')
        
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
        
        # --- 2. Preparar los datos para el POST del registro ---
        create_form_data["rol_id"] = str(self.valid_rol_id) # Usar el ID de rol válido
        create_form_data["nombres"] = user_name
        create_form_data["email"] = user_email
        create_form_data["password"] = user_password
        create_form_data["password_repeat"] = user_password # Repetir la contraseña

        # --- 3. POST la solicitud para registrar el usuario ---
        self.client.post("/config/controllers/usuarios/create.php",
                         data=create_form_data,
                         name="/admin/usuarios/register_post", # Nombre específico para la métrica
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

        print(f"Usuario {self.environment.runner.user_count}: Intento de registro para '{user_email}'.")
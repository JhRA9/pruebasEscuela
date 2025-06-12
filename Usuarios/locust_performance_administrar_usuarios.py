from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

# Un contador global para asegurar nombres/emails de usuarios únicos a través de todas las instancias de Locust
global_user_unique_id_perf = 0

class AdministrarUsuariosPerformanceTest(HttpUser):
    # Tiempo de espera entre tareas (simula pausas de usuario)
    wait_time = between(1, 3)

    host = "http://localhost/proyectoEscuela"

    # Credenciales de admin
    ADMIN_EMAIL = "admin@admin.com"
    ADMIN_PASSWORD = "123"

    # ID de rol válido, se obtendrá dinámicamente al inicio
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

    @task(3) # Ponderación más alta, ya que es una lectura común
    def view_users_list_performance(self):
        """ Prioridad 1: Visualizar el listado de usuarios (lectura). """
        self.client.get("/admin/usuarios/", name="/admin/usuarios/list_performance")

    @task(2) # Ponderación media
    def edit_user_performance(self):
        """ Prioridad 2: Editar un usuario existente. """
        # Asumiremos que el ID 2 (ej. el admin) siempre existe y es editable.
        # En un escenario real, esto debería ser un usuario de prueba creado y luego editado.
        user_id_to_edit = 32 # Cambiado a 32, el ID del admin que me pasaste en sistemaescolar.sql
        
        global global_user_unique_id_perf
        global_user_unique_id_perf += 1
        new_username = f"EditedPerfUser_{int(time.time())}_{global_user_unique_id_perf}"
        
        try:
            edit_form_response = self.client.get(f"/admin/usuarios/edit.php?id={user_id_to_edit}", name="/admin/usuarios/edit_form_load_performance")
            edit_form_response.raise_for_status()
        except Exception as e:
            print(f"ERROR: Fallo al cargar el formulario de edición de usuario (ID: {user_id_to_edit}): {e}")
            return
        
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

        # Sobrescribir solo el campo que queremos cambiar, y asegurar los campos obligatorios
        edit_form_data["id_usuario"] = str(user_id_to_edit)
        edit_form_data["nombres"] = new_username
        # Asegurarse de que email y rol_id se envíen si son obligatorios y no se obtienen del formulario
        if 'email' not in edit_form_data:
            edit_form_data['email'] = self.ADMIN_EMAIL # O el email original del usuario
        if 'rol_id' not in edit_form_data and self.valid_rol_id:
             edit_form_data['rol_id'] = str(self.valid_rol_id) # Usar el rol_id obtenido al inicio

        try:
            update_response = self.client.post(f"/config/controllers/usuarios/update.php",
                                                     data=edit_form_data,
                                                     name="/admin/usuarios/update_post_performance",
                                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
            update_response.raise_for_status()
        except Exception as e:
            print(f"ERROR: Fallo al editar el usuario (ID: {user_id_to_edit}): {e}")

    @task(1) # Ponderación baja
    def create_user_performance(self):
        """ Prioridad 3: Crear un nuevo usuario (escritura). """
        if not self.valid_rol_id:
            print(f"[{self.environment.runner.user_count}] Saltando creación de usuario: No hay ID de rol válido.")
            return

        global global_user_unique_id_perf
        global_user_unique_id_perf += 1
        
        user_name = f"NewPerfUser_{global_user_unique_id_perf}_{int(time.time())}"
        user_email = f"newperfuser_{global_user_unique_id_perf}_{int(time.time())}@test.com"
        user_password = "password123"

        try:
            create_form_response = self.client.get("/admin/usuarios/create.php", name="/admin/usuarios/create_form_load_performance")
            create_form_response.raise_for_status()
        except Exception as e:
            print(f"ERROR: Fallo al cargar el formulario de creación de usuario: {e}")
            return
        
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

        create_form_data["rol_id"] = str(self.valid_rol_id)
        create_form_data["nombres"] = user_name
        create_form_data["email"] = user_email
        create_form_data["password"] = user_password
        create_form_data["password_repeat"] = user_password

        try:
            create_post_response = self.client.post("/config/controllers/usuarios/create.php",
                                                     data=create_form_data,
                                                     name="/admin/usuarios/create_post_performance",
                                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
            create_post_response.raise_for_status()
        except Exception as e:
            print(f"ERROR: Fallo al crear el usuario '{user_email}': {e}")
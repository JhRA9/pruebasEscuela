from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

# Un contador global para asegurar nombres de roles únicos a través de todas las instancias de Locust
global_rol_unique_id = 0

class EditarEliminarRolStressTest(HttpUser):
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

    @task(1) # Ponderación 1, ya que es un flujo completo de creación-edición-eliminación
    def create_edit_delete_rol(self):
        """ Simula la creación, edición y posterior eliminación de un rol. """
        
        global global_rol_unique_id
        global_rol_unique_id += 1
        
        # --- 1. Crear un rol de prueba ---
        rol_name_original = f"ROL_STRESS_{global_rol_unique_id}_{int(time.time())}_ORIGINAL"
        
        # GET el formulario de creación de rol
        create_rol_form_response = self.client.get("/admin/roles/create.php", name="/admin/roles/create_form_load")
        soup_create = BeautifulSoup(create_rol_form_response.text, 'html.parser')
        
        create_form_data = {}
        for input_tag in soup_create.find_all(['input', 'textarea', 'select']):
            name = input_tag.get('name')
            value = input_tag.get('value')
            if name:
                create_form_data[name] = value if value is not None else ''

        create_form_data["nombre_rol"] = rol_name_original
        
        self.client.post("/config/controllers/roles/create.php",
                         data=create_form_data,
                         name="/admin/roles/create_post",
                         headers={"Content-Type": "application/x-www-form-urlencoded"})

        print(f"Usuario {self.environment.runner.user_count}: Rol '{rol_name_original}' creado.")

        # --- 2. Editar el rol recién creado ---
        # Primero, necesitamos obtener el ID del rol creado.
        # Vamos a la lista de roles para obtener el ID del rol que acabamos de crear.
        self.client.get("/admin/roles/index.php", name="/admin/roles/list_for_edit_delete")
        
        # Dar un tiempo extra para que la tabla de DataTables se actualice
        time.sleep(1) 

        soup_list = BeautifulSoup(self.client.last_response.text, 'html.parser')
        
        # Buscar el botón de edición (que contiene el ID) para el rol con el nombre original
        # El ID del rol está en el 'href' del botón de edición.
        edit_button = soup_list.find('a', href=lambda href: href and 'edit.php?id=' in href and f'nombre_rol={rol_name_original}' not in href)
        
        rol_id_to_edit = None
        if edit_button:
            rol_id_to_edit = edit_button['href'].split('id=')[1]
        else:
            print(f"ADVERTENCIA: No se encontró el botón de edición para el rol '{rol_name_original}'.")

        if rol_id_to_edit:
            rol_name_edited = f"ROL_STRESS_{global_rol_unique_id}_{int(time.time())}_EDITED"
            
            # GET el formulario de edición de rol para obtener datos actuales y token CSRF
            edit_rol_form_response = self.client.get(f"/admin/roles/edit.php?id={rol_id_to_edit}", name="/admin/roles/edit_form_load")
            soup_edit = BeautifulSoup(edit_rol_form_response.text, 'html.parser')

            edit_form_data = {}
            for input_tag in soup_edit.find_all(['input', 'textarea', 'select']):
                name = input_tag.get('name')
                value = input_tag.get('value')
                if name:
                    edit_form_data[name] = value if value is not None else ''
            
            # Asegurarse de que el ID del rol esté presente en los datos del formulario
            edit_form_data["id_rol"] = str(rol_id_to_edit)
            edit_form_data["nombre_rol"] = rol_name_edited # El nuevo nombre
            
            self.client.post("/config/controllers/roles/update.php",
                             data=edit_form_data,
                             name="/admin/roles/update_post",
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
            print(f"Usuario {self.environment.runner.user_count}: Rol '{rol_name_original}' (ID: {rol_id_to_edit}) editado a '{rol_name_edited}'.")
        else:
            print(f"Usuario {self.environment.runner.user_count}: No se pudo editar el rol '{rol_name_original}' porque no se encontró su ID.")


        # --- 3. Eliminar el rol recién creado (o editado) ---
        if rol_id_to_edit: # Solo intentar eliminar si logramos obtener el ID para editar
            # La eliminación de rol en tu index.php usa un formulario sin SweetAlert2 directo.
            # Simplemente un POST directo al controlador de delete.
            self.client.post("/config/controllers/roles/delete.php",
                             data={"id_rol": rol_id_to_edit},
                             name="/admin/roles/delete_post",
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
            print(f"Usuario {self.environment.runner.user_count}: Rol '{rol_name_edited if rol_id_to_edit else rol_name_original}' (ID: {rol_id_to_edit}) eliminado.")
        else:
            print(f"Usuario {self.environment.runner.user_count}: Saltando eliminación de rol: No se pudo obtener el ID para editar.")
from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

# Un contador global para asegurar nombres de roles únicos a través de todas las instancias de Locust
global_rol_unique_id_perf = 0

class EliminarRolPerformanceTest(HttpUser):
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

    @task(1) # Cada tarea simula un flujo completo de creación-edición-eliminación
    def create_edit_delete_rol_performance(self):
        """ Simula la creación, edición y posterior eliminación de un rol, midiendo el rendimiento. """
        
        global global_rol_unique_id_perf
        global_rol_unique_id_perf += 1
        
        # --- 1. Crear un rol de prueba ---
        rol_name_original = f"ROL_PERF_{global_rol_unique_id_perf}_{int(time.time())}_ORIGINAL"
        
        try:
            create_rol_form_response = self.client.get("/admin/roles/create.php", name="/admin/roles/create_form_load")
            create_rol_form_response.raise_for_status()
        except Exception as e:
            print(f"ERROR: Fallo al cargar el formulario de creación de rol: {e}")
            return
        
        soup_create = BeautifulSoup(create_rol_form_response.text, 'html.parser')
        create_form_data = {}
        for input_tag in soup_create.find_all(['input', 'textarea', 'select']):
            name = input_tag.get('name')
            value = input_tag.get('value')
            if name:
                create_form_data[name] = value if value is not None else ''

        create_form_data["nombre_rol"] = rol_name_original
        
        try:
            create_post_response = self.client.post("/config/controllers/roles/create.php",
                                                     data=create_form_data,
                                                     name="/admin/roles/create_post",
                                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
            create_post_response.raise_for_status()
        except Exception as e:
            print(f"ERROR: Fallo al crear el rol '{rol_name_original}': {e}")
            return

        # --- 2. Editar el rol recién creado ---
        # Ir a la lista de roles para obtener el ID del rol que acabamos de crear
        try:
            list_roles_response = self.client.get("/admin/roles/index.php", name="/admin/roles/list_for_edit_delete")
            list_roles_response.raise_for_status()
        except Exception as e:
            print(f"ERROR: Fallo al cargar la lista de roles para edición/eliminación: {e}")
            return
        
        # Aumentar el tiempo de espera si DataTables necesita más tiempo para cargar
        time.sleep(2) # Ajusta este tiempo si sigues viendo "rol no encontrado"

        soup_list = BeautifulSoup(list_roles_response.text, 'html.parser')
        
        rol_id_to_edit = None
        rol_name_edited = f"ROL_PERF_{global_rol_unique_id_perf}_{int(time.time())}_EDITED"

        # Buscar la fila del rol por su nombre
        found_row = None
        for row in soup_list.find_all('tr'):
            # En tu index.php de roles, el nombre de rol está en la segunda columna (td[1])
            # <td><?= $rol['nombre_rol'] ?></td>
            rol_cells = row.find_all('td')
            if len(rol_cells) > 1:
                cell_text = rol_cells[1].get_text(strip=True)
                if cell_text == rol_name_original: # Comparación exacta
                    found_row = row
                    break
        
        if found_row:
            # Buscar el botón de edición para extraer el ID
            edit_button = found_row.find('a', href=lambda href: href and 'edit.php?id=' in href)
            if edit_button:
                rol_id_to_edit = edit_button['href'].split('id=')[1]
            else:
                print(f"ADVERTENCIA: Fila para '{rol_name_original}' encontrada, pero no se encontró el botón de edición.")
        else:
            print(f"ADVERTENCIA: Fila para '{rol_name_original}' NO encontrada en el HTML de la lista. Puede que la tabla no se haya cargado a tiempo.")


        if rol_id_to_edit:
            try:
                # GET el formulario de edición para obtener datos actuales y token CSRF
                edit_rol_form_response = self.client.get(f"/admin/roles/edit.php?id={rol_id_to_edit}", name="/admin/roles/edit_form_load")
                edit_rol_form_response.raise_for_status()

                soup_edit = BeautifulSoup(edit_rol_form_response.text, 'html.parser')
                edit_form_data = {}
                for input_tag in soup_edit.find_all(['input', 'textarea', 'select']):
                    name = input_tag.get('name')
                    value = input_tag.get('value')
                    if name:
                        edit_form_data[name] = value if value is not None else ''
                
                edit_form_data["id_rol"] = str(rol_id_to_edit)
                edit_form_data["nombre_rol"] = rol_name_edited 
                
                update_response = self.client.post("/config/controllers/roles/update.php",
                                                     data=edit_form_data,
                                                     name="/admin/roles/update_post_performance", # Nombre específico para la métrica
                                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
                update_response.raise_for_status()
            except Exception as e:
                print(f"ERROR: Fallo al editar el rol '{rol_name_original}' (ID: {rol_id_to_edit}): {e}")
                rol_id_to_edit = None # Marcar para no intentar eliminar si la edición falla
        else:
            print(f"Usuario {self.environment.runner.user_count}: No se pudo editar el rol '{rol_name_original}' porque no se encontró su ID o la fila.")


        # --- 3. Eliminar el rol recién creado (o editado) ---
        if rol_id_to_edit: # Solo intentar eliminar si logramos obtener el ID para editar
            try:
                delete_response = self.client.post("/config/controllers/roles/delete.php",
                                                     data={"id_rol": rol_id_to_edit},
                                                     name="/admin/roles/delete_post_performance", # Nombre específico para la métrica
                                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
                delete_response.raise_for_status()
            except Exception as e:
                print(f"ERROR: Fallo al eliminar el rol '{rol_name_edited if rol_id_to_edit else rol_name_original}' (ID: {rol_id_to_edit}): {e}")
        else:
            print(f"Usuario {self.environment.runner.user_count}: Saltando eliminación de rol: No se pudo obtener el ID del rol para editarlo/eliminarlo.")
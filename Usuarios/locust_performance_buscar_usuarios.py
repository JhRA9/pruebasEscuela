from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

class BuscarUsuariosPerformanceTest(HttpUser):
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

    @task(1) # Una única tarea para el flujo de búsqueda
    def search_users_performance(self):
        """ Simula la carga de la página de listado de usuarios, que realiza la 'búsqueda' inicial. """
        
        # Simular la carga de la página del listado de usuarios.
        # En tu configuración actual, el DataTables de usuarios carga todos los datos al inicio (searching: false).
        # Por lo tanto, esta es la operación que estresa la "búsqueda" (obtención de todos los datos).
        self.client.get("/admin/usuarios/", name="/admin/usuarios/search_users_performance")
        
        print(f"Usuario {self.environment.runner.user_count}: Página de listado de usuarios cargada para simular búsqueda.")
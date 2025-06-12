from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

class FiltrarTareaEstadoPerformanceTest(HttpUser): # Nombre de clase para la prueba de performance de filtrado
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

    @task(1) # Una sola tarea para este flujo de filtrado
    def filter_tasks_by_status_performance(self):
        """ Simula la visualización inicial de la tabla y la solicitud de filtrado por estado. """
        
        # --- 1. Simular la carga de la página del listado de tareas ---
        # Esto representa la carga inicial del HTML y la activación del JavaScript
        self.client.get("/admin/tareas/index.php", name="/admin/tareas/list_initial_performance")
        
        # --- 2. Simular la solicitud de datos ordenados por estado ---
        # Esto es lo que se ejecuta cuando el usuario hace clic en el botón "Ordenar por estado"
        # en tu aplicación. Es una llamada AJAX al controlador `list.php` con el parámetro `order=estado`.
        self.client.get("/config/controllers/tareas/list.php?order=estado", name="/admin/tareas/filter_by_estado_api_performance")
        
        print(f"Usuario {self.environment.runner.user_count}: Tareas solicitadas ordenadas por estado para performance.")
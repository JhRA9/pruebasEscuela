from locust import HttpUser, task, between
import random
import time
from bs4 import BeautifulSoup

class FiltrarTareaEstadoStressTest(HttpUser):
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

    @task(1) # Ponderación 1 para el flujo de filtrado
    def filter_tasks_by_status(self):
        """ Simula la visualización inicial y el filtrado por estado. """
        
        # --- 1. Visualizar el listado inicial de tareas (sin ordenar) ---
        # Esto simula la carga de la página inicial de tareas
        self.client.get("/admin/tareas/index.php", name="/admin/tareas/list_initial")
        
        # --- 2. Solicitar las tareas ordenadas por estado ---
        # Tu index.php de tareas llama a loadTable('estado') cuando se hace clic en btn-estado
        # y loadTable hace un fetch a '/config/controllers/tareas/list.php?order=estado'
        self.client.get("/config/controllers/tareas/list.php?order=estado", name="/admin/tareas/filter_by_estado_api")
        
        print(f"Usuario {self.environment.runner.user_count}: Tareas solicitadas ordenadas por estado.")

    # Opcional: Podrías añadir otra tarea para visualizar por otra columna
    # @task(0.5) # Menor prioridad
    # def filter_tasks_by_date(self):
    #     self.client.get("/admin/tareas/index.php", name="/admin/tareas/list_initial_again")
    #     self.client.get("/config/controllers/tareas/list.php?order=fecha_entrega", name="/admin/tareas/filter_by_fecha_api")
    #     print(f"Usuario {self.environment.runner.user_count}: Tareas solicitadas ordenadas por fecha.")
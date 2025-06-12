from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserManagementTests:
    def __init__(self):
        self.base_url = "http://localhost/proyectoEscuela"
        self.driver = None # Inicializa driver como None

    def _start_driver(self):
        # Inicializa el driver si no está activo o si se cerró
        if self.driver is None or not self.driver.session_id:
            self.driver = webdriver.Chrome()

    def _quit_driver(self):
        # Cierra el driver si está activo
        if self.driver:
            self.driver.quit()
        self.driver = None # Restablece a None

    def login_as_admin(self):
        self._start_driver() # Asegura que el driver esté iniciado para cada login
        self.driver.get(f"{self.base_url}/index.php")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        self.driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
        self.driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
        WebDriverWait(self.driver, 10).until(EC.url_contains("admin")) # Esperar a que la URL cambie después del login
        print("Login exitoso como administrador.")

    def tearDown(self):
        pass


    def test_eliminar_tarea(self):
        """
        CA: La función debe retornar un mensaje de éxito sin errores.
        """
        print("\n--- Ejecutando prueba: Eliminar una tarea ---")
        try:
            self.login_as_admin()
            
            # 1. Crear una tarea de prueba
            print("Creando tarea de prueba para eliminación...")
            self.driver.get(f"{self.base_url}/admin/tareas/create.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "titulo")))

            # Llenar el formulario de creación de tarea
            test_tarea_titulo = f"Tarea para eliminar"
            test_tarea_descripcion = f"Descripción de la tarea a eliminar"
            test_tarea_fecha = "2025-12-31" # Fecha futura
            test_tarea_hora = "23:59:00"

            self.driver.find_element(By.NAME, "titulo").send_keys(test_tarea_titulo)
            self.driver.find_element(By.NAME, "descripcion").send_keys(test_tarea_descripcion)
            self.driver.execute_script("document.getElementsByName('fecha_entrega')[0].value = arguments[0]", test_tarea_fecha)
            self.driver.execute_script("document.getElementsByName('hora_entrega')[0].value = arguments[0]", test_tarea_hora)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

            WebDriverWait(self.driver, 10).until(EC.url_contains("index.php")) # Esperar a la redirección a la lista
            print("Tarea de prueba creada exitosamente.")

            # 2. Navegar a la página del listado de tareas
            self.driver.get(f"{self.base_url}/admin/tareas/index.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "example1")))

            # 3. Encontrar la tarea recién creada y hacer clic en su botón de eliminar
            # XPath para encontrar el botón de eliminar para la tarea específica
            # Buscamos un <td> que contenga el título de nuestra tarea, luego sube al <tr> padre
            # y desde allí se busca el botón de eliminar (que es un <button type="submit"> dentro de un <form>)
            delete_button_xpath = f"//table[@id='example1']/tbody/tr[./td/center[text()='{test_tarea_titulo}']]/td//form/button[contains(@class, 'btn-danger')]"
            
            print(f"Buscando botón de eliminar con XPath: {delete_button_xpath}")
            delete_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
            
            print("Haciendo clic en el botón de eliminar...")
            delete_button.click()

            # 4. Verificar el mensaje de éxito de eliminación
            # El mensaje de éxito está en un div con clase 'alert-success' o similar.
            success_message = "Tarea eliminada correctamente"
            try:
                if success_message in self.driver.page_source:
                    print("Prueba 'Eliminar una tarea' exitosa: Mensaje de confirmación encontrado. :D")
                else:
                    print("Prueba 'Eliminar una tarea' fallida: Mensaje de confirmación no es el esperado.")
            except:
                print("Prueba 'Eliminar una tarea' fallida: No se encontró el mensaje de éxito o la tarea no se eliminó.")

        except Exception as e:
            print(f"Error durante la prueba 'Eliminar una tarea': {str(e)}")
        finally:
            self._quit_driver()

# Ejecutar las pruebas
if __name__ == "__main__":
    tester = UserManagementTests()

    tester.test_eliminar_tarea()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class UserManagementTests:
    def __init__(self):
        self.base_url = "http://localhost/proyectoEscuela" # Asegúrate de que esta sea la URL base de tu proyecto
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
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))) # Asegurar que el campo email esté presente
        self.driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
        self.driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
        WebDriverWait(self.driver, 10).until(EC.url_contains("admin")) # Esperar a que la URL cambie después del login
        print("Login exitoso como administrador.")

    def tearDown(self):
        pass


    def test_visualizar_todos_los_usuarios(self):
        """
        CA: La función debe retornar una lista con todos los usuarios existentes sin errores.
        """
        print("\n--- Ejecutando prueba: Visualizar todos los usuarios ---")
        try:
            self.login_as_admin()
            self.driver.get(f"{self.base_url}/admin/usuarios/index.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "example1"))) # Esperar a que la tabla cargue

            filas = self.driver.find_elements(By.XPATH, "//table[@id='example1']/tbody/tr")

            if len(filas) > 0:
                print(f"Prueba 'Visualizar todos los usuarios' exitosa: se encontraron {len(filas)} usuarios en la tabla. :D")
            else:
                print("Prueba 'Visualizar todos los usuarios' fallida: No se encontraron usuarios en la tabla. :'( ")
        except Exception as e:
            print(f"Error durante la prueba 'Visualizar todos los usuarios': {str(e)}")
        finally:
            self._quit_driver() # Asegura que el driver se cierre al final de CADA prueba

    def test_actualizacion_exitosa_usuario(self):
        """
        CA: La función debe confirmar la edición con un mensaje como "Usuario actualizado correctamente."
        """
        print("\n--- Ejecutando prueba: Actualización exitosa de usuario ---")
        try:
            self.login_as_admin()
            
            test_user_email = f"prueba@test.com"

            time.sleep(1) # Pequeña espera adicional para que el DOM se asiente

            # Ahora, ir a la página de edición para el usuario recién creado
            self.driver.get(f"{self.base_url}/admin/usuarios/index.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "example1")))

            # Encontrar el botón de editar del usuario recién creado
            # Usamos EC.element_to_be_clickable para asegurar que el elemento esté en el DOM y sea interactuable
            edit_button_xpath = f"//td[text()='{test_user_email}']/following-sibling::td//a[contains(@href, 'edit.php')]"
            edit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, edit_button_xpath)))
            edit_button.click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "nombres")))

            new_name = f"UsuarioEditado"
            self.driver.find_element(By.NAME, "nombres").clear()
            self.driver.find_element(By.NAME, "nombres").send_keys(new_name)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

            # Verificar el mensaje de éxito
            success_message = "El usuario se actualizo correctamente"
            try:
                if success_message in self.driver.page_source:
                    print("Prueba 'Actualización exitosa de usuario' exitosa: Mensaje de confirmación encontrado. :D")
                else:
                    print("Prueba 'Actualización exitosa de usuario' fallida: Mensaje de confirmación no es el esperado.")
            except:
                print("Prueba 'Actualización exitosa de usuario' fallida: No se encontró el mensaje de éxito.")

        except Exception as e:
            print(f"Error durante la prueba 'Actualización exitosa de usuario': {str(e)}")
        finally:
            self._quit_driver()

    def test_validacion_campos_obligatorios_edicion(self):
        """
        CA: Si un campo requerido está vacío, debe retornar: "Por favor, complete todos los campos obligatorios."
        """
        print("\n--- Ejecutando prueba: Validación de campos obligatorios en edición ---")
        try:
            self.login_as_admin()
            test_user_email = f"vacio@test.com"

            # Ir a la página de edición del usuario
            self.driver.get(f"{self.base_url}/admin/usuarios/index.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "example1")))

            edit_button_xpath = f"//td[text()='{test_user_email}']/following-sibling::td//a[contains(@href, 'edit.php')]"
            edit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, edit_button_xpath)))
            edit_button.click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "nombres")))

            # Vaciar un campo obligatorio (nombre del usuario)
            self.driver.find_element(By.NAME, "nombres").clear()
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

            # Verificar el mensaje de error de validación
            error_message = "Por favor, complete todos los campos obligatorios"
            try:
                if error_message in self.driver.page_source:
                    print("Prueba 'Validación de campos obligatorios en edición' exitosa: Mensaje de error encontrado. :D")
                else:
                    print("Prueba 'Validación de campos obligatorios en edición' fallida: Mensaje de error no es el esperado.")
            except:
                print("Prueba 'Validación de campos obligatorios en edición' fallida: No se encontró el mensaje de error.")

        except Exception as e:
            print(f"Error durante la prueba 'Validación de campos obligatorios en edición': {str(e)}")
        finally:
            self._quit_driver()


# Ejecutar las pruebas
if __name__ == "__main__":
    tester = UserManagementTests()

    tester.test_visualizar_todos_los_usuarios()
    tester.test_actualizacion_exitosa_usuario()
    tester.test_validacion_campos_obligatorios_edicion()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class RolManagementTests: # Renombrado para mayor claridad
    def __init__(self):
        self.base_url = "http://localhost/proyectoEscuela"
        self.driver = None
        self.test_rol_nombre_original = None # Para almacenar el nombre del rol creado

    def _start_driver(self):
        if self.driver is None or not self.driver.session_id:
            self.driver = webdriver.Chrome()

    def _quit_driver(self):
        if self.driver:
            self.driver.quit()
        self.driver = None

    def login_as_admin(self):
        self._start_driver()
        # Path de login según tu última referencia
        self.driver.get(f"{self.base_url}/index.php")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        self.driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
        self.driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
        WebDriverWait(self.driver, 10).until(EC.url_contains("admin"))
        print("Login exitoso como administrador.")

    def test_editar_rol(self):
        """
        Prueba unitaria para la edición de un rol.
        CA: La función debe confirmar la edición con un mensaje como "Se actualiza el rol de manera correcta."
        """
        print("\n--- Ejecutando prueba unitaria: Editar un rol ---")
        try:
            self.login_as_admin()

            # 1. Crear un rol de prueba para poder editarlo
            print("Creando rol de prueba para edición...")
            self.driver.get(f"{self.base_url}/admin/roles/create.php") #
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "nombre_rol"))) #

            timestamp = int(time.time())
            self.test_rol_nombre_original = f"ROL PRUEBA EDITAR {timestamp}"
            
            self.driver.find_element(By.NAME, "nombre_rol").send_keys(self.test_rol_nombre_original) #
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click() #

            # Esperar la redirección a la página de listado de roles después de la creación
            WebDriverWait(self.driver, 10).until(EC.url_contains("admin/roles/index.php")) #
            time.sleep(2) # Dar un poco de tiempo para que DataTables cargue y renderice

            print(f"Rol '{self.test_rol_nombre_original}' creado exitosamente.")

            # 2. Navegar a la página de edición del rol recién creado
            # Primero, necesitamos encontrar el ID del rol recién creado desde la tabla.
            # Dada la estructura de tu index.php, el ID no está directamente visible en la celda del nombre.
            # Necesitamos encontrar la fila por el nombre y luego extraer el 'id' de la URL del botón de edición.
            
            print(f"Buscando el ID del rol '{self.test_rol_nombre_original}' para editar...")
            edit_button_xpath = f"//table[@id='example1']//tr[td[contains(., '{self.test_rol_nombre_original}')]]//a[contains(@href, 'edit.php')]"
            edit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, edit_button_xpath)))
            
            # Obtener el href del botón de edición para extraer el ID
            edit_url = edit_button.get_attribute("href")
            # Extraer el id del URL (e.g., "edit.php?id=123")
            id_rol_para_editar = edit_url.split("id=")[1] 
            print(f"ID del rol encontrado: {id_rol_para_editar}")

            self.driver.get(f"{self.base_url}/admin/roles/edit.php?id={id_rol_para_editar}") #
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "nombre_rol"))) #
            print(f"Navegado a la página de edición del rol ID: {id_rol_para_editar}")

            # 3. Modificar el nombre del rol
            new_rol_nombre = f"ROL EDITADO {timestamp}"
            rol_name_input = self.driver.find_element(By.NAME, "nombre_rol")
            rol_name_input.clear()
            rol_name_input.send_keys(new_rol_nombre)
            print(f"Cambiando nombre del rol de '{self.test_rol_nombre_original}' a '{new_rol_nombre}'")

            # 4. Enviar el formulario de edición
            self.driver.find_element(By.XPATH, "//button[@type='submit' and text()='Actualizar']").click()
            print("Formulario de edición enviado.")

            # 5. Verificar el mensaje de éxito de la actualización
            # El mensaje esperado es "Se actualiza el rol de manera correcta"
            success_message_expected = "Se actualiza el rol de manera correcta"
            success_message_xpath = f"//div[contains(@class, 'alert-success') or contains(text(), '{success_message_expected}')]"
            
            mensaje_exito_encontrado = None
            try:
                mensaje_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, success_message_xpath))
                )
                mensaje_exito_encontrado = mensaje_element.text
            except:
                mensaje_exito_encontrado = None

            # 6. Verificar que el nombre del rol se actualizó en el listado
            # Después de la actualización, la página redirige a index.php, verificar que el nuevo nombre esté allí.
            WebDriverWait(self.driver, 10).until(EC.url_contains("admin/roles/index.php"))
            time.sleep(2) # Dar tiempo para que la tabla se refresque con el nuevo dato

            # Buscamos si el nuevo nombre aparece y el viejo nombre NO aparece
            new_name_present = new_rol_nombre in self.driver.page_source
            old_name_present = self.test_rol_nombre_original in self.driver.page_source

            # 7. Imprimir los resultados de la prueba
            if new_name_present and not old_name_present and mensaje_exito_encontrado and (success_message_expected in mensaje_exito_encontrado):
                print(f"✅ Prueba 'Editar un rol' exitosa: Rol '{new_rol_nombre}' actualizado correctamente y mensaje de éxito mostrado. :D")
                print(f"🟢 Mensaje: {mensaje_exito_encontrado}")
            elif new_name_present and not old_name_present:
                print(f"⚠️ Prueba 'Editar un rol' con advertencia: Rol '{new_rol_nombre}' actualizado, pero el mensaje de éxito no fue encontrado o no coincidió. :|")
            else:
                print(f"❌ Prueba 'Editar un rol' fallida: El rol no se actualizó correctamente. Nuevo nombre presente: {new_name_present}, Viejo nombre presente: {old_name_present}. :'( ")
                if mensaje_exito_encontrado:
                    print(f"Mensaje del sistema: {mensaje_exito_encontrado}")

        except Exception as e:
            print(f"❌ Error durante la prueba 'Editar un rol': {str(e)}")
        finally:
            self._quit_driver()

# Ejecutar la prueba unitaria
if __name__ == "__main__":
    tester = RolManagementTests()
    tester.test_editar_rol()
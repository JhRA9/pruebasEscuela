from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MateriaManagementTests:
    def __init__(self):
        self.base_url = "http://localhost/proyectoEscuela"
        self.driver = None
        self.test_materia_nombre = None # Inicializamos la variable aquí para que sea accesible en toda la clase

    def _start_driver(self):
        # Inicializa el driver si no está activo o si se cerró
        if self.driver is None or not self.driver.session_id:
            self.driver = webdriver.Chrome()

    def _quit_driver(self):
        # Cierra el driver si está activo
        if self.driver:
            self.driver.quit()
        self.driver = None

    def login_as_admin(self):
        self._start_driver()
        # CORRECCIÓN: Usar /index.php para el login según tu indicación
        self.driver.get(f"{self.base_url}/index.php") 
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        self.driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
        self.driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
        WebDriverWait(self.driver, 10).until(EC.url_contains("admin"))
        print("Login exitoso como administrador.")

    def test_eliminar_materia(self):
        """
        Prueba unitaria para la eliminación de una materia, incluyendo la interacción con SweetAlert2.
        CA: La función debe retornar un mensaje de éxito sin errores al eliminar una materia.
        """
        print("\n--- Ejecutando prueba unitaria: Eliminar una materia ---")
        try:
            self.login_as_admin()
            
            # 1. Crear una materia de prueba para asegurar su existencia y unicidad
            print("Creando materia de prueba para eliminación...")
            self.driver.get(f"{self.base_url}/admin/materias/create.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "nombre_materia")))

            timestamp = int(time.time()) # Para asegurar un nombre único
            # Asignamos a self.test_materia_nombre para que sea accesible fuera del try si hay un error
            self.test_materia_nombre = f"Materia de Prueba Eliminacion {timestamp}" 
            test_materia_descripcion = f"Descripcion para la prueba de eliminacion {timestamp}"

            self.driver.find_element(By.NAME, "nombre_materia").send_keys(self.test_materia_nombre)
            self.driver.find_element(By.NAME, "descripcion").send_keys(test_materia_descripcion)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

            # Esperar la redirección a la página de listado después de la creación
            WebDriverWait(self.driver, 10).until(EC.url_contains("admin/materias/index.php"))
            time.sleep(2) # Pequeña espera para que la tabla se cargue completamente con DataTables

            print(f"Materia '{self.test_materia_nombre}' creada exitosamente.")

            # 2. Navegar a la página del listado de materias (ya deberíamos estar aquí, pero es una seguridad)
            self.driver.get(f"{self.base_url}/admin/materias/index.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "example1")))
            time.sleep(3) # Aumentar este tiempo para dar más chance a DataTables de renderizar

            # 3. Encontrar la fila de la materia y el botón de eliminar
            delete_button_xpath = f"//table[@id='example1']//tr[td[contains(., '{self.test_materia_nombre}')]]//button[contains(@class, 'btn-danger')]"
            
            print(f"Buscando botón de eliminar con XPath: {delete_button_xpath}")
            delete_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
            
            print("Haciendo clic en el botón de eliminar (que dispara SweetAlert2)...")
            delete_button.click()

            # 4. Manejar el diálogo de SweetAlert2
            confirm_button_xpath = "//button[contains(@class, 'swal2-confirm') and text()='Eliminar']"
            print("Esperando el diálogo de SweetAlert2...")
            confirm_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
            
            print("Haciendo clic en 'Eliminar' dentro del diálogo de SweetAlert2 para confirmar...")
            confirm_button.click()

            time.sleep(3) # Espera a que la página recargue después de la eliminación y el submit de SweetAlert2

            # 5. Verificar que la materia ya no aparece en la tabla
            # Usamos self.test_materia_nombre aquí
            materia_sigue_en_tabla = self.test_materia_nombre in self.driver.page_source

            # 6. Verificar el mensaje de éxito
            success_message_expected = "Se elimino la materia de manera correcta"
            mensaje_exito_encontrado = None
            try:
                mensaje_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'alert-success') or contains(text(), '{success_message_expected}')]"))
                )
                mensaje_exito_encontrado = mensaje_element.text
            except:
                mensaje_exito_encontrado = None

            # 7. Imprimir los resultados de la prueba
            if not materia_sigue_en_tabla and mensaje_exito_encontrado and (success_message_expected in mensaje_exito_encontrado):
                print(f"✅ Prueba 'Eliminar una Materia' exitosa: Materia '{self.test_materia_nombre}' eliminada y mensaje de éxito mostrado. :D")
                print(f"🟢 Mensaje: {mensaje_exito_encontrado}")
            elif not materia_sigue_en_tabla:
                print(f"⚠️ Prueba 'Eliminar una Materia' con advertencia: Materia '{self.test_materia_nombre}' eliminada, pero el mensaje de éxito no fue encontrado o no coincidió. :|")
            else:
                print(f"❌ Prueba 'Eliminar una Materia' fallida: La materia '{self.test_materia_nombre}' aún aparece en la tabla. No se eliminó correctamente. :'( ")

        except Exception as e:
            # Aquí también usamos self.test_materia_nombre
            print(f"❌ Error durante la prueba 'Eliminar una materia': {str(e)} (Materia: {self.test_materia_nombre if self.test_materia_nombre else 'No definida'})")
        finally:
            self._quit_driver()

if __name__ == "__main__":
    tester = MateriaManagementTests()
    tester.test_eliminar_materia()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class LoginExitosoTest(unittest.TestCase):
    def setUp(self):
        # Inicializa el WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost/proyectoEscuela/login/index.php")

    def test_login_exitoso(self):
        driver = self.driver

        # Ingresar credenciales válidas
        driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Esperar hasta que aparezca el mensaje de bienvenida (SweetAlert2)
        try:
            # Espera a que el popup de SweetAlert2 esté visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "swal2-popup")  # Esperamos el popup de SweetAlert
                )
            )

            # Verificar que el texto del mensaje de bienvenida sea el esperado
            mensaje = driver.find_element(By.CLASS_NAME, "swal2-title").text
            self.assertIn("Bienvenido al sistema", mensaje)
            print("Prueba de inicio de sesión exitosa: El mensaje de bienvenida fue detectado correctamente.")
        except Exception as e:
            self.fail(f"Error al verificar el mensaje de bienvenida: {str(e)}")

    def tearDown(self):
        # Cierra el navegador después de la prueba
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

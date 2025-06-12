from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    # Flujo 1: Creación de tarea válida
    try:        
       # Datos del rol a crear
        nuevo_rol = "DIRECTOR"

        # Navegar a la página de roles
        driver.get("http://localhost/proyectoEscuela/admin/roles/")
        time.sleep(5)

        # Negación a la página de creación de tarea
        driver.get("http://localhost/proyectoEscuela/admin/roles/create.php")
        driver.find_element(By.NAME, "nombre_rol").clear()
        driver.find_element(By.NAME, "nombre_rol").send_keys(nuevo_rol)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)

        # Verificar que la creación fue exitosa
        
        driver.get("http://localhost/proyectoEscuela/admin/roles/")

        print("✅ Flujo 1: Creación del rol válida - PASÓ")

    except Exception as e:
        print("❌ Flujo 1: Creación del rol - FALLÓ:", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    # Flujo 1: Edición de materia válida
    try:        
        # Datos de la materia a editar
        nuevo_titulo = "Corte y confección de tamales"
        driver.get("http://localhost/proyectoEscuela/admin/materias/edit.php?id=9")

        input_titulo = driver.find_element(By.NAME, "nombre_materia")
        input_titulo.clear()
        input_titulo.send_keys(nuevo_titulo)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)

        print("✅ Flujo 1: Edición de materia válida - PASÓ")
        
    except Exception as e:
        print("❌ Flujo 1: Edición de materia válida - FALLÓ:", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()

try:
    # Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    try:        
        nuevo_titulo = "Corte y confección de tamales"
        
        # Navegar a la página de edición de materia
        driver.get("http://localhost/proyectoEscuela/admin/materias/edit.php?id=7")

        try:
            input_titulo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "nombre_materia"))
            )
            input_titulo.clear()
            input_titulo.send_keys(nuevo_titulo)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(10)
        except TimeoutException:
            print("❌ Error: El campo 'nombre_materia' no apareció.")

        # Verificar que la edición fue exitosa
        mensaje_exito = "Se actualizó la materia de la manera correcta en la base de datos"
        if mensaje_exito in driver.page_source:
            print("✅ Prueba exitosa: tarea editada correctamente.")
        else:
            print("❌ No se detectó mensaje de éxito.")
        
    except Exception as e:
        print("❌ Prueba fallida", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
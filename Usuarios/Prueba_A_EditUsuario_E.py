from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    # Flujo 1: Edición de usuario válida
    try:
        driver.get("http://localhost/proyectoEscuela/admin/usuarios/edit.php?id=43")
        
        driver.find_element(By.NAME, "nombres").clear()
        driver.find_element(By.NAME, "nombres").send_keys("Juanito Alimaña")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("juanito@estudiante.com")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.find_element(By.NAME, "password_repeat").clear()
        driver.find_element(By.NAME, "password_repeat").send_keys("123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)

        print("✅ Flujo 1: Edición de usuarios válida - PASÓ")
        
    except Exception as e:
        print("❌ Flujo 1: Edición de usuarios válida - FALLÓ:", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
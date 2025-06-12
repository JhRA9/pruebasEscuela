from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    # Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    try:
        # Página de edición de usuario id=41
        driver.get("http://localhost/proyectoEscuela/admin/usuarios/edit.php?id=41")
        
        # Llenar los campos de edición de usuario
        driver.find_element(By.NAME, "nombres").clear()
        driver.find_element(By.NAME, "nombres").send_keys("Pepito Perez")

        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("pepito@estudiante.com")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)

        # Verificar que la edición fue exitosa
        if "El usuario se actualizó" in driver.page_source:
            print("✅ Prueba exitosa: usuario editado correctamente.")
        else:
            print("❌ No se detectó mensaje de éxito.")
        
    except Exception as e:
        print("❌ Prueba fallida", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
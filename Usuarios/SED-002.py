from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    # Ir a la página de login
    driver.get("http://localhost/proyectoEscuela/login/index.php")

    # Inyección SQL 
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com' OR '1'='1")
    driver.find_element(By.NAME, "password").send_keys("' OR '1'='1")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()   

    # Inyección SQL 
    # driver.find_element(By.NAME, "email").send_keys("' OR '1'='1")
    # driver.find_element(By.NAME, "password").send_keys("' OR '1'='1")
    # driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Inyección SQL 
    # driver.find_element(By.NAME, "email").send_keys("\" OR \"\"=\"")
    # driver.find_element(By.NAME, "password").send_keys("\" OR \"\"=\"")
    # driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(2)

    
    # Validar si se logró iniciar sesión
    if driver.current_url != "http://localhost/proyectoEscuela/login/index.php":
        print("❌ La inyección SQL pasó desapercibida.")
    else:
        print("✅ Protección contra inyección SQL implementada correctamente.")

except Exception as e:
    print("❌ Error en la prueba de inyección SQL:", str(e))

finally:
    driver.quit()

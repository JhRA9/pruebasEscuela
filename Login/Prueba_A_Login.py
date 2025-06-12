from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    
    # Login con credenciales incorrectas
    driver.find_element(By.NAME, "email").send_keys("usuario@falso.com")
    driver.find_element(By.NAME, "password").send_keys("claveincorrecta", Keys.ENTER)
    time.sleep(3)

    # Verificar si aparece un mensaje de error
    if "Credenciales incorrectas" in driver.page_source or "Los datos son incorrectos, porfavor verifiquelos y vuelva a intentarlo" in driver.page_source:
        print("✅ Prueba de Aceptación: Login fallido correctamente manejado.")
    else:
        print("❌ Prueba de Aceptación: No se detectó mensaje de error para login fallido.")
except Exception as e:
    print("❌ Error durante la prueba de aceptación:", str(e))
finally:
    driver.quit()

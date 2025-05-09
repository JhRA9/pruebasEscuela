from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

xss_payload = '<script>alert("XSS en Login detectado")</script>'
driver = webdriver.Chrome()

try:
    # Ir al formulario de inicio de sesión
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    
    # Inyectar XSS en el campo de email
    driver.find_element(By.NAME, "email").send_keys(xss_payload)
    
    # Llenar el campo de contraseña (por ejemplo, contraseña válida)
    driver.find_element(By.NAME, "password").send_keys("123")
    
    # Intentar enviar el formulario
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

    # Verificar si se ejecuta un alert (script inyectado)
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        print("❌ Vulnerabilidad XSS detectada (se ejecutó alert())")
        driver.switch_to.alert.accept()
    except:
        print("✅ El sistema está protegido contra XSS (no se ejecutó el script)")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

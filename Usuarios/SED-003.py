from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

try:
    driver.get("http://localhost/proyectoEscuela/login/index.php")

    for _ in range(5):  # Intentos fallidos
        # Limpiar campos antes de cada intento
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        email_field.clear()
        password_field.clear()

        email_field.send_keys("admin@admin.com")
        password_field.send_keys("incorrecto")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(1)

        # Hacer clic en algún lugar vacío de la pantalla para cerrar el mensaje emergente
        ActionChains(driver).move_by_offset(10, 10).click().perform()

        time.sleep(1)

    # Verificar si aparece un mensaje de cuenta bloqueada
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    if "bloqueado" in body_text:
        print("✅ Medidas de protección contra fuerza bruta implementadas correctamente.")
    else:
        print("❌ El sistema no bloqueó la cuenta tras múltiples intentos fallidos.")

except Exception as e:
    print("❌ Error en la prueba de fuerza bruta:", str(e))

finally:
    driver.quit()

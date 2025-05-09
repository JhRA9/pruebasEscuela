from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inicializar el navegador
driver = webdriver.Chrome()

try:
    # Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)

    # Ir a la lista de materias
    driver.get("http://localhost/proyectoEscuela/admin/materias/")
    time.sleep(2)

    # Esperar a que cargue la tabla con las materias
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example1"))
    )

    # Verificar que las materias están en la tabla
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    if len(filas) > 0:
        print("✅ Prueba caja negra: Se visualizan las materias correctamente.")
    else:
        print("❌ Prueba caja negra: No se visualizan materias en la tabla.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    # Paso 1: Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)

    # Paso 2: Ir a la página de materias
    driver.get("http://localhost/proyectoEscuela/admin/materias/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example1"))  # tabla de materias
    )
    time.sleep(1)

    # Paso 3: Verificar que al menos una materia está listada
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")

    if len(filas) > 0:
        print(f"✅ Prueba caja negra: Se encontraron {len(filas)} materias en el listado.")
    else:
        print("❌ Prueba caja negra: No se encontraron materias en la tabla.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

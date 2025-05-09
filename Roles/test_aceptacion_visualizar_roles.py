from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # 1. Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    # 2. Ir a la página de administración de roles
    driver.get("http://localhost/proyectoEscuela/admin/roles/")
    tabla = wait.until(EC.visibility_of_element_located((By.ID, "example1")))

    # 3. Verificar que hay al menos una fila (rol) en la tabla
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    if filas and any("ROL" in fila.text.upper() or fila.text.strip() for fila in filas):
        print("✅ Prueba de aceptación: Se visualizaron roles correctamente.")
    else:
        print("❌ Prueba de aceptación: No se encontraron roles en la tabla.")

except Exception as e:
    print(f"❌ Error durante la prueba de aceptación: {str(e)}")

finally:
    driver.quit()

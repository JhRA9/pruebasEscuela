from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    # Paso 1: Medir tiempo inicial
    tiempo_inicio = time.time()

    # Iniciar sesión
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)

    # Paso 2: Ir a la página de materias
    driver.get("http://localhost/proyectoEscuela/admin/materias/")

    # Esperar hasta que la tabla esté visible
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example1"))
    )

    # Paso 3: Esperar a que la tabla tenga al menos una fila
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#example1 tbody tr"))
    )

    # Paso 4: Medir tiempo final
    tiempo_fin = time.time()
    duracion = tiempo_fin - tiempo_inicio

    # Guardar evidencia
    driver.save_screenshot("C:/Users/casas/Documents/Docs Santiago/Universidad/Ing. Software 3/Pruebas/Prueba Rendimiento/Visualizar Materias/interfaz.png")

    print(f"✅ La carga de materias tomó {duracion:.2f} segundos.")
    if duracion > 3:
        print("⚠️ Advertencia: La carga está tomando más de 3 segundos.")
    else:
        print("✅ Rendimiento aceptable.")

except Exception as e:
    driver.save_screenshot("C:/Users/casas/Documents/Docs Santiago/Universidad/Ing. Software 3/Pruebas/Prueba Rendimiento/Visualizar Materias/error_rendimiento.png")
    print("❌ Error durante la prueba de rendimiento:", str(e))

finally:
    driver.quit()
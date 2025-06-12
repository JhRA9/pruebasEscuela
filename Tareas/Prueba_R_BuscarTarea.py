from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # Paso 1: Login
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)

    # Paso 2: Ir al listado de tareas
    driver.get("http://localhost/proyectoEscuela/admin/tareas/index.php")

    # Esperar a que cargue la tabla
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example1"))
    )

    # Paso 3: Esperar que cargue al menos una fila
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#example1 tbody tr"))
    )

    # Paso 4: Buscar tarea y medir tiempo
    tarea_a_buscar = "Prueba de lectura"
    buscador = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#example1_filter input"))
    )

    tiempo_inicio_busqueda = time.time()
    buscador.clear()
    buscador.send_keys(tarea_a_buscar)
    time.sleep(1)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//table[@id='example1']//td[contains(text(), '{tarea_a_buscar}')]"))
    )
    tiempo_fin_busqueda = time.time()

    duracion_busqueda = tiempo_fin_busqueda - tiempo_inicio_busqueda

    # Guardar evidencia
    driver.save_screenshot("C:/Users/casas/Documents/Docs Santiago/Universidad/Ing. Software 3/Pruebas/Prueba Rendimiento/Buscar Tareas/resultado_busqueda_tarea.png")

    print(f"✅ La búsqueda de la tarea tomó {duracion_busqueda:.2f} segundos.")
    if duracion_busqueda > 2:
        print("⚠️ Advertencia: La búsqueda tardó más de 2 segundos.")
    else:
        print("✅ Búsqueda rápida y aceptable.")

except Exception as e:
    driver.save_screenshot("C:/Users/casas/Documents/Docs Santiago/Universidad/Ing. Software 3/Pruebas/Prueba Rendimiento/Buscar Tareas/error_busqueda.png")
    print("❌ Error durante la prueba de rendimiento:", str(e))

finally:
    driver.quit()

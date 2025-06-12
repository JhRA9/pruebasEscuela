from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # Paso 1: Iniciar sesión
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)

    # Paso 2: Ir al listado de tareas
    driver.get("http://localhost/proyectoEscuela/admin/tareas/")
    time.sleep(2)

    # Paso 3: Buscar una tarea por su título
    titulo_a_buscar = "Prueba de lectura"
    input_busqueda = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#example1_filter input"))
    )
    input_busqueda.clear()
    input_busqueda.send_keys(titulo_a_buscar)
    time.sleep(2)


    # Paso 4: Verificar si aparece al menos una fila con el título buscado
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    encontrada = any(titulo_a_buscar.lower() in fila.text.lower() for fila in filas)

    if encontrada:
        print(f"✅ Prueba de búsqueda exitosa: la tarea '{titulo_a_buscar}' fue encontrada.")
    else:
        print(f"❌ La tarea '{titulo_a_buscar}' no fue encontrada con el buscador.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()
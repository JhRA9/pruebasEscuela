from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(4)

    # Ir al listado de tareas
    driver.get("http://localhost/proyectoEscuela/admin/tareas/index.php")
    time.sleep(4)

    # Esperar que cargue la tabla con las tareas
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tbody"))
    )

    # Comprobar que la lista no esté vacía
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    
    if len(filas) > 0:
        print("✅ Prueba caja negra: Se muestran tareas en la lista.")
    else:
        print("❌ Prueba caja negra: No se muestran tareas en la lista.")

    # Comprobar que una tarea específica aparece en la lista 
    tarea_a_buscar = "Traducción de oraciones"

    tarea_encontrada = any(tarea_a_buscar in fila.text for fila in filas)

    if tarea_encontrada:
        print(f"✅ Prueba caja negra: Tarea '{tarea_a_buscar}' encontrada en la lista.")
    else:
        print(f"❌ Prueba caja negra: Tarea '{tarea_a_buscar}' no encontrada en la lista.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

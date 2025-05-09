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
    time.sleep(2)

    # Ir al listado de tareas
    driver.get("http://localhost/proyectoEscuela/admin/tareas/index.php")
    time.sleep(10)

    # Esperar que cargue la tabla
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tbody"))
    )

    # Buscar una tarea por el nombre para eliminar
    tarea_a_eliminar = "Análisis de cuento"

    fila_tarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//td[contains(., '{tarea_a_eliminar}')]/..")
        )
    )

    # Eliminar la tarea
    fila_tarea.find_element(By.CLASS_NAME, "btn-danger").click()
    time.sleep(10)


    # Verificar que ya no aparece en la tabla
    if tarea_a_eliminar not in driver.page_source:
        print("✅ Prueba caja negra: Tarea eliminada correctamente.")
    else:
        print("❌ Prueba caja negra: La tarea aún aparece en la lista.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

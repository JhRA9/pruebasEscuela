from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inicializar el navegador
driver = webdriver.Chrome()

try:
    # Iniciar sesión como admin
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(10)

    # # Ir al formulario de creación
    # driver.get("http://localhost/proyectoEscuela/admin/tareas/create.php")
    # time.sleep(10)

    # # Llenar los campos del formulario
    # driver.find_element(By.NAME, "titulo").send_keys("Tarea prueba borrar")
    # driver.find_element(By.NAME, "descripcion").send_keys("Esto es para probar el borrado")
    # driver.find_element(By.NAME, "fecha_entrega").send_keys("2025-05-01")

    # # Llenar hora de entrega
    # hora = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.NAME, "hora_entrega"))
    # )
    # driver.execute_script("arguments[0].value = '11:11'", hora)

    # # Seleccionar materia
    # materia = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.NAME, "id_materia"))
    # )
    # materia.send_keys("MATEMÁTICA")

    # # Enviar el formulario
    # driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # time.sleep(10)

    # print("✅ Tarea creada correctamente")

    # Ir al listado de tareas
    driver.get("http://localhost/proyectoEscuela/admin/tareas/index.php")
    time.sleep(10)

    # Esperar a que cargue la tabla
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tbody"))
    )

    # Buscar la fila de la tarea 
    fila_tarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//td[contains(., 'Tarea 8')]/..")
        )
    )

    # Dentro de esa fila, encontrar el botón de borrar
    boton_borrar = fila_tarea.find_element(By.CLASS_NAME, "btn-danger")
    boton_borrar.click()

    print("✅ Se presionó el botón de borrar correctamente")

    time.sleep(10)
    if "Tarea prueba borrar" not in driver.page_source:
        print("✅ La tarea fue eliminada exitosamente.")
    else:
        print("❌ La tarea todavía aparece en el listado.")
        time.sleep(10)

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

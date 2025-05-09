from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # Paso 1: Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)
    print("✅ Paso 1: Iniciar sesión como administrador correctamente.")

    # Iniciar sesión como profesor 
    # driver.get("http://localhost/proyectoEscuela/login/index.php")
    # driver.find_element(By.NAME, "email").send_keys("profesor@gmail.com")
    # driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    # time.sleep(2)
    # print("✅ Paso 1: Iniciar sesión como profesor correctamente.")

    # Paso 2: Crear tarea para eliminar
    driver.get("http://localhost/proyectoEscuela/admin/tareas/create.php")
    driver.find_element(By.NAME, "titulo").send_keys("Tarea para eliminar")
    driver.find_element(By.NAME, "descripcion").send_keys("Creada solo para prueba de eliminación")
    driver.find_element(By.NAME, "fecha_entrega").send_keys("2025-05-30")

    hora = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "hora_entrega"))
    )
    driver.execute_script("arguments[0].value = '15:00'", hora)

    materia = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "id_materia"))
    )
    materia.send_keys("MATEMÁTICA")

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)
    print("✅ Paso 2: Tarea creada correctamente.")

    # Paso 3: Ir al listado de tareas y eliminar la creada
 
    driver.get("http://localhost/proyectoEscuela/admin/tareas/index.php")
    time.sleep(10)

    # Esperar a que cargue la tabla
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tbody"))
    )

    # Buscar la fila de la tarea 
    fila_tarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//td[contains(., 'Tarea para eliminar')]/..")
        )
    )

    # Dentro de esa fila, encontrar el botón de borrar
    boton_borrar = fila_tarea.find_element(By.CLASS_NAME, "btn-danger")
    boton_borrar.click()

    print("✅ Se presionó el botón de borrar correctamente")


    time.sleep(2)
    print("✅ Paso 3: Tarea eliminada correctamente.")

    # Paso 4: Verificar que ya no esté en la lista
    page_source = driver.page_source
    if "Tarea para eliminar" not in page_source:
        print("✅ Prueba de Aceptación: Tarea ya no aparece en el listado.")
    else:
        print("❌ Prueba de Aceptación: La tarea sigue en el listado.")

except Exception as e:
    print("❌ Error durante la prueba de aceptación:", str(e))

finally:
    driver.quit()
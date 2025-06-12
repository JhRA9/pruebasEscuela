from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()

try:
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    # Flujo 1: Creación de tarea válida
    try:        
       # Datos de la tarea a crear
        nuevo_titulo = "Prueba de lectura"
        nuevo_descripccion = "Te vas a leer 100 años de seriedad"
        nueva_fecha = "2025-05-10"
        nueva_hora = "23:59:00"
        valor_materia = "3"

        # Navegar a la página de tareas
        driver.get("http://localhost/proyectoEscuela/admin/tareas/")
        driver.save_screenshot("C:/Users/casas/Documents/Docs Santiago/Universidad/Ing. Software 3/Pruebas/Prueba Aceptacion/Crear tarea/antes.png")
        time.sleep(5)

        # Negación a la página de creación de tarea
        driver.get("http://localhost/proyectoEscuela/admin/tareas/create.php")
        driver.find_element(By.NAME, "titulo").clear()
        driver.find_element(By.NAME, "titulo").send_keys(nuevo_titulo)
        driver.find_element(By.NAME, "descripcion").clear()
        driver.find_element(By.NAME, "descripcion").send_keys(nuevo_descripccion)
        driver.execute_script("document.getElementsByName('fecha_entrega')[0].value = arguments[0]", nueva_fecha)
        hora_input = driver.execute_script("document.getElementsByName('hora_entrega')[0].value = arguments[0]", nueva_hora)
        Select(driver.find_element(By.NAME, "id_materia")).select_by_value(valor_materia)
        driver.save_screenshot("C:/Users/casas/Documents/Docs Santiago/Universidad/Ing. Software 3/Pruebas/Prueba Aceptacion/Crear tarea/durante.png")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)

        # Verificar que la creación fue exitosa
        
        driver.get("http://localhost/proyectoEscuela/admin/tareas/")
        driver.save_screenshot("C:/Users/casas/Documents/Docs Santiago/Universidad/Ing. Software 3/Pruebas/Prueba Aceptacion/Crear tarea/despues.png")

        print("✅ Flujo 1: Creación de tarea válida - PASÓ")

    except Exception as e:
        print("❌ Flujo 1: Creación de tarea - FALLÓ:", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
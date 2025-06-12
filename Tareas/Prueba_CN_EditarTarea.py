from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()

try:
    # Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    try:        
        nuevo_titulo = "Prueba de anatomia"
        nuevo_descripccion = "Chúzate un pulmón a ver si duele"
        nueva_fecha = "2025-05-10"
        nueva_hora = "23:59:00"
        valor_materia = "4"
        nuevo_estado = "Pendiente"
        
        # Navegar a la página de edición de tarea
        driver.get("http://localhost/proyectoEscuela/admin/tareas/edit.php?id=64")

        # Llenar los campos de edición de tarea
        driver.find_element(By.NAME, "titulo").clear()
        driver.find_element(By.NAME, "titulo").send_keys(nuevo_titulo)
        driver.find_element(By.NAME, "descripcion").clear()
        driver.find_element(By.NAME, "descripcion").send_keys(nuevo_descripccion)
        driver.execute_script("document.getElementsByName('fecha_entrega')[0].value = arguments[0]", nueva_fecha)
        driver.find_element(By.NAME, "hora_entrega").send_keys(Keys.CONTROL + "a", nueva_hora)
        Select(driver.find_element(By.NAME, "id_materia")).select_by_value(valor_materia)
        Select(driver.find_element(By.NAME, "estado")).select_by_visible_text(nuevo_estado)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)

        # Verificar que la edición fue exitosa
        if "La tarea se actualizó" in driver.page_source:
            print("✅ Prueba exitosa: tarea editada correctamente.")
        else:
            print("❌ No se detectó mensaje de éxito.")
        
    except Exception as e:
        print("❌ Prueba fallida", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
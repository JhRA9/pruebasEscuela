from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # Login como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(3)

    # ✅ FLUJO 1: Edición válida
    try:
        # Datos de la tarea a editar
        nuevo_titulo = "Tirar el yoyo"
        driver.get("http://localhost/proyectoEscuela/admin/materias/edit.php?id=7")

        input_titulo = driver.find_element(By.NAME, "nombre_materia")
        input_titulo.clear()
        input_titulo.send_keys(nuevo_titulo)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)

        print("✅ Flujo 1: Edición válida realizada.")
    except Exception as e:
        print("❌ Flujo 1: Falló al editar el usuario:", str(e))

    # FLUJO 2: Confirmación post-edición
    try:
        time.sleep(5) 
        mensaje_confirmacion = driver.page_source
        if "Se actualizó la materia de la manera correcta en la base de datos" in mensaje_confirmacion:
            print("✅ Flujo 2: Mensaje de confirmación visible.")
        else:
            print("⚠️ Flujo 2: No se encontró mensaje de confirmación, verificar manualmente.")
    except Exception as e:
        print("❌ Flujo 2: Error al verificar mensaje de confirmación:", str(e))

    # FLUJO 3: Verificación en tabla
    try:
        driver.get("http://localhost/proyectoEscuela/admin/materias/")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "example1"))
        )
        time.sleep(5)

        filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
        tarea_encontrada = any(nuevo_titulo in fila.text for fila in filas)

        if tarea_encontrada:
            print(f"✅ Flujo 3: Titulo '{nuevo_titulo}' actualizado encontrado en la tabla.")
        else:
            print(f"❌ Flujo 3: Titulo '{nuevo_titulo}' no aparece en la tabla.")
    except Exception as e:
        print("❌ Flujo 3: Error al buscar Titulo en la tabla:", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
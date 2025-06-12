from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    # 1. Iniciar sesión
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)

    # 2. Ir al listado de materias
    driver.get("http://localhost/proyectoEscuela/admin/materias/")
    time.sleep(2)

    # 3. Buscar la materia a eliminar
    materia_a_eliminar = "Corte y confección de tamales"
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    eliminada = False

    for fila in filas:
        if materia_a_eliminar in fila.text:
            formulario = fila.find_element(By.XPATH, ".//form[contains(@id,'miFormulario')]")
            form_id = formulario.get_attribute("id")
            # Enviar el formulario con JS
            driver.execute_script(f"document.getElementById('{form_id}').submit();")
            eliminada = True
            break

    if eliminada:
        time.sleep(3)  # Espera a que recargue después de eliminar

        # 4. Verificar que la materia ya no aparece
        materia_sigue = materia_a_eliminar in driver.page_source

        # 5. Verificar si hay un mensaje de éxito
        mensaje_exito = None
        try:
            mensaje_element = driver.find_element(By.CLASS_NAME, "alert-success")
            mensaje_exito = mensaje_element.text
        except:
            mensaje_exito = None

        # Resultados
        if not materia_sigue or mensaje_exito:
            print("✅ Materia eliminada correctamente y mensaje de éxito mostrado.")
            print("🟢 Mensaje:", mensaje_exito)
        elif not materia_sigue:
            print("⚠️ Materia eliminada pero no se mostró el mensaje de éxito.")
        else:
            print("❌ La materia aún aparece en la tabla. No se eliminó correctamente.")
    else:
        print("❌ Materia no encontrada.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    # Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)

    # Ir al listado de roles
    driver.get("http://localhost/proyectoEscuela/admin/roles/")
    time.sleep(2)

    # Buscar el rol a eliminar
    rol_a_eliminar = "DIRECTOR"
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    encontrado = False

    for fila in filas:
        if rol_a_eliminar.upper() in fila.text.upper():
            # Eliminar directamente el formulario
            formulario = fila.find_element(By.XPATH, ".//form[contains(@action,'delete.php')]")
            formulario.submit()
            encontrado = True
            break

    if encontrado:
        time.sleep(3)

        # Verificar mensaje de éxito
        mensaje = ""
        try:
            mensaje_element = driver.find_element(By.CLASS_NAME, "alert-success")
            mensaje = mensaje_element.text
        except:
            pass

        # Verificar que el rol ya no esté en la tabla
        driver.refresh()
        time.sleep(2)
        if rol_a_eliminar.upper() not in driver.page_source.upper() and mensaje:
            print("✅ Prueba de caja negra exitosa: el rol fue eliminado y el usuario recibió confirmación.")
        elif rol_a_eliminar.upper() not in driver.page_source.upper():
            print("⚠️ El rol fue eliminado, pero no se mostró mensaje de éxito.")
        else:
            print("❌ El rol no se eliminó correctamente.")
    else:
        print("❌ No se encontró el rol en la tabla para eliminar.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()
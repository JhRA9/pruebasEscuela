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
        driver.get("http://localhost/proyectoEscuela/admin/usuarios/edit.php?id=43")
        time.sleep(2)

        # Editar datos
        nuevo_nombre = "Juanito Alimaña"
        nuevo_email = "juanito@estudiante.com"

        driver.find_element(By.NAME, "nombres").clear()
        driver.find_element(By.NAME, "nombres").send_keys(nuevo_nombre)
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys(nuevo_email)
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("123")
        driver.find_element(By.NAME, "password_repeat").clear()
        driver.find_element(By.NAME, "password_repeat").send_keys("123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        print("✅ Flujo 1: Edición válida realizada.")
    except Exception as e:
        print("❌ Flujo 1: Falló al editar el usuario:", str(e))

    # FLUJO 2: Confirmación post-edición
    try:
        mensaje_confirmacion = driver.page_source
        if "actualizado correctamente" in mensaje_confirmacion or "modificado" in mensaje_confirmacion:
            print("✅ Flujo 2: Mensaje de confirmación visible.")
        else:
            print("⚠️ Flujo 2: No se encontró mensaje de confirmación, verificar manualmente.")
    except Exception as e:
        print("❌ Flujo 2: Error al verificar mensaje de confirmación:", str(e))

    # FLUJO 3: Verificación en tabla
    try:
        driver.get("http://localhost/proyectoEscuela/admin/usuarios/")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "example1"))
        )
        time.sleep(2)

        filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
        for fila in filas:
            print("➡️ Fila:", fila.text)  # Debug: ver qué lee Selenium

        usuario_encontrado = any(nuevo_nombre in fila.text and nuevo_email in fila.text for fila in filas)

        if usuario_encontrado:
            print(f"✅ Flujo 3: Usuario '{nuevo_nombre}' actualizado encontrado en la tabla.")
        else:
            print(f"❌ Flujo 3: Usuario '{nuevo_nombre}' no aparece en la tabla.")
    except Exception as e:
        print("❌ Flujo 3: Error al buscar usuario en la tabla:", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
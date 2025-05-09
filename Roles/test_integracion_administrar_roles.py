from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    wait = WebDriverWait(driver, 10)
    rol_prueba = "DIRECTOR"

    # 1. Login como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    # 2. Crear el rol
    driver.get("http://localhost/proyectoEscuela/admin/roles/create.php")
    wait.until(EC.visibility_of_element_located((By.NAME, "nombre_rol"))).clear()
    driver.find_element(By.NAME, "nombre_rol").send_keys(rol_prueba)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # 3. Confirmación del mensaje de creación (SweetAlert)
    try:
        titulo_alerta = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title"))).text
        icono_alerta = driver.find_element(By.CLASS_NAME, "swal2-icon").get_attribute("class")

        if "success" in icono_alerta and "Se registro el rol" in titulo_alerta:
            print("🟢 Rol creado exitosamente con ícono de éxito.")
        else:
            print(f"⚠️ Mensaje inesperado: '{titulo_alerta}' con ícono '{icono_alerta}'.")
    except Exception as e:
        print("❌ No se encontró el mensaje de éxito tras la creación del rol (SweetAlert).")

    # 4. Verificar en la tabla
    driver.get("http://localhost/proyectoEscuela/admin/roles/")
    tabla = wait.until(EC.visibility_of_element_located((By.ID, "example1")))
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")

    encontrado = False
    for fila in filas:
        if rol_prueba.upper() in fila.text.upper():
            print("🟢 Rol encontrado en la lista.")
            # 5. Eliminar el rol
            formulario = fila.find_element(By.XPATH, ".//form[contains(@action,'delete.php')]")
            formulario.submit()
            encontrado = True
            break

    if not encontrado:
        print("❌ Rol no encontrado en la tabla para eliminar.")

    # 6. Verificar eliminación (SweetAlert)
    if encontrado:
        try:
            titulo_alerta = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title"))).text
            icono_alerta = driver.find_element(By.CLASS_NAME, "swal2-icon").get_attribute("class")

            if "success" in icono_alerta and "Se elimino el rol" in titulo_alerta:
                print("🟢 Rol eliminado exitosamente con ícono de éxito.")
            else:
                print(f"⚠️ Mensaje inesperado: '{titulo_alerta}' con ícono '{icono_alerta}'.")
        except Exception as e:
            print("❌ No se encontró el mensaje de éxito tras la eliminación del rol (SweetAlert).")

        # Confirmar que ya no esté en la tabla
        driver.refresh()
        wait.until(EC.visibility_of_element_located((By.ID, "example1")))
        if rol_prueba.upper() not in driver.page_source.upper():
            print("🟢 El rol fue eliminado correctamente de la tabla.")
        else:
            print("❌ El rol aún aparece en la tabla tras eliminación.")

except Exception as e:
    print(f"❌ Error general durante la prueba: {str(e)}")

finally:
    driver.quit()

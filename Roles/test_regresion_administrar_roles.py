from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verificar_alerta_exito(wait, driver, mensaje_esperado):
    try:
        titulo_alerta = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title"))).text
        icono_alerta = driver.find_element(By.CLASS_NAME, "swal2-icon").get_attribute("class")

        if "success" in icono_alerta and mensaje_esperado in titulo_alerta:
            print(f"[✔️ ÉXITO] {mensaje_esperado} - Operación completada con éxito.")
        else:
            print(f"[⚠️ ADVERTENCIA] Mensaje inesperado: '{titulo_alerta}' con ícono '{icono_alerta}'.")
    except Exception as e:
        print(f"[❌ ERROR] No se encontró el mensaje esperado: {str(e)}")

def gestionar_rol(driver, wait, rol_prueba):
    try:
        # 1. Login como administrador
        driver.get("http://localhost/proyectoEscuela/login/index.php")
        wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("admin@admin.com")
        driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

        # 2. Crear el rol
        driver.get("http://localhost/proyectoEscuela/admin/roles/create.php")
        wait.until(EC.visibility_of_element_located((By.NAME, "nombre_rol"))).clear()
        driver.find_element(By.NAME, "nombre_rol").send_keys(rol_prueba)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # 3. Confirmación de creación (SweetAlert)
        verificar_alerta_exito(wait, driver, "Se registro el rol de manera correcta")


        # 4. Verificar en la tabla
        driver.get("http://localhost/proyectoEscuela/admin/roles/")
        tabla = wait.until(EC.visibility_of_element_located((By.ID, "example1")))
        filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")

        encontrado = False
        for fila in filas:
            if rol_prueba.upper() in fila.text.upper():
                print(f"[✔️ ROL ENCONTRADO] El rol '{rol_prueba}' se encuentra en la lista.")
                # 5. Eliminar el rol
                formulario = fila.find_element(By.XPATH, ".//form[contains(@action,'delete.php')]")
                formulario.submit()
                encontrado = True
                break

        if not encontrado:
            print(f"[❌ ROL NO ENCONTRADO] El rol '{rol_prueba}' no fue encontrado en la tabla.")

        # 6. Verificar eliminación (SweetAlert)
        if encontrado:
            verificar_alerta_exito(wait, driver, "Se elimino el rol de manera correcta")

            # Confirmar que ya no esté en la tabla
            driver.refresh()
            wait.until(EC.visibility_of_element_located((By.ID, "example1")))
            if rol_prueba.upper() not in driver.page_source.upper():
                print(f"[✔️ ELIMINACIÓN CONFIRMADA] El rol '{rol_prueba}' fue eliminado correctamente.")
            else:
                print(f"[❌ ERROR AL ELIMINAR] El rol '{rol_prueba}' aún aparece en la tabla tras eliminación.")

    except Exception as e:
        print(f"[❌ ERROR GENERAL] Ocurrió un error durante la prueba: {str(e)}")

# Ejecución principal
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
rol_prueba = "DIRECTOR"

try:
    gestionar_rol(driver, wait, rol_prueba)
finally:
    driver.quit()

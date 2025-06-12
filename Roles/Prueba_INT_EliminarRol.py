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

    # 2. Ir al listado de roles
    driver.get("http://localhost/proyectoEscuela/admin/roles/")
    time.sleep(2)

    # 3. Buscar el rol a eliminar
    rol_a_eliminar = "COORDINADOR"
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    eliminada = False

    for fila in filas:
        texto_fila = fila.text.strip().upper()
        if rol_a_eliminar.upper() in texto_fila:
            formulario = fila.find_element(By.XPATH, ".//form[contains(@action,'delete.php')]")
            formulario.submit()
            eliminada = True
            break

    if eliminada:
        time.sleep(3)

        # 4. Verificar que el rol ya no aparece
        driver.refresh()
        time.sleep(2)
        rol_sigue = rol_a_eliminar.upper() in driver.page_source.upper()

        # 5. Verificar si hay un mensaje de éxito
        mensaje_exito = None
        try:
            mensaje_element = driver.find_element(By.CLASS_NAME, "alert-success")
            mensaje_exito = mensaje_element.text
        except:
            mensaje_exito = None

        # Resultados
        if not rol_sigue and mensaje_exito:
            print("✅ Rol eliminado correctamente y mensaje de éxito mostrado.")
            print("🟢 Mensaje:", mensaje_exito)
        elif not rol_sigue:
            print("⚠️ Rol eliminado pero no se mostró el mensaje de éxito.")
        else:
            print("❌ El rol aún aparece en la tabla. No se eliminó correctamente.")
    else:
        print("❌ Rol no encontrado. Verifica que el nombre del rol sea correcto.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()
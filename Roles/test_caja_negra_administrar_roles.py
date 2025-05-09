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

    # Ir a la vista de roles
    driver.get("http://localhost/proyectoEscuela/admin/roles/")
    time.sleep(2)

    # Verificar que la tabla de roles aparece
    tabla_roles = driver.find_elements(By.XPATH, "//table[contains(@id, 'example')]//tr")
    if len(tabla_roles) > 1:
        print("✅ Prueba caja negra: La tabla de roles se muestra correctamente.")
    else:
        print("❌ Prueba caja negra: La tabla de roles está vacía o no cargó correctamente.")

    # Verificar que el rol "PROFESOR" está presente
    if "PROFESOR" in driver.page_source:
        print("✅ Prueba caja negra: Rol 'PROFESOR' encontrado.")
    else:
        print("❌ Prueba caja negra: Rol 'PROFESOR' no encontrado.")

    if "bayron" in driver.page_source:
        print("✅ Prueba caja negra: Rol 'bayron' encontrado.")
    else:
        print("❌ Prueba caja negra: Rol 'bayron' no encontrado.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

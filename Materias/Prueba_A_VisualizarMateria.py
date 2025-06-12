from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    # Iniciar sesión como admin
    driver.get("http://localhost/proyectoEscuela//login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)

    time.sleep(5)

    # Ir a la página del listado de materias
    driver.get("http://localhost/proyectoEscuela/admin/materias/")

    time.sleep(10)

    # Verificar que la tabla de materias se haya cargado correctamente
    filas = driver.find_elements(By.XPATH, "//table//tbody//tr")

    if len(filas) > 0:
        print(f"Prueba exitosa: se encontraron {len(filas)} materias en la tabla. :D")
    else:
        print("No se encontraron materias en la tabla. :'( ")

except Exception as e:
    print("Error durante la prueba :(", str(e))

finally:
    driver.quit()
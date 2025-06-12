from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:
    # Flujo 1: Login como administrador
    try:
        driver.get("http://localhost/proyectoEscuela/login/index.php")
        driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
        driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
        time.sleep(5)

        print("✅ Flujo 1: Login administrador - PASÓ")
    except Exception as e:
        print("❌ Flujo 1: Login administrador - FALLÓ:", str(e))

    # Flujo 2: Acceso y carga de usuarios
    try:
        driver.get("http://localhost/proyectoEscuela/admin/usuarios/")
        time.sleep(5)

        # Verificar que hay al menos una fila en la tabla de usuarios
        filas = driver.find_elements(By.XPATH, "//table//tbody//tr")
        if len(filas) > 0:
            print(f"✅ Flujo 2: Visualización de usuarios - PASÓ: {len(filas)} usuarios encontrados.")
        else:
            print("❌ Flujo 2: Visualización de usuarios - FALLÓ: no se encontraron filas.")
    except Exception as e:
        print("❌ Flujo 2: Visualización de usuarios - FALLÓ:", str(e))

     # Flujo 3: Verificación en la tabla de usuarios (por nombre o email)
    try:
        usuario_encontrado = False
        nombre_buscado = "Pepito Perez"
        filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
        
        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, "td")
            for celda in celdas:
                if nombre_buscado in celda.text:
                    usuario_encontrado = True
                    break
            if usuario_encontrado:
                break

        if usuario_encontrado:
            print(f"✅ Flujo 3: Usuario '{nombre_buscado}' está presente en la tabla.")
        else:
            print(f"❌ Flujo 3: Usuario '{nombre_buscado}' NO se encontró.")
    except Exception as e:
        print("❌ Flujo 3: Verificación de usuario en tabla - FALLÓ:", str(e))

except Exception as e:
    print("❌ Error general durante la prueba:", str(e))

finally:
    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # Paso 1: Login como admin
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(2)

    # Paso 2: Ir a Crear Materia
    driver.get("http://localhost/proyectoEscuela/admin/materias/create.php")
    time.sleep(5)
    nombre_materia = "Materia Integración"
    descripcion_materia = "integración"

    driver.find_element(By.NAME, "nombre_materia").send_keys(nombre_materia)
    driver.find_element(By.NAME, "descripcion").send_keys(descripcion_materia)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(8)
    print("✅ Materia creada correctamente.")

    # Paso 3: Buscar en el listado
    driver.get("http://localhost/proyectoEscuela/admin/materias/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example1"))
    )
    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    encontrada = None
    for fila in filas:
        if nombre_materia in fila.text:
            encontrada = fila
            break

    if not encontrada:
        raise Exception("No se encontró la materia recién creada en el listado.")

    print("✅ Materia aparece en la tabla.")

    # Paso 4: Ir a Editar
    boton_editar = encontrada.find_element(By.CLASS_NAME, "btn-success")
    boton_editar.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "nombre_materia")))

    nuevo_nombre = "Materia Editada"
    campo_nombre = driver.find_element(By.NAME, "nombre_materia")
    campo_nombre.clear()
    campo_nombre.send_keys(nuevo_nombre)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(8)
    print("✅ Materia editada correctamente.")

    # Paso 5: Eliminar la materia (con confirmación modal)
    driver.get("http://localhost/proyectoEscuela/admin/materias/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example1"))
    )

    filas = driver.find_elements(By.XPATH, "//table[@id='example1']//tbody//tr")
    for fila in filas:
        if nuevo_nombre in fila.text:
            # Clic en botón eliminar (abre el modal de SweetAlert2)
            fila.find_element(By.CLASS_NAME, "btn-danger").click()

            # Esperar a que el modal sea visible y clic en "Eliminar" (SweetAlert2)
            boton_confirmar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Eliminar')]"))
            )
            boton_confirmar.click()

            print("✅ Materia eliminada correctamente.")
            break
    else:
        raise Exception("No se encontró la materia para eliminar.")
    
except Exception as e:
    print("❌ Error durante la prueba de integración:", str(e))

finally:
    driver.quit()

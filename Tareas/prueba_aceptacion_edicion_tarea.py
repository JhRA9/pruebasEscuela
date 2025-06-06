from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Configuro el navegador para realizar las pruebas
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://localhost/proyectoEscuela/login/index.php")


# Creo una carpeta para guardar las capturas de pantalla
if not os.path.exists("Capturas de pantalla"):
    os.makedirs("Capturas de pantalla")

# Defino una función para tomar capturas de pantalla
def capturar_pantalla(nombre):
    driver.save_screenshot(f"Capturas de pantalla/{nombre}.png")

# Defino una función para verificar si el usuario fue redirigido correctamente
def verificar_redireccion(url_esperada):
    return url_esperada in driver.current_url

# Flujo 1: Inicio de sesión para usuarios autenticados
try:
    print("Iniciando sesión como usuario autenticado...")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    driver.find_element(By.NAME, "email").send_keys("profesor@gmail.com")  # Credenciales actualizadas
    driver.find_element(By.NAME, "password").send_keys("123")
    capturar_pantalla("flujo1_ingresando_datos_login")
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Verifico si el usuario fue redirigido correctamente al dashboard
    WebDriverWait(driver, 10).until(lambda d: verificar_redireccion("admin"))
    capturar_pantalla("flujo1_login_exitoso")
    print("Flujo 1: Inicio de sesión - PASÓ")
except Exception as e:
    capturar_pantalla("flujo1_error")
    print(f"Flujo 1: Inicio de sesión - FALLÓ: {e}")
    driver.quit()
    exit()

# Flujo 2: Acceso a la tarea existente
try:
    print("Probando acceso a la tarea existente...")
    driver.get("http://localhost/proyectoEscuela/admin/tareas/index.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "example1")))

    # Si hay una alerta en pantalla, la cierro antes de continuar
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-container")))
        driver.find_element(By.CLASS_NAME, "swal2-confirm").click()
    except:
        pass

    # Selecciono dinámicamente el primer enlace de edición disponible
    primer_enlace_editar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'edit.php')]"))
    )
    primer_enlace_editar.click()

    # Espero a que cargue el formulario de edición
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "titulo")))
    capturar_pantalla("flujo2_acceso_edicion")
    print("Flujo 2: Acceso a la tarea existente - PASÓ")
except Exception as e:
    capturar_pantalla("flujo2_error")
    print(f"Flujo 2: Acceso a la tarea existente - FALLÓ: {e}")

# Flujo 3: Modificación válida de campos
try:
    print("Probando modificación válida de campos...")
    titulo_input = driver.find_element(By.NAME, "titulo")
    descripcion_input = driver.find_element(By.NAME, "descripcion")
    fecha_entrega_input = driver.find_element(By.NAME, "fecha_entrega")

    # Modifico los campos con valores válidos
    titulo_input.clear()
    titulo_input.send_keys("Tarea Editada Correctamente")  # Aseguro que el título sea llenado correctamente
    descripcion_input.clear()
    descripcion_input.send_keys("Descripción actualizada de la tarea.")
    fecha_entrega_input.clear()
    driver.execute_script("document.getElementsByName('fecha_entrega')[0].value = '2025-05-15'")
    capturar_pantalla("flujo3_campos_modificados")

    # Guardo los cambios
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar Tarea')]").click()
    WebDriverWait(driver, 10).until(lambda d: verificar_redireccion("admin/tareas"))
    capturar_pantalla("flujo3_tarea_actualizada")
    print("Flujo 3: Modificación válida de campos - PASÓ")
except Exception as e:
    capturar_pantalla("flujo3_error")
    print(f"Flujo 3: Modificación válida de campos - FALLÓ: {e}")

# Cierro el navegador después de realizar las pruebas
driver.quit()
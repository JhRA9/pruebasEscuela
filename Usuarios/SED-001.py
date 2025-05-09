from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Generar datos únicos
correo_nuevo = f"seguridad_test_{random.randint(1000, 9999)}@gmail.com"
password = "Test123456"

driver = webdriver.Chrome()

try:
    # 1. Iniciar sesión como administrador
    driver.get("http://localhost/proyectoEscuela/login/index.php")
    driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
    time.sleep(1)

    # 2. Ir al módulo de usuarios
    driver.get("http://localhost/proyectoEscuela/admin/usuarios/")
    time.sleep(1)

    # 3. Ir al formulario de creación
    driver.get("http://localhost/proyectoEscuela/admin/usuarios/create.php")
    time.sleep(1)

    # 4. Llenar el formulario
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "nombres"))
    )

    driver.find_element(By.NAME, "nombres").send_keys("Usuario Seguridad")
    driver.find_element(By.NAME, "email").send_keys(correo_nuevo)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password_repeat").send_keys(password)

    # Dejar el rol por defecto (primer opción) o seleccionarlo si lo deseas
    # También podrías usar Select() si necesitas elegir uno específico

    # 5. Click en el botón "Guardar rol"
    botones = driver.find_elements(By.XPATH, "//button[@type='submit']")
    for boton in botones:
        if "Guardar rol" in boton.text:
            boton.click()
            break

    time.sleep(10)
    print(f"✅ Usuario creado con éxito: {correo_nuevo}")
    print("🔍 Verifica manualmente en la base de datos si la contraseña está hasheada correctamente.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

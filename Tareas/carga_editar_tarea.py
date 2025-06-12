# carga_editar_tarea.py

import requests

URL_LOGIN = "http://localhost/proyectoEscuela//logout.php"
URL_EDITAR = "http://localhost/proyectoEscuela//admin/materias/edit.php?id=3"

session = requests.Session()

# Iniciar sesión como admin
login_payload = {
    "email": "admin@admin.com",
    "password": "123"
}
login_response = session.post(URL_LOGIN, data=login_payload)

if "Dashboard" in login_response.text or login_response.ok:
    print("✅ Sesión iniciada correctamente.")
else:
    print("❌ Error al iniciar sesión.")
    exit()

# Ejecutar la carga
total_intentos = 500
exitosos = 0
errores = 0

for i in range(total_intentos):
    nuevo_titulo = f"Materia Carga #{i}"
    editar_payload = {
        "id_materia": "7",  # ID real de la materia a editar
        "nombre_materia": nuevo_titulo
    }

    response = session.post(URL_EDITAR, data=editar_payload)
    if "actualizó la materia" in response.text or response.status_code == 200:
        exitosos += 1
    else:
        errores += 1

print(f"\nTotal intentos: {total_intentos}")
print(f"Ediciones exitosas: {exitosos}")
print(f"Errores: {errores}")

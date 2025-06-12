# performance_editar_tarea.py

import requests
import time

# Configurar URLs
URL_LOGIN = "http://localhost/proyectoEscuela/login/index.php"
URL_EDITAR = "http://localhost/proyectoEscuela/admin/materias/edit.php?id=7"

# Crear sesión
session = requests.Session()

# Iniciar sesión
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

# Prueba de performance
intentos = 100
tiempos = []

for i in range(intentos):
    nuevo_titulo = f"Materia Perf #{i}"
    editar_payload = {
        "id_materia": "7",
        "nombre_materia": nuevo_titulo
    }

    inicio = time.time()
    response = session.post(URL_EDITAR, data=editar_payload)
    fin = time.time()

    duracion = fin - inicio
    tiempos.append(duracion)

    if not response.ok:
        print(f"❌ Error en intento {i + 1}")

# Resultados
promedio = sum(tiempos) / intentos
print(f"\n📊 Total de intentos: {intentos}")
print(f"⏱️ Tiempo promedio por edición: {promedio:.4f} segundos")
print(f"⏱️ Tiempo máximo: {max(tiempos):.4f} segundos")
print(f"⏱️ Tiempo mínimo: {min(tiempos):.4f} segundos")

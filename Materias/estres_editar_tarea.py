import requests
import time
import statistics

# Configuración
URL_LOGIN = "http://localhost/proyectoEscuela/login/index.php"
ID_TAREA = 127  # Cambiar si se desea probar otra tarea
URL_EDITAR = f"http://localhost/proyectoEscuela/admin/tareas/edit.php?id={ID_TAREA}"
TOTAL_INTENTOS = 100

# Datos de prueba
editar_payload_base = {
    "fecha_entrega": "2025-06-30",
    "hora_entrega": "23:59:00",
    "id_materia": "4",  # ID válido según la BD
    "estado": "Pendiente"
}

# Iniciar sesión
session = requests.Session()
login_payload = {
    "email": "admin@admin.com",
    "password": "123"
}
login_response = session.post(URL_LOGIN, data=login_payload)

if "Dashboard" not in login_response.text and not login_response.ok:
    print("❌ Error al iniciar sesión. Detalles:", login_response.status_code)
    exit()
else:
    print("✅ Sesión iniciada correctamente.")

# Resultados
exitosos = 0
errores = 0
tiempos_respuesta = []

# Prueba de estrés
for i in range(TOTAL_INTENTOS):
    editar_payload = editar_payload_base.copy()
    editar_payload["titulo"] = f"Tarea Estrés #{i}"
    editar_payload["descripcion"] = f"Descripción automática #{i}"

    try:
        inicio = time.time()
        response = session.post(URL_EDITAR, data=editar_payload)
        fin = time.time()

        duracion = fin - inicio
        tiempos_respuesta.append(duracion)

        if "actualizó" in response.text or response.ok:
            exitosos += 1
            print(f"✅ Intento #{i}: éxito ({duracion:.2f} seg)")
        else:
            errores += 1
            print(f"❌ Intento #{i}: fallo HTTP {response.status_code} ({duracion:.2f} seg)")

    except requests.exceptions.RequestException as e:
        errores += 1
        print(f"❌ Error de red en intento #{i}: {e}")

# Estadísticas
print("\n📊 Resumen de la prueba de estrés:")
print(f"Total intentos: {TOTAL_INTENTOS}")
print(f"✔️ Éxitos: {exitosos}")
print(f"❌ Errores: {errores}")
if tiempos_respuesta:
    print(f"⏱️ Tiempo medio de respuesta: {statistics.mean(tiempos_respuesta):.3f} seg")
    print(f"⏱️ Tiempo máximo de respuesta: {max(tiempos_respuesta):.3f} seg")
    print(f"⏱️ Tiempo mínimo de respuesta: {min(tiempos_respuesta):.3f} seg")

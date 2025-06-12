import requests
import time
import statistics

# Configuración
URL_LOGIN = "http://localhost/proyectoEscuela/login/index.php"
ID_MATERIA = 130  # Cambia este valor según tu base de datos
URL_EDITAR = f"http://localhost/proyectoEscuela/admin/materias/edit.php?id={ID_MATERIA}"
TOTAL_INTENTOS = 100

# Datos base para la materia
editar_payload_base = {
    "id_materia": str(ID_MATERIA),
}

# Iniciar sesión
session = requests.Session()
login_payload = {
    "email": "admin@admin.com",
    "password": "123"
}
login_response = session.post(URL_LOGIN, data=login_payload)

if "Dashboard" not in login_response.text and not login_response.ok:
    print("❌ Error al iniciar sesión:", login_response.status_code)
    exit()
else:
    print("✅ Sesión iniciada correctamente.\n")

# Resultados
exitosos = 0
errores = 0
tiempos_respuesta = []

# Ejecutar carga sin imprimir cada intento
for i in range(TOTAL_INTENTOS):
    editar_payload = editar_payload_base.copy()
    editar_payload["nombre_materia"] = f"Materia Carga #{i}"

    try:
        inicio = time.time()
        response = session.post(URL_EDITAR, data=editar_payload)
        duracion = time.time() - inicio
        tiempos_respuesta.append(duracion)

        if "actualizó la materia" in response.text or response.ok:
            exitosos += 1
        else:
            errores += 1

    except requests.exceptions.RequestException:
        errores += 1

# Estadísticas
print("📊 Resumen de la prueba de carga:")
print(f"Total intentos: {TOTAL_INTENTOS}")
print(f"✔️ Éxitos: {exitosos}")
print(f"❌ Errores: {errores}")

if tiempos_respuesta:
    print(f"⏱️ Tiempo medio de respuesta: {statistics.mean(tiempos_respuesta):.3f} seg")
    print(f"⏱️ Tiempo máximo de respuesta: {max(tiempos_respuesta):.3f} seg")
    print(f"⏱️ Tiempo mínimo de respuesta: {min(tiempos_respuesta):.3f} seg")

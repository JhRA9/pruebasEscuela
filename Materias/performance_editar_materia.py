import requests
import time
import statistics

# Configuración
URL_LOGIN = "http://localhost/proyectoEscuela/login/index.php"
ID_MATERIA = 3
URL_EDITAR = f"http://localhost/proyectoEscuela/admin/materias/edit.php?id={ID_MATERIA}"
TOTAL_INTENTOS = 100

# Datos base
editar_payload_base = {
    "id_materia": str(ID_MATERIA),
}

# Autenticación
session = requests.Session()
login_payload = {
    "email": "admin@admin.com",
    "password": "123"
}
login_response = session.post(URL_LOGIN, data=login_payload)

if "Dashboard" not in login_response.text and not login_response.ok:
    print("❌ Error al iniciar sesión")
    exit()
else:
    print("✅ Sesión iniciada correctamente.\n")

# Medición de rendimiento
tiempos_respuesta = []
exitos = 0
errores = 0

tiempo_inicio_total = time.time()

for i in range(TOTAL_INTENTOS):
    editar_payload = editar_payload_base.copy()
    editar_payload["nombre_materia"] = f"MateriaPerformance#{i}"

    try:
        inicio = time.time()
        response = session.post(URL_EDITAR, data=editar_payload)
        duracion = time.time() - inicio
        tiempos_respuesta.append(duracion)

        if "actualizó la materia" in response.text or response.ok:
            exitos += 1
        else:
            errores += 1
    except Exception:
        errores += 1

tiempo_total = time.time() - tiempo_inicio_total

# Resultados
print("📈 Resultados de la prueba de performance (Editar Materia):")
print(f"🔁 Total de intentos: {TOTAL_INTENTOS}")
print(f"✔️ Éxitos: {exitos}")
print(f"❌ Errores: {errores}")
print(f"⏱️ Tiempo total: {tiempo_total:.2f} seg")
print(f"📉 Tiempo medio por solicitud: {statistics.mean(tiempos_respuesta):.3f} seg")
print(f"⏱️ Tiempo máximo: {max(tiempos_respuesta):.3f} seg")
print(f"⏱️ Tiempo mínimo: {min(tiempos_respuesta):.3f} seg")
print(f"⚙️ Throughput (TPS): {TOTAL_INTENTOS / tiempo_total:.2f} transacciones/seg")

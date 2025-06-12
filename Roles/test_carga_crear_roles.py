import concurrent.futures
import time
from rol_service import crear_rol, eliminar_rol

NUM_ROLES = 1000  # Puedes ajustar este valor según tu prueba
MAX_WORKERS = 20  # Hilos concurrentes (ajustable según tu CPU y DB)

def crear_rol_con_nombre(i):
    nombre_rol = f"CARGA_PRUEBA_{i}"
    eliminar_rol(nombre_rol)  # Limpieza previa
    resultado = crear_rol(nombre_rol)
    return (nombre_rol, resultado)

def main():
    start = time.time()
    exitosos = []
    fallidos = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futuros = [executor.submit(crear_rol_con_nombre, i) for i in range(NUM_ROLES)]

        for futuro in concurrent.futures.as_completed(futuros):
            nombre_rol, resultado = futuro.result()
            if resultado:
                exitosos.append(nombre_rol)
            else:
                fallidos.append(nombre_rol)

    duracion = time.time() - start

    print(f"\n✅ Prueba de Carga Finalizada en {duracion:.2f} segundos.")
    print(f"✔️ Éxitos: {len(exitosos)}")
    print(f"❌ Fallos: {len(fallidos)}")

    if exitosos:
        print("✔️ Roles exitosos:")
        for r in exitosos:
            print(f"  - {r}")

    if fallidos:
        print("❗ Roles fallidos:")
        for r in fallidos:
            print(f"  - {r}")

    # Limpieza final (opcional)
    for r in exitosos + fallidos:
        eliminar_rol(r)

if __name__ == "__main__":
    main()

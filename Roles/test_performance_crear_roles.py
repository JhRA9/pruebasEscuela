import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import string
import time
# import csv  # Descomenta si quieres guardar los resultados
from rol_service import crear_rol, eliminar_rol

def generar_nombre_rol():
    return "ROL_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class TestEstresCrearRol(unittest.TestCase):

    def setUp(self):
        self.nombres_roles = []
        self.resultados = []

    def test_creacion_masiva_roles(self):
        cantidad_roles = 50
        self.nombres_roles = [generar_nombre_rol() for _ in range(cantidad_roles)]

        print(f"\n⏳ Iniciando creación masiva de {cantidad_roles} roles...\n")
        inicio_total = time.perf_counter()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futuros = {executor.submit(crear_rol, nombre): nombre for nombre in self.nombres_roles}

            for futuro in as_completed(futuros):
                nombre = futuros[futuro]
                inicio_rol = time.perf_counter()
                try:
                    resultado = futuro.result()
                    fin_rol = time.perf_counter()
                    tiempo_rol = fin_rol - inicio_rol
                    print(f"Rol {nombre}: {'✅ Creado' if resultado else '❌ Fallo'} - {tiempo_rol:.4f}s")
                    self.resultados.append((nombre, resultado, tiempo_rol))
                except Exception as e:
                    fin_rol = time.perf_counter()
                    print(f"Rol {nombre}: ❌ Excepción - {e}")
                    self.resultados.append((nombre, False, fin_rol - inicio_rol))

        fin_total = time.perf_counter()
        duracion_total = fin_total - inicio_total

        print(f"\n📊 Resultados de la prueba de rendimiento:")
        exitosos = [r for r in self.resultados if r[1]]
        fallidos = [r for r in self.resultados if not r[1]]
        tiempos_exitosos = [r[2] for r in exitosos]

        print(f"✔️ Éxitos: {len(exitosos)} / {cantidad_roles}")
        print(f"❌ Fallos: {len(fallidos)}")
        print(f"⏱️ Tiempo total: {duracion_total:.2f} segundos")
        if tiempos_exitosos:
            print(f"📈 Tiempo promedio por rol exitoso: {sum(tiempos_exitosos)/len(tiempos_exitosos):.4f} segundos")

        # CSV opcional
        """
        with open('resultado_creacion_roles.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Rol', 'Éxito', 'Tiempo (s)'])
            for nombre, exito, tiempo in self.resultados:
                writer.writerow([nombre, 'Sí' if exito else 'No', f"{tiempo:.4f}"])
        """

        self.assertTrue(len(fallidos) == 0, f"Fallaron {len(fallidos)} creaciones de rol.")

    def tearDown(self):
        print("\n🧹 Eliminando roles creados...")
        for rol in self.nombres_roles:
            eliminar_rol(rol)

if __name__ == "__main__":
    unittest.main()

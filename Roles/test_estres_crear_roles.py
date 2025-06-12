import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from rol_service import crear_rol, eliminar_rol
import random
import string

def generar_nombre_rol():
    return "ROL_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class TestEstresCrearRol(unittest.TestCase):

    def test_creacion_masiva_roles(self):
        cantidad_roles = 50  # Puedes subir a 100, 500, 1000 si quieres estresar más

        nombres_roles = [generar_nombre_rol() for _ in range(cantidad_roles)]
        resultados = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            futuros = {executor.submit(crear_rol, nombre): nombre for nombre in nombres_roles}

            for futuro in as_completed(futuros):
                nombre = futuros[futuro]
                try:
                    resultado = futuro.result()
                    print(f"Rol {nombre}: {'✅ Creado' if resultado else '❌ Fallo'}")
                    resultados.append((nombre, resultado))
                except Exception as e:
                    print(f"Rol {nombre}: ❌ Excepción - {e}")
                    resultados.append((nombre, False))

        fallos = [r for r in resultados if not r[1]]
        self.assertTrue(len(fallos) == 0, f"Fallaron {len(fallos)} creaciones de rol.")

    def tearDown(self):
        # Limpieza: elimina todos los roles que se usaron en la prueba
        for rol in getattr(self, "nombres_roles", []):
            eliminar_rol(rol)

if __name__ == "__main__":
    unittest.main()

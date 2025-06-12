import unittest
from rol_service import crear_rol, obtener_rol_por_nombre, eliminar_rol

class TestCrearRolUnitario(unittest.TestCase):
    def setUp(self):
        self.nombre_rol = "COORDINADOR_PRUEBA"
        eliminar_rol(self.nombre_rol)  # Asegura un entorno limpio antes de la prueba

    def test_crear_rol_exitosamente(self):
        # Crear el rol
        resultado = crear_rol(self.nombre_rol)
        print("Resultado crear_rol:", resultado)  # 👈 Línea extra
        self.assertTrue(resultado, "❌ No se pudo crear el rol")

        # Verificar que el rol fue creado
        rol = obtener_rol_por_nombre(self.nombre_rol)
        self.assertIsNotNone(rol, "❌ El rol no fue encontrado en la base de datos")
        self.assertEqual(rol["nombre_rol"], self.nombre_rol, "❌ El nombre del rol no coincide")

    def tearDown(self):
        eliminar_rol(self.nombre_rol)  # Limpieza después de la prueba

if __name__ == "__main__":
    unittest.main()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class TareaManagementTests:
    def __init__(self):
        self.base_url = "http://localhost/proyectoEscuela"
        self.driver = None
        self.test_tarea_titulo_completada = None
        self.test_tarea_titulo_pendiente = None
        self.materia_id_valido = None # Para almacenar el ID de materia

    def _start_driver(self):
        if self.driver is None or not self.driver.session_id:
            self.driver = webdriver.Chrome()

    def _quit_driver(self):
        if self.driver:
            self.driver.quit()
        self.driver = None

    def login_as_admin(self):
        self._start_driver()
        # CORRECCIÓN: Usar /index.php para el login
        self.driver.get(f"{self.base_url}/index.php")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        self.driver.find_element(By.NAME, "email").send_keys("admin@admin.com")
        self.driver.find_element(By.NAME, "password").send_keys("123", Keys.ENTER)
        WebDriverWait(self.driver, 10).until(EC.url_contains("admin"))
        print("Login exitoso como administrador.")

    def _create_test_materia(self, titulo, descripcion, fecha, hora, materia_id):
        """Función auxiliar para crear una tarea y devolver su título."""
        self.driver.get(f"{self.base_url}/admin/tareas/create.php")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "titulo")))

        self.driver.find_element(By.NAME, "titulo").send_keys(titulo)
        self.driver.find_element(By.NAME, "descripcion").send_keys(descripcion)
        self.driver.execute_script("document.getElementsByName('fecha_entrega')[0].value = arguments[0]", fecha)
        self.driver.execute_script("document.getElementsByName('hora_entrega')[0].value = arguments[0]", hora)
        
        select_materia = Select(self.driver.find_element(By.NAME, 'id_materia'))
        select_materia.select_by_value(str(materia_id))
        
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("admin/tareas/index.php"))
        time.sleep(1)
        print(f"Tarea '{titulo}' creada exitosamente.")
        return titulo

    def test_filtrar_tarea_por_estado(self):
        """
        Prueba unitaria para la funcionalidad de filtrar tareas por estado.
        CA: La tabla de tareas debe mostrar las tareas ordenadas por su estado.
        """
        print("\n--- Ejecutando prueba unitaria: Filtrar tarea por estado ---")
        try:
            self.login_as_admin()

            # Obtener el ID de una materia existente para asociar las tareas
            self.driver.get(f"{self.base_url}/admin/materias/index.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "example1")))
            time.sleep(2)

            first_edit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//table[@id='example1']/tbody/tr[1]//a[contains(@href, 'edit.php')]"))
            )
            self.materia_id_valido = first_edit_button.get_attribute("href").split("id=")[1]
            print(f"Usando ID de materia: {self.materia_id_valido} para las tareas de prueba.")

            timestamp = int(time.time())
            
            # Tarea 1: PENDIENTE (estado por defecto al crear)
            self.test_tarea_titulo_pendiente = self._create_test_materia(
                f"Tarea Pendiente {timestamp}",
                "Descripción de tarea pendiente",
                "2025-07-15",
                "10:00",
                self.materia_id_valido
            )
            
            # Tarea 2: COMPLETADA (la creamos y luego la editamos)
            self.test_tarea_titulo_completada = self._create_test_materia(
                f"Tarea Completada {timestamp}",
                "Descripción de tarea completada",
                "2025-07-10",
                "09:00",
                self.materia_id_valido
            )

            # --- Editar la Tarea Completada para que tenga el estado "completada" ---
            print(f"Editando tarea '{self.test_tarea_titulo_completada}' para cambiar su estado a 'completada'...")
            self.driver.get(f"{self.base_url}/admin/tareas/index.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "example1")))
            time.sleep(2)

            edit_tarea_xpath = f"//table[@id='example1']//tr[td[contains(., '{self.test_tarea_titulo_completada}')]]//a[contains(@href, 'edit.php')]"
            edit_tarea_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, edit_tarea_xpath)))
            edit_tarea_button.click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "estado")))
            
            select_estado = Select(self.driver.find_element(By.NAME, 'estado'))
            select_estado.select_by_value('completada')

            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            WebDriverWait(self.driver, 10).until(EC.url_contains("admin/tareas/index.php"))
            time.sleep(2)
            print(f"Tarea '{self.test_tarea_titulo_completada}' actualizada a 'completada'.")


            # 2. Navegar al listado de tareas
            self.driver.get(f"{self.base_url}/admin/tareas/index.php")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "example1")))
            time.sleep(3) # Esperar un poco más para que DataTables cargue y renderice

            # 3. Hacer clic en el botón "Ordenar por estado"
            print("Haciendo clic en 'Ordenar por estado'...")
            btn_estado = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn-estado"))
            )
            btn_estado.click()
            time.sleep(3) # Dar tiempo para que la tabla se reordene vía AJAX

            # 4. Verificar el orden de las tareas por estado
            print("Verificando el orden de las tareas...")
            estados_en_tabla = []
            # Volvemos a buscar las filas después del reordenamiento.
            filas_tareas = self.driver.find_elements(By.XPATH, "//table[@id='example1']/tbody/tr")
            for fila in filas_tareas:
                try:
                    # La columna de estado es la sexta columna (índice 5) en el <tbody>
                    estado_celda = fila.find_element(By.XPATH, ".//td[6]")
                    estados_en_tabla.append(estado_celda.text.strip())
                except Exception as e:
                    print(f"No se pudo extraer el estado de una fila: {e}")
            
            # Verificación del orden:
            # Según tu `list.php`, la estrategia `TareasByEstado` usa `ORDER BY estado`.
            # En MySQL/SQL, ORDER BY por defecto es ascendente (ASC).
            # Por lo tanto, 'completada' (c) debería aparecer antes que 'pendiente' (p) alfabéticamente.
            # Sin embargo, si tienes un `enum` o un ordenamiento personalizado en SQL, esto podría variar.
            # Asumiremos el orden alfabético simple: "completada", luego "pendiente".

            orden_alfabetico_esperado = True
            found_pendiente_after_completada = False
            for estado in estados_en_tabla:
                if estado.lower() == "pendiente" and not found_pendiente_after_completada:
                    found_pendiente_after_completada = True
                elif estado.lower() == "completada" and found_pendiente_after_completada:
                    # Si encontramos una "completada" después de una "pendiente", el orden no es alfabético ascendente
                    orden_alfabetico_esperado = False
                    break
            
            if orden_alfabetico_esperado:
                print("✅ Prueba 'Filtrar tarea por estado' exitosa: Las tareas están ordenadas correctamente por estado (alfabético ascendente). :D")
                print("Orden de estados observado:", estados_en_tabla)
            else:
                print("❌ Prueba 'Filtrar tarea por estado' fallida: El orden de las tareas por estado no es el esperado. :'( ")
                print("Orden de estados observado:", estados_en_tabla)

        except Exception as e:
            print(f"❌ Error durante la prueba 'Filtrar tarea por estado': {str(e)}")
        finally:
            self._quit_driver()

# Ejecutar la prueba unitaria
if __name__ == "__main__":
    tester = TareaManagementTests()
    tester.test_filtrar_tarea_por_estado()
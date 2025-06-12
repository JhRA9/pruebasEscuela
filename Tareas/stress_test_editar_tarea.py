import sqlite3
import time

def editar_tarea(conn, tarea_id, nuevo_titulo):
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas SET titulo = ? WHERE id = ?", (nuevo_titulo, tarea_id))
    conn.commit()
    return True

# Configuración inicial
conn = sqlite3.connect(":memory:")
conn.execute('''
    CREATE TABLE tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT
    )
''')

# Crear tareas de prueba
for i in range(1000):
    conn.execute("INSERT INTO tareas (titulo) VALUES (?)", (f"Tarea {i+1}",))

# Prueba de estrés
errores = 0
inicio = time.time()

for i in range(1000):
    try:
        nuevo_titulo = f"Tarea actualizada {i+1}"
        editar_tarea(conn, i + 1, nuevo_titulo)
    except Exception as e:
        errores += 1
        print(f"❌ Error al editar tarea {i+1}: {str(e)}")

fin = time.time()
print(f"\nTotal intentos de edición: 1000")
print(f"Tareas editadas correctamente: {1000 - errores}")
print(f"Errores encontrados: {errores}")
print(f"Tiempo total de ejecución: {fin - inicio:.2f} segundos")

conn.close()

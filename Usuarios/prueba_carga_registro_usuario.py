import sqlite3
import bcrypt
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def crear_usuario(conn, nombres, rol_id, email, password, password_repeat):
    if password != password_repeat:
        raise ValueError("Las contraseñas no coinciden")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        raise ValueError("El email del usuario ya existe en la base de datos")

    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hora_creacion = '2025-06-07 00:00:00'
    estado = 1

    cursor.execute(
        "INSERT INTO usuarios (nombres, rol_id, email, password, hora_creacion, estado) VALUES (?, ?, ?, ?, ?, ?)",
        (nombres, rol_id, email, password_hashed, hora_creacion, estado)
    )
    conn.commit()
    return True

def setup_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT,
            rol_id INTEGER,
            email TEXT UNIQUE,
            password BLOB,
            hora_creacion TEXT,
            estado INTEGER
        )
    ''')
    return conn

def prueba_carga(total_usuarios=100):
    conn = setup_db()

    def tarea(i):
        email = f"usuario{i}@mail.com"
        try:
            crear_usuario(conn, f"Usuario{i}", 1, email, "password123", "password123")
            return True
        except Exception as e:
            print(f"Error en usuario {i}: {e}")
            return False

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=20) as executor:
        futuros = [executor.submit(tarea, i) for i in range(total_usuarios)]
        resultados = [f.result() for f in as_completed(futuros)]
    end_time = time.time()

    print(f"Total intentos: {total_usuarios}")
    print(f"Usuarios creados correctamente: {sum(resultados)}")
    print(f"Errores encontrados: {total_usuarios - sum(resultados)}")
    print(f"Tiempo total de carga: {end_time - start_time:.2f} segundos")

if __name__ == "__main__":
    prueba_carga(100)

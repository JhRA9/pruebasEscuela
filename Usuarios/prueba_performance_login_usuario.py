import sqlite3
import bcrypt
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Función para validar login
def login(conn, email, password):
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE email = ?", (email,))
    fila = cursor.fetchone()
    if fila and bcrypt.checkpw(password.encode('utf-8'), fila[0]):
        return True
    return False

# Setup de base de datos con usuario de prueba
def setup_db_login_test():
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
    password_hashed = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
    conn.execute(
        "INSERT INTO usuarios (nombres, rol_id, email, password, hora_creacion, estado) VALUES (?, ?, ?, ?, ?, ?)",
        ("Prueba", 1, "usuario@mail.com", password_hashed, "2025-06-07 00:00:00", 1)
    )
    conn.commit()
    return conn

# Prueba de performance
def prueba_performance_login(conexiones=500):
    conn = setup_db_login_test()

    def tarea(i):
        return login(conn, "usuario@mail.com", "password123")

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=20) as executor:
        futuros = [executor.submit(tarea, i) for i in range(conexiones)]
        resultados = [f.result() for f in as_completed(futuros)]
    end_time = time.time()

    print(f"Intentos de inicio de sesión: {conexiones}")
    print(f"Inicios de sesión exitosos: {sum(resultados)}")
    print(f"Inicios fallidos: {conexiones - sum(resultados)}")
    print(f"Tiempo total: {end_time - start_time:.2f} segundos")
    print(f"Tiempo promedio por login: {(end_time - start_time)/conexiones:.4f} segundos")

if __name__ == "__main__":
    prueba_performance_login(500)

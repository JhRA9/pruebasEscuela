import sqlite3
import bcrypt
from datetime import datetime

# Reutilizamos la función de creación de usuario
def crear_usuario(conn, nombres, rol_id, email, password, password_repeat):
    if password != password_repeat:
        raise ValueError("Las contraseñas no coinciden")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        raise ValueError("El email del usuario ya existe en la base de datos")

    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hora_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    estado = 1

    cursor.execute(
        "INSERT INTO usuarios (nombres, rol_id, email, password, hora_creacion, estado) VALUES (?, ?, ?, ?, ?, ?)",
        (nombres, rol_id, email, password_hashed, hora_creacion, estado)
    )
    conn.commit()
    return True

# Función para realizar la prueba de estrés
def prueba_estres_crear_usuarios(total_usuarios):
    conn = sqlite3.connect(":memory:")
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

    errores = 0

    for i in range(total_usuarios):
        try:
            nombre = f"Usuario{i}"
            email = f"usuario{i}@mail.com"
            crear_usuario(conn, nombre, 1, email, "password123", "password123")
        except Exception as e:
            errores += 1
            print(f"[ERROR] No se pudo crear el usuario {email}: {e}")

    print(f"\nTotal intentos: {total_usuarios}")
    print(f"Usuarios creados correctamente: {total_usuarios - errores}")
    print(f"Errores encontrados: {errores}")

    conn.close()

# Ejecutar prueba de estrés con 1000 usuarios
if __name__ == "__main__":
    prueba_estres_crear_usuarios(1000)

import sqlite3
import pytest
import bcrypt

def crear_usuario(conn, nombres, rol_id, email, password, password_repeat):
    if password != password_repeat:
        raise ValueError("Las contraseñas no coinciden")
    
    cursor = conn.cursor()

    # Verificar si email existe
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        raise ValueError("El email del usuario ya existe en la base de datos")
    
    # Hashear contraseña
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    hora_creacion = '2025-06-07 00:00:00'  # Puede ser datetime.now() en producción
    estado = 1

    cursor.execute(
        "INSERT INTO usuarios (nombres, rol_id, email, password, hora_creacion, estado) VALUES (?, ?, ?, ?, ?, ?)",
        (nombres, rol_id, email, password_hashed, hora_creacion, estado)
    )
    conn.commit()
    return True

# --- Pruebas unitarias ---

@pytest.fixture
def db():
    # Base de datos en memoria para pruebas
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
    yield conn
    conn.close()

def test_contrasenas_no_coinciden(db):
    print("\n[TEST] Verificando que las contraseñas deben coincidir para crear usuario.")
    with pytest.raises(ValueError, match="Las contraseñas no coinciden"):
        crear_usuario(db, "Juan", 1, "juan@mail.com", "123", "321")

def test_email_duplicado(db):
    print("\n[TEST] Verificando que no se permita registrar un correo duplicado.")
    crear_usuario(db, "Juan", 1, "juan@mail.com", "123", "123")
    with pytest.raises(ValueError, match="El email del usuario ya existe en la base de datos"):
        crear_usuario(db, "Pedro", 1, "juan@mail.com", "abc", "abc")

def test_crear_usuario_exitoso(db):
    print("\n[TEST] Verificando que se pueda registrar un usuario correctamente con datos válidos.")
    resultado = crear_usuario(db, "Ana", 2, "ana@mail.com", "pass123", "pass123")
    assert resultado is True
    cursor = db.execute("SELECT * FROM usuarios WHERE email = 'ana@mail.com'")
    usuario = cursor.fetchone()
    assert usuario is not None
    assert usuario[1] == "Ana"  # columna nombres

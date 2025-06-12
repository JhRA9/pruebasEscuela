import sqlite3
import pytest

def editar_tarea(conn, tarea_id, nuevo_titulo):
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,))
    if cursor.fetchone() is None:
        raise ValueError("La tarea no existe")

    cursor.execute("UPDATE tareas SET titulo = ? WHERE id = ?", (nuevo_titulo, tarea_id))
    conn.commit()
    return True


# --- Pruebas unitarias ---

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute('''
        CREATE TABLE tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT
        )
    ''')
    # Insertar tarea de prueba
    conn.execute("INSERT INTO tareas (titulo) VALUES (?)", ("Tarea original",))
    yield conn
    conn.close()


def test_editar_tarea_existente(db):
    resultado = editar_tarea(db, 1, "Nueva tarea actualizada")
    assert resultado is True
    cursor = db.execute("SELECT titulo FROM tareas WHERE id = 1")
    nueva_tarea = cursor.fetchone()
    assert nueva_tarea[0] == "Nueva tarea actualizada"

def test_editar_tarea_inexistente(db):
    with pytest.raises(ValueError, match="La tarea no existe"):
        editar_tarea(db, 99, "Cambio inválido")

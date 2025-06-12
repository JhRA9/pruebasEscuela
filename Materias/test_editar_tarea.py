# test_editar_tarea.py

import sqlite3
import pytest
from datetime import datetime

# Lógica a probar (simula lo que hace edit.php en backend)
def editar_tarea(conn, tarea_id, titulo, descripcion, fecha_entrega, hora_entrega, id_materia, estado):
    cursor = conn.cursor()

    # Verificar que la tarea exista
    cursor.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,))
    if cursor.fetchone() is None:
        raise ValueError("La tarea no existe")

    # Actualizar tarea
    cursor.execute("""
        UPDATE tareas 
        SET titulo = ?, descripcion = ?, fecha_entrega = ?, hora_entrega = ?, id_materia = ?, estado = ?
        WHERE id = ?
    """, (titulo, descripcion, fecha_entrega, hora_entrega, id_materia, estado, tarea_id))
    
    conn.commit()
    return True

# 🔧 Setup para pruebas
@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute('''
        CREATE TABLE tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descripcion TEXT,
            fecha_entrega TEXT,
            hora_entrega TEXT,
            id_materia INTEGER,
            estado TEXT
        )
    ''')
    conn.execute('''
        INSERT INTO tareas (titulo, descripcion, fecha_entrega, hora_entrega, id_materia, estado)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Tarea vieja", "Descripción vieja", "2025-01-01", "12:00:00", 1, "Pendiente"))
    yield conn
    conn.close()

# ✅ Test editar una tarea existente
def test_editar_tarea_existente(db):
    nueva_data = {
        "titulo": "Prueba de anatomía",
        "descripcion": "Chúzate un pulmón a ver si duele",
        "fecha_entrega": "2025-05-10",
        "hora_entrega": "23:59:00",
        "id_materia": 4,
        "estado": "Pendiente"
    }

    resultado = editar_tarea(
        db, 1,
        nueva_data["titulo"],
        nueva_data["descripcion"],
        nueva_data["fecha_entrega"],
        nueva_data["hora_entrega"],
        nueva_data["id_materia"],
        nueva_data["estado"]
    )
    assert resultado is True

    # Validar que se haya actualizado correctamente
    cursor = db.cursor()
    cursor.execute("SELECT titulo, descripcion, fecha_entrega, hora_entrega, id_materia, estado FROM tareas WHERE id = 1")
    datos = cursor.fetchone()
    assert datos == (
        nueva_data["titulo"],
        nueva_data["descripcion"],
        nueva_data["fecha_entrega"],
        nueva_data["hora_entrega"],
        nueva_data["id_materia"],
        nueva_data["estado"]
    )

# ❌ Test para tarea inexistente
def test_editar_tarea_inexistente(db):
    with pytest.raises(ValueError, match="La tarea no existe"):
        editar_tarea(
            db, 999,
            "Inexistente",
            "No debería funcionar",
            "2025-06-01",
            "10:00:00",
            2,
            "Completado"
        )

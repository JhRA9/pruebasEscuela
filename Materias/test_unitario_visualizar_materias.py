# test_unitario_visualizar_materias.py

import pytest

# Simulamos función que retorna lista de materias
def obtener_materias():
    # Simulación de datos que vendrían de la base de datos
    return [
        {"id": 1, "nombre": "Matemáticas"},
        {"id": 2, "nombre": "Lengua"},
        {"id": 3, "nombre": "Historia"},
    ]

def test_visualizar_materias():
    materias = obtener_materias()
    
    # Asegurar que se retorna una lista
    assert isinstance(materias, list)
    
    # Asegurar que hay al menos una materia
    assert len(materias) > 0
    
    # Asegurar que cada materia tiene un id y un nombre
    for materia in materias:
        assert "id" in materia
        assert "nombre" in materia
        assert isinstance(materia["id"], int)
        assert isinstance(materia["nombre"], str)

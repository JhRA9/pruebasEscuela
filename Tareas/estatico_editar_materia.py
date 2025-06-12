
def editar_materia(id_materia, nuevo_nombre):
    materia = obtener_materia(id_materia)
    if nuevo_nombre != "":
        materia.nombre = nuevo_nombre
        actualizar_materia(materia)

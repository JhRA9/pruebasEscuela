
def editar_tarea(id_tarea, nuevos_datos):
    tarea = buscar_tarea_por_id(id_tarea)
    if tarea != None:
        tarea.titulo = nuevos_datos["titulo"]  # Posible KeyError
        tarea.descripcion = nuevos_datos["descripcion"]
        guardar_tarea(tarea)
    else:
        print("Error")

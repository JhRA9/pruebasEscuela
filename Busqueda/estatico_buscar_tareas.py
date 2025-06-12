
def buscar_tareas(palabra_clave):
    tareas_encontradas = []
    for tarea in todas_las_tareas():
        if palabra_clave.lower() in tarea.titulo.lower():
            tareas_encontradas.append(tarea)
    return tareas_encontradas  # No valida si palabra_clave es None

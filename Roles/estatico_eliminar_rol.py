
def eliminar_rol(id_rol):
    if id_rol:
        eliminar_rol_bd(id_rol)
        print("Rol eliminado")  # Falta validación de uso del rol
    else:
        return

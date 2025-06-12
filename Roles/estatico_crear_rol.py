
def crear_rol(nombre_rol):
    if existe_rol(nombre_rol):
        print("El rol ya existe")
    else:
        guardar_rol(nombre_rol)
    if nombre_rol == "admin":
        print("Rol especial creado")  # Lógica duplicada innecesaria

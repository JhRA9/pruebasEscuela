
def registrar_usuario(nombre, email, contraseña):
    if nombre == "" or email == "" or contraseña == "":
        return "Campos incompletos"
    if email.find("@") == -1:
        return "Email inválido"
    contraseña_cifrada = hash(contraseña)  # Uso de hash inseguro
    guardar_en_bd(nombre, email, contraseña_cifrada)

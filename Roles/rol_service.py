import pymysql
from datetime import datetime


def crear_rol(nombre_rol):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='sistemaescolar',
            port=3306
        )
        with connection.cursor() as cursor:
            query = "INSERT INTO roles (nombre_rol, hora_creacion, estado) VALUES (%s, %s, %s)"
            hora_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            estado = 'activo'
            cursor.execute(query, (nombre_rol, hora_creacion, estado))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        print(f"Error al crear rol: {e}")
        return False

def obtener_rol_por_nombre(nombre_rol):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='sistemaescolar',
            port=3306
        )
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = "SELECT * FROM roles WHERE nombre_rol = %s"
            cursor.execute(query, (nombre_rol,))
            rol = cursor.fetchone()
        connection.close()
        return rol
    except pymysql.MySQLError as e:
        print(f"Error al obtener rol: {e}")
        return None

def eliminar_rol(nombre_rol):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='sistemaescolar',
            port=3306
        )
        with connection.cursor() as cursor:
            query = "DELETE FROM roles WHERE nombre_rol = %s"
            cursor.execute(query, (nombre_rol,))
        connection.commit()
        connection.close()
        return True
    except pymysql.MySQLError as e:
        print(f"Error al eliminar rol: {e}")
        return False

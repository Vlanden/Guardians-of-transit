# Aquí puedes definir tus funciones de interacción con la base de datos

def obtener_usuarios(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios')
    return cursor.fetchall()

import sqlite3

# Función para conectarse a la base de datos
def conectar_bd():
    return sqlite3.connect('usuarios.db')

# Crear la tabla de usuarios si no existe
def inicializar_bd():
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()

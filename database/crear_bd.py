import sqlite3

def crear_base_de_datos():
    conn = sqlite3.connect('usuarios.db')  # Conectar o crear la BD
    cursor = conn.cursor()

    # Crear la tabla de usuarios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("📂 Base de datos creada correctamente.")

if __name__ == "__main__":
    crear_base_de_datos()

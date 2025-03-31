from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

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

inicializar_bd()  # Inicializar base de datos al ejecutar el programa

# Página de inicio (requiere autenticación)
@app.route('/')
def index():
    if 'username' in session:
        return f'Bienvenido {session["username"]} a la aplicación de aprendizaje vial.'
    return redirect(url_for('login'))

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        with conectar_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO usuarios (username, password, email) VALUES (?, ?, ?)', 
                               (username, password, email))
                conn.commit()
                flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('El usuario o email ya están registrados.', 'danger')

    return render_template('register.html')

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()

            if user:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')

# Ruta de recuperación de contraseña
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM usuarios WHERE email = ?', (email,))
            user = cursor.fetchone()

            if user:
                flash(f'Tu contraseña es: {user[0]}', 'info')  # En una app real, se enviaría un correo en lugar de mostrarlo
            else:
                flash('No se encontró ninguna cuenta con ese email.', 'danger')

    return render_template('forgot_password.html')

# Ruta de logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

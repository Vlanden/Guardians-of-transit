from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave segura

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nombre de la vista para el login

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

inicializar_bd()  # Inicializar la base de datos al ejecutar el programa

# Función para cifrar la contraseña
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Guardar como string en SQLite

# Función para verificar la contraseña
def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))  # Convertir a bytes


# 🚀 API para registrar usuario
@app.route('/api/register', methods=['POST'])
def register_api():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    hashed_password = hash_password(password)

    with conectar_bd() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO usuarios (username, password, email) VALUES (?, ?, ?)', 
                           (username, hashed_password, email))
            conn.commit()
            return jsonify({"message": "Usuario registrado exitosamente"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "El usuario o email ya están registrados"}), 400


# Página de inicio (requiere autenticación)
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = hash_password(password)

        with conectar_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO usuarios (username, password, email) VALUES (?, ?, ?)', 
                               (username, hashed_password, email))
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
            cursor.execute('SELECT id, username, password FROM usuarios WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user and check_password(user[2], password):  # user[2] es la contraseña
                session['user_id'] = user[0]
                session['username'] = user[1]
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
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
            user = cursor.fetchone()

            if user:
                flash('Se han enviado instrucciones a tu correo.', 'info')  # Simulación
            else:
                flash('No se encontró ninguna cuenta con ese email.', 'danger')

    return render_template('forgot_password.html')


# Ruta de perfil del usuario
@app.route('/profile')
def profile():
    if 'username' in session:
        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, email FROM usuarios WHERE username = ?', (session['username'],))
            user = cursor.fetchone()

        return render_template('profile.html', user=user)
    
    return redirect(url_for('login'))


# Ruta de logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

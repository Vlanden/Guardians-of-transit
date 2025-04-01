from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import conectar_bd
import bcrypt

# API de registro
def register_api():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with conectar_bd() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO usuarios (username, password, email) VALUES (?, ?, ?)', 
                           (username, hashed_password, email))
            conn.commit()
            return jsonify({"message": "Usuario registrado exitosamente"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"message": "El usuario o email ya están registrados"}), 400

# API de login
def login_api():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return jsonify({"message": "Login exitoso"}), 200
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

# API de recuperación de contraseña
def forgot_password_api():
    data = request.get_json()
    email = data.get('email')

    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user:
            return jsonify({"message": f'Tu contraseña es: {user[0]}'}), 200
        return jsonify({"message": "No se encontró ninguna cuenta con ese email"}), 404

# API de perfil
def profile_api():
    if 'username' in session:
        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE username = ?', (session['username'],))
            user = cursor.fetchone()
        return jsonify({"username": user[1], "email": user[3]}), 200
    return jsonify({"message": "No autenticado"}), 401

# API de logout
def logout_api():
    session.pop('user_id', None)
    session.pop('username', None)
    return jsonify({"message": "Logout exitoso"}), 200

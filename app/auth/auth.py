from flask import Blueprint, render_template, request, redirect, url_for, request, jsonify
from models.user import User
from flask_login import login_user, login_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import bcrypt
import sqlite3

auth_bp = Blueprint('auth', __name__, template_folder='templates')


# Ruta de inicio de sesión
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aquí agregarás la lógica para la autenticación
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

# Ruta de registro
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        new_user.save()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

# Ruta de perfil de usuario
@auth_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


            

# Conexión a la base de datos (mover a un archivo aparte si es grande)
def get_db():
    return sqlite3.connect('usuarios.db')

# ... (incluye aquí todas las funciones auxiliares: hash_password, check_password, etc.)


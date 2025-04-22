from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db, limiter
import re
import bcrypt
from datetime import datetime
import secrets
import smtplib
from email.mime.text import MIMEText

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email))

def is_valid_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_strong_password(password):
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)

def send_reset_email(user):
    # Configuración básica del correo (debes completar con tus credenciales)
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.token_expiration = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()
    
    msg = MIMEText(f"""
    Para restablecer tu contraseña, visita el siguiente enlace:
    {url_for('auth.reset_password', token=token, _external=True)}
    
    Este enlace expirará en 1 hora.
    """)
    
    msg['Subject'] = 'Restablecimiento de contraseña'
    msg['From'] = 'no-reply@guardianesdelavia.com'
    msg['To'] = user.email
    
    # Configuración SMTP (ejemplo para Gmail)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('tu_email@gmail.com', 'tu_contraseña')
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error enviando email: {e}")
        return False

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor complete todos los campos', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        
        flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('auth/log-in.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        errors = []
        if not all([username, email, password, confirm_password]):
            errors.append("Todos los campos son requeridos")
        if not is_valid_username(username):
            errors.append("Nombre de usuario inválido (3-20 caracteres alfanuméricos)")
        if not is_valid_email(email):
            errors.append("Correo electrónico inválido")
        if password != confirm_password:
            errors.append("Las contraseñas no coinciden")
        if not is_strong_password(password):
            errors.append("La contraseña debe tener al menos 8 caracteres, una mayúscula y un número")

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Nombre de usuario ya registrado', 'error')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('Correo electrónico ya registrado', 'error')
            return redirect(url_for('auth.register'))

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Por favor inicie sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/sign-up.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            if send_reset_email(user):
                flash('Se ha enviado un correo con instrucciones para restablecer tu contraseña', 'info')
            else:
                flash('Error al enviar el correo de recuperación', 'error')
        else:
            flash('Si el email existe, se enviaron instrucciones', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset-password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or user.token_expiration < datetime.utcnow():
        flash('El enlace de recuperación es inválido o ha expirado', 'error')
        return redirect(url_for('auth.reset_password_request'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
        elif not is_strong_password(password):
            flash('La contraseña debe tener al menos 8 caracteres, una mayúscula y un número', 'error')
        else:
            user.set_password(password)
            user.reset_token = None
            user.token_expiration = None
            db.session.commit()
            flash('Tu contraseña ha sido actualizada. Por favor inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/new-password.html', token=token)

@auth_bp.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recover():  # Cambiado de reset_password_request a recover
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            if send_reset_email(user):
                flash('Se ha enviado un correo con instrucciones', 'info')
            else:
                flash('Error al enviar el correo', 'error')
        else:
            flash('Si el email existe, se enviaron instrucciones', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset-password.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.inicio'))

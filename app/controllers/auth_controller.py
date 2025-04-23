from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask_login import login_user, current_user, logout_user
from app import limiter, db
from app.models.user import User
from app.services.auth_service import (
    is_valid_email, is_valid_username, is_strong_password, send_reset_email
)
import bcrypt
from sqlalchemy.exc import SQLAlchemyError

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'], endpoint='login')
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Por favor complete todos los campos', 'error')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Usuario o contraseña incorrectos', 'error')

    return render_template('auth/log-in.html')


@auth.route('/logout', methods=['GET'], endpoint='logout')
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'], endpoint="register")
@limiter.limit("10 per minute")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        errors = []
        if not all([username, email, password, confirm_password]):
            errors.append("Todos los campos son requeridos")
        if not is_valid_username(username):
            errors.append("Nombre de usuario inválido")
        if not is_valid_email(email):
            errors.append("Correo electrónico inválido")
        if password != confirm_password:
            errors.append("Las contraseñas no coinciden")
        if not is_strong_password(password):
            errors.append("La contraseña debe ser más segura")

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
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Si")
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/sign-up.html')


@auth.route('/recover', methods=['GET', 'POST'], endpoint='recover')
@limiter.limit("3 per hour")
def recover():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not is_valid_email(email):
            flash('Correo electrónico inválido', 'error')
            return redirect(url_for('auth.recover'))

        user = User.query.filter_by(email=email).first()
        if user:
            # Generar token y enviar email
            token = user.generate_reset_token()
            send_reset_email(user.email, token)
            
        flash('Si el email existe, recibirás instrucciones para resetear tu contraseña', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/new-password.html')

@auth.route('/reset_password', methods=['GET', 'POST'], endpoint='reset_password')
@limiter.limit("5 per hour")
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)
    if not user:
        flash('Token inválido o expirado', 'error')
        return redirect(url_for('auth.recover'))

    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.reset_password', token=token))

        if not is_strong_password(password):
            flash('La contraseña debe ser más segura', 'error')
            return redirect(url_for('auth.reset_password', token=token))

        # Actualizar contraseña
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password_hash = hashed_pw
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()

        flash('Contraseña actualizada exitosamente', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)
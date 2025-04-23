from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask_login import login_user, current_user, logout_user
from app import limiter, db
from app.models.user import User
from app.services.auth_service import (
    is_valid_email, is_valid_username, is_strong_password, send_reset_email
)
import bcrypt
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from contextlib import contextmanager

auth = Blueprint('auth', __name__)


# Contexto para manejo seguro de sesiones
@contextmanager
def session_scope():
    session = db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise


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
            return render_template('auth/log-in.html', username=username)

        try:
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                login_user(user)
                return redirect(request.args.get('next') or url_for('main.index'))

            flash('Usuario o contraseña incorrectos', 'error')

        except OperationalError as e:
            flash('Error de conexión con la base de datos. Intente nuevamente.', 'error')
            current_app.logger.error(f"Error de conexión MySQL: {str(e)}")
            return render_template('auth/log-in.html', username=username)
        
        if current_user.is_authenticated:
            token = current_user.generate_reset_token()
        else:
                token = None
                return render_template('auth/log-in.html', token=token)

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
            return render_template('auth/sign-up.html', username=username, email=email)

        if User.query.filter_by(username=username).first():
            flash('Nombre de usuario ya registrado', 'error')
            return render_template('auth/sign-up.html', username=username, email=email)
        if User.query.filter_by(email=email).first():
            flash('Correo electrónico ya registrado', 'error')
            return render_template('auth/sign-up.html', username=username, email=email)

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_pw)

        try:
            with session_scope() as session:
                session.add(new_user)

        except SQLAlchemyError as e:
            flash('Hubo un error al registrar el usuario. Intente nuevamente.', 'error')
            current_app.logger.error(f"Error de base de datos: {str(e)}")
            return render_template('auth/sign-up.html', username=username, email=email)

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/sign-up.html')

@auth.route('/new-password/<token>', methods=['GET', 'POST'], endpoint='new_password')
@limiter.limit("5 per minute")
def new_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)  # Verificar si el token es válido
    if not user:
        flash('Token inválido o expirado', 'error')
        return redirect(url_for('auth.recover'))  # Redirigir si el token no es válido

    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/new-password.html', token=token)

        if not is_strong_password(password):
            flash('La contraseña debe ser más segura', 'error')
            return render_template('auth/new-password.html', token=token)

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password_hash = hashed_pw

        try:
            with session_scope() as session:
                session.add(user)

            flash('Tu contraseña ha sido restablecida correctamente. Inicia sesión.', 'success')
            return redirect(url_for('auth.login'))

        except SQLAlchemyError as e:
            flash('Error al actualizar la contraseña. Intente nuevamente.', 'error')
            current_app.logger.error(f"Error de base de datos: {str(e)}")
    
    return render_template('auth/new-password.html', token=token)

@auth.route('/reset-password', methods=['GET', 'POST'], endpoint='reset_password')
@limiter.limit("5 per minute")
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not is_valid_email(email):
            flash('Correo electrónico inválido', 'error')
            return render_template('auth/reset-password.html')

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/reset-password.html')

        if not is_strong_password(password):
            flash('La contraseña debe ser más segura', 'error')
            return render_template('auth/reset-password.html')

        user = User.query.filter_by(email=email).first()

        if user:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password_hash = hashed_pw

            try:
                with session_scope() as session:
                    session.add(user)
                    send_reset_email(user)  # Opcionalmente enviar un correo de confirmación

                flash('Tu contraseña ha sido restablecida correctamente.', 'success')
                return redirect(url_for('auth.login'))

            except SQLAlchemyError as e:
                flash('Error al actualizar la contraseña. Intente nuevamente.', 'error')
                current_app.logger.error(f"Error de base de datos: {str(e)}")
        else:
            flash('No hay cuenta asociada a este correo', 'error')
    
    return render_template('auth/reset-password.html')


def send_reset_email(user):
    token = user.generate_reset_token()  # Genera el token para el correo
    send_email(
        user.email,
        'Recuperación de contraseña',
        'auth/reset_password_email',  # Usar template de correo con link a new-password.html
        user=user,
        token=token
    )


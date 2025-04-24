from flask import flash
from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask import current_app
from flask_login import login_user, current_user, logout_user
from app import limiter, db
from app.models.user import User, Perfil
from app.services.auth_service import (
    is_valid_email, is_valid_username, is_strong_password, send_reset_email
)
import bcrypt
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from contextlib import contextmanager
from datetime import datetime, timedelta
from app.utils.database import session_scope

auth = Blueprint('auth', __name__)


# Funcion para iniciar la sesión del usuario
@auth.route('/login', methods=['GET', 'POST'], endpoint='login')
@limiter.limit("10 per minute")  # Límite de intentos por seguridad
def login():
    # Si ya está autenticado, redirige al índice
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Validación de campos vacíos
        if not username or not password:
            flash('Por favor complete todos los campos', 'error')
            return render_template('auth/log-in.html', username=username)

        try:
            # Busca el usuario por nombre
            user = User.query.filter_by(username=username).first()
            # Verifica que exista y que la contraseña coincida
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                login_user(user)  # Inicia sesión
                return redirect(request.args.get('next') or url_for('main.index'))

            flash('Usuario o contraseña incorrectos', 'error')

        # Captura error de conexión con la base de datos
        except OperationalError as e:
            flash('Error de conexión con la base de datos. Intente nuevamente.', 'error')
            current_app.logger.error(f"Error de conexión MySQL: {str(e)}")
            return render_template('auth/log-in.html', username=username)

        # Si ya inició sesión, genera token para recuperación
        if current_user.is_authenticated:
            token = current_user.generate_reset_token()
        else:
            token = None
            return render_template('auth/log-in.html', token=token)

    return render_template('auth/log-in.html')




#Funcion para terminar la sesion
@auth.route('/logout', methods=['GET'], endpoint='logout')
def logout():
    if current_user.is_authenticated:
        try:
            with session_scope() as session:
                perfil = session.query(Perfil).filter_by(username=current_user.username).first()
                if perfil:
                    perfil.ultima_conexion = datetime.now()  # Asegúrate que exista este campo
        except SQLAlchemyError as e:
            flash('No se pudo guardar la hora de cierre de sesión', 'error')
            current_app.logger.error(f"Error al guardar logout: {str(e)}")

    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('main.index'))




#Funcion para registrar al usuario
#Agregar que se registre en la tabla de perfil su username y su fecha de registro
@auth.route('/register', methods=['GET', 'POST'], endpoint="register")
@limiter.limit("10 per minute")
def register():
    from flask import flash

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

        try:
            with session_scope() as session:
                new_user = User(username=username, email=email, password_hash=hashed_pw)
                session.add(new_user)
                session.flush()

                new_perfil = Perfil(username=new_user.username, fecha_registro=datetime.now())
                session.add(new_perfil)

            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for("auth.login"))

        except SQLAlchemyError as e:
            flash('Hubo un error al registrar el usuario y su perfil. Intente nuevamente.', 'error')
            current_app.logger.error(f"Error de base de datos: {str(e)}")
            return render_template('auth/sign-up.html', username=username, email=email)

    # Para GET
    return render_template('auth/sign-up.html')





# Funcion para cuando el usuario olvidó su contraseña
# Se accede a través de un link enviado por correo con un token
@auth.route('/new-password/<token>', methods=['GET', 'POST'], endpoint='new_password')
@limiter.limit("5 per minute")
def new_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Si ya está autenticado, redirigir al inicio

    user = User.verify_reset_token(token)  # Verificar si el token es válido y obtener el usuario asociado
    if not user:
        flash('Token inválido o expirado', 'error')  # Mensaje si el token ya no es válido
        return redirect(url_for('auth.recover'))  # Redirigir al formulario de recuperación

    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')  # Validar que ambas contraseñas coincidan
            return render_template('auth/new-password.html', token=token)

        if not is_strong_password(password):
            flash('La contraseña debe ser más segura', 'error')  # Validar seguridad de la contraseña
            return render_template('auth/new-password.html', token=token)

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Hashear la nueva contraseña
        user.password_hash = hashed_pw  # Actualizar la contraseña del usuario

        try:
            with session_scope() as session:
                session.add(user)  # Guardar cambios en la base de datos

            flash('Tu contraseña ha sido restablecida correctamente. Inicia sesión.', 'success')
            return redirect(url_for('auth.login'))  # Redirigir al login

        except SQLAlchemyError as e:
            flash('Error al actualizar la contraseña. Intente nuevamente.', 'error')  # Error en base de datos
            current_app.logger.error(f"Error de base de datos: {str(e)}")
    
    return render_template('auth/new-password.html', token=token)  # Mostrar formulario si es GET o hay errores



# Función para restablecer la contraseña directamente desde el correo
# Este endpoint se usa si el usuario ya recibió el token pero se prefiere permitir cambio directo (sin token en URL)
@auth.route('/reset-password', methods=['GET', 'POST'], endpoint='reset_password')
@limiter.limit("5 per minute")
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Redirigir si ya inició sesión

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not is_valid_email(email):
            flash('Correo electrónico inválido', 'error')  # Validación de correo
            return render_template('auth/reset-password.html')

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')  # Validar contraseñas
            return render_template('auth/reset-password.html')

        if not is_strong_password(password):
            flash('La contraseña debe ser más segura', 'error')  # Validar seguridad
            return render_template('auth/reset-password.html')

        user = User.query.filter_by(email=email).first()  # Buscar al usuario por correo

        if user:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Hashear nueva contraseña
            user.password_hash = hashed_pw  # Guardar nuevo hash

            try:
                with session_scope() as session:
                    session.add(user)  # Guardar en base de datos
                    #send_reset_email(user)  # ← Comentado, pero se puede usar para confirmar el cambio

                flash('Tu contraseña ha sido restablecida correctamente.', 'success')
                return redirect(url_for('auth.login'))  # Redirigir al login

            except SQLAlchemyError as e:
                flash('Error al actualizar la contraseña. Intente nuevamente.', 'error')  # Errores de base de datos
                current_app.logger.error(f"Error de base de datos: {str(e)}")
        else:
            flash('No hay cuenta asociada a este correo', 'error')  # Usuario no encontrado
    
    return render_template('auth/reset-password.html')  # Mostrar formulario por defecto


# Función para enviar el correo con el enlace para restablecer la contraseña
def send_reset_email(user):
    token = user.generate_reset_token()  # Genera un token único con expiración
    send_email(
        user.email,
        'Recuperación de contraseña',
        'auth/reset_password_email',  # Template HTML del correo
        user=user,
        token=token  # Este token se usará para acceder a la vista /new-password/<token>
    )

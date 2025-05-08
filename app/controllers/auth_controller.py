import flask_login
from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
from app import limiter, db
from app.models.user import User
from app.services.auth_service import (
    is_valid_email, is_valid_username, is_strong_password, send_reset_email
)
import bcrypt
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from contextlib import contextmanager
from datetime import datetime, timezone
from flask_login import logout_user, current_user, login_required, login_user
from app.models.user import Perfil

auth_web = Blueprint('auth_web', __name__, url_prefix='/auth')

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

@auth_web.route('/login', methods=['GET', 'POST'], endpoint='login')
@limiter.limit("100 per minute")
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

        return render_template('auth/log-in.html', username=username)

    return render_template('auth/log-in.html')


@auth_web.route('/logout', methods=['GET'], endpoint='logout')
@login_required
def logout():
    if current_user.is_authenticated:
        try:
            # Actualizar última conexión
            perfil = Perfil.query.filter_by(username=current_user.username).first()
            if perfil:
                perfil.ultima_conexion = datetime.now(timezone.utc)
                db.session.commit()
                current_app.logger.info(f"Actualizada última conexión para {current_user.username}")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al actualizar última conexión: {str(e)}")
    
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth_web.login'))

@auth_web.route('/register', methods=['GET', 'POST'], endpoint='register')
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

        # Verificar existencia de usuario/email usando la misma sesión
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                flash('Nombre de usuario ya registrado', 'error')
            else:
                flash('Correo electrónico ya registrado', 'error')
            return render_template('auth/sign-up.html', username=username, email=email)

        try:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(username=username, email=email, password_hash=hashed_pw)
            
            with session_scope() as session:
                session.add(new_user)
                # Forzar flush para obtener el ID del nuevo usuario
                session.flush()  
                
                # Crear perfil asociado usando el mismo contexto de sesión
                if not Perfil.query.filter_by(username=new_user.username).first():
                    new_perfil = Perfil(
                        username=new_user.username,
                        fecha_registro=datetime.now(timezone.utc),
                        ultima_conexion = datetime.now(timezone.utc),
                        juegos_jugados=0
                    )
                    session.add(new_perfil)

            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth_web.login'))

        except SQLAlchemyError as e:
            current_app.logger.error(f"Error al registrar usuario: {e}")
            flash('Error al registrar. Inténtalo de nuevo.', 'error')
            return render_template('auth/sign-up.html', username=username, email=email)

    return render_template('auth/sign-up.html')


@auth_web.route('/reset-password', methods=['GET', 'POST'], endpoint='reset_password')
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')  # Nombre corregido
        confirm_password = request.form.get('confirm_password')  # Nuevo campo
        
        # Validaciones básicas
        if not all([email, password, confirm_password]):
            flash('Todos los campos son requeridos', 'error')
            return redirect(url_for('auth_web.reset_password'))
            
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth_web.reset_password'))
            
        if not is_strong_password(password):
            flash('La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, números y símbolos', 'error')
            return redirect(url_for('auth_web.reset_password'))

        user = User.query.filter_by(email=email).first()
        
        if user:
            try:
                # Usar bcrypt consistentemente con el resto de la app
                hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password_hash = hashed_pw
                
                # Usar el contexto transaccional
                with session_scope():
                    db.session.merge(user)
                
                flash('Contraseña actualizada exitosamente', 'success')
                return redirect(url_for('auth_web.login'))

            except Exception as e:
                current_app.logger.error(f"Error reset password: {str(e)}")
                flash('Error interno al actualizar la contraseña', 'error')
                return redirect(url_for('auth_web.reset_password'))

        flash('No existe una cuenta con este correo electrónico', 'error')
        return redirect(url_for('auth_web.reset_password'))

    return render_template('auth/reset-password.html')

@auth_web.route('/new-password/<token>', methods=['GET', 'POST'], endpoint='new_password')
def new_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('Token inválido o expirado', 'error')
        return redirect(url_for('auth_web.reset_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if not password or password != confirm:
            flash('Las contraseñas no coinciden o están vacías', 'error')
            return render_template('auth/new-password.html', token=token)

        if not is_strong_password(password):
            flash('La nueva contraseña no es lo suficientemente segura', 'error')
            return render_template('auth/new-password.html', token=token)

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password_hash = hashed_pw

        try:
            with session_scope():
                db.session.add(user)
            flash('Contraseña actualizada. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth_web.login'))

        except SQLAlchemyError as e:
            current_app.logger.error(f"Error al actualizar contraseña: {e}")
            flash('Error al guardar la nueva contraseña', 'error')

    return render_template('auth/new-password.html', token=token)


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

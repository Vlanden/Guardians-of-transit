
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user

from app.models.user import User
from app import db
from datetime import datetime
from flask import make_response


# Creamos el blueprint principal
main_bp = Blueprint('main', __name__)

# Página pública de bienvenida
@main_bp.route('/')
def inicio():
    return render_template('/main/main-page.html')

@main_bp.route('/iniciar-sesion')
def iniciodesesion():
    return render_template("/auth/log-in.html")

@main_bp.route('/registro')
def registro():
    return render_template('Registro.html')

@main_bp.route('/terminos')
def terminos():
    return render_template('main/terminos.html')

@main_bp.route('/privacidad')
def privacidad():
    return render_template('main/politicas.html')

@main_bp.route('/index')
@login_required
def index():
    return render_template('main/menu.html', user=current_user)

@main_bp.route('/perfil')
@login_required

def perfil():
    return render_template('main/profile.html', user=current_user)

@main_bp.route('/juego')
@login_required
def juego():
    return render_template('game/game.html', user=current_user)


# Página de recuperación de contraseña
@main_bp.route('/recuperacion', methods=['GET', 'POST'])
def recuperacion():
    if request.method == 'POST':
        email = request.form.get('email')
        # Aquí puedes implementar el envío de correo de recuperación
        flash('Si el correo existe, se han enviado las instrucciones para recuperar la contraseña.', 'info')
        return redirect(url_for('main.iniciodesesion'))
    return render_template('Recuperacion.html')


@main_bp.route('/save-score', methods=['POST'])
@login_required
def save_score():
    if request.method == 'POST':
        score = request.form.get('score')
        if score is None:
            return make_response('Falta puntuación', 400)
        try:
            current_user.score = int(score)
            db.session.commit()
            return make_response('Puntuación guardada', 200)
        except Exception as e:
            return make_response(f'Error: {str(e)}', 400)
    return make_response('Método no permitido', 405)


@main_bp.route('/guardar-puntuacion', methods=['POST'])
@login_required
def guardar_puntuacion():
    if request.method == 'POST':
        puntuacion = request.form.get('puntuacion')
        if puntuacion is None:
            return make_response('Puntuación faltante', 400)
        try:
            current_user.score = int(puntuacion)
            db.session.commit()
            return make_response('¡Puntuación guardada con éxito!', 200)
        except Exception as e:
            return make_response(f'Error: {str(e)}', 400)


@main_bp.route('/logout')
def cerrar_secion():
    logout_user()
    return render_template('/InicioDeSesion.html')

@main_bp.route('/actualizar_perfil', methods=['POST'])
@login_required
def actualizar_perfil():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            
            if not username or not email:
                flash('Nombre de usuario y email son requeridos', 'error')
                return redirect(url_for('main.perfil'))
            
            if not current_user.check_password(current_password):
                flash('Contraseña actual incorrecta', 'error')
                return redirect(url_for('main.perfil'))
            
            current_user.username = username
            current_user.email = email
            
            if new_password:
                if len(new_password) < 8:
                    flash('La nueva contraseña debe tener al menos 8 caracteres', 'error')
                    return redirect(url_for('main.perfil'))
                
                if not any(c.isupper() for c in new_password) or not any(c.isdigit() for c in new_password):
                    flash('La contraseña debe contener al menos una mayúscula y un número', 'error')
                    return redirect(url_for('main.perfil'))
                
                current_user.set_password(new_password)
            
            db.session.commit()
            flash('Tus credenciales se actualizaron correctamente', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {str(e)}', 'error')
        
        return redirect(url_for('main.perfil'))



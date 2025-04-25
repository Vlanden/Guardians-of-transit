from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import limiter
from app.controllers.user_controller import UserController

main_bp = Blueprint('main', __name__)

# ──────── RUTAS PÚBLICAS ────────

@main_bp.route('/')
@limiter.limit("100 per minute")
def inicio():
    return render_template('main/main-page.html')

@main_bp.route('/iniciar-sesion')
def iniciodesesion():
    # Redirigir a la ruta de login dentro del Blueprint 'auth_web'
    return redirect(url_for('auth_web.login'))

@main_bp.route('/registro')
def registro():
    # Redirigir a la ruta de registro dentro del Blueprint 'auth_web'
    return redirect(url_for('auth_web.register'))

@main_bp.route('/terminos')
def terminos():
    return render_template('main/terminos.html')

@main_bp.route('/privacidad')
def privacidad():
    return render_template('main/politicas.html')


# ──────── RUTAS PRIVADAS ────────

@main_bp.route('/index')
@login_required
def index():
    return render_template('main/menu.html', user=current_user)

@main_bp.route('/perfil')
@login_required
@limiter.limit("30 per minute")
def perfil():
    return render_template('main/profile.html', user=current_user)

@main_bp.route('/juego/', defaults={'juego_id': None})
@main_bp.route('/juego/<int:juego_id>')
@login_required
def juego(juego_id):
    if juego_id not in range(1, 8):  # acepta del 1 al 7
        return render_template('errors/404.html'), 404
    return render_template('game/game.html', juego_id=juego_id, user=current_user)#, request=request


# ──────── API: FUNCIONES DEL USUARIO ────────

#cambiar el codigo de save_score y save_user_score, el actual es incorrecto
@main_bp.route('/save-score', methods=['POST'])
@login_required
def save_score():
    return UserController.save_score()


#API sin uso
@main_bp.route('/guardar-puntuacion', methods=['POST'])
@login_required
def guardar_puntuacion():
    return UserController.save_score()

#API para actualizar El nombre, correo, o contraseña, El prerequisito es la contraseña
@main_bp.route('/actualizar_perfil', methods=['POST'])
@login_required
def actualizar_perfil():
    return UserController.update_profile()

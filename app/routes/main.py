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
    return redirect(url_for('auth.login'))

@main_bp.route('/registro')
def registro():
    return redirect(url_for('auth.register'))

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

@main_bp.route('/juego')
@login_required
def juego():
    return render_template('game/game.html', user=current_user)



# ──────── API: FUNCIONES DEL USUARIO ────────

@main_bp.route('/save-score', methods=['POST'])
@login_required
def save_score():
    return UserController.save_score()

@main_bp.route('/guardar-puntuacion', methods=['POST'])
@login_required
def guardar_puntuacion():
    return UserController.save_score()

@main_bp.route('/actualizar_perfil', methods=['POST'])
@login_required
def actualizar_perfil():
    return UserController.update_profile()

from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user 
from app import limiter
from app.controllers.user_controller import UserController
from app.models.user import juegos_quiz, juegos_extra, juegos_sim, Perfil


main_bp = Blueprint('main', __name__)

# ──────── RUTAS PÚBLICAS ────────

@main_bp.route('/')
@limiter.limit("100 per minute")
def inicio():
    return render_template('main/main-page.html')

@main_bp.route('/iniciar-sesion')
@limiter.limit("100 per minute")
def iniciodesesion():
    # Redirigir a la ruta de login dentro del Blueprint 'auth_web'
    return redirect(url_for('auth_web.login'))

@main_bp.route('/registro')
@limiter.limit("20 per minute")
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
    quiz_games = juegos_quiz.query.all()
    sim_games = juegos_sim.query.all()
    extra_games = juegos_extra.query.all()
    return render_template('main/menu.html',
                           user=current_user,
                           quiz_games=quiz_games,
                           sim_games=sim_games,
                           extra_games=extra_games)

@main_bp.route('/juego')
@main_bp.route('/juego/<int:juego_id>')
@limiter.limit("100 per minute")
@login_required
def ver_juego(juego_id=None):
    if juego_id is None:
        abort(400, description="ID de juego no proporcionado")
    if juego_id < 100000:
        juego = juegos_quiz.query.get(juego_id)
        tipo = 'quiz'
    elif juego_id < 200000:
        juego = juegos_sim.query.get(juego_id)
        tipo = 'simulacion'
    else:
        juego = juegos_extra.query.get(juego_id)
        tipo = 'extra'
    if not juego:
        abort(404, description="Juego no encontrado")
    return render_template('game/game.html',
                           user=current_user,
                           juego=juego,
                           juego_id=juego_id,
                           juego_tipo=tipo)


@main_bp.route('/perfil')
@login_required
def perfil():
    # Obtener el perfil del usuario actual
    user_profile = Perfil.query.filter_by(username=current_user.username).first()
    
    return render_template(
        'main/profile.html',
        user=current_user,          # Datos básicos del usuario
        user_profile=user_profile   # Datos extendidos del perfil
    )

@main_bp.route('/jugar-juegoextra')
@login_required
def jugar_juegoextra():
    return render_template('game/juegoextra.html')


# ──────── API: FUNCIONES DEL USUARIO ────────


#API para actualizar El nombre, correo, o contraseña, El prerequisito es la contraseña
@main_bp.route('/actualizar_perfil', methods=['POST'])
@limiter.limit("10 per minute")
@login_required
def actualizar_perfil():
    return UserController.update_profile()

# app/routes/games.py

from flask import Blueprint, request, current_app, jsonify
from flask_login import login_required
from app.controllers.game_controller import (
    guardar_puntuacion,
    obtener_quiz
)
from app.models.user import juegos_quiz, QuizPregunta

games_bp = Blueprint('games', __name__, url_prefix='/games')

# === Rutas para la tabla juegos_quiz ===

#@games_bp.route('/quiz', methods=['GET'])
#def list_quiz_games():
  #  """Retorna una lista simple de juegos tipo quiz"""
    #juegos = get_all_quiz_games()
    #salida = "\n".join([f"- {juego['titulo']}" for juego in juegos])
    #return f"Juegos tipo quiz:\n{salida}"

#@games_bp.route('/quiz', methods=['POST'])
#def new_quiz_game():
   # """Crea un nuevo juego tipo quiz"""
   # data = request.form or {}
    #create_quiz_game(data)
    #return "Nuevo juego tipo quiz creado correctamente."

@games_bp.route('/quiz/<int:juego_id>', methods=['GET'], endpoint="obtener_juego")
@login_required
def get_quiz(juego_id):
    try:
        current_app.logger.info(f"Buscando juego con ID {juego_id}")
        juego = juegos_quiz.query.get_or_404(juego_id)

        current_app.logger.info("Juego encontrado. Buscando preguntas...")
        preguntas = QuizPregunta.query.filter_by(id_quiz=juego_id).all()

        current_app.logger.info(f"{len(preguntas)} preguntas encontradas.")

        data = {
                "titulo": juego.titulo,
                "preguntas": [
        {
            "pregunta": p.q_pregunta,
            "opciones": [p.opcioncorrecta, p.opcion2, p.opcion3, p.opcion4],
            "respuesta_correcta": p.opcioncorrecta
        }
        for p in preguntas
    ]
}


        return jsonify(data)

    except Exception as e:
        current_app.logger.error(f"Error en get_quiz: {str(e)}")
        return jsonify({"error": "Datos no disponibles"}), 500


# === Rutas para la tabla juegos_sim ===

@games_bp.route('/sim', methods=['GET'])
def list_sim_games():
    #juegos = get_all_sim_games()
    #salida = "\n".join([f"- {juego['titulo']}" for juego in juegos])
    return f"Juegos tipo simulación:\n{salida}"

@games_bp.route('/sim', methods=['POST'])
def new_sim_game():
    data = request.form or {}
    #create_sim_game(data)
    return "Nuevo juego tipo simulación creado correctamente."

# === Rutas para la tabla juegos_extra ===

@games_bp.route('/extra', methods=['GET'])
def list_extra_games():
    #juegos = get_all_extra_games()
    #salida = "\n".join([f"- {juego['titulo']}" for juego in juegos])
    return f"Juegos tipo extra:\n{salida}"

@games_bp.route('/extra', methods=['POST'])
def new_extra_game():
    data = request.form or {}
    #create_extra_game(data)
    return "Nuevo juego tipo extra creado correctamente."

# === Ruta para guardar puntuación ===

@games_bp.route('/guardar-puntuacion', methods=['POST'])
@login_required
def save_score():
    data = request.form or {}
    guardar_puntuacion(data)
    return "Puntuación guardada correctamente."

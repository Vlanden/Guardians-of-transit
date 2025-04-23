# app/routes/games.py

from flask import Blueprint, request, jsonify
from app.controllers.games_controller import (
    get_all_quiz_games,
    get_all_sim_games,
    get_all_extra_games,
    create_quiz_game,
    create_sim_game,
    create_extra_game
)

# Creamos el Blueprint con el nombre 'games' y un prefijo de URL '/games'
games_bp = Blueprint('games', __name__, url_prefix='/games')

# === Rutas para la tabla juegos_quiz ===
@games_bp.route('/quiz', methods=['GET'])
def list_quiz_games():
    """Retorna todos los juegos tipo quiz"""
    return jsonify(get_all_quiz_games())

@games_bp.route('/quiz', methods=['POST'])
def new_quiz_game():
    """Crea un nuevo juego tipo quiz"""
    data = request.get_json()
    return jsonify(create_quiz_game(data))


# === Rutas para la tabla juegos_sim ===
@games_bp.route('/sim', methods=['GET'])
def list_sim_games():
    """Retorna todos los juegos tipo simulación"""
    return jsonify(get_all_sim_games())

@games_bp.route('/sim', methods=['POST'])
def new_sim_game():
    """Crea un nuevo juego tipo simulación"""
    data = request.get_json()
    return jsonify(create_sim_game(data))


# === Rutas para la tabla juegos_extra ===
@games_bp.route('/extra', methods=['GET'])
def list_extra_games():
    """Retorna todos los juegos tipo extra"""
    return jsonify(get_all_extra_games())

@games_bp.route('/extra', methods=['POST'])
def new_extra_game():
    """Crea un nuevo juego tipo extra"""
    data = request.get_json()
    return jsonify(create_extra_game(data))

# app/routes/games.py
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from flask import Blueprint, request, current_app, jsonify
import sqlalchemy.exc
from werkzeug.exceptions import HTTPException  # <-- Importación correctafrom flask_login import login_required, current_user
from app.controllers.game_controller import (
    guardar_puntuacion,
    obtener_quiz
)
from app.models.user import  (User, Perfil, intentos, juegos_quiz, QuizPregunta, juegos_extra, juegos_sim)
from app.routes.main import ver_juego
from flask_login import login_required,current_user
from flask_wtf.csrf import CSRFProtect, validate_csrf, ValidationError
from datetime import datetime, timedelta
from app import limiter


csrf = CSRFProtect()  # Inicialización en tu aplicación

games_bp = Blueprint('games', __name__, url_prefix='/games')

# === Rutas para la tabla juegos_quiz ===

@games_bp.route('/api/juegos')
@limiter.limit("10 per minute")
def obtener_juegos():
    categorias = {
        'quiz': juegos_quiz.query.all(),
        'simulacion': juegos_sim.query.all(),
        'extra': juegos_extra.query.all()
    }
    return jsonify({
        cat: [juego.to_dict() for juego in juegos] 
        for cat, juegos in categorias.items()
    })
    

@games_bp.route('/buscar')
@limiter.limit("100 per minute")
def buscar():
    termino = request.args.get('q', '')
    if not termino:
        return jsonify([])
    
    results = []
    # Buscar en todos los tipos de juegos
    for model in [juegos_quiz, juegos_sim, juegos_extra]:
        query = text(f"SELECT * FROM {model.__tablename__} WHERE titulo LIKE :term OR descripcion LIKE :term")
        results.extend(db.session.execute(query, {'term': f'%{termino}%'}).fetchall())
    
    return jsonify([dict(row) for row in results])




@games_bp.route('/quiz/<int:juego_id>', methods=['GET'])
@limiter.limit("100 per minute")
@login_required
def obtener_quiz(juego_id):
    try:
        # Verificar existencia del juego
        juego = juegos_quiz.query.get_or_404(juego_id)
        
        # Obtener preguntas
        preguntas = QuizPregunta.query.filter_by(id_quiz=juego_id).all()
        
        # Validar preguntas
        if not preguntas:
            current_app.logger.warning(f"Quiz {juego_id} sin preguntas")
            return jsonify({"error": "El quiz no tiene preguntas configuradas"}), 404

        # Construir respuesta
        data = {
            "titulo": juego.titulo,
            "preguntas": []
        }

        for p in preguntas:
            opciones = [
                p.opcioncorrecta,
                p.opcion2,
                p.opcion3,
                p.opcion4
            ]
            
            # Filtrar y validar opciones
            opciones_validas = [op for op in opciones if op is not None]
            
            if len(opciones_validas) < 2:
                raise ValueError("Cada pregunta debe tener al menos 2 opciones válidas")

            data["preguntas"].append({
                "pregunta": p.q_pregunta,
                "opciones": opciones_validas,
                "respuesta_correcta": p.opcioncorrecta,
                "explicacion": p.explicacion or "Explicación no disponible"
            })

        return jsonify(data)

    except HTTPException as e:
        raise e
    except Exception as e:
        current_app.logger.error(f"Error en obtener_quiz: {str(e)}")
        return jsonify({
            "error": "Error al cargar el quiz",
            "detalle": str(e)
        }), 500


@games_bp.route('/guardar-puntuacion', methods=['POST'])
@login_required
@limiter.limit("50 per minute")
def guardar_puntuacion():
    try:
        # obtenemos y validamos el token CSRF lanzando si no es válido
        csrf_token = request.headers.get('X-CSRFToken', '')
        try:
            validate_csrf(csrf_token)
        except ValidationError as ve:
            current_app.logger.warning(f"CSRF inválido: {ve}")
            return jsonify({"error": "Token CSRF inválido"}), 403
        
        
        data = request.get_json()
        juego_id = str(data.get('juego_id'))  # Convertir a string
        puntuacion = int(data.get('puntuacion'))

        # Obtener o crear perfil
        perfil = Perfil.query.get(current_user.username)
        if not perfil:
            perfil = Perfil(username=current_user.username)
            db.session.add(perfil)

        # Actualizar juegos_jugados (IDs separados por comas)
        if perfil.juegos_jugados:
            juegos_existentes = perfil.juegos_jugados.split(',')
            if juego_id not in juegos_existentes:  # Evitar duplicados
                perfil.juegos_jugados = f"{perfil.juegos_jugados},{juego_id}"
        else:
            perfil.juegos_jugados = juego_id  # Primer juego

        # Guardar intento y actualizar perfil
        nuevo_intento = intentos(
            username=current_user.username,
            juego_id=juego_id,
            puntaje=puntuacion,
            fecha_inicio=datetime.utcnow(),
            fecha_fin=datetime.utcnow()
        )
        db.session.add(nuevo_intento)
        db.session.commit()

        return jsonify({"success": True, "juegos_jugados": perfil.juegos_jugados})

    except ValueError as e:
        return jsonify({"error": "Datos inválidos", "detalle": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error de base de datos: {str(e)}")
        return jsonify({"error": "Error al guardar datos"}), 500


# === Rutas para la tabla juegos_sim ===

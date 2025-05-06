# app/routes/games.py
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from flask import Blueprint, request, current_app, jsonify
from werkzeug.exceptions import HTTPException
from app.models.user import  ( Perfil, intentos, juegos_quiz, QuizPregunta, juegos_extra, juegos_sim)
from flask_login import login_required,current_user
from flask_wtf.csrf import CSRFProtect, validate_csrf, ValidationError
from datetime import datetime, timezone, timedelta
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
    termino = request.args.get('q', '').strip().lower()
    
    # if len(termino) < 2:
    #     return jsonify({"quiz": [], "simulacion": [], "extra": []})


    try:
        # Función auxiliar para búsqueda en cualquier modelo
        def buscar_en_modelo(modelo):
            return modelo.query.filter(
                db.or_(
                    modelo.titulo.ilike(f'%{termino}%'),
                    modelo.descripcion.ilike(f'%{termino}%')
                )
            ).all()

        return jsonify({
            "quiz": [j.to_dict() for j in buscar_en_modelo(juegos_quiz)],
            "simulacion": [j.to_dict() for j in buscar_en_modelo(juegos_sim)],
            "extra": [j.to_dict() for j in buscar_en_modelo(juegos_extra)]
        }), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        current_app.logger.error(f"Error en búsqueda: {str(e)}")
        return jsonify({"error": str(e)}), 500




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
        fecha_inicio = datetime.strptime(data.get('fecha_inicio'), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        fecha_fin = datetime.strptime(data.get('fecha_fin'), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

        if int(data.get('juego_id')) < 100000:
            if not juegos_quiz.query.get(juego_id):
                return {"error": "Juego no existe"}, 404
    
        if not (0 <= puntuacion <= 100):
                    return {'error': 'Puntuación inválida'}, 400
                
                # Guardar intento y actualizar perfil
        nuevo_intento = intentos(
            username=current_user.username,
            juego_id=juego_id,
            puntaje=puntuacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        db.session.add(nuevo_intento)
        db.session.commit()


        # Obtener o crear perfil
        perfil = Perfil.query.filter_by(username=current_user.username).first()
        if not perfil:
            perfil = Perfil(username=current_user.username, juegos_jugados=None)  # Inicializar como None
            db.session.add(perfil)
            db.session.flush()

        # Actualizar juegos_jugados (IDs separados por comas)
        if perfil.juegos_jugados:
            juegos_existentes = perfil.juegos_jugados.split(',')
        else:
            perfil.juegos_jugados = juego_id  # Primer juego
            
            
        

        # Filtrar elementos vacíos y espacios
        juegos_actuales = (
            [x.strip() for x in perfil.juegos_jugados.split(',') if x.strip()] 
            if perfil.juegos_jugados 
            else []
        )
        
        juegos_actuales.append(juego_id)
        if len(juegos_actuales) > 5:
                juegos_actuales.pop(0)
                
        perfil.juegos_jugados = ','.join(juegos_actuales)
        gdl = timezone(timedelta(hours=-6))
        
        perfil.ultima_conexion = datetime.now(gdl)
        
        current_app.logger.info(f"Perfil actualizado: {perfil.username} | Juegos: {perfil.juegos_jugados} | Ultima Conexion: {perfil.ultima_conexion}")
        
        db.session.commit()

        return {
                'success': True,
                'intento_id': nuevo_intento.id,
                'juegos_jugados': perfil.juegos_jugados,
                'fecha_inicio': nuevo_intento.fecha_inicio,
                'fecha_fin': nuevo_intento.fecha_fin
            }, 200  # ← Código HTTP explícito
        
    except ValueError as e:
        return jsonify({"error": "Datos inválidos", "detalle": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error de base de datos: {str(e)}")
        return jsonify({"error": "Error al guardar datos"}), 500


# === Rutas para la tabla juegos_sim ===

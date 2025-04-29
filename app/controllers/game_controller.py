from flask import current_app, app
from flask_login import login_required, current_user
from datetime import datetime, timezone
from werkzeug.exceptions import HTTPException
from app.models.user import juegos_quiz, QuizPregunta, intentos, Perfil
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError

def obtener_quiz(juego_id):
    """
    Obtiene las preguntas de un quiz específico
    Args:
        juego_id (int): ID del juego a buscar
    Returns:
        dict: Diccionario con título y preguntas del quiz
        tuple: (dict, int) en caso de error (mensaje, código HTTP)
    """
    try:
        juego = juegos_quiz.query.get_or_404(juego_id)
        preguntas = QuizPregunta.query.filter_by(id_quiz=juego_id).all()
        
        if not preguntas:
            current_app.logger.warning(f'Quiz {juego_id} sin preguntas')
            return {'error': 'El quiz no tiene preguntas configuradas'}, 404

        preguntas_formateadas = []
        for p in preguntas:
            opciones = [op for op in [p.opcioncorrecta, p.opcion2, p.opcion3, p.opcion4] if op is not None]
            
            if len(opciones) < 2:
                raise ValueError(f"Pregunta ID {p.id} no tiene suficientes opciones")

            preguntas_formateadas.append({
                'texto': p.q_pregunta,
                'opciones': opciones,
                'correcta': 0,  # Índice de la opción correcta
                'explicacion': p.explicacion or "Explicación no disponible"
            })

        return {
            'titulo': juego.titulo,
            'preguntas': preguntas_formateadas
        }

    except HTTPException:
        raise  # Re-lanzar excepciones HTTP (como 404)
    except Exception as e:
        current_app.logger.error(f'Error en obtener_quiz: {str(e)}')
        return {'error': 'Error al cargar el quiz', 'detalle': str(e)}, 500


@login_required
def guardar_puntuacion(data):
    try:
        required_keys = ['juego_id', 'puntuacion', 'fecha_inicio', 'fecha_fin']
        missing = [key for key in required_keys if key not in data]
        if missing:
            return {'error': 'Datos incompletos', 'campos_faltantes': missing}, 400

        try:
            # Convertir fechas a UTC correctamente
            juego_id = str(int(data['juego_id']))
            puntuacion = int(data['puntuacion'])
            #Calcular las fechas en otra funcion 
            fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            fecha_fin = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        except (ValueError, TypeError) as e:
            return {'error': 'Datos inválidos', 'detalle': str(e)}, 400

        if not (0 <= puntuacion <= 100):
            return {'error': 'Puntuación inválida'}, 400

        with db.session.begin():
            nuevo_intento = intentos(
            username=current_user.username,
            juego_id=juego_id,
            puntaje=puntuacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        db.session.add(nuevo_intento)
        
        
        perfil = Perfil.query.filter_by(username=current_user.username).first()
        if not perfil:
            perfil = Perfil(username=current_user.username, juegos_jugados=None)  # Inicializar como None
            db.session.add(perfil)
            db.session.flush()

        # Filtrar elementos vacíos y espacios
        juegos_actuales = (
            [x.strip() for x in perfil.juegos_jugados.split(',') if x.strip()] 
            if perfil.juegos_jugados 
            else []
        )
        
        if juego_id not in juegos_actuales:
            juegos_actuales.append(juego_id)
            if len(juegos_actuales) > 5:
                juegos_actuales.pop(0)
            perfil.juegos_jugados = ','.join(juegos_actuales)
        
        perfil.ultima_conexion = datetime.now(timezone.utc)
        
        current_app.logger.info(f"Perfil actualizado: {perfil.username} | Juegos: {perfil.juegos_jugados}")

        return {
                'success': True,
                'intento_id': nuevo_intento.id,
                'juegos_jugados': perfil.juegos_jugados,
                'fecha_inicio': nuevo_intento.fecha_inicio,
                'fecha_fin': nuevo_intento.fecha_fin
            }, 200  # ← Código HTTP explícito

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f'Error DB: {str(e)}')
        return {'error': 'Error en base de datos'}, 500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error inesperado: {str(e)}')
        app.logger.error(f"Error crítico: {str(e)}")
        return {'error': 'Error interno'}, 500

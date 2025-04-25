from flask import jsonify, request
from flask_login import current_user
from datetime import datetime
from app.models.user import juegos_quiz, QuizPregunta, intentos, Perfil
from app.extensions import db


def obtener_quiz(juego_id):
    juego = juegos_quiz.query.get_or_404(juego_id)
    preguntas = QuizPregunta.query.filter_by(id_quiz=juego_id).all()
    
    preguntas_formateadas = []
    for p in preguntas:
        opciones = [p.opcioncorrecta, p.opcion2]
        if p.opcion3: opciones.append(p.opcion3)
        if p.opcion4: opciones.append(p.opcion4)
        
        preguntas_formateadas.append({
            'texto': p.q_pregunta,
            'opciones': opciones,
            'correcta': 0,  # Porque opcioncorrecta siempre es la primera
            'explicacion': p.explicacion
        })
    
    return {
        'titulo': juego.titulo,
        'preguntas': preguntas_formateadas
    }

def guardar_puntuacion(data):
    nuevo_intento = intentos(
        username=current_user.username,
        juego_id=data['juego_id'],
        puntaje=data['puntuacion'],
        fecha_inicio=datetime.utcnow(),
        fecha_fin=datetime.utcnow()
    )
    db.session.add(nuevo_intento)
    
    # Actualizar perfil
    perfil = Perfil.query.get(current_user.username)
    if perfil:
        perfil.juegos_jugados = (perfil.juegos_jugados or 0) + 1
    
    db.session.commit()
    
    return {'mensaje': 'Puntuación guardada correctamente'}
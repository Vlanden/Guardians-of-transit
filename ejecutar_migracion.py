# Crear aplicación Flask
from app import db
from app.models.user import juegos_quiz, QuizPregunta
from app import create_app  # Importar create_app
from app.extensions import db
# Definir quizzes como en tu JS
quizzes = {
    1: [
    {
        "texto": "¿Qué significa una luz roja en un semáforo?",
        "opciones": [
        "Avanzar con precaución",
        "Detenerse",
        "Girar a la derecha",
        "Cruzar rápido",
        ],
        "correcta": 1,
    },
    {
        "texto": "¿Quién tiene prioridad en un cruce peatonal sin semáforo?",
        "opciones": ["El ciclista", "El peatón", "El conductor", "El motociclista"],
        "correcta": 1,
    },
    {
        "texto": "¿Cuál es el límite de velocidad en zonas escolares?",
        "opciones": ["60 km/h", "40 km/h", "30 km/h", "20 km/h"],
        "correcta": 2,
    },
    {
        "texto": "¿Qué debes hacer si escuchas una sirena de ambulancia detrás?",
        "opciones": [
        "Acelerar",
        "Ignorarla",
        "Detenerte y ceder el paso",
        "Cambiar de carril sin señalizar",
        ],
        "correcta": 2,
    },
    {
        "texto":
        "¿Qué indica una señal de tránsito con un triángulo rojo y un símbolo de peatón?",
        "opciones": [
        "Cruce peligroso",
        "Zona escolar",
        "Cruce peatonal",
        "Alto obligatorio",
        ],
        "correcta": 2,
    },
    ],
          2: [
        {
          "texto": "¿Qué debes hacer antes de cambiar de carril?",
          "opciones": ["Acelerar", "Usar las luces direccionales", "Frenar", "Nada"],
          "correcta": 1,
          "explicacion": "Siempre usa las luces direccionales para indicar tus movimientos."
        },
        {
          "texto": "¿Cuál es la distancia mínima que debes mantener con el vehículo de adelante?",
          "opciones": ["1 metro", "3 segundos", "10 metros", "Depende del clima"],
          "correcta": 1,
          "explicacion": "La regla de los 3 segundos permite mantener una distancia segura en condiciones normales."
        },
        {
          "texto": "¿Qué significa una línea continua en el centro de la carretera?",
          "opciones": ["Puedes rebasar", "No puedes rebasar", "Calle cerrada", "Solo peatones"],
          "correcta": 1,
          "explicacion": "Una línea continua indica que no está permitido rebasar."
        },
        {
          "texto": "¿Qué documento necesitas para conducir legalmente?",
          "opciones": ["Pasaporte", "Licencia de conducir", "CURP", "INE"],
          "correcta": 1,
          "explicacion": "La licencia de conducir es obligatoria para manejar legalmente."
        },
        {
          "texto": "¿Qué hacer si se te pincha una llanta en carretera?",
          "opciones": ["Seguir conduciendo", "Frenar de golpe", "Encender luces intermitentes y orillarte", "Salir del coche en medio del camino"],
          "correcta": 2,
          "explicacion": "Oríllate con precaución y enciende intermitentes para evitar accidentes."
        }
      ]
}
def migrar_quizzes():
    app = create_app()
    
    with app.app_context():
        try:
            for juego_id in range(1, 3):  # Para los juegos 1 y 2
                # Forma recomendada SQLAlchemy 2.0
                juego = db.session.get(juegos_quiz, juego_id)
                
                if not juego:
                    juego = juegos_quiz(
                        id_quiz=juego_id,
                        titulo=f"Educación Vial {juego_id}",
                        descripcion=f"Quiz sobre normas de tránsito {juego_id}",
                        img_referencia=f"game{juego_id}.jpg"
                    )
                    db.session.add(juego)
                
                preguntas_js = quizzes.get(juego_id, [])
                for pregunta_js in preguntas_js:
                    pregunta = QuizPregunta(
                        id_quiz=juego_id,
                        q_pregunta=pregunta_js['texto'],  # Usar q_pregunta en lugar de pregunta
                        opcioncorrecta=pregunta_js['opciones'][pregunta_js['correcta']],
                        opcion2=pregunta_js['opciones'][1] if len(pregunta_js['opciones']) > 1 else "",
                        opcion3=pregunta_js['opciones'][2] if len(pregunta_js['opciones']) > 2 else "",
                        opcion4=pregunta_js['opciones'][3] if len(pregunta_js['opciones']) > 3 else "",
                        explicacion=pregunta_js.get('explicacion', '')
                    )
                    db.session.add(pregunta)
            
            db.session.commit()
            print("¡Migración completada con éxito!")
        except Exception as e:
            db.session.rollback()
            print(f"Error durante la migración: {str(e)}")
            raise

if __name__ == '__main__':
    print("Iniciando migración de datos...")
    migrar_quizzes()
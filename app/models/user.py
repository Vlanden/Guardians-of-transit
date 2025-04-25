from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db
import bcrypt
from datetime import datetime, timedelta
import secrets
from sqlalchemy import event
from sqlalchemy.schema import DDL

#   Clase para User
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Las siguientes columnas son para cuando este para enviar correos de recuperacion:
    # reset_token = db.Column(db.String(100), nullable=True)
    # reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    # Método para cambiar la contraseña directamente sin usar un token
    def change_password_direct(self, new_password):
        """Cambia la contraseña del usuario directamente sin token"""
        self.set_password(new_password)  # Cifra y guarda la nueva contraseña
        db.session.commit()  # Guarda los cambios en la base de datos

    # Método para cifrar una contraseña antes de guardarla
    def set_password(self, password):
        """Encripta la contraseña antes de guardarla"""
        self.password_hash = bcrypt.hashpw(  # Genera un hash seguro con bcrypt
            password.encode('utf-8'),        # Convierte la contraseña en bytes
            bcrypt.gensalt()                 # Genera una sal aleatoria
        ).decode('utf-8')                    # Guarda el hash como texto (string)

    # Método para verificar que una contraseña coincida con el hash guardado
    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada"""
        return bcrypt.checkpw(  # Compara la contraseña proporcionada con el hash
            password.encode('utf-8'),        # Convierte la contraseña en bytes
            self.password_hash.encode('utf-8')  # Convierte el hash guardado en bytes
        )

    # Método para generar un token temporal para restablecer contraseña
    def generate_reset_token(self, expires_in=3600):
        """
        Genera un token de restablecimiento de contraseña y lo almacena en la base de datos.
        El token es válido por el tiempo definido en `expires_in` (por defecto: 3600 segundos).
        """
        self.reset_token = secrets.token_urlsafe(32)  # Crea un token seguro de 32 caracteres
        self.reset_token_expires = datetime.utcnow() + timedelta(seconds=expires_in)  # Fecha de expiración
        db.session.commit()  # Guarda el token y su expiración en la base de datos
        return self.reset_token  # Devuelve el token para enviarlo al usuario (por correo, por ejemplo)

    # Método estático para verificar si un token de reseteo es válido
    @staticmethod
    def verify_reset_token(token):
        """
        Verifica si el token de restablecimiento proporcionado existe y no ha expirado.
        Retorna el usuario asociado si es válido, o None si no lo es.
        """
        return User.query.filter(
            User.reset_token == token,  # Compara con el token almacenado
            User.reset_token_expires > datetime.utcnow()  # Asegura que aún no haya expirado
        ).first()  # Devuelve el primer usuario que cumpla con las condiciones

    # Método especial para mostrar el objeto de usuario como una cadena
    def __repr__(self) -> str:
        return f'<User {self.username}>'  # Útil para depuración: muestra el nombre de usuario

    
    

# Clases adicionales como QuizPregunta,Perfil, intentos, juegos_quiz, juegos_sim, y juegos_extra


    

class Perfil(UserMixin, db.Model):
    __tablename__ = 'perfil'  

    username = db.Column(db.String(80), db.ForeignKey('users.username'), primary_key=True)
    fecha_registro = db.Column(db.DateTime)
    ultima_conexion = db.Column(db.DateTime)
    juegos_jugados = db.Column(db.Integer, default=0) 




class intentos(UserMixin, db.Model):
    __tablename__ = 'intentos'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    juego_id = db.Column(db.Integer, nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)

class juegos_quiz(UserMixin, db.Model):
    __tablename__ = 'juegos_quiz'

    id_quiz = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable = False)
    descripcion = db.Column(db.String(255), nullable=False)
    img_referencia = db.Column(db.String(255), nullable=False)
    
    preguntas = db.relationship('QuizPregunta', backref='juego', lazy=True, cascade='all, delete-orphan')
        

class juegos_sim(UserMixin, db.Model):
    __tablename__ = 'juegos_sim'

    id_sim = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable = False)
    descripcion = db.Column(db.String(255), nullable=False)
    img_referencia = db.Column(db.String(255), nullable=False)
event.listen(
    juegos_sim.__table__,
    'after_create',
    DDL("ALTER TABLE juegos_sim AUTO_INCREMENT = 100000;")
)


class juegos_extra(UserMixin, db.Model):
    __tablename__ = 'juegos_extra'

    id_extra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable = False)
    descripcion = db.Column(db.String(255), nullable=False)
    img_referencia = db.Column(db.String(255), nullable=False)
event.listen(
    juegos_extra.__table__,
    'after_create',
    DDL("ALTER TABLE juegos_extra AUTO_INCREMENT = 200000;")
)

class QuizPregunta(db.Model):
    __tablename__ = 'quiz_preguntas'
    
    id_pregunta = db.Column(db.Integer, primary_key=True)
    id_quiz = db.Column(db.Integer, db.ForeignKey('juegos_quiz.id_quiz'))  # FK al juego
    q_pregunta = db.Column(db.String(500), nullable=False)
    opcioncorrecta = db.Column(db.String(200), nullable=False)  # Correcta
    opcion2 = db.Column(db.String(200), nullable=False)
    opcion3 = db.Column(db.String(200), nullable=False)
    opcion4 = db.Column(db.String(200), nullable=False)
    explicacion = db.Column(db.String(500))
    

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
import bcrypt
from datetime import datetime

from sqlalchemy import event
from sqlalchemy.schema import DDL

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
        
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    

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


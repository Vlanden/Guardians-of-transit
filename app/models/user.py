from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
import bcrypt
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)  # Asegúrate que esta línea existe
    reset_token = db.Column(db.String(100), nullable=True)
    token_expiration = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Integer, default=0)
        
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
    
    

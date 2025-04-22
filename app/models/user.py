import bcrypt
import secrets
from datetime import datetime, timedelta
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

    def set_password(self, password: str) -> None:
        if not password:
            raise ValueError("La contraseña no puede estar vacía")
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def generate_reset_token(self, expires_in=3600):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(seconds=expires_in)
        db.session.commit()
        return self.reset_token

    @staticmethod
    def verify_reset_token(token):
        return User.query.filter(
            User.reset_token == token,
            User.reset_token_expires > datetime.utcnow()
        ).first()

    def __repr__(self) -> str:
        return f'<User {self.username}>'
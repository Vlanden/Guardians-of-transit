import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

# Cargar las variables de entorno
load_dotenv()

class Config:
    # Configuración básica
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_urlsafe(64))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(64))
    
    # Base de datos
    BASE_DIR = Path(__file__).parent.parent
    INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
    DB_PATH = BASE_DIR / 'database.db'  # En el directorio del proyecto
    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Seguridad
    SESSION_COOKIE_SECURE = True  # Asegúrate de que esté en True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Asegúrate de que esta variable esté en el .env
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Asegúrate de que esta variable esté en el .env
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@superiorteam.site')
    
    # Logging
    LOG_FOLDER = 'logs'
    LOG_FILE = 'app.log'
    LOG_MAX_BYTES = 1024 * 1024  # 1MB
    LOG_BACKUP_COUNT = 5

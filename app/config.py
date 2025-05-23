import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """Configuración base de la aplicación Flask"""
    
    # -------------------------------
    # Configuración de Seguridad
    # -------------------------------
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_urlsafe(64))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(64))
    
    # Configuración de cookies seguras
    SESSION_COOKIE_SECURE = True  # Requiere HTTPS en producción
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protección contra CSRF
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # -------------------------------
    # Configuración de Base de Datos
    # -------------------------------
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,
    'max_overflow': 2,
    'pool_recycle': 3600,
    'pool_pre_ping': True
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactiva el tracking de modificaciones
    
    # -------------------------------
    # Configuración de Archivos
    # -------------------------------
    # Directorio para uploads (relativo al directorio del paquete)
    BASE_DIR = Path(__file__).parent.parent
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    
    # Extensiones permitidas para uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Límite de 16MB para uploads
    
    # -------------------------------
    # Métodos de Clase
    # -------------------------------
 
            
    @classmethod
    def init_app(cls, app):
        """Inicialización adicional para la aplicación"""
        # Asegurar que el directorio instance existe
        instance_path = Path(app.instance_path)
        instance_path.mkdir(parents=True, exist_ok=True)
        
        # Actualizar dinámicamente la URI para SQLite
        if cls.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
            db_path = instance_path / 'local_database.db'
            cls.SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

    @classmethod
    def check_config(cls):
        """Verifica que la configuración esencial esté establecida"""
        required_keys = ['SECRET_KEY', 'JWT_SECRET_KEY', 'SQLALCHEMY_DATABASE_URI']
        for key in required_keys:
            if not getattr(cls, key):
                raise ValueError(f"La configuración requerida {key} no está establecida")
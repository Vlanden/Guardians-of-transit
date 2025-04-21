from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
import secrets
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
csrf = CSRFProtect()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="fixed-window",
    headers_enabled=True
)

# Redirección por defecto para usuarios no autenticados
login_manager.login_view = 'main.iniciodesesion'

def create_app():
    # Cargar variables de entorno
    load_dotenv()
    print("🔍 DATABASE_URL:", os.getenv("DATABASE_URL"))

    app = Flask(__name__, instance_relative_config=True)

    # Configuración de directorios
    csrf.init_app(app)
    instance_path = os.path.abspath(app.instance_path)
    os.makedirs(instance_path, exist_ok=True)
    os.makedirs(os.path.join(instance_path, 'logs'), exist_ok=True)
    
    # Configuración base
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Configurar ruta de base de datos
    raw_db_uri = os.getenv('DATABASE_URL')
    if raw_db_uri.startswith('sqlite:///instance/'):
        db_path = raw_db_uri.replace(
            'sqlite:///instance/',
            f"sqlite:///{os.path.join(app.instance_path, '')}"
        )
        app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_uri


        # Configuración de seguridad
    app.config.update(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY', secrets.token_urlsafe(64)),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(64)),
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=timedelta(days=7),
        
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USERNAME = 'tu_email@gmail.com',
        MAIL_PASSWORD = 'tu_contraseña',
        MAIL_DEFAULT_SENDER = 'no-reply@superiorteam.site'
    )
    
    # Configuración de logging
    handler = RotatingFileHandler(
        os.path.join(instance_path, 'logs/app.log'),
        maxBytes=1024 * 1024,
        backupCount=5)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    # Inicialización de extensiones
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)
    Talisman(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
    login_manager.login_message_category = 'info'

    # ✅ Importar el modelo User correctamente desde models/user.py
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except Exception as e:
            app.logger.error(f"Error loading user: {str(e)}")
            return None
       # Context processor para inyectar 'now' en todos los templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
        
        # Registrar blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Registrar blueprints
    from app.routes import main_bp
    from app.Registro import auth_bp  # Si tienes este blueprint también
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Creación de tablas
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created successfully")
        except Exception as e:
            app.logger.error(f"Database error: {str(e)}")
            raise

    return app

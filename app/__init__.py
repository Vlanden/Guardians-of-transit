# app/__init__.py
import os
from flask import Flask, flash , redirect,url_for
from app.routes.games import games_bp
from .config import Config
from .extensions import db, login_manager, jwt, csrf, limiter, talisman
from .utils.logging import configure_logging
from sqlalchemy.exc import OperationalError
from flask_talisman import Talisman

def create_app(config_class=Config):
    app = Flask(__name__)
    # Configuración de CSP más permisiva pero segura
    csp = {
        'default-src': "'self'",
        'style-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
        'script-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
        'img-src': ["'self'", "data:", "https://*"],
        'font-src': ["'self'", "https://cdn.jsdelivr.net"]
    }

    Talisman(app, content_security_policy=csp)

    app.config.from_object(config_class)

    # Configurar procesadores de contexto
    configure_context_processors(app)
    
    # Inicializar extensiones —> esto registra 'app' con SQLAlchemy
    initialize_extensions(app)

    # 2. Inicializar Flask-Migrate INMEDIATAMENTE después de db
    #from flask_migrate import Migrate
    #migrate = Migrate(app, db)  # <-- Esta línea debe estar aquí
    
    # Configurar logging (si decides activarlo)
    # configure_logging(app)

    # Configurar manejo de usuarios
    configure_user_loader(app)

    # Registrar blueprints
    register_blueprints(app)

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verifica conexiones antes de usarlas
        'pool_recycle': 3600,   # Recicla conexiones cada 1 hora
        'pool_size': 10,        # Conexiones mantenidas abiertas
        'max_overflow': 5,      # Conexiones adicionales permitidas
        'pool_timeout': 30      # Tiempo de espera para obtener conexión
    }

    # ✅ AHORA SÍ: crear la base de datos una vez que db ya está registrado con app
    configure_database(app)

    @app.errorhandler(OperationalError)
    def handle_db_errors(e):
        db.session.rollback()
        flash('Error temporal con la base de datos. Por favor intente nuevamente.', 'error')
        return redirect(url_for('main.index'))

    return app




def initialize_extensions(app):
    """Inicializa todas las extensiones Flask"""
    from app.extensions import db, login_manager, jwt, limiter, csrf, talisman  # Importación local
    
    db.init_app(app)
    login_manager.init_app(app)
    ##Es el manejador de la ventana de logeo
    login_manager.login_view = 'auth_web.login'
    jwt.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)
    talisman.init_app(app)

def configure_user_loader(app):
    """Configura el user_loader para Flask-Login"""
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            user = db.session.get(User, int(user_id))
            if user is None:
                app.logger.warning(f"User with id {user_id} not found.")
            return user
        except Exception as e:
            app.logger.error(f"Error loading user with id {user_id}: {str(e)}")
            return None

def register_blueprints(app):
    """Registra todos los blueprints de la aplicación"""
    from app.routes.main import main_bp
    from app.routes.auth import auth_api
    from app.controllers.auth_controller import auth_web 
    from app.routes.games import games_bp
    from app.controllers.admin.quiz_controller import quiz_admin
    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_admin, url_prefix='/admin/quizzes')
    app.register_blueprint(games_bp, url_prefix='/games')
    app.register_blueprint(auth_web, url_prefix='/auth')
    app.register_blueprint(auth_api, url_prefix='/api/auth')

def configure_context_processors(app):
    """Configura los context processors"""
    from datetime import datetime
    
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

def configure_database(app):
    """Configuración segura de la base de datos"""
    with app.app_context():
        try:
            # Verificar permisos de escritura
            #test_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            db.create_all()
            app.logger.info("Base de datos creada exitosamente")
        except Exception as e:
            app.logger.error(f"Error crítico: {str(e)}")
            raise


        
        
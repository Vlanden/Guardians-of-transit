# app/__init__.py
import os
from flask import Flask
from .config import Config
from .extensions import db, login_manager, jwt, csrf, limiter, talisman
from .utils.logging import configure_logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configurar logging
    #configure_logging(app)
    
    # Inicializar extensiones
    initialize_extensions(app)
    
    # Configurar manejo de usuarios
    configure_user_loader(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Configuración adicional
    configure_context_processors(app)
    configure_database(app)
    
    return app

def initialize_extensions(app):
    """Inicializa todas las extensiones Flask"""
    from app.extensions import db, login_manager, jwt, limiter, csrf, talisman  # Importación local
    
    db.init_app(app)
    login_manager.init_app(app)
    ##Pendiente de checar
    login_manager.login_view = 'auth.login'
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
    from app.routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

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
# app/__init__.py
import os
from werkzeug.middleware.proxy_fix import ProxyFix  # ✅ Añadir al inicio
from flask import Flask, flash , redirect,url_for
from .config import Config
from .extensions import db, login_manager, jwt, csrf, limiter, talisman
from sqlalchemy.exc import OperationalError
from pathlib import Path



def create_app(config_class=Config):
    app = Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

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

    # En la configuración de SQLAlchemy (funcion de init create_app):
    # En app/__init__.py
    #app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    #        'pool_size': 5,
    #        'pool_recycle': 280,  # Menor que el wait_timeout de MySQL (generalmente 300s)
    #        'pool_pre_ping': True,  # Verifica conexiones antes de usarlas
    #        'max_overflow': 2
    #}



    # ✅ AHORA SÍ: crear la base de datos una vez que db ya está registrado con app
    configure_database(app)

    @app.errorhandler(OperationalError)
    def handle_db_errors(e):
        db.session.rollback()
        flash('Error temporal con la base de datos. Por favor intente nuevamente.', 'error')
        return redirect(url_for('main.index'))
    
    
    
    
    # Configurar logs
    #handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    #handler.setLevel(logging.INFO)
    #app.logger.addHandler(handler)


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
    """Configuración segura con verificación de archivo y manejo de errores"""
    
    with app.app_context():
        try:
            # Solo para SQLite: Verificar y crear directorio instance/
            if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
                db_path = Path(app.instance_path) / 'local_database.db'
                db_path.parent.mkdir(exist_ok=True, parents=True)
                
                if not db_path.exists():
                    open(db_path, 'a').close()  # Crear archivo vacío
                    app.logger.info(f"Archivo SQLite creado en {db_path}")

            # Crear tablas con manejo de errores
            db.create_all()
            app.logger.info("Tablas creadas exitosamente")
            
        except Exception as e:
            app.logger.error(f"Error crítico en DB: {str(e)}")
            # Crear archivo manualmente si es SQLite y no existe
            if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
                db_path = Path(app.instance_path) / 'local_database.db'
                try:
                    db_path.touch(exist_ok=True)
                    db.create_all()
                except Exception as create_error:
                    app.logger.error(f"Fallo al crear archivo SQLite: {create_error}")
            raise
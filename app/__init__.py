

from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_talisman import Talisman

from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
import secrets
import logging
from logging.handlers import RotatingFileHandler

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
csrf = CSRFProtect()

# Redirección por defecto para usuarios no autenticados
login_manager.login_view = 'main.iniciodesesion'
def create_app():
    load_dotenv()
    print("🔍 DATABASE_URL:", os.getenv("DATABASE_URL"))
 
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

 # Configuración base
    raw_db_uri = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_uri
    
    
 
     # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)


     # ✅ Importar el modelo User correctamente desde models/user.py
    from app.models.user import User
 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
 
  # Registrar blueprints
    from app.routes import main_bp
    from app.Registro import auth_bp  # Si tienes este blueprint también
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
 
     # Crear tablas si no existen

    with app.app_context():
        db.create_all()

    return app
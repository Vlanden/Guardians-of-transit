from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

# Redirección por defecto para usuarios no autenticados
login_manager.login_view = 'main.iniciodesesion'

def create_app():
    # Cargar variables de entorno
    load_dotenv()
    print("🔍 DATABASE_URL:", os.getenv("DATABASE_URL"))

    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

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
        
    print(raw_db_uri)

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
    from app.auth import auth_bp  # Si tienes este blueprint también
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app

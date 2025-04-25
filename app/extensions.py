# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from sqlalchemy.exc import DisconnectionError, OperationalError


# Declarar las extensiones sin inicializarlas globalmente
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
talisman = Talisman()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="fixed-window",
    headers_enabled=True
)

def configure_db_engine(app):
    """Configura el motor de la base de datos con manejo de reconexión"""
    engine = db.engine
    
    # Configuración para manejar reconexiones
    @event.listens_for(engine, "engine_connect")
    def ping_connection(connection, branch):
        if branch:
            return
        
        try:
            # Ejecuta un ping simple para verificar la conexión
            connection.scalar("SELECT 1")
        except (DisconnectionError, OperationalError):
            # Si falla, fuerza una reconexión
            connection.scalar("SELECT 1")
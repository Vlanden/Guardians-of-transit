import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from sqlalchemy.exc import DisconnectionError, OperationalError
from sqlalchemy import event
from typing import Any
from flask import Flask


# --------------------------------------------------
# Inicialización de extensiones Flask
# --------------------------------------------------

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
csrf = CSRFProtect()


csp = {
        'style-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
        'font-src': ["'self'", "https://cdn.jsdelivr.net"]
    }

csp = {
    'default-src': "'self'",
    'script-src': [
        "'self'",
        "'unsafe-inline'",  # Necesario para montar event listeners
        "https://cdn.jsdelivr.net"  # Si usas recursos externos
    ],
    'img-src': ["'self'", "data:", "https://*"],
    'connect-src': "'self'"
}

talisman = Talisman(
    content_security_policy=csp,
    force_https=True,  # Obligatorio en producción
    force_https_permanent=True,
    strict_transport_security=False  # Ya lo maneja Nginx
)

# Configuración del rate limiter con valores por defecto seguros
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],  # Límites razonables por defecto
    storage_uri="memory://",  # Almacenamiento en memoria para desarrollo
    strategy="fixed-window",  # Estrategia de ventana fija
    headers_enabled=True  # Mostrar headers de límites en respuestas
)

# --------------------------------------------------
# Configuración avanzada de la base de datos
# --------------------------------------------------

def configure_db_engine(app: Flask) -> None:
    """
    Configura el motor de la base de datos con manejo avanzado de conexiones.
    
    Parámetros:
        app (Flask): Instancia de la aplicación Flask
    
    Características:
        - Ping periódico para verificar conexiones activas
        - Reconexión automática en caso de fallos
        - Manejo de errores de conexión
    """
    engine = db.engine
    
    @event.listens_for(engine, "engine_connect")
    def ping_connection(connection: Any, branch: bool) -> None:
        """
        Verifica la conexión a la base de datos y maneja reconexiones.
        
        Args:
            connection: Objeto de conexión SQLAlchemy
            branch: Indica si es una conexión ramificada
        """
        if branch:
            return
        
        try:
            # Verificación simple de conexión
            connection.scalar("SELECT 1")
        except (DisconnectionError, OperationalError) as e:
            app.logger.warning(f"Error de conexión a la base de datos: {str(e)}")
            try:
                # Intentar reconexión
                connection.scalar("SELECT 1")
                app.logger.info("Reconexión a la base de datos exitosa")
            except Exception as recon_error:
                app.logger.error(f"Fallo en reconexión: {str(recon_error)}")
                raise

def configure_extensions(app: Flask) -> None:
    """
    Configura todas las extensiones de la aplicación.
    
    Parámetros:
        app (Flask): Instancia de la aplicación Flask
    """
    # Configuración básica de Flask-Login
    login_manager.login_view = 'auth.login'  # Ruta a la vista de login
    login_manager.session_protection = "strong"  # Protección de sesión
    
    # Configuración de JWT
    jwt.token_location = ['headers']  # Aceptar tokens solo en headers
    
    # Configurar el motor de la base de datos
    configure_db_engine(app)
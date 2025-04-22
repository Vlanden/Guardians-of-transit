# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

# Declarar las extensiones sin inicializarlas globalmente
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
csrf = CSRFProtect()
talisman = Talisman()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="fixed-window",
    headers_enabled=True
)

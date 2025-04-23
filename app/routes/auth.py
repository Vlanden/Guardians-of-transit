from flask import Blueprint
from app.controllers.auth_controller import (login, logout, register, reset_password, new_password)

# Creamos el Blueprint con el nombre 'auth' y prefijo opcional si se necesita.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Definimos las rutas y las funciones asociadas
auth_bp.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['GET'])
auth_bp.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
auth_bp.add_url_rule('/reset-password', view_func=reset_password, methods=['GET', 'POST'])  # Para cambiar la contraseña sin token
auth_bp.add_url_rule('/new-password/<token>', view_func=new_password, methods=['GET', 'POST'])  # Para el flujo basado en token

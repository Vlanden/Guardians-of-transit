from flask import Blueprint
from app.controllers.auth_controller import (login, logout, recover, register, reset_password)

# Creamos el Blueprint con el nombre 'auth' y prefijo opcional si se necesita.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Definimos las rutas y las funciones asociadas
auth_bp.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['GET'])
auth_bp.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
auth_bp.add_url_rule('/recover', view_func=recover, methods=['GET', 'POST'])
auth_bp.add_url_rule('/reset_password', view_func=reset_password, methods=['GET', 'POST'])
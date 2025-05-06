from flask import make_response, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import limiter
from app.services.user_service import UserService
from flask import request, session
from flask_wtf.csrf import generate_csrf

class UserController:
    @staticmethod
    @login_required
    def update_profile():
        """Endpoint para actualizar el perfil"""
        # Regenerar CSRF token para cada solicitud
        csrf_token = generate_csrf()
        
        if request.method == 'POST':
            # Verificar origen de la solicitud
            if not request.referrer or request.host not in request.referrer:
                flash("Solicitud no válida", "error")
                return redirect(url_for('main.perfil'))
            # Extrae y limpia los datos del formulario
            data = {
                'username': request.form.get('username', '').strip(),
                'email': request.form.get('email', '').strip(),
                'current_password': request.form.get('current_password', '').strip(),
                'new_password': request.form.get('new_password', '').strip()
            }

            # Validación mínima: nombre de usuario y email son obligatorios
            if not data['username'] or not data['email']:
                flash("Nombre de usuario y correo son requeridos", 'error')
                return redirect(url_for('main.perfil'))

            # Intenta actualizar el perfil usando el servicio correspondiente
            success, message = UserService.update_user_profile(current_user, data)

            # Muestra mensaje al usuario y redirige al perfil
            flash(message, 'success' if success else 'error')
            return redirect(url_for('main.perfil'))

        # Si no es una solicitud POST, rechaza con error 405
        return make_response('Método no permitido', 405)
    
    #Funcion para perfil
    #def update_table_perfil()
    
    
    
    
    
    #Funcion para intentos
    #def update_table_intentos()


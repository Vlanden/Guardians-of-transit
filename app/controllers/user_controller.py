from flask import make_response, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import limiter
from app.services.user_service import UserService

# Controlador para manejar operaciones relacionadas con el usuario
class UserController:
    @staticmethod
    @login_required  # Asegura que el usuario esté autenticado
    @limiter.limit("10 per minute")  # Limita a 10 solicitudes por minuto para evitar abuso
    def save_score():
        """Endpoint para guardar puntuación del usuario actual."""
        if request.method == 'POST':
            # Intenta obtener la puntuación desde el formulario (compatibilidad con 'score' o 'puntuacion')
            score = request.form.get('score') or request.form.get('puntuacion')
            score = score.strip() if score else None  # Elimina espacios en blanco

            # Validación básica: debe existir y ser un número entero
            if not score or not score.isdigit():
                return make_response('Puntuación faltante o inválida', 400)

            # Guarda la puntuación mediante el servicio de usuario
            success, message = UserService.save_user_score(current_user, int(score))
            status = 200 if success else 400  # Código HTTP según resultado
            return make_response(message, status)

        # Si el método HTTP no es POST, rechaza la solicitud
        return make_response('Método no permitido', 405)

    @staticmethod
    @login_required  # Requiere que el usuario esté logueado
    @limiter.limit("3 per minute")  # Limita a 3 solicitudes por minuto
    def update_profile():
        """Endpoint para actualizar el perfil del usuario actual."""
        if request.method == 'POST':
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


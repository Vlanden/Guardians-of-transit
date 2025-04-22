from flask import make_response, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import limiter
from app.services.user_service import UserService

class UserController:
    @staticmethod
    @login_required
    @limiter.limit("10 per minute")
    def save_score():
        """Endpoint para guardar puntuación del usuario actual."""
        if request.method == 'POST':
            score = request.form.get('score') or request.form.get('puntuacion')
            score = score.strip() if score else None

            if not score or not score.isdigit():
                return make_response('Puntuación faltante o inválida', 400)

            success, message = UserService.save_user_score(current_user, int(score))
            status = 200 if success else 400
            return make_response(message, status)

        return make_response('Método no permitido', 405)

    @staticmethod
    @login_required
    @limiter.limit("5 per minute")
    def update_profile():
        """Endpoint para actualizar el perfil del usuario actual."""
        if request.method == 'POST':
            data = {
                'username': request.form.get('username', '').strip(),
                'email': request.form.get('email', '').strip(),
                'current_password': request.form.get('current_password', '').strip(),
                'new_password': request.form.get('new_password', '').strip()
            }

            # Validación simple
            if not data['username'] or not data['email']:
                flash("Nombre de usuario y correo son requeridos", 'error')
                return redirect(url_for('main.perfil'))

            success, message = UserService.update_user_profile(current_user, data)
            flash(message, 'success' if success else 'error')
            return redirect(url_for('main.perfil'))

        return make_response('Método no permitido', 405)

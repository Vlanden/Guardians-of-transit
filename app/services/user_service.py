from app import db
from app.models.user import User
from typing import Tuple

class UserService:
    @staticmethod
    def save_user_score(user: User, score: str) -> Tuple[bool, str]:
        """Guarda la puntuación del usuario."""
        try:
            # Validar si score es un número entero antes de asignarlo
            score = int(score)
            if score < 0:
                return False, "La puntuación no puede ser negativa"
            
            user.score = score
            db.session.commit()
            return True, "Puntuación guardada correctamente"
        except ValueError:
            return False, "La puntuación debe ser un número válido"
        except Exception as e:
            db.session.rollback()
            return False, f"Error guardando puntuación: {str(e)}"

    @staticmethod
    def update_user_profile(user: User, data: dict) -> Tuple[bool, str]:
        """Actualiza el perfil del usuario."""
        try:
            # Validar que se incluyan los campos requeridos
            if not data.get('username') or not data.get('email'):
                return False, "Nombre de usuario y correo electrónico son requeridos"
            
            # Validar que la contraseña actual sea correcta
            if not user.check_password(data.get('current_password', '')):
                return False, "Contraseña actual incorrecta"

            # Actualizar los datos del usuario
            user.username = data['username']
            user.email = data['email']

            # Verificar si hay una nueva contraseña
            new_pw = data.get('new_password', '')
            if new_pw:
                if len(new_pw) < 8:
                    return False, "La nueva contraseña debe tener al menos 8 caracteres"
                if not any(c.isupper() for c in new_pw) or not any(c.isdigit() for c in new_pw):
                    return False, "La contraseña debe contener al menos una mayúscula y un número"
                user.set_password(new_pw)

            db.session.commit()
            return True, "Perfil actualizado correctamente"
        except Exception as e:
            db.session.rollback()
            return False, f"Error actualizando perfil: {str(e)}"

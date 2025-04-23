from app import db
from app.models.user import User
from typing import Tuple
import logging

# Configuración del logger para capturar los errores
logger = logging.getLogger(__name__)

class UserService:
    
    @staticmethod
    def save_user_score(user: User, score: str) -> Tuple[bool, str]:
        """Guarda la puntuación del usuario en la base de datos.

        Args:
            user (User): Objeto del usuario.
            score (str): Puntuación a guardar.

        Returns:
            Tuple[bool, str]: Resultado de la operación y mensaje.
        """
        try:
            # Validar si score es un número entero antes de asignarlo
            if not score.isdigit():
                return False, "La puntuación debe ser un número válido"
            
            score = int(score)

            if score < 0:
                return False, "La puntuación no puede ser negativa"
            
            user.score = score
            db.session.commit()  # Guardar la puntuación en la base de datos
            return True, "Puntuación guardada correctamente"
        
        except ValueError:
            return False, "La puntuación debe ser un número válido"
        
        except Exception as e:
            db.session.rollback()  # Deshacer los cambios si ocurre un error
            logger.error(f"Error al guardar la puntuación para el usuario {user.id}: {str(e)}")
            return False, f"Error guardando puntuación: {str(e)}"

    @staticmethod
    def update_user_profile(user: User, data: dict) -> Tuple[bool, str]:
        """Actualiza el perfil del usuario.

        Args:
            user (User): Objeto del usuario.
            data (dict): Diccionario con los nuevos datos del perfil.

        Returns:
            Tuple[bool, str]: Resultado de la operación y mensaje.
        """
        try:
            # Validar que se incluyan los campos requeridos
            username = data.get('username', '')
            email = data.get('email', '')

            if not username or not email:
                return False, "Nombre de usuario y correo electrónico son requeridos"
            
            # Validar que la contraseña actual sea correcta
            current_password = data.get('current_password', '')
            if not user.check_password(current_password):
                return False, "Contraseña actual incorrecta"

            # Actualizar los datos del usuario
            user.username = username
            user.email = email

            # Verificar si hay una nueva contraseña
            new_pw = data.get('new_password', '')
            if new_pw:
                if len(new_pw) < 8:
                    return False, "La nueva contraseña debe tener al menos 8 caracteres"
                if not any(c.isupper() for c in new_pw) or not any(c.isdigit() for c in new_pw):
                    return False, "La contraseña debe contener al menos una mayúscula y un número"
                
                user.set_password(new_pw)  # Guardar la nueva contraseña

            db.session.commit()  # Guardar cambios en la base de datos
            return True, "Perfil actualizado correctamente"
        
        except Exception as e:
            db.session.rollback()  # Deshacer los cambios si ocurre un error
            logger.error(f"Error al actualizar el perfil del usuario {user.id}: {str(e)}")
            return False, f"Error actualizando perfil: {str(e)}"

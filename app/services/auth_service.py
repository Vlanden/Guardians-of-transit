import os
import re
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from flask import url_for
from app import db

def is_valid_email(email: str) -> bool:
    """Valida el formato del correo electrónico."""
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email))

def is_valid_username(username: str) -> bool:
    """Valida que el nombre de usuario tenga entre 3 y 20 caracteres alfanuméricos o guiones bajos."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_strong_password(password: str) -> bool:
    """Valida que la contraseña sea fuerte: mínimo 8 caracteres, al menos 1 mayúscula y 1 número."""
    return (
        len(password) >= 8 and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password)
    )








def send_reset_email(user) -> bool:
    """Envía un correo de restablecimiento de contraseña al usuario."""
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.token_expiration = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    link = url_for('auth.reset_password', token=token, _external=True)
    body = f"""Hola {user.username},

Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para continuar:

{link}

Este enlace expirará en 1 hora. Si no solicitaste esto, puedes ignorar este mensaje.

Atentamente,
Guardianes de la Vía
"""

    msg = MIMEText(body)
    msg['Subject'] = 'Restablecimiento de contraseña'
    msg['From'] = os.getenv('MAIL_USERNAME', 'no-reply@guardianesdelavia.com')
    msg['To'] = user.email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(
                os.getenv('MAIL_USERNAME'),
                os.getenv('MAIL_PASSWORD')
            )
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[ERROR] Fallo al enviar el correo de recuperación: {e}")
        return False

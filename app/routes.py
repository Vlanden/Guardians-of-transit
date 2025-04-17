from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

# Creamos el blueprint principal
main_bp = Blueprint('main', __name__)

# Página pública de bienvenida
@main_bp.route('/')
def inicio():
    return render_template('Inicio.html')

# Página de inicio de sesión
@main_bp.route('/iniciar-sesion')
def iniciodesesion():
    return render_template('InicioDeSesion.html')

# Página de registro
@main_bp.route('/registro')
def registro():
    return render_template('Registro.html')

# Página de recuperación de contraseña
@main_bp.route('/recuperacion', methods=['GET', 'POST'])
def recuperacion():
    if request.method == 'POST':
        email = request.form.get('email')
        # Aquí puedes implementar el envío de correo de recuperación
        flash('Si el correo existe, se han enviado las instrucciones para recuperar la contraseña.', 'info')
        return redirect(url_for('main.iniciodesesion'))
    return render_template('Recuperacion.html')

# Página protegida - solo si el usuario está autenticado
@main_bp.route('/index')
@login_required
def index():
    return render_template('Index.html', user=current_user)

# Perfil del usuario
@main_bp.route('/perfil')
@login_required
def perfil():
    return render_template('Perfil.html', user=current_user)

# Términos y Condiciones
@main_bp.route('/terminos')
def terminos():
    return render_template('terminos.html')

# Políticas de Privacidad
@main_bp.route('/privacidad')
def privacidad():
    return render_template('politicas.html')

from flask import Flask
from flask_jwt_extended import JWTManager
from auth import auth_bp  # Importa el Blueprint de autenticación

app = Flask(__name__)

# Configuración JWT
app.config['JWT_SECRET_KEY'] = 'clave_super_secreta'
jwt = JWTManager(app)

# Registra los Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

# Mantén tu ruta principal si es necesaria
@app.route('/')
def home():
    return render_template('Inicio.html')

if __name__ == '__main__':
    app.run(debug=True)
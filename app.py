from flask import Flask
from config.config import Config
from auth.auth import auth_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Registrar el blueprint de autenticación
app.register_blueprint(auth_blueprint)

@app.route('/')
def index():
    return "Bienvenidos a Guardianes de la Vía"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

# app/main.py
from app import app

@app.route('/')
def index():
    return "¡Hola, Guardianes del Vía!"

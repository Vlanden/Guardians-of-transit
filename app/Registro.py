from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db, jwt
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='templates')

#funcion de validacion:
#valida que el largo del username y la contraseña sea mayor a 8
#Que el usuario no exista en la bd(libera posibles inyecciones sql)
#Que las contraseñas coincidan
def validacion(username, password, password1):

    passwordhash = generate_password_hash(password)

    if len(username) >= 8 and len(password) >= 8:
        db.execute("SELECT * FROM usuarios Where username = %s", (username))
        if db.fetchone() == None:
            if check_password_hash(passwordhash, password1):

                return [passwordhash]
            else:
                 print("Las contraseñas no coinciden")
        else:
             print("Ese usuario ya existe")
    else:
        print("El usuario y la contraseña deben tener al menos 8 caracteres")


def inyeccion(username, email, hash):

    try:
        db.execute("INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)", 
                   (username, email, hash))
        db.connection.commit()

        print("Usuario registrado correctamente")

    except Exception as e:
        print(f"Error al insertar: {e}")
     
    
     
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registrar():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["pass"]
        password1 = request.form["pass1"]

    hash = validacion(username, password, password1)

    if hash:
        inyeccion(username, email, hash)
        

    print(request.form)

    return render_template("InicioDeSesion.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("Si")

    return render_template("politicas.html")
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db, jwt
import bcrypt
from flask_login import login_user


auth_bp = Blueprint('auth', __name__, template_folder='templates')



#funcion de validacion:
#valida que el largo del username y la contraseña sea mayor a 8
#Que el usuario no exista en la bd(libera posibles inyecciones sql)
#Que las contraseñas coincidan
def validacion_registro(username, email, password, password1):

    if len(username) < 8 and len(password) < 8:
        return "El usuario y la contraseña deben tener al menos 8 caracteres"
           
    if password != password1:
        #Hacer aviso al usuario
        return "Las contraseñas no coinciden"

    if User.query.filter_by(username=username).first():
        return "Ese usuario ya existe"
    
    if User.query.filter_by(email=email).first():
        return "Ese email ya está registrado"
    
    return None
        
def inyeccion(username, email, password):

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

     
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registrar():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password1 = request.form["confirm_password"]

        val = validacion_registro(username, email, password, password1)
        if val:
            #Generar mensaje de error
            print(val)
            return render_template("Registro.html")
        
        inyeccion(username, email, password)
    
    else: 
        print("Hay un error con el formulario")
        render_template("Registro.html")

    return render_template("InicioDeSesion.html")








def validar_login(username, password):

    user = User.query.filter_by(username=username).first()

    if user:
        if user.check_password(password):
            login_user(user)
            return redirect(url_for("main.terminos"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    else:
        flash("El usuario no esta registrado")



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        validar_login(username, password)

    return render_template("/auth/log-in.html")
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db, jwt
import bcrypt


from flask_login import UserMixin
from . import login_manager  # 👈 importa login_manager desde __init__.py

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    return render_template('InicioDeSesion.html')

#@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Usuario ya existe"}), 400
            
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "Usuario registrado"}), 201
    
    return render_template('Registro.html')

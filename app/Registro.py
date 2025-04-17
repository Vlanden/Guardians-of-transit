from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db, jwt
import bcrypt


def registro():
    return render_template("/templates/Registro.html")
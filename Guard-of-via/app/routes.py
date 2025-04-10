from flask import Blueprint, render_template, request, redirect, url_for
from . import mysql

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Aquí se podría procesar respuestas
        return redirect(url_for('main.rewards'))
    return render_template('quiz.html')

@main.route('/game')
def game():
    return render_template('game.html')

@main.route('/rewards')
def rewards():
    return render_template('rewards.html')

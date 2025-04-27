from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.quiz_forms import QuizForm, PreguntaForm
from app.models.user import juegos_quiz, QuizPregunta
from app import db
from werkzeug.utils import secure_filename
import os
from app.config import Config

quiz_admin = Blueprint('quiz_admin', __name__, url_prefix='/admin/quizzes')

@quiz_admin.route('/', methods=['GET'])
@login_required
def listar_quizzes():
    quizzes = juegos_quiz.query.all()
    return render_template('admin/listar_quizzes.html', quizzes=quizzes)

@quiz_admin.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        try:
            # Guardar imagen si se proporcionó
            imagen_path = None
            if form.imagen.data:
                filename = secure_filename(form.imagen.data.filename)
                imagen_path = os.path.join('quizzes', filename)
                form.imagen.data.save(os.path.join(Config.UPLOAD_FOLDER, imagen_path))
            
            # Crear nuevo quiz
            nuevo_quiz = juegos_quiz(
                titulo=form.titulo.data,
                descripcion=form.descripcion.data,
                img_referencia=imagen_path or 'default.jpg'
            )
            
            db.session.add(nuevo_quiz)
            db.session.commit()
            
            flash('Quiz creado exitosamente!', 'success')
            return redirect(url_for('quiz_admin.listar_quizzes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear quiz: {str(e)}', 'danger')
    
    return render_template('admin/crear_quiz.html', form=form)

@quiz_admin.route('/<int:quiz_id>/preguntas/agregar', methods=['GET', 'POST'])
@login_required
def agregar_pregunta(quiz_id):
    form = PreguntaForm()
    quiz = juegos_quiz.query.get_or_404(quiz_id)
    
    if form.validate_on_submit():
        try:
            nueva_pregunta = QuizPregunta(
                id_quiz=quiz_id,
                q_pregunta=form.pregunta.data,
                opcioncorrecta=form.opcion_correcta.data,
                opcion2=form.opcion2.data,
                opcion3=form.opcion3.data or None,
                opcion4=form.opcion4.data or None,
                explicacion=form.explicacion.data or None,
                orden=form.orden.data
            )
            
            db.session.add(nueva_pregunta)
            db.session.commit()
            
            flash('Pregunta agregada exitosamente!', 'success')
            return redirect(url_for('quiz_admin.agregar_pregunta', quiz_id=quiz_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar pregunta: {str(e)}', 'danger')
    
    return render_template('admin/agregar_pregunta.html', form=form, quiz=quiz)

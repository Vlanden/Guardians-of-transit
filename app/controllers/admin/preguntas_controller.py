from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed

class QuizForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    imagen = FileField('Imagen del Quiz', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Solo imágenes JPG/PNG')
    ])

class PreguntaForm(FlaskForm):
    pregunta = StringField('Texto de la pregunta', validators=[DataRequired()])
    opcion_correcta = StringField('Opción correcta', validators=[DataRequired()])
    opcion2 = StringField('Opción 2', validators=[DataRequired()])
    opcion3 = StringField('Opción 3', validators=[Optional()])
    opcion4 = StringField('Opción 4', validators=[Optional()])
    explicacion = TextAreaField('Explicación', validators=[Optional()])
    orden = IntegerField('Orden de la pregunta', validators=[DataRequired()])


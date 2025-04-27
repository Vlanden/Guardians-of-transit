from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField, validators
from flask_wtf.file import FileAllowed, FileRequired

class QuizForm(FlaskForm):
    titulo = StringField('Título del Quiz', validators=[
        validators.DataRequired(message="El título es obligatorio"),
        validators.Length(min=3, max=255, message="El título debe tener entre 3 y 255 caracteres")
    ])
    
    descripcion = TextAreaField('Descripción', validators=[
        validators.DataRequired(message="La descripción es obligatoria"),
        validators.Length(min=10, max=500, message="La descripción debe tener entre 10 y 500 caracteres")
    ])
    
    imagen = FileField('Imagen del Quiz', validators=[
        FileRequired(message="Se requiere una imagen"),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes JPG, JPEG o PNG')
    ])

class PreguntaForm(FlaskForm):
    pregunta = TextAreaField('Texto de la pregunta', validators=[
        validators.DataRequired(message="El texto de la pregunta es obligatorio"),
        validators.Length(min=10, max=500, message="La pregunta debe tener entre 10 y 500 caracteres")
    ])
    
    opcioncorrecta = StringField('Opción Correcta', validators=[
        validators.DataRequired(message="Esta opción es obligatoria"),
        validators.Length(min=1, max=200, message="Máximo 200 caracteres")
    ])
    
    opcion2 = StringField('Opción 2', validators=[
        validators.DataRequired(message="Esta opción es obligatoria"),
        validators.Length(min=1, max=200, message="Máximo 200 caracteres")
    ])
    
    opcion3 = StringField('Opción 3', validators=[
        validators.DataRequired(message="Esta opción es obligatoria"),
        validators.Length(min=1, max=200, message="Máximo 200 caracteres")
    ])
    
    opcion4 = StringField('Opción 4', validators=[
        validators.DataRequired(message="Esta opción es obligatoria"),
        validators.Length(min=1, max=200, message="Máximo 200 caracteres")
    ])
    
    explicacion = TextAreaField('Explicación', validators=[
        validators.DataRequired(message="La explicación es obligatoria"),
        validators.Length(min=10, max=500, message="La explicación debe tener entre 10 y 500 caracteres")
    ])

    def validate(self, extra_validators=None):
        # Validación inicial
        if not super().validate():
            return False

        # Validar que todas las opciones sean únicas
        opciones = [
            self.opcioncorrecta.data.strip().lower(),
            self.opcion2.data.strip().lower(),
            self.opcion3.data.strip().lower(),
            self.opcion4.data.strip().lower()
        ]
        
        if len(set(opciones)) < 4:
            self.opcioncorrecta.errors.append('Todas las opciones deben ser diferentes')
            return False

        # Validar que la opción correcta no sea igual a las demás
        correcta = opciones[0]
        for opcion in opciones[1:]:
            if correcta == opcion:
                self.opcioncorrecta.errors.append('La opción correcta no puede coincidir con otras opciones')
                return False

        return True
import click
from app import create_app, db
from app.models.user import User

@click.command('create-admin')
def create_admin():
    """Crear un usuario administrador"""
    username = input("Nombre de usuario: ")
    email = input("Email: ")
    password = getpass.getpass("Contraseña: ")
    
    admin = User(
        username=username,
        email=email,
        is_admin=True
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    print("Administrador creado exitosamente!")

# En tu aplicación Flask (__init__.py o similar):
app.cli.add_command(create_admin)
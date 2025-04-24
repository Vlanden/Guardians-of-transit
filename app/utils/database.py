import os
from app import db


#Esta funcion solo funciona en la db local
def ensure_db_exists(app):
    """Asegura que el archivo de base de datos existe y tiene permisos adecuados."""
    db_path = os.path.join(app.instance_path, 'app.db')
    
    try:
        # Asegurarse de que el directorio de la base de datos exista
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path, exist_ok=True)

        # Si el archivo de la base de datos no existe, lo creamos
        if not os.path.exists(db_path):
            with open(db_path, 'w'):  # Abrir con 'with' asegura que el archivo se cierre adecuadamente
                pass  # Solo necesitamos crear el archivo vacío

            # Establecer permisos adecuados (aquí usaremos 0o644, más restrictivo)
            os.chmod(db_path, 0o644)

    except Exception as e:
        app.logger.error(f"No se pudo crear el archivo de BD: {str(e)}")
        raise  # Re-lanzar la excepción después de loguearla

from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

@contextmanager
def session_scope():
    """Proporciona un ámbito transaccional seguro"""
    session = db.session
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()
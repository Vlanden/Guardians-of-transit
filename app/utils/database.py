import os
from time import sleep
from contextlib import contextmanager
from typing import Callable, Any, TypeVar, Generator
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session
from flask import Flask
import logging
from run import app
from app.extensions import db

T = TypeVar('T')

def ensure_db_exists(app: Flask) -> None:
    """
    Asegura que el archivo de base de datos SQLite existe y tiene los permisos adecuados.
    
    Args:
        app: Instancia de la aplicación Flask
        
    Raises:
        OSError: Si no se pueden crear los directorios o archivos necesarios
        Exception: Para otros errores inesperados
    """
    db_path = os.path.join(app.instance_path, 'app.db')
    
    try:
        # Crear directorio instance si no existe
        os.makedirs(app.instance_path, exist_ok=True)
        app.logger.debug(f"Directorio de instancia verificado: {app.instance_path}")

        # Crear archivo de base de datos si no existe
        if not os.path.exists(db_path):
            with open(db_path, 'w'):
                pass
            os.chmod(db_path, 0o644)  # rw-r--r--
            app.logger.info(f"Archivo de base de datos creado: {db_path}")

        # Verificar permisos
        if oct(os.stat(db_path).st_mode & 0o777) != '0o644':
            os.chmod(db_path, 0o644)
            app.logger.warning(f"Permisos ajustados para: {db_path}")

    except OSError as e:
        app.logger.error(f"Error del sistema al configurar BD: {str(e)}")
        raise
    except Exception as e:
        app.logger.critical(f"Error inesperado al configurar BD: {str(e)}")
        raise

@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Proporciona un ámbito transaccional seguro para operaciones con la base de datos.
    
    Uso:
        with session_scope() as session:
            # operaciones con la sesión
            
    Yields:
        Session: Sesión de SQLAlchemy
        
    Raises:
        SQLAlchemyError: Si ocurre algún error durante la transacción
    """
    session = db.session
    try:
        yield session
        session.commit()
        app.logger.debug("Transacción completada exitosamente")
    except SQLAlchemyError as e:
        session.rollback()
        app.logger.error(f"Error en transacción: {str(e)} - Realizando rollback")
        raise
    finally:
        session.close()

def safe_db_operation(func: Callable[[], T], max_retries: int = 3) -> T:
    """
    Ejecuta operaciones de base de datos con reintentos automáticos para errores transitorios.
    
    Args:
        func: Función que realiza la operación de base de datos
        max_retries: Número máximo de reintentos (default: 3)
        
    Returns:
        El resultado de la función si es exitosa
        
    Raises:
        OperationalError: Si persisten los errores después de los reintentos
        SQLAlchemyError: Para otros errores de base de datos
    """
    for attempt in range(max_retries):
        try:
            result = func()
            if attempt > 0:
                app.logger.info(f"Operación exitosa después de {attempt} reintentos")
            return result
        except OperationalError as e:
            if "2006" in str(e):  # MySQL server has gone away
                wait_time = 0.5 * (attempt + 1)
                app.logger.warning(
                    f"Error de conexión (intento {attempt + 1}/{max_retries}). "
                    f"Reintentando en {wait_time} segundos..."
                )
                db.session.rollback()
                sleep(wait_time)
                continue
            app.logger.error(f"Error operacional no recuperable: {str(e)}")
            raise
        except SQLAlchemyError as e:
            app.logger.error(f"Error de base de datos: {str(e)}")
            raise

    raise OperationalError("No se pudo completar la operación después de los reintentos", {}, None)
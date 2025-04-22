import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    """Configura el sistema de logging de la aplicación."""
    # Configuración de la carpeta de logs
    log_folder = os.path.join(app.instance_path, app.config['LOG_FOLDER'])
    
    # Asegurarse de que el directorio de logs exista y tenga permisos adecuados
    try:
        os.makedirs(log_folder, exist_ok=True)
        # Aseguramos que los permisos sean correctos
        os.chmod(log_folder, 0o755)
    except Exception as e:
        app.logger.error(f"Error al crear el directorio de logs: {str(e)}")
        raise  # Re-lanzar la excepción si falla la creación del directorio

    # Configuración del archivo de logs
    log_file = os.path.join(log_folder, app.config['LOG_FILE'])
    
    # Crear un handler de archivos rotativos
    handler = RotatingFileHandler(
        log_file,
        maxBytes=app.config['LOG_MAX_BYTES'],
        backupCount=app.config['LOG_BACKUP_COUNT']
    )
    
    # Establecer el nivel de logging según la configuración
    log_level = app.config.get('LOG_LEVEL', logging.INFO)  # Por defecto es INFO
    handler.setLevel(log_level)
    
    # Añadir el handler al logger de la aplicación
    app.logger.addHandler(handler)
    
    # Opción para también configurar el logger principal si se necesita más configuración
    logging.basicConfig(level=log_level)


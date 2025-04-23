import os
import sys
import subprocess
import platform

def get_venv_python():
    """Retorna la ruta del ejecutable Python dentro del entorno virtual."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

VENV_PATH = os.path.join(os.path.dirname(__file__), 'venv')  # Ruta del entorno virtual
PYTHON_BIN = get_venv_python()

def is_using_virtualenv():
    """Verifica si el entorno actual está usando el entorno virtual."""
    return os.path.commonpath([sys.prefix, VENV_PATH]) == VENV_PATH

def create_virtualenv():
    """Crea un entorno virtual si no existe."""
    print("Entorno virtual no encontrado. Creando entorno virtual...")
    subprocess.check_call([sys.executable, '-m', 'venv', VENV_PATH])

def install_requirements():
    """Instala las dependencias desde requirements.txt."""
    print("Instalando dependencias desde requirements.txt...")
    pip_executable = os.path.join(VENV_PATH, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(VENV_PATH, 'bin', 'pip')
    subprocess.check_call([pip_executable, 'install', '-r', 'requirements.txt'])

if __name__ == "__main__":
    if not is_using_virtualenv():
        if not os.path.exists(VENV_PATH):
            create_virtualenv()

        # Activar el entorno virtual en Windows
        if os.name == 'nt':
            activate_script = os.path.join(VENV_PATH, 'Scripts', 'activate_this.py')
        else:  # Linux/MacOS
            activate_script = os.path.join(VENV_PATH, 'bin', 'activate_this.py')

        if os.path.exists(activate_script):
            exec(open(activate_script).read(), dict(__file__=activate_script))
        else:
            print(f"No se pudo encontrar el script de activación en {activate_script}. Asegúrate de que el entorno virtual esté correctamente creado, o que sea el sistema operativo correcto.")
    
    print("Entorno virtual activo. Instalando dependencias...")
    try:
        install_requirements()
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias: {e}")
        sys.exit(1)

    # Ahora que estamos dentro del entorno virtual, puedes ejecutar la aplicación Flask
    from app import create_app
    app = create_app()
    app.run(debug=True)
    #app.run(debug=True, host="0.0.0.0", port=5000)

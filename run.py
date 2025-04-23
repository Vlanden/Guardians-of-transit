import os
import sys
import subprocess
import platform

def get_venv_python():
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

VENV_PATH = os.path.abspath("venv")
PYTHON_BIN = get_venv_python()

def is_using_virtualenv():
    return os.path.commonpath([sys.prefix, VENV_PATH]) == VENV_PATH

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    if not is_using_virtualenv():
        print(f"Reiniciando desde el entorno virtual: {PYTHON_BIN}")
        subprocess.check_call([PYTHON_BIN, __file__])
        sys.exit(0)

    print("Entorno virtual activo. Instalando dependencias...")
    try:
        install_requirements()
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias: {e}")
        sys.exit(1)

    from app import create_app
    app = create_app()
    app.run()

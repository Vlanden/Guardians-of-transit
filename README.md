# Guardianes de la Vía

Aplicación web construida con Flask. Lista para desplegar en local o en un VPS con Gunicorn.

## Ejecutar localmente

```bash
pip install -r requirements.txt
python run.py
```
```bash
Con un ambiente 
python run_env.py
```

## Desplegar en VPS con Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```
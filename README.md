# Guardianes de la Vía

Aplicación web construida con Flask. Lista para desplegar en local o en un VPS con Gunicorn.

## Ejecutar localmente

```bash
python run.py
```

## Desplegar en VPS con Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```
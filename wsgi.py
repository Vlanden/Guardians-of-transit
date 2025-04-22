from app import create_app

app = create_app()

if __name__ == "__main__":
    # Configura el host y puerto para que la aplicación sea accesible desde cualquier lugar
    # y habilita el modo debug solo en desarrollo.
    app.run(debug=True, host="0.0.0.0", port=5000)

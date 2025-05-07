from app import create_app

app = create_app()

if __name__ == "__main__":
    # Configura el host y puerto para que la aplicación sea accesible desde cualquier lugar
    # y habilita el modo debug solo en desarrollo.
    app.run(debug=True, ssl_context='adhoc')
    #el de abajo es un intento para usar el dominio con una pc en local
    # app.run(debug=True, ssl_context=('superiorteam.site.pem', 'superiorteam.site-key.pem'), host="0.0.0.0", port=5000, ssl_context='adhoc')

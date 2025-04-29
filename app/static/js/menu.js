const estadosCarrusel = {};

document.addEventListener('DOMContentLoaded', function() {
    // 1. Función para mostrar el juego activo
    const mostrarJuego = (prefix, index) => {
        const contenedor = document.querySelector(`[data-carrusel="${prefix}"]`);
        if (!contenedor) return;

        const tarjetas = contenedor.querySelectorAll('.game-card');
        if (tarjetas.length === 0) return;

        // Ocultar todas las tarjetas
        tarjetas.forEach(card => card.classList.add('d-none'));
        
        // Mostrar tarjeta correspondiente
        const indiceReal = index % tarjetas.length;
        tarjetas[indiceReal].classList.remove('d-none');
        
        // Scroll suave
        tarjetas[indiceReal].scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'start'
        });
        
        // Actualizar estado
        estadosCarrusel[prefix] = indiceReal;
    };

    // 2. Función de navegación
    const cambiarJuego = (prefix, direccion) => {
        const contenedor = document.querySelector(`[data-carrusel="${prefix}"]`);
        if (!contenedor) return;

        const tarjetas = contenedor.querySelectorAll('.game-card');
        if (tarjetas.length === 0) return;

        const currentIndex = estadosCarrusel[prefix] || 0;
        const nuevoIndex = (currentIndex + direccion + tarjetas.length) % tarjetas.length;
        
        mostrarJuego(prefix, nuevoIndex);
    };

    // 3. Configurar Event Listeners
    document.querySelectorAll('.carrusel-prev, .carrusel-next').forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            const prefix = this.dataset.carruselPrefix;
            const direccion = this.classList.contains('carrusel-prev') ? -1 : 1;
            cambiarJuego(prefix, direccion);
        });
    });


    // 4. Inicializar carruseles
    document.querySelectorAll('[data-carrusel]').forEach(contenedor => {
        const prefix = contenedor.dataset.carrusel;
        estadosCarrusel[prefix] = 0;
        mostrarJuego(prefix, 0);
    });
});
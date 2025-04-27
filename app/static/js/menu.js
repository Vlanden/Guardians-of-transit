const estadosCarrusel = {};

document.addEventListener('DOMContentLoaded', function() {
    // Función de búsqueda mejorada
    function buscarJuego() {
        const input = document.getElementById("searchInput").value.trim().toLowerCase();
        const contenedores = document.querySelectorAll('.carrusel-container');

        contenedores.forEach(contenedor => {
            const juegos = contenedor.querySelectorAll('.game-card');
            let resultadosVisibles = 0;

            juegos.forEach(juego => {
                const id = juego.dataset.juegoId.toLowerCase();
                const titulo = juego.dataset.gameTitle.toLowerCase();
                const coincide = id.includes(input) || titulo.includes(input);

                // Modificar solo clases de Bootstrap
                juego.classList.toggle('d-none', !coincide);
                juego.classList.toggle('search-match', coincide);

                if (coincide) resultadosVisibles++;
            });

            // Actualizar visibilidad del contenedor
            const contenedorPadre = contenedor.closest('.mb-5');
            contenedorPadre.style.display = resultadosVisibles > 0 ? 'block' : 'none';
            
            // Reiniciar índice del carrusel
            const prefix = contenedor.querySelector('.game-card').dataset.juegoTipo;
            estadosCarrusel[prefix] = 0;
            mostrarJuego(prefix, 0);
        });
    }
});

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
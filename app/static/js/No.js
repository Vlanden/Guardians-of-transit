const estadosCarrusel = {};

// Función para mostrar el juego activo
function mostrarJuego(prefix, index) {
    const contenedor = document.querySelector(`[data-carrusel="${prefix}"]`);
    if (!contenedor) return;

    const tarjetas = contenedor.querySelectorAll('.game-card');
    if (tarjetas.length === 0) return;

    // Asegurar que el índice esté dentro del rango
    index = (index + tarjetas.length) % tarjetas.length;
    
    // Ocultar todas y mostrar la activa
    tarjetas.forEach((card, i) => {
        card.classList.toggle('d-none', i !== index);
    });

    // Scroll suave
    tarjetas[index].scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
        inline: 'center'
    });
    
    // Actualizar estado
    estadosCarrusel[prefix] = index;
}

// Función para navegación
function cambiarJuego(prefix, direccion) {
    const currentIndex = estadosCarrusel[prefix] || 0;
    mostrarJuego(prefix, currentIndex + direccion);
}

// Inicialización de carruseles
function inicializarCarruseles() {
    document.querySelectorAll('[data-carrusel]').forEach(contenedor => {
        const prefix = contenedor.dataset.carrusel;
        estadosCarrusel[prefix] = 0;
        mostrarJuego(prefix, 0);
    });
}

// Delegación de eventos para TODOS los carruseles
document.addEventListener('click', (e) => {
    // Manejar botones de navegación (tanto en popup como en carruseles principales)
    if (e.target.closest('.carrusel-prev, .carrusel-next')) {
        e.preventDefault();
        const boton = e.target.closest('.carrusel-prev, .carrusel-next');
        const prefix = boton.dataset.carruselPrefix;
        const direccion = boton.classList.contains('carrusel-prev') ? -1 : 1;
        cambiarJuego(prefix, direccion);
    }
    
    // Manejar botón de limpiar búsqueda
    if (e.target.closest('#clearSearch')) {
        document.getElementById('searchInput').value = '';
        document.getElementById('searchResultsContent').innerHTML = '';
        document.getElementById('searchResultsPopup').classList.add('d-none');
    }
});


// Búsqueda dinámica
document.getElementById('searchInput')?.addEventListener('input', async function() {
    const term = this.value.trim();
    const popup = document.getElementById('searchResultsPopup');
    
    if (term.length < 2) {
        popup.classList.add('d-none');
        return;
    }

    try {
        const response = await fetch(`/games/buscar?q=${encodeURIComponent(term)}`);
        const { quiz, simulacion, extra } = await response.json();
        
        const contenedor = document.getElementById('searchResultsContent');
        contenedor.innerHTML = '';
        
        // Combinar resultados manteniendo la categoría de origen
        const resultadosCombinados = [
            ...quiz.map(juego => ({ ...juego, tipo: 'quiz' })),
            ...simulacion.map(juego => ({ ...juego, tipo: 'simulacion' })),
            ...extra.map(juego => ({ ...juego, tipo: 'extra' }))
        ];

        if (resultadosCombinados.length > 0) {
            resultadosCombinados.forEach(juego => {
                const card = document.createElement('div');
                card.className = 'game-card card mx-2';
                card.innerHTML = `
                    <div class="card h-100">
                        <img src="/static/images/${juego.img_referencia}" 
                             class="card-img-top" 
                             alt="${juego.titulo}"
                             style="height: 150px; object-fit: cover;"
                             onerror="this.src='/static/images/default-game.jpg'">
                        <div class="card-body">
                            <span class="badge bg-${juego.tipo === 'quiz' ? 'primary' : juego.tipo === 'simulacion' ? 'success' : 'warning'} mb-2">
                                ${juego.tipo.toUpperCase()}
                            </span>
                            <h5 class="card-title">${juego.titulo}</h5>
                            <p class="card-text small text-muted">${juego.descripcion}</p>
                            <a href="/juego/${juego.id_quiz || juego.id_sim || juego.id_extra}" 
                               class="btn btn-sm btn-primary">
                               Jugar
                            </a>
                        </div>
                    </div>
                `;
                contenedor.appendChild(card);
            });
            popup.classList.remove('d-none');
            mostrarJuego('search', 0);
        } else {
            contenedor.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-search fs-1 text-muted"></i>
                    <p class="mt-2">No se encontraron resultados</p>
                </div>
            `;
            popup.classList.remove('d-none');
        }
    } catch (error) {
        console.error('Error en búsqueda:', error);
        document.getElementById('searchResultsContent').innerHTML = `
            <div class="alert alert-danger">Error al cargar resultados</div>
        `;
    }
});

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    // Iniciar carruseles de categorías
    document.querySelectorAll('[data-carrusel]').forEach(contenedor => {
        const prefix = contenedor.dataset.carrusel;
        if (prefix !== 'search') { // Excluye el carrusel de búsqueda
            estadosCarrusel[prefix] = 0;
            mostrarJuego(prefix, 0);
        }
    });
});
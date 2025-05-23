// Estado global único para todos los carruseles
const estadosCarrusel = {};

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

// Función universal para mostrar juegos
function mostrarJuego(prefix, index) {
    const contenedor = document.querySelector(`[data-carrusel="${prefix}"]`);
    if (!contenedor) return;

    const tarjetas = contenedor.querySelectorAll('.game-card');
    if (tarjetas.length === 0) return;

    // Manejo circular del índice
    index = (index + tarjetas.length) % tarjetas.length;
    
    // Ocultar todas las tarjetas primero
    tarjetas.forEach(card => {
        card.style.display = 'none';
    });
    
    // Mostrar solo la tarjeta actual
    tarjetas[index].style.display = 'block';
    
    // Scroll suave
    tarjetas[index].scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
        inline: 'center'
    });
    
    // Actualizar estado
    estadosCarrusel[prefix] = index;
}

// Navegación unificada
function cambiarJuego(prefix, direccion) {
    const currentIndex = estadosCarrusel[prefix] || 0;
    mostrarJuego(prefix, currentIndex + direccion);
}

// Inicialización mejorada
function inicializarCarruseles() {
    document.querySelectorAll('[data-carrusel]').forEach(contenedor => {
        const prefix = contenedor.dataset.carrusel;
        if (!estadosCarrusel.hasOwnProperty(prefix)) {
            estadosCarrusel[prefix] = 0;
            mostrarJuego(prefix, 0);
        }
    });
}

// Sistema de búsqueda (versión optimizada)
const buscarJuegos = debounce(async function(term) {
    const popup = document.getElementById('searchResultsPopup');
    const contenedor = document.getElementById('searchResultsContent');
    
    if (term.length === 0) {
        popup.classList.add('d-none');
        return;
    }

    try {
        const response = await fetch(`/games/buscar?q=${encodeURIComponent(term)}`);
        const { quiz = [], simulacion = [], extra = [] } = await response.json();
        
        contenedor.innerHTML = '';
        
        const resultados = [...quiz, ...simulacion, ...extra];
        
        if (resultados.length > 0) {
            resultados.forEach(juego => {
                const tipo = juego.id_quiz ? 'quiz' : juego.id_sim ? 'simulacion' : 'extra';
                const card = document.createElement('div');
                card.className = 'game-card card mx-2';
                card.style.display = 'none'; // Ocultar inicialmente
                card.innerHTML = `
                    <div class="card h-100">
                        <img src="/static/images/${juego.img_referencia}" 
                             class="card-img-top" 
                             alt="${juego.titulo}"
                             style="height: 150px; object-fit: cover;"
                             onerror="this.src='/static/images/default-game.jpg'">
                        <div class="card-body">
                            <span class="badge bg-${tipo === 'quiz' ? 'primary' : tipo === 'simulacion' ? 'success' : 'warning'} mb-2">
                                ${tipo.toUpperCase()}
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
        contenedor.innerHTML = `
            <div class="alert alert-danger">Error al cargar resultados</div>
        `;
    }
}, 300);

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    inicializarCarruseles();
    
    // Búsqueda
    document.getElementById('searchInput')?.addEventListener('input', (e) => {
        buscarJuegos(e.target.value.trim());
    });
    
    // Botón limpiar
    document.getElementById('clearSearch')?.addEventListener('click', () => {
        document.getElementById('searchInput').value = '';
        document.getElementById('searchResultsPopup').classList.add('d-none');
    });
    
    // Delegación para todos los botones de carrusel
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-carrusel-prefix]');
        if (btn) {
            e.preventDefault();
            const prefix = btn.dataset.carruselPrefix;
            const direction = btn.classList.contains('carrusel-prev') ? -1 : 1;
            cambiarJuego(prefix, direction);
        }
    });
});
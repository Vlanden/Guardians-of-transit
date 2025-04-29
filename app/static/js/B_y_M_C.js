//Busqueda y Mostrar carruseles
// Estado global único para todos los carruseles
const estadosCarrusel = {};

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}


// Función universal para mostrar juegos
function mostrarJuego(prefix, index) {
    const contenedor = document.querySelector(`[data-carrusel="${prefix}"]`);
    if (!contenedor) return;

    // Seleccionar solo tarjetas visibles para el carrusel de búsqueda
    const selector = prefix === 'search' ? '.game-card:not(.d-none)' : '.game-card';
    const tarjetas = contenedor.querySelectorAll(selector);
    
    if (tarjetas.length === 0) return;

    // Manejo circular del índice
    index = (index + tarjetas.length) % tarjetas.length;
    
    // Ocultar/mostrar tarjetas
    tarjetas.forEach((card, i) => {
        if (prefix === 'search') {
            card.style.display = i === index ? 'block' : 'none';
        } else {
            card.classList.toggle('d-none', i !== index);
        }
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

// Navegación unificada
function cambiarJuego(prefix, direccion) {
    const currentIndex = estadosCarrusel[prefix] || 0;
    mostrarJuego(prefix, currentIndex + direccion);
}

// Inicialización mejorada
function inicializarCarruseles() {
    document.querySelectorAll('[data-carrusel]').forEach(contenedor => {
        const prefix = contenedor.dataset.carrusel;
        estadosCarrusel[prefix] = 0;
        mostrarJuego(prefix, 0);
    });
}

// Sistema de búsqueda (versión optimizada)
async function handleSearch(term) {
    const popup = document.getElementById('searchResultsPopup');
    const contenedor = document.getElementById('searchResultsContent');
    
    // if (term.length < 2) {
    //     popup.classList.add('d-none');
    //     return;
    // }
    
    if (term.length === 0) {
        popup.classList.add('d-none');
        return;
    }

    try {
        const response = await fetch(`/games/buscar?q=${encodeURIComponent(term)}`);
        const { quiz = [], simulacion = [], extra = [] } = await response.json();
        
        contenedor.innerHTML = '';
        
        // Mostrar mensaje especial si no hay término de búsqueda
        if (term.length === 0) {
            contenedor.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-grid fs-1 text-muted"></i>
                    <p class="mt-2">Ingresa un término de búsqueda</p>
                </div>
            `;
            popup.classList.remove('d-none');
            return;
        }
        
        // Resto del código permanece igual...
        const resultados = [...quiz, ...simulacion, ...extra];
        
        if (resultados.length > 0) {
            resultados.forEach(juego => {
                const tipo = juego.id_quiz ? 'quiz' : juego.id_sim ? 'simulacion' : 'extra';
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
}

// Al cargar la página
/*document.addEventListener('DOMContentLoaded', () => {
    inicializarCarruseles();
    handleSearch('');  // Muestra todos los juegos inicialmente
});*/

// Modifica el event listener:
document.getElementById('searchInput')?.addEventListener('input', 
    debounce((e) => handleSearch(e.target.value.trim()), 300));
    inicializarCarruseles();
    
    // Búsqueda
    document.getElementById('searchInput')?.addEventListener('input', (e) => {
        handleSearch(e.target.value.trim());
    });
    
    // Botón limpiar
    document.getElementById('clearSearch')?.addEventListener('click', () => {
        document.getElementById('searchInput').value = '';
        document.getElementById('searchResultsContent').innerHTML = '';
        document.getElementById('searchResultsPopup').classList.add('d-none');
    });
    
    // Delegación para todos los botones de carrusel
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.carrusel-prev, .carrusel-next');
        if (btn) {
            e.preventDefault();
            const prefix = btn.dataset.carruselPrefix;
            const direction = btn.classList.contains('carrusel-prev') ? -1 : 1;
            cambiarJuego(prefix, direction);
        }
    });
});
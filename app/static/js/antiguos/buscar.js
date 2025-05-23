document.addEventListener('DOMContentLoaded', () => {
    const inp = document.getElementById('searchInput'),
          clr = document.getElementById('clearSearch'),
          pop = document.getElementById('searchResultsPopup'),
          cnt = document.getElementById('searchResultsContent');
  

          document.getElementById('searchInput')?.addEventListener('input', async function() {
            const term = this.value.trim();
            const popup = document.getElementById('searchResultsPopup');
            
            if (term.length < 2) {
                popup.classList.add('d-none');
                return;
            }
        
            try {
                const response = await fetch(`/games/buscar?q=${encodeURIComponent(term)}`);
                const data = await response.json();
                
                const contenedor = document.getElementById('searchResultsContent');
                contenedor.innerHTML = '';
                
                // Procesar los datos del JSON correctamente
                if (data.quiz && data.quiz.length > 0) {
                    data.quiz.forEach(juego => {
                        const card = document.createElement('div');
                        card.className = 'game-card card mx-2';
                        card.innerHTML = `
                            <img src="{{ url_for('static', filename='') }}${juego.img_referencia}" 
                                 class="card-img-top" 
                                 alt="${juego.titulo}"
                                 onerror="this.src='{{ url_for('static', filename='images/default-game.jpg') }}'">
                            <div class="card-body">
                                <h5 class="card-title">${juego.titulo}</h5>
                                <p class="card-text small">${juego.descripcion}</p>
                                <a href="/juego/${juego.id_quiz}" class="btn btn-primary btn-sm">Jugar</a>
                            </div>
                        `;
                        contenedor.appendChild(card);
                    });
                    popup.classList.remove('d-none');
                    mostrarJuego('search', 0);
                } else {
                    contenedor.innerHTML = '<p class="text-center py-3">No se encontraron juegos</p>';
                    popup.classList.remove('d-none');
                }
            } catch (error) {
                console.error('Error en búsqueda:', error);
                contenedor.innerHTML = '<p class="text-center py-3 text-danger">Error al buscar</p>';
            }
        });



  
    clr.addEventListener('click', () => {
      inp.value = '';
      cnt.innerHTML = '';
      pop.classList.add('d-none');
      window.estadosCarrusel['search'] = 0;
    });
  });
  


  /*inp.addEventListener('input', function() {
    const term = this.value.trim().toLowerCase();
  
    if (term.length < 1) {
      pop.classList.add('d-none');
      cnt.innerHTML = '';
      return;
    }

    const matches = [];
    document.querySelectorAll('.game-card').forEach(card => {
      const id    = (card.dataset.juegoId   || '').toLowerCase(),
            title = (card.dataset.gameTitle || '').toLowerCase();
      if (id.includes(term) || title.includes(term)) {
        matches.push(card.cloneNode(true));
      }
    });

    // limpiamos resultados anteriores
    cnt.innerHTML = '';

    if (matches.length) {
      // para cada clone: quitamos cualquier d-none heredado,
      // y luego añadimos d-none sólo si NO es el primero
      matches.forEach((clone, i) => {
        clone.classList.remove('d-none');
        if (i > 0) clone.classList.add('d-none');
        cnt.appendChild(clone);
      });

      // reiniciamos índice de carrusel
      window.estadosCarrusel = window.estadosCarrusel || {};
      window.estadosCarrusel['search'] = 0;

      // mostramos el popup
      pop.classList.remove('d-none');
    } else {
      pop.classList.add('d-none');
    }
  });*/
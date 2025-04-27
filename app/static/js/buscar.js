document.addEventListener('DOMContentLoaded', () => {
    const inp = document.getElementById('searchInput'),
          clr = document.getElementById('clearSearch'),
          pop = document.getElementById('searchResultsPopup'),
          cnt = document.getElementById('searchResultsContent');
  
    inp.addEventListener('input', function() {
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
    });
  
    clr.addEventListener('click', () => {
      inp.value = '';
      cnt.innerHTML = '';
      pop.classList.add('d-none');
      window.estadosCarrusel['search'] = 0;
    });
  });
  
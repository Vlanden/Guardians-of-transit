// Función para mezclar array 
function mezclarArray(array) {
  console.log('[DEBUG] Mezclando array de opciones');
  const nuevoArray = [...array];
  for (let i = nuevoArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [nuevoArray[i], nuevoArray[j]] = [nuevoArray[j], nuevoArray[i]];
  }
  console.log('[DEBUG] Opciones mezcladas:', nuevoArray);
  return nuevoArray;
}

// Función para mostrar errores (Mejorada)
function mostrarError(mensaje) {
  console.error('[ERROR]', mensaje);
  const contenedor = document.querySelector('.game-container');
  contenedor.innerHTML = `
      <div class="alert alert-danger">
          <h4>Error</h4>
          <p>${mensaje}</p>
          <a href="/" class="btn btn-secondary">Volver al inicio</a>
      </div>
  `;
}

// Función principal para iniciar el quiz
function iniciarQuiz(datosJuego) {
    // Al iniciar el quiz:
    if (!document.querySelector('meta[name="csrf-token"]')) {
        window.location.reload();
    }
    if (!document.querySelector('meta[name="csrf-token"]')) {
        mostrarError("Sesión inválida. Recarga la página.");
        return;
    }
    // Guardamos la fecha de inicio
    const fechaInicio = new Date().toISOString().slice(0, 19).replace('T', ' ');// Resultado: "2023-10-05 18:25:30" (UTC)  // Mantener formato ISO

  console.log('[DEBUG] Iniciando quiz con datos:', datosJuego);
  
  if (!datosJuego?.preguntas?.length) {
      console.warn('[WARN] Quiz sin preguntas válidas');
      mostrarError("El quiz no contiene preguntas válidas");
      return;
  }

  const elementosDOM = {
      pregunta: document.getElementById("pregunta"),
      respuestas: document.getElementById("respuestas"),
      resultado: document.getElementById("resultado"),
      progreso: document.getElementById("progress"),
      puntuacion: document.getElementById("puntuacion-actual"),
      highScore: document.getElementById("high-score")
  };
  console.log('[DEBUG] Elementos DOM encontrados:', elementosDOM);

  if (!elementosDOM.pregunta || !elementosDOM.respuestas) {
      console.error('[ERROR] Elementos críticos no encontrados');
      mostrarError("Error crítico: Elementos del juego no encontrados");
      return;
  }

  let preguntaActual = 0;
  let puntuacion = 0;
  const preguntas = datosJuego.preguntas;
  const totalPreguntas = preguntas.length;
  console.log(`[DEBUG] Total de preguntas: ${totalPreguntas}`);
 

    // Función para mostrar pregunta con video
    function mostrarPregunta() {
        const pregunta = preguntas[preguntaActual];
        console.log(`Mostrando pregunta ID: ${pregunta.id_pregunta}`);
        
        // Configurar video
        const videoElement = document.getElementById('pregunta-video');
        const videoSource = document.getElementById('video-source');
        const videoPlaceholder = document.getElementById('video-placeholder');
    
        if (pregunta.video_url) {
            videoSource.src = pregunta.video_url;
            videoElement.load();
            
            // Ocultar placeholder y mostrar video
            videoElement.style.display = 'block';
            videoPlaceholder.style.display = 'none';
            
            // Configurar eventos del video
            videoElement.oncanplay = () => {
                videoPlaceholder.innerHTML = '<i class="bi bi-play-circle-fill display-4"></i>';
            };
            videoElement.onerror = () => {
                videoElement.style.display = 'none';
                videoPlaceholder.innerHTML = '<div class="alert alert-warning">Error al cargar video</div>';
                videoPlaceholder.style.display = 'flex';
            };
        } else {
            videoElement.style.display = 'none';
            videoPlaceholder.style.display = 'flex';
            videoPlaceholder.innerHTML = '<i class="bi bi-film display-4"></i><p class="mt-2">No hay video para esta pregunta</p>';
        }
    
        // Mostrar opciones de respuesta
        const opcionesMezcladas = mezclarArray(pregunta.opciones.filter(Boolean));
        elementosDOM.respuestas.innerHTML = '';
        
        opcionesMezcladas.forEach((opcion, index) => {
            const boton = document.createElement("button");
            boton.className = `btn btn-${['primary', 'success', 'warning', 'danger'][index % 4]} respuesta-btn`;
            boton.textContent = opcion;
            boton.onclick = (e) => {
                verificarRespuesta(e, opcion === pregunta.respuesta_correcta, pregunta.explicacion);
                if (pregunta.video_url) {
                    videoElement.play().catch(e => console.error("Error al reproducir:", e));
                }
            };
            elementosDOM.respuestas.appendChild(boton);
        });
    }

    // Event listener para el placeholder del video
    document.getElementById('video-placeholder').addEventListener('click', function() {
        const video = document.getElementById('pregunta-video');
        if (video.style.display !== 'none') {
            video.play().catch(e => console.error("Error al reproducir:", e));
            this.style.display = 'none';
        }
    });








  function verificarRespuesta(evento, esCorrecta, explicacion) {
      console.log(`[DEBUG] Respuesta ${esCorrecta ? 'correcta' : 'incorrecta'}`);
      
      const botones = elementosDOM.respuestas.querySelectorAll("button");
      botones.forEach(boton => {
          boton.disabled = true;
          boton.classList.remove("btn-outline-primary");
      });

      const botonSeleccionado = evento.currentTarget;
      if (esCorrecta) {
          puntuacion += 10;
          elementosDOM.puntuacion.textContent = puntuacion;
          console.log(`[DEBUG] Nueva puntuación: ${puntuacion}`);
          botonSeleccionado.classList.add("btn-success");
      } else {
          botonSeleccionado.classList.add("btn-danger");
          const opcionCorrecta = botones[
              [...botones].findIndex(b => 
                  b.textContent === preguntas[preguntaActual].respuesta_correcta
              )
          ];
          if (opcionCorrecta) {
              console.log('[DEBUG] Mostrando respuesta correcta');
              opcionCorrecta.classList.add("btn-success");
          }
      }

      elementosDOM.resultado.innerHTML = esCorrecta 
          ? `✅ Correcto! +10 puntos<br>${explicacion}`
          : `❌ Incorrecto<br>${explicacion}`;
      elementosDOM.resultado.className = `alert ${esCorrecta ? 'alert-success' : 'alert-danger'} show`;
      // En la función verificarRespuesta:
    elementosDOM.resultado.style.cssText = `
    display: block !important;
    background-color: #212121;
    color: #FFD700;
    padding: 15px;
    border-radius: 4px;
    border-left: 4px solid ${esCorrecta ? '#d4edda' : '#f8d7da'};
    margin-top: 1rem;
    `;
      elementosDOM.resultado.style.display = "block";

      setTimeout(() => {
          preguntaActual++;
          elementosDOM.resultado.style.display = "none";
          mostrarPregunta();
      }, 2000);
  }

  async function finalizarQuiz() {
    if (!document.querySelector('meta[name="csrf-token"]')) {
        window.location.reload();  // Forzar recarga si falta CSRF
        return;
    }
      const puntuacionFinal = Math.round((puntuacion / (totalPreguntas * 10)) * 100);
      const fechaFin = new Date().toISOString().slice(0, 19).replace('T', ' ');
      console.log(`[DEBUG] Puntuación final calculada: ${puntuacionFinal}%`);
      console.log(`[DEBUG] Fecha Inicio: ${fechaInicio}%`);

      console.log(`[DEBUG] Fecha fin: ${fechaFin}%`);
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
      try {


            
          console.log('[DEBUG] Enviando puntuación al servidor');
          const respuesta = await fetch('/games/guardar-puntuacion', {
            method: 'POST',
            credentials: 'same-origin',      // ← incluye cookies de este dominio
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content,
              'X-Requested-With': 'XMLHttpRequest'  // ayuda a algunos frameworks a detectar AJAX
            },
            body: JSON.stringify({
                juego_id: document.getElementById('gameDetails').dataset.juegoId,
                puntuacion: puntuacionFinal,
                fecha_inicio: fechaInicio,  // Ej: "2023-10-05T15:30:00.123Z"
                fecha_fin: fechaFin
            })
          });
          if (respuesta.redirected) {
            window.location.href = respuesta.url;  // Redirigir al login
            return;
        }
          
          console.log('[DEBUG] Respuesta del servidor:', respuesta.status);

            // Manejar redirecciones primero
            if (respuesta.redirected) {
                window.location.href = respuesta.url;
                return;
            }
        
        if (!respuesta.ok) throw new Error('Error HTTP');
        const datos = await respuesta.json();
        console.log('[DEBUG] Datos recibidos del servidor:', datos);
          
          if (!respuesta.ok) {
              console.error('[ERROR] Error en respuesta del servidor:', respuesta.statusText);
              throw new Error("Error al guardar puntuación");
          }
          

          
          elementosDOM.pregunta.textContent = "¡Quiz Completado!";
          elementosDOM.resultado.innerHTML = `
              <h4>Puntuación Final: ${puntuacionFinal}%</h4>
              <p>${datosJuego.titulo}</p>
              <p>${datos.mensaje || ""}</p>
              <div class="mt-3">
                <button id="btnReiniciar" class="btn btn-outline-secondary me-2">Reiniciar quiz</button>
                <button id="btnOtroQuiz" class="btn btn-outline-success">Hacer otro quiz</button>
              </div>
          `;
           elementosDOM.resultado.className = "alert alert-info";
           elementosDOM.resultado.style.display = "block";
           
          // --- wiring de los nuevos botones ---
          /*document.getElementById('btnRepasar')                <!--<button id="btnRepasar" class="btn btn-outline-primary me-2">Repasar contenido</button>-->

            .addEventListener('click', () => {
              // aquí puedes redirigir a la sección teórica,
              // o bien mostrar todas las preguntas con su explicación:
              window.location.href = `/games/teoria/${gameDetails.dataset.juegoId}`;
            });*/

          document.getElementById('btnReiniciar')
            .addEventListener('click', () => {
              // reinicia variables y vuelve a la primera pregunta
              preguntaActual = 0;
              puntuacion = 0;
              elementosDOM.puntuacion.textContent = puntuacion;
              elementosDOM.resultado.style.display = "none";
              mostrarPregunta();
            });

          document.getElementById('btnOtroQuiz')
            .addEventListener('click', () => {
              // redirige al listado de quizzes u otra categoría
              window.location.href = '/index';
            });

          if (datos.record) {
              console.log('[DEBUG] Nuevo récord:', datos.record);
              elementosDOM.highScore.textContent = `Récord: ${datos.record} puntos`;
          }
          
      } catch (error) {
        if (error.message.includes('JSON')) {
            mostrarError('Sesión expirada. Por favor recarga la página.');
            }else{
          console.error('[ERROR] Error en finalizarQuiz:', error);
          elementosDOM.resultado.innerHTML = `Error: ${error.message}`;
          elementosDOM.resultado.className = "alert alert-danger";
          elementosDOM.resultado.style.display = "block";
            }
      }
  }

  mostrarPregunta();
}

// Inicialización (Mejorada)
document.addEventListener("DOMContentLoaded", () => {
  console.log('[DEBUG] DOM cargado, iniciando juego');
  try {
      const gameDetails = document.getElementById('gameDetails');
      console.log('[DEBUG] gameDetails:', gameDetails);
      
      if (!gameDetails) {
          console.error('[ERROR] gameDetails no encontrado');
          throw new Error("Configuración del juego no encontrada");
      }
      
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
      console.log('[DEBUG] CSRF Token:', csrfToken ? 'Encontrado' : 'No encontrado');

      console.log(`[DEBUG] Solicitando datos para juego ID: ${gameDetails.dataset.juegoId}`);
      fetch(`/games/simulacion/${gameDetails.dataset.juegoId}`, {
          headers: { 'X-CSRFToken': csrfToken }
      })
      

      .then(response => {
          console.log('[DEBUG] Respuesta recibida, status:', response.status);
          if (!response.ok) {
              console.error('[ERROR] HTTP Error:', response.statusText);
              throw new Error(`HTTP ${response.status}`);
          }
          return response.json();
      })
      .then(iniciarQuiz)
      .catch(error => {
          console.error('[ERROR] Error en carga inicial:', error);
          mostrarError(error.message.includes("fetch") 
              ? "Error de conexión" 
              : error.message);
      });
  } catch (error) {
      console.error('[ERROR] Error en inicialización:', error);
      mostrarError(error.message);
  }
});

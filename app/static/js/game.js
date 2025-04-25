document.addEventListener("DOMContentLoaded", async () => {
  // Obtener ID del juego
  const gameElement = document.getElementById("gameDetails");
  const juego_id = parseInt(document.getElementById("gameDetails")?.dataset.juegoId);
  const juego_id2 = gameElement ? parseInt(gameElement.dataset.juegoId) : 1;

  if (isNaN(juego_id)) {
    console.error("ID de juego inválido");
    console.log(juego_id2)
    console.log(document.getElementById("gameDetails").dataset);
    document.getElementById("pregunta").textContent = "Error: ID de juego inválido";
    return;
  }

  // Variables del juego
  let preguntas = [];
  let indicePregunta = 0;
  let puntuacion = 0;
  const puntosPorRespuesta = 10;

  // Cargar datos del quiz
  try {
    console.log(document.getElementById("gameDetails").dataset);
    const response = await fetch(`/games/quiz/${juego_id}`);
    if (!response.ok) {
    const errorText = await response.text();
    console.error("Respuesta no válida del servidor:", errorText);
    throw new Error("Error en la respuesta del servidor");
    console.log(document.getElementById("gameDetails").dataset);
    }

    const quizData = await response.json();
    console.log(quizData);  // Verifica el formato de la respuesta del servidor

    
    // Transformar datos al formato esperado
    function mezclarOpciones(opciones) {
      for (let i = opciones.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [opciones[i], opciones[j]] = [opciones[j], opciones[i]]; // Intercambiar los elementos
      }
      return opciones;
    }
    
    preguntas = quizData.preguntas.map(p => ({
      texto: p.pregunta,
      opciones: mezclarOpciones([...new Set(p.opciones)]),  // Eliminar duplicados y mezclar
      correcta: p.opciones.indexOf(p.respuesta_correcta),
      explicacion: p.explicacion || "Sin explicación disponible"
    }));
    
    
    // Mostrar primera pregunta si hay datos
    if (preguntas.length > 0) {
      console.log(preguntas);  // Verifica que las preguntas estén cargadas correctamente
      mostrarPregunta();
  } else {
      document.getElementById("pregunta").textContent = "No hay preguntas disponibles";
  }
  
  } catch (error) {
    console.error("Error cargando quiz:", error);
    console.log(juego_id2)
    document.getElementById("pregunta").textContent = "Error cargando el juego";
  }

  function mostrarPregunta() {
    const actual = preguntas[indicePregunta];
    document.getElementById("pregunta").textContent = actual.texto;
    document.getElementById("progress").textContent = `Pregunta ${indicePregunta + 1} de ${preguntas.length}`;
    document.getElementById("respuestas").innerHTML = "";
    document.getElementById("resultado").style.display = "none";

            // Asignar colores alternados a las opciones
            const colores = ['rojo', 'amarillo', 'negro', 'blanco'];
            
    actual.opciones.forEach((opcion, i) => {
      const boton = document.createElement("button");
      boton.className = `opcion ${colores[i % colores.length]}`;
      boton.textContent = opcion;
      boton.onclick = (e) => verificarRespuesta(i === actual.correcta, actual.explicacion, e);
      document.getElementById("respuestas").appendChild(boton);
    });
  }

  function verificarRespuesta(esCorrecta, explicacion, event) {
    const botones = document.querySelectorAll(".opcion");
    botones.forEach(boton => boton.disabled = true);
  
    if (esCorrecta) {
      puntuacion += puntosPorRespuesta;
      event.target.classList.add("btn-success");
      event.target.classList.remove("btn-outline-primary");
    } else {
      event.target.classList.add("btn-danger");
      event.target.classList.remove("btn-outline-primary");
    }
  
    const resultadoDiv = document.getElementById("resultado");
    resultadoDiv.innerHTML = esCorrecta ? 
      `✅ Correcto! +${puntosPorRespuesta} puntos<br>${explicacion}` : 
      `❌ Incorrecto<br>${explicacion}`;
    resultadoDiv.className = esCorrecta ? "alert alert-success" : "alert alert-danger";
    resultadoDiv.style.display = "block";
  
    // Actualizar puntuación
    document.getElementById("puntuacion-actual").textContent = puntuacion;
  
    setTimeout(() => {
      indicePregunta++;
      if (indicePregunta < preguntas.length) {
        mostrarPregunta();
      } else {
        finalizarJuego();
      }
    }, 2000);
  }

  async function finalizarJuego() {
    try {
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || "";
      
      const response = await fetch('/games/guardar-puntuacion', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ 
          puntuacion: calcularPorcentaje(),
          juego_id: juego_id
        })
      });
      
      const data = await response.json();
      
      document.getElementById("pregunta").textContent = "¡Quiz completado!";
      document.getElementById("respuestas").innerHTML = "";
      const resultadoDiv = document.getElementById("resultado");
      resultadoDiv.innerHTML = `
        <h4>Puntuación final: ${calcularPorcentaje()}%</h4>
        <p>${data.mensaje || "Gracias por jugar"}</p>
      `;
      resultadoDiv.className = "alert alert-info";
      resultadoDiv.style.display = "block";
    } catch (error) {
      console.error('Error al guardar puntuación:', error);
    }
  }

  function calcularPorcentaje() {
    return Math.round((puntuacion / (preguntas.length * puntosPorRespuesta)) * 100);
  }
});
const preguntas = [
  {
    texto: "¿Qué significa una luz roja en un semáforo?",
    opciones: [
      "Avanzar con precaución",
      "Detenerse",
      "Girar a la derecha",
      "Cruzar rápido",
    ],
    correcta: 1,
  },
  {
    texto: "¿Quién tiene prioridad en un cruce peatonal sin semáforo?",
    opciones: ["El ciclista", "El peatón", "El conductor", "El motociclista"],
    correcta: 1,
  },
  {
    texto: "¿Cuál es el límite de velocidad en zonas escolares?",
    opciones: ["60 km/h", "40 km/h", "30 km/h", "20 km/h"],
    correcta: 2,
  },
  {
    texto: "¿Qué debes hacer si escuchas una sirena de ambulancia detrás?",
    opciones: [
      "Acelerar",
      "Ignorarla",
      "Detenerte y ceder el paso",
      "Cambiar de carril sin señalizar",
    ],
    correcta: 2,
  },
  {
    texto:
      "¿Qué indica una señal de tránsito con un triángulo rojo y un símbolo de peatón?",
    opciones: [
      "Cruce peligroso",
      "Zona escolar",
      "Cruce peatonal",
      "Alto obligatorio",
    ],
    correcta: 2,
  },
];

let indicePregunta = 0;
let puntuacion = 0;
const puntosPorRespuesta = 10;

function mostrarPregunta() {
  const actual = preguntas[indicePregunta];
  document.getElementById("pregunta").textContent = actual.texto;
  document.getElementById("respuestas").innerHTML = "";
  document.getElementById("resultado").style.display = "none";

  actual.opciones.forEach((opcion, i) => {
    const boton = document.createElement("button");
    boton.className = "opcion";
    boton.textContent = opcion;
    boton.onclick = () => verificarRespuesta(i === actual.correcta, actual.explicacion);
    document.getElementById("respuestas").appendChild(boton);
  });
}

function verificarRespuesta(esCorrecta, explicacion) {
  const botones = document.querySelectorAll(".opcion");
  botones.forEach(boton => boton.disabled = true);

  if (esCorrecta) {
    puntuacion += puntosPorRespuesta;
    event.target.classList.add("correcta");
  } else {
    event.target.classList.add("incorrecta");
  }

  document.getElementById("resultado").innerHTML = 
    esCorrecta ? 
    `✅ Correcto! +${puntosPorRespuesta} puntos<br>${explicacion}` : 
    `❌ Incorrecto<br>${explicacion}`;
  document.getElementById("resultado").style.display = "block";

  setTimeout(() => {
    indicePregunta++;
    if (indicePregunta < preguntas.length) {
      mostrarPregunta();
    } else {
      finalizarJuego();
    }
  }, 2000);
}
function finalizarJuego() {
  fetch("/guardar-puntuacion", {  // Cambia esta línea
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
    },
    body: JSON.stringify({ puntuacion: puntuacion })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById("pregunta").textContent = "Quiz completado!";
    document.getElementById("respuestas").innerHTML = "";
    document.getElementById("resultado").innerHTML = `
      Puntuación final: ${puntuacion} puntos<br>
      ${data.mensaje || ""}
    `;
  })
  .catch(error => console.error('Error:', error));
}
// Iniciar el juego
mostrarPregunta();
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
let correctas = 0;
let incorrectas = 0;

function mostrarPregunta() {
  const contenedorPregunta = document.getElementById("pregunta");
  const contenedorRespuestas = document.getElementById("respuestas");
  const resultado = document.getElementById("resultado");
  resultado.style.display = "none";

  const actual = preguntas[indicePregunta];
  contenedorPregunta.textContent = actual.texto;
  contenedorRespuestas.innerHTML = "";

  const colores = ["rojo", "amarillo", "negro", "blanco"];

  actual.opciones.forEach((opcion, i) => {
    const div = document.createElement("div");
    div.classList.add("opcion", colores[i]);
    div.textContent = opcion;
    div.onclick = () => verificarRespuesta(div, i === actual.correcta);
    contenedorRespuestas.appendChild(div);
  });
}

function verificarRespuesta(elemento, esCorrecta) {
  const opciones = document.querySelectorAll(".opcion");
  opciones.forEach((op) => op.classList.add("desactivada"));

  if (esCorrecta) {
    elemento.classList.add("correcta");
    correctas++;
  } else {
    elemento.style.opacity = "0.6";
    incorrectas++;
  }

  setTimeout(() => {
    indicePregunta++;
    if (indicePregunta < preguntas.length) {
      mostrarPregunta();
    } else {
      mostrarResultado();
    }
  }, 1000);
}

function mostrarResultado() {
  const contenedorPregunta = document.getElementById("pregunta");
  const contenedorRespuestas = document.getElementById("respuestas");
  const resultado = document.getElementById("resultado");

  contenedorPregunta.textContent = "¡Has completado el quiz!";
  contenedorRespuestas.innerHTML = "";
  resultado.innerHTML = `
        ✅ Respuestas correctas: <strong>${correctas}</strong><br/>
        ❌ Respuestas incorrectas: <strong>${incorrectas}</strong>
      `;
  resultado.style.display = "block";

  setTimeout(() => {
    window.location.href = "menu.html";
  }, 3000);
}

// Iniciar
mostrarPregunta();

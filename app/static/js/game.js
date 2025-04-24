document.addEventListener("DOMContentLoaded", () => {
    // Elementos del DOM
    const gameElement = document.getElementById("gameDetails");
    const juego_id = gameElement ? parseInt(gameElement.dataset.juegoId) : 1;
    
    // Banco de preguntas ampliado
    const quizzes = {
      1: [
        {
          texto: "¿Qué significa una luz roja en un semáforo?",
          opciones: ["Avanzar con precaución", "Detenerse", "Girar a la derecha", "Cruzar rápido"],
          correcta: 1,
          explicacion: "Una luz roja en un semáforo indica que debes detenerte completamente."
        },
        {
          texto: "¿Quién tiene prioridad en un cruce peatonal sin semáforo?",
          opciones: ["El ciclista", "El peatón", "El conductor", "El motociclista"],
          correcta: 1,
          explicacion: "En un cruce peatonal sin semáforo, el peatón siempre tiene prioridad."
        },
        {
          texto: "¿Cuál es el límite de velocidad en zonas escolares?",
          opciones: ["60 km/h", "40 km/h", "30 km/h", "20 km/h"],
          correcta: 2,
          explicacion: "El límite suele ser 30 km/h en zonas escolares para proteger a los niños."
        },
        {
          texto: "¿Qué debes hacer si escuchas una sirena de ambulancia detrás?",
          opciones: ["Acelerar", "Ignorarla", "Detenerte y ceder el paso", "Cambiar de carril sin señalizar"],
          correcta: 2,
          explicacion: "Debes ceder el paso deteniéndote o moviéndote al costado si es seguro."
        },
        {
          texto: "¿Qué indica una señal de tránsito con un triángulo rojo y un símbolo de peatón?",
          opciones: ["Cruce peligroso", "Zona escolar", "Cruce peatonal", "Alto obligatorio"],
          correcta: 2,
          explicacion: "Esa señal indica un cruce peatonal cercano, ten precaución."
        }
      ],
      2: [
        {
          texto: "¿Qué debes hacer antes de cambiar de carril?",
          opciones: ["Acelerar", "Usar las luces direccionales", "Frenar", "Nada"],
          correcta: 1,
          explicacion: "Siempre usa las luces direccionales para indicar tus movimientos."
        },
        {
          texto: "¿Cuál es la distancia mínima que debes mantener con el vehículo de adelante?",
          opciones: ["1 metro", "3 segundos", "10 metros", "Depende del clima"],
          correcta: 1,
          explicacion: "La regla de los 3 segundos permite mantener una distancia segura en condiciones normales."
        },
        {
          texto: "¿Qué significa una línea continua en el centro de la carretera?",
          opciones: ["Puedes rebasar", "No puedes rebasar", "Calle cerrada", "Solo peatones"],
          correcta: 1,
          explicacion: "Una línea continua indica que no está permitido rebasar."
        },
        {
          texto: "¿Qué documento necesitas para conducir legalmente?",
          opciones: ["Pasaporte", "Licencia de conducir", "CURP", "INE"],
          correcta: 1,
          explicacion: "La licencia de conducir es obligatoria para manejar legalmente."
        },
        {
          texto: "¿Qué hacer si se te pincha una llanta en carretera?",
          opciones: ["Seguir conduciendo", "Frenar de golpe", "Encender luces intermitentes y orillarte", "Salir del coche en medio del camino"],
          correcta: 2,
          explicacion: "Oríllate con precaución y enciende intermitentes para evitar accidentes."
        }
      ],
        // Añadir más juegos según sea necesario
        3: [
            {
                texto: "¿Qué indica una señal amarilla en forma de rombo?",
                opciones: ["Peligro adelante", "Ceda el paso", "Velocidad máxima", "Dirección obligatoria"],
                correcta: 0,
                explicacion: "Las señales amarillas en forma de rombo indican advertencias de peligro."
            }
        ]
    };

    // Variables del juego
    const preguntas = quizzes[juego_id] || [];
    let indicePregunta = 0;
    let puntuacion = 0;
    const puntosPorRespuesta = 10;
    let highScore = localStorage.getItem(`highScore_${juego_id}`) || 0;

    // Mostrar récord al inicio
    document.getElementById("high-score").textContent = `Récord: ${highScore} puntos`;

    // Si no hay preguntas
    if (preguntas.length === 0) {
        document.getElementById("pregunta").textContent = "No hay preguntas disponibles para este juego.";
        return;
    }

    // Función para mostrar cada pregunta
    function mostrarPregunta() {
        const preguntaActual = preguntas[indicePregunta];
        
        // Actualizar texto de la pregunta
        document.getElementById("pregunta").textContent = preguntaActual.texto;
        
        // Limpiar respuestas anteriores
        document.getElementById("respuestas").innerHTML = "";
        document.getElementById("resultado").style.display = "none";
        
        // Asignar colores alternados a las opciones
        const colores = ['rojo', 'amarillo', 'negro', 'blanco'];

        // Crear botones para cada opción
        preguntaActual.opciones.forEach((opcion, indice) => {
            const boton = document.createElement("button");
            boton.className = `opcion ${colores[indice % colores.length]}`;
            boton.textContent = opcion;
            boton.onclick = () => verificarRespuesta(indice === preguntaActual.correcta, preguntaActual.explicacion, boton);
            document.getElementById("respuestas").appendChild(boton);
        });
        
        // Actualizar progreso
        document.getElementById("progress").textContent = `Pregunta ${indicePregunta + 1} de ${preguntas.length}`;
    }

    // Función para verificar la respuesta
    function verificarRespuesta(esCorrecta, explicacion, botonSeleccionado) {
        const todosBotones = document.querySelectorAll(".opcion");
        
        // Deshabilitar todos los botones
        todosBotones.forEach(boton => boton.disabled = true);
        
        // Resaltar respuesta seleccionada
        if (esCorrecta) {
            puntuacion += puntosPorRespuesta;
            botonSeleccionado.classList.remove("btn-outline-primary");
            botonSeleccionado.classList.add("btn-success");
        } else {
            botonSeleccionado.classList.remove("btn-outline-primary");
            botonSeleccionado.classList.add("btn-danger");
            // Mostrar la respuesta correcta
            todosBotones[preguntas[indicePregunta].correcta].classList.add("btn-success");
        }
        
        // Mostrar feedback
        const resultadoElement = document.getElementById("resultado");
        resultadoElement.innerHTML = esCorrecta ?
            `<div class="text-success">✅ ¡Correcto! +${puntosPorRespuesta} puntos</div>
             <div class="mt-2">${explicacion}</div>` :
            `<div class="text-danger">❌ Incorrecto</div>
             <div class="mt-2">${explicacion}</div>`;
        
        resultadoElement.style.display = "block";
        resultadoElement.className = esCorrecta ? "alert alert-success" : "alert alert-danger";
        
        // Actualizar puntuación en pantalla
        document.getElementById("puntuacion-actual").textContent = puntuacion;
        
        // Siguiente pregunta o finalizar
        setTimeout(() => {
            indicePregunta++;
            if (indicePregunta < preguntas.length) {
                mostrarPregunta();
            } else {
                finalizarJuego();
            }
        }, 2500);
    }

    // Función para terminar el juego
    function finalizarJuego() {
        // Actualizar récord si es necesario
        if (puntuacion > highScore) {
            highScore = puntuacion;
            localStorage.setItem(`highScore_${juego_id}`, highScore);
            document.getElementById("high-score").textContent = `Récord: ${highScore} puntos`;
        }
        
        // Mostrar mensaje final
        document.getElementById("pregunta").textContent = "🏁 Juego Completado";
        document.getElementById("respuestas").innerHTML = `
            <button onclick="location.reload()" class="btn btn-primary btn-lg">
                Jugar Nuevamente
            </button>
            <a href="/index" class="btn btn-outline-secondary btn-lg mt-2">
                Volver al Menú
            </a>
        `;
        
        // Mostrar resultados finales
        const resultadoFinal = document.getElementById("resultado");
        resultadoFinal.innerHTML = `
            <h4 class="text-center">Resultado Final</h4>
            <p class="text-center fs-3">${puntuacion} puntos</p>
            ${puntuacion > highScore ? 
                '<div class="alert alert-warning text-center">¡Nuevo récord! 🏆</div>' : 
                `<p class="text-center">Tu mejor puntuación: ${highScore} puntos</p>`}
        `;
        resultadoFinal.style.display = "block";
        resultadoFinal.className = "alert alert-info";
    }

    // Iniciar el juego
    mostrarPregunta();
});
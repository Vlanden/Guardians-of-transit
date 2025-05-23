document.addEventListener('DOMContentLoaded', function() {
    // Configuración del juego
    const preguntas = [
        {
            frase: "Cuando un semáforo es rojo",
            opciones: ["Me tengo que detener", "Le acelero", "Lo ignoro", "Me cambio de carril"],
            correcta: "Me tengo que detener"
        },
        {
            frase: "Al ver una señal de pare",
            opciones: ["Freno completamente", "Acelero", "Solo reduzco velocidad", "Toco el claxon"],
            correcta: "Freno completamente"
        },
        {
            frase: "En un cruce peatonal",
            opciones: ["Tengo prioridad", "Los peatones tienen prioridad", "Es opcional detenerse", "Solo si hay policía"],
            correcta: "Los peatones tienen prioridad"
        },
        {
            frase: "Al cambiar de carril en la autopista",
            opciones: ["Solo uso los espejos", "Uso espejos y giro la cabeza", "Cambio sin mirar", "Solo uso la cámara trasera"],
            correcta: "Uso espejos y giro la cabeza"
        },
        {
            frase: "Cuando un conductor me da paso",
            opciones: ["Le hago señas con la mano", "Acelero rápidamente", "Le cedo el paso a él", "Agradezco con un gesto"],
            correcta: "Agradezco con un gesto"
        }
    ];

    // Variables de estado
    let preguntaActual = 0;
    let puntaje = 0;
    let dropzone = null;

    // Elementos del DOM
    const contenedorJuego = document.querySelector('.cuerpo_juego_palabras');
    const titulo = document.querySelector('h1');
    const fraseElement = document.querySelector('.frase_a_completar');
    const opcionesContainer = document.querySelector('.opciones_para_frase');

    // Inicializar juego
    function iniciarJuego() {
        mostrarPregunta();
    }

    // Mostrar la pregunta actual
    function mostrarPregunta() {
        if (preguntaActual >= preguntas.length) {
            finalizarJuego();
            return;
        }

        const pregunta = preguntas[preguntaActual];
        
        // Actualizar la interfaz
        titulo.textContent = "Completa la Frase";
        fraseElement.innerHTML = `
            ${pregunta.frase} 
            <div id="dropzone" class="dropzone">[Arrastra aquí]</div>
        `;
        
        opcionesContainer.innerHTML = '';
        
        // Crear opciones de respuesta
        pregunta.opciones.forEach(opcion => {
            const opcionElement = document.createElement('div');
            opcionElement.className = 'opcion';
            opcionElement.draggable = true;
            opcionElement.textContent = opcion;
            opcionesContainer.appendChild(opcionElement);
        });

        // Configurar eventos
        configurarDragAndDrop();
    }

    // Configurar el sistema de arrastrar y soltar
    function configurarDragAndDrop() {
        dropzone = document.getElementById('dropzone');
        const opciones = document.querySelectorAll('.opcion');

        // Eventos para las opciones
        opciones.forEach(opcion => {
            opcion.addEventListener('dragstart', function(e) {
                e.dataTransfer.setData('text/plain', this.textContent);
                this.classList.add('dragging');
            });

            opcion.addEventListener('dragend', function() {
                this.classList.remove('dragging');
            });
        });

        // Eventos para la dropzone
        dropzone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('highlight');
        });

        dropzone.addEventListener('dragleave', function() {
            this.classList.remove('highlight');
        });

        dropzone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('highlight');
            
            const respuesta = e.dataTransfer.getData('text/plain');
            const opciones = document.querySelectorAll('.opcion');
            
            // Mostrar la respuesta en la dropzone
            this.textContent = respuesta;
            
            // Verificar si es correcta
            const esCorrecta = respuesta === preguntas[preguntaActual].correcta;
            
            // Aplicar estilos
            opciones.forEach(opcion => {
                opcion.classList.remove('correcto', 'incorrecto');
                if (opcion.textContent === respuesta) {
                    opcion.classList.add(esCorrecta ? 'correcto' : 'incorrecto');
                }
                if (opcion.textContent === preguntas[preguntaActual].correcta && !esCorrecta) {
                    opcion.classList.add('correcto');
                }
            });
            
            // Actualizar puntaje y avanzar
            if (esCorrecta) puntaje++;
            
            setTimeout(() => {
                preguntaActual++;
                mostrarPregunta();
            }, esCorrecta ? 1000 : 2000);
        });
    }

    // Finalizar el juego
    function finalizarJuego() {
        fraseElement.innerHTML = `
            <div class="resultado-final">
                <h2>¡Juego Completado!</h2>
                <p>Puntaje final: ${puntaje}/${preguntas.length}</p>
                <div class="botones-final">
                    <button id="reiniciar" class="btn-juego">Jugar Nuevamente</button>
                    <button id="volver-inicio" class="btn-juego">Volver al Inicio</button>
                </div>
            </div>
        `;
        
        opcionesContainer.innerHTML = '';
        
        // Eventos para los botones
        document.getElementById('reiniciar').addEventListener('click', function() {
            preguntaActual = 0;
            puntaje = 0;
            mostrarPregunta();
        });
        
        document.getElementById('volver-inicio').addEventListener('click', function() {
            window.location.pathname = "/index";
        });
    }

    // Iniciar el juego
    iniciarJuego();
});
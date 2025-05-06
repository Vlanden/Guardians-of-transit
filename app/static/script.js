const dropzone = document.getElementById('dropzone');
const opciones = document.querySelectorAll('.opcion');

opciones.forEach(opcion => {
    opcion.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', opcion.id);
        e.dataTransfer.setData('text/texto', opcion.innerText);
    });
});

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    const id = e.dataTransfer.getData('text/plain');
    const texto = e.dataTransfer.getData('text/texto');
    
    dropzone.textContent = texto;

    if (id === "correcta") {
        dropzone.classList.remove('incorrecto');
        dropzone.classList.add('correcto');
    } else {
        dropzone.classList.remove('correcto');
        dropzone.classList.add('incorrecto');
    }
});

function buscarJuego() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const juegos = document.getElementsByClassName("game-card");

  for (let juego of juegos) {
    if (juego.id.toLowerCase().includes(input)) {
      juego.style.display = "block";
    } else {
      juego.style.display = "none";
    }
  }
}

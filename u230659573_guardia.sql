PRAGMA foreign_keys = OFF;

-- Eliminar tablas existentes
DROP TABLE IF EXISTS intentos;
DROP TABLE IF EXISTS quiz_preguntas;
DROP TABLE IF EXISTS perfil;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS juegos_quiz;
DROP TABLE IF EXISTS juegos_sim;
DROP TABLE IF EXISTS juegos_extra;

-- Crear tablas en orden correcto
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL
);

CREATE TABLE juegos_quiz (
  id_quiz INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  descripcion TEXT NOT NULL,
  img_referencia TEXT NOT NULL
);

CREATE TABLE juegos_sim (
  id_sim INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  descripcion TEXT NOT NULL,
  img_referencia TEXT NOT NULL
);

CREATE TABLE juegos_extra (
  id_extra INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  descripcion TEXT NOT NULL,
  img_referencia TEXT NOT NULL
);

CREATE TABLE intentos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  juego_id INTEGER NOT NULL,
  puntaje INTEGER NOT NULL,
  fecha_inicio TEXT,
  fecha_fin TEXT,
  FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE perfil (
  username TEXT PRIMARY KEY,
  fecha_registro TEXT,
  ultima_conexion TEXT,
  juegos_jugados TEXT,
  FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE quiz_preguntas (
  id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT,
  id_quiz INTEGER,
  q_pregunta TEXT NOT NULL,
  opcioncorrecta TEXT NOT NULL,
  opcion2 TEXT NOT NULL,
  opcion3 TEXT NOT NULL,
  opcion4 TEXT NOT NULL,
  explicacion TEXT,
  FOREIGN KEY(id_quiz) REFERENCES juegos_quiz(id_quiz)
);

CREATE TABLE quiz_simulacion (
  id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT,
  id_sim INTEGER,
  q_pregunta TEXT NOT NULL,
  url_sim TEXT NOT NULL,
  opcioncorrecta TEXT NOT NULL,
  opcion2 TEXT NOT NULL,
  opcion3 TEXT NOT NULL,
  opcion4 TEXT NOT NULL,
  explicacion TEXT,
  FOREIGN KEY(id_sim) REFERENCES juegos_sim(id_sim)
);

-- Insertar usuarios
INSERT INTO users (id, username, email, password_hash) VALUES
(1, 'olorex12', 'sigala@gmail.com', '$2b$12$u1e3oZ3E/N296K98FG2Yv.4f2jVh2EiNMJoq3h.fgnzGOEBMlmesu'),
(2, 'Vladi', 'vladimirlaraalejo@gmail.com', '$2b$12$ZpUUFTD10EZdT75oggrZQumFpPvCNEmYCd.Tl93eKoDMvS5vfBk5e'),
(3, 'Tejuino2', 'tejuino2@gmail.com', '$2b$12$Scf1rczQ/r3PBISwgzTphOc0DxZc647uUitxSQSPzyj3P.pRwMKii'),
(4, 'Tejuino', 'tejuino@gmail.com', '$2b$12$HAWuOw3chT2axYvLT7t4aOPQNUmrtQu3FKL2HcL.Wu9WO1Q81Nflm'),
(5, 'Bruhcin', 'sebastian.zuniga1376@alumnos.udg.mx', '$2b$12$dOCePEY60pUM0EuUKAQpdOJSWNi5hbzm6iWiyRAFeJNAY5vWx8Iam'),
(6, 'UrielYO', 'urielbarajas@gmail.com', '$2b$12$Nmo7uWf1qMV2lkmp5L6qGuhI34EUIhyVBfMwo2W9MAAJbSwTM3/TK'),
(7, 'ssssssss', 'sssss@gmail.com', '$2b$12$K9Ee43qmISDn0Q2uB5MIx.ZvYiIpZoXk28nZR8A8TcXXjbPdtlaR6'),
(8, 'ssssssss2', 'sssss2@gmail.com', '$2b$12$.C4BtXbvrl2vUdA8SAhyxOBhE9gyZ9t2HeGQoXVE/QdNC3BLb5jT.');

-- Insertar juegos_quiz
INSERT INTO juegos_quiz (id_quiz, titulo, descripcion, img_referencia) VALUES
(1, 'Educación Vial 1', 'Quiz sobre normas de tránsito 1', 'juegos/quiz/game1.jpg'),
(2, 'Educación Vial 2', 'Quiz sobre normas de tránsito 2', 'juegos/quiz/game2.jpg');

-- Insertar intentos 
INSERT INTO intentos (id, username, juego_id, puntaje, fecha_inicio, fecha_fin) VALUES
(1, 'olorex12', 2, 0, '2025-05-01 22:08:38', '2025-05-01 22:08:50'),
(2, 'Vladi', 1, 0, '2025-05-01 22:18:14', '2025-05-01 22:18:27'),
(3, 'Vladi', 1, 40, '2025-05-01 22:22:54', '2025-05-01 22:23:32'),
(4, 'Vladi', 1, 40, '2025-05-01 22:26:14', '2025-05-01 22:26:52'),
(5, 'Vladi', 2, 0, '2025-05-01 22:29:16', '2025-05-01 22:29:30'),
(6, 'Vladi', 1, 20, '2025-05-01 22:29:47', '2025-05-01 22:30:00'),
(7, 'Vladi', 1, 20, '2025-05-01 22:43:16', '2025-05-01 22:43:27'),
(8, 'Tejuino', 1, 0, '2025-05-01 23:17:16', '2025-05-01 23:17:27'),
(9, 'Vladi', 2, 60, '2025-05-01 23:17:51', '2025-05-01 23:18:04'),
(10, 'Vladi', 2, 80, '2025-05-01 23:17:51', '2025-05-01 23:18:26'),
(11, 'Bruhcin', 1, 0, '2025-05-02 00:44:36', '2025-05-02 00:45:08'),
(12, 'Bruhcin', 1, 60, '2025-05-02 00:44:36', '2025-05-02 00:46:20'),
(13, 'Bruhcin', 1, 80, '2025-05-02 00:44:36', '2025-05-02 00:47:24'),
(14, 'Bruhcin', 1, 80, '2025-05-02 00:44:36', '2025-05-02 00:48:07'),
(15, 'Bruhcin', 1, 80, '2025-05-02 00:44:36', '2025-05-02 00:48:53'),
(16, 'Bruhcin', 1, 100, '2025-05-02 00:44:36', '2025-05-02 00:49:22'),
(17, 'Bruhcin', 1, 100, '2025-05-02 00:49:35', '2025-05-02 00:50:09'),
(18, 'Vladi', 1, 20, '2025-05-03 02:20:54', '2025-05-03 02:21:27'),
(19, 'olorex12', 1, 60, '2025-05-05 17:40:49', '2025-05-05 17:41:29'),
(20, 'Tejuino', 1, 40, '2025-05-05 21:45:23', '2025-05-05 21:45:44'),
(21, 'Tejuino', 1, 40, '2025-05-05 21:55:19', '2025-05-05 21:55:37'),
(22, 'Tejuino', 1, 20, '2025-05-05 21:57:38', '2025-05-05 21:57:50'),
(23, 'Tejuino', 1, 20, '2025-05-05 22:10:04', '2025-05-05 22:10:16'),
(24, 'Tejuino', 1, 20, '2025-05-05 22:13:37', '2025-05-05 22:14:02'),
(25, 'Tejuino', 2, 40, '2025-05-05 22:22:41', '2025-05-05 22:22:58'),
(26, 'Tejuino', 1, 20, '2025-05-05 22:25:14', '2025-05-05 22:25:27'),
(27, 'Tejuino', 2, 80, '2025-05-05 22:25:38', '2025-05-05 22:25:55'),
(28, 'Tejuino', 1, 100, '2025-05-05 22:35:24', '2025-05-05 22:36:03'),
(29, 'Tejuino', 2, 60, '2025-05-05 22:36:19', '2025-05-05 22:36:55'),
(30, 'Tejuino', 1, 60, '2025-05-05 22:40:19', '2025-05-05 22:40:38'),
(31, 'ssssssss', 1, 40, '2025-05-06 01:51:49', '2025-05-06 01:52:01'),
(32, 'Vladi', 1, 20, '2025-05-07 00:10:35', '2025-05-07 00:10:51');

-- Insertar perfil
INSERT INTO perfil (username, fecha_registro, ultima_conexion, juegos_jugados) VALUES
('Bruhcin', '2025-05-02 00:43:58', '2025-05-02 00:50:11', '1,1,1,1,1'),
('ssssssss', '2025-05-06 01:41:52', '2025-05-06 01:55:57', '0,1'),
('ssssssss2', '2025-05-06 01:56:22', '2025-05-05 20:35:36', '0'),
('Tejuino', '2025-05-01 16:45:32', '2025-05-06 01:10:46', '1,2,1,2,1'),
('UrielYO', '2025-05-02 00:58:00', '2025-05-05 21:37:44', '0'),
('Vladi', '2025-05-01 16:45:32', '2025-05-07 00:17:38', '1,2,2,1,1');

-- Insertar quiz_preguntas
INSERT INTO quiz_preguntas (id_pregunta, id_quiz, q_pregunta, opcioncorrecta, opcion2, opcion3, opcion4, explicacion) VALUES
(1, 1, '¿Qué significa una luz roja en un semáforo?', 'Detenerse', 'Avanzar con precaución', 'Girar a la derecha', 'Cruzar rápido', 'El rojo en semáforos indica detención obligatoria.'),
(2, 1, '¿Quién tiene prioridad en un cruce peatonal sin semáforo?', 'El peatón', 'El ciclista', 'El conductor', 'El motociclista', 'Los peatones siempre tienen prioridad en cruces no señalizados.'),
(3, 1, '¿Cuál es el límite de velocidad en zonas escolares?', '30 km/h', '40 km/h', '60 km/h', '20 km/h', 'En muchas ciudades, el límite en zonas escolares es 30 km/h para proteger a los niños.'),
(4, 1, '¿Qué debes hacer si escuchas una sirena de ambulancia detrás?', 'Detenerte y ceder el paso', 'Ignorarla', 'Acelerar', 'Cambiar de carril sin señalizar', 'Debes ceder el paso a vehículos de emergencia.'),
(5, 1, '¿Qué indica una señal de tránsito con un triángulo rojo y un símbolo de peatón?', 'Cruce peatonal', 'Zona escolar', 'Cruce peligroso', 'Alto obligatorio', 'Señal de advertencia: indica proximidad a un cruce peatonal.'),
(6, 2, '¿Qué debes hacer antes de cambiar de carril?', 'Usar las luces direccionales', 'Acelerar', 'Frenar', 'Nada', 'Siempre usa las luces direccionales para indicar tus movimientos.'),
(7, 2, '¿Cuál es la distancia mínima que debes mantener con el vehículo de adelante?', '3 segundos', '1 metro', '10 metros', 'Depende del clima', 'La regla de los 3 segundos permite mantener una distancia segura en condiciones normales.'),
(8, 2, '¿Qué significa una línea continua en el centro de la carretera?', 'No puedes rebasar', 'Puedes rebasar', 'Calle cerrada', 'Solo peatones', 'Una línea continua indica que no está permitido rebasar.'),
(9, 2, '¿Qué documento necesitas para conducir legalmente?', 'Licencia de conducir', 'Pasaporte', 'CURP', 'INE', 'La licencia de conducir es obligatoria para manejar legalmente.'),
(10, 2, '¿Qué hacer si se te pincha una llanta en carretera?', 'Encender luces intermitentes y orillarte', 'Frenar de golpe', 'Seguir conduciendo', 'Salir del coche en medio del camino', 'Oríllate con precaución y enciende intermitentes para evitar accidentes.');


-- Insertar juegos_extra
INSERT INTO juegos_extra (id_extra, titulo, descripcion, img_referencia) VALUES
(200000, 'Acompleta la frase 1', 'Se mostrarán una serie de frases y el usuario tendrá que completarlas con la palabra faltante', 'juegos/quiz/game1.jpg');

-- Insertar juegos_sim
INSERT INTO juegos_sim (id_sim, titulo, descripcion, img_referencia) VALUES
(100000, 'Juego simulación 1', 'Se presenta una serie de caídas para analizar errores', 'juegos/quiz/game1.jpg');

-- Insertar quiz_simulacion
INSERT INTO quiz_simulacion (id_pregunta, id_sim, q_pregunta, url_sim, opcioncorrecta, opcion2, opcion3, opcion4, explicacion) VALUES
(1, 100000, '¿Que podrian hacer los motociclistas para evitar caer?', 'simulation/Caidas.mp4', 'No frenar tan bruscamente', 'Acelerar mas', 'Inclinarse al otro lado', 'Bajarse de la moto', 'En este tipo de casos, lo mas recomendable es tener una velocidad moderada para evitar tener que usar el freno y asi evitar un derrape');

-- Crear índices
CREATE INDEX idx_intentos_username ON intentos(username);
CREATE INDEX idx_juegos_quiz_titulo ON juegos_quiz(titulo);
CREATE INDEX idx_juegos_quiz_descripcion ON juegos_quiz(descripcion);

PRAGMA foreign_keys = ON;
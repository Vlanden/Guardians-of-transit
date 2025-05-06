PRAGMA foreign_keys = OFF;

-- Eliminar tablas existentes
DROP TABLE IF EXISTS intentos;
DROP TABLE IF EXISTS quiz_preguntas;
DROP TABLE IF EXISTS perfil;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS juegos_quiz;
DROP TABLE IF EXISTS juegos_sim;
DROP TABLE IF EXISTS juegos_extra;

-- Crear tablas en orden correcto (primero las independientes)
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
  juegos_jugados TEXT DEFAULT '0',
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

INSERT INTO users (username, email, password_hash) VALUES
('ssssssss', 'sssss@gmail.com', '$2b$12$wFZFXHJpVhzdxzn9w/MDAea.6oqQ0YWa.f51qe8SuPZX6LksaBeP2'),
('Vladi', 'vladimirlaraalejo@gmail.com', '$2b$12$5GRxpHb5CS.BNlUHyolQzOiPIvy56ko3GZ2UvTv.yHqdEWhfcIyCe'),
('Hola', 'vladimirlaraalejo@hotmail.com', '$2b$12$AdTHUjhDOR31PHXL8TEtqORy9kBoIrsQMGBPsYarspyYVTmCL0LFa');

INSERT INTO juegos_quiz (titulo, descripcion, img_referencia) VALUES
('Educación Vial 1', 'Quiz sobre normas de tránsito 1', 'juegos/quiz/game1.jpg'),
('Epa', 'Quiz sobre normas de tránsito 2', 'juegos/quiz/game2.jpg');

INSERT INTO intentos (username, juego_id, puntaje, fecha_inicio, fecha_fin) VALUES
('Vladi', 1, 20, '2025-04-27 02:57:36', '2025-04-27 02:57:36'),
('Vladi', 1, 40, '2025-04-27 03:32:49', '2025-04-27 03:32:49'),
('Vladi', 1, 100, '2025-04-27 04:22:41', '2025-04-27 04:22:41'),
('Vladi', 2, 20, '2025-04-27 04:32:30', '2025-04-27 04:32:30'),
('Vladi', 2, 20, '2025-04-27 04:39:37', '2025-04-27 04:39:37'),
('Vladi', 2, 0, '2025-04-27 04:40:04', '2025-04-27 04:40:04'),
('Vladi', 1, 40, '2025-04-27 04:47:08', '2025-04-27 04:47:08'),
('Vladi', 1, 20, '2025-04-27 04:54:15', '2025-04-27 04:54:15'),
('Vladi', 1, 80, '2025-04-27 05:04:35', '2025-04-27 05:04:35'),
('Vladi', 1, 0, '2025-04-27 05:19:41', '2025-04-27 05:19:41'),
('Vladi', 1, 40, '2025-04-27 05:20:53', '2025-04-27 05:20:53'),
('Vladi', 1, 80, '2025-04-27 05:42:59', '2025-04-27 05:42:59'),
('Vladi', 1, 20, '2025-04-27 05:46:23', '2025-04-27 05:46:23'),
('Vladi', 1, 20, '2025-04-27 05:48:15', '2025-04-27 05:48:15'),
('Vladi', 1, 80, '2025-04-27 17:14:28', '2025-04-27 17:14:28'),
('Vladi', 1, 40, '2025-04-27 17:16:03', '2025-04-27 17:16:03'),
('Vladi', 1, 40, '2025-04-27 17:24:17', '2025-04-27 17:24:17'),
('Vladi', 1, 20, '2025-04-27 17:27:05', '2025-04-27 17:27:05'),
('Vladi', 1, 80, '2025-04-27 18:50:54', '2025-04-27 18:50:54'),
('Vladi', 1, 20, '2025-04-27 19:29:46', '2025-04-27 19:29:46'),
('Vladi', 1, 20, '2025-04-27 19:34:46', '2025-04-27 19:34:46'),
('Vladi', 1, 60, '2025-04-27 19:36:17', '2025-04-27 19:36:17'),
('Vladi', 1, 0, '2025-04-27 19:44:01', '2025-04-27 19:44:01'),
('Vladi', 1, 20, '2025-04-27 19:58:14', '2025-04-27 19:58:14'),
('Vladi', 1, 20, '2025-04-27 20:26:31', '2025-04-27 20:26:31'),
('Vladi', 1, 20, '2025-04-27 20:27:49', '2025-04-27 20:27:49'),
('Vladi', 1, 20, '2025-04-27 21:01:00', '2025-04-27 21:01:00'),
('Vladi', 2, 80, '2025-04-27 21:02:29', '2025-04-27 21:02:29'),
('Vladi', 1, 20, '2025-04-27 21:20:50', '2025-04-27 21:20:50'),
('Vladi', 1, 20, '2025-04-27 22:02:06', '2025-04-27 22:02:06'),
('Vladi', 1, 0, '2025-04-27 22:03:39', '2025-04-27 22:03:39'),
('Vladi', 1, 20, '2025-04-27 22:04:57', '2025-04-27 22:04:57');

INSERT INTO perfil (username, fecha_registro, ultima_conexion, juegos_jugados) VALUES
('Hola', NULL, NULL, '1'),
('Vladi', '2025-04-23 18:16:04', '2025-04-23 22:14:50', '1,2,');

INSERT INTO quiz_preguntas (id_quiz, q_pregunta, opcioncorrecta, opcion2, opcion3, opcion4, explicacion) VALUES
(1, '¿Qué significa una luz roja en un semáforo?', 'Detenerse', 'Avanzar con precaución', 'Girar a la derecha', 'Cruzar rápido', ''),
(1, '¿Quién tiene prioridad en un cruce peatonal sin semáforo?', 'El peatón', 'El ciclista', 'El conductor', 'El motociclista', ''),
(1, '¿Cuál es el límite de velocidad en zonas escolares?', '30 km/h', '40 km/h', '60 km/h', '20 km/h', ''),
(1, '¿Qué debes hacer si escuchas una sirena de ambulancia detrás?', 'Detenerte y ceder el paso', 'Ignorarla', 'Acelerar', 'Cambiar de carril sin señalizar', ''),
(1, '¿Qué indica una señal de tránsito con un triángulo rojo y un símbolo de peatón?', 'Cruce peatonal', 'Zona escolar', 'Cruce peligroso', 'Alto obligatorio', ''),
(2, '¿Qué debes hacer antes de cambiar de carril?', 'Usar las luces direccionales', 'Acelerar', 'Frenar', 'Nada', 'Siempre usa las luces direccionales para indicar tus movimientos.'),
(2, '¿Cuál es la distancia mínima que debes mantener con el vehículo de adelante?', '3 segundos', '1 metro', '10 metros', 'Depende del clima', 'La regla de los 3 segundos permite mantener una distancia segura en condiciones normales.'),
(2, '¿Qué significa una línea continua en el centro de la carretera?', 'No puedes rebasar', 'Puedes rebasar', 'Calle cerrada', 'Solo peatones', 'Una línea continua indica que no está permitido rebasar.'),
(2, '¿Qué documento necesitas para conducir legalmente?', 'Licencia de conducir', 'Pasaporte', 'CURP', 'INE', 'La licencia de conducir es obligatoria para manejar legalmente.'),
(2, '¿Qué hacer si se te pincha una llanta en carretera?', 'Encender luces intermitentes y orillarte', 'Frenar de golpe', 'Seguir conduciendo', 'Salir del coche en medio del camino', 'Oríllate con precaución y enciende intermitentes para evitar accidentes.');

-- Índices
CREATE INDEX idx_intentos_username ON intentos(username);
CREATE INDEX idx_quiz_preguntas_id_quiz ON quiz_preguntas(id_quiz);

PRAGMA foreign_keys = ON;
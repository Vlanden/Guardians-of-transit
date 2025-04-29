-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 29-04-2025 a las 01:42:46
-- Versión del servidor: 10.11.10-MariaDB
-- Versión de PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `u230659573_guardia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `intentos`
--

CREATE TABLE `intentos` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `juego_id` int(11) NOT NULL,
  `puntaje` int(11) NOT NULL,
  `fecha_inicio` datetime DEFAULT NULL,
  `fecha_fin` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `intentos`
--

INSERT INTO `intentos` (`id`, `username`, `juego_id`, `puntaje`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 'Vladi', 1, 20, '2025-04-27 02:57:36', '2025-04-27 02:57:36'),
(2, 'Vladi', 1, 40, '2025-04-27 03:32:49', '2025-04-27 03:32:49'),
(3, 'Vladi', 1, 100, '2025-04-27 04:22:41', '2025-04-27 04:22:41'),
(4, 'Vladi', 2, 20, '2025-04-27 04:32:30', '2025-04-27 04:32:30'),
(5, 'Vladi', 2, 20, '2025-04-27 04:39:37', '2025-04-27 04:39:37'),
(6, 'Vladi', 2, 0, '2025-04-27 04:40:04', '2025-04-27 04:40:04'),
(7, 'Vladi', 1, 40, '2025-04-27 04:47:08', '2025-04-27 04:47:08'),
(8, 'Vladi', 1, 20, '2025-04-27 04:54:15', '2025-04-27 04:54:15'),
(9, 'Vladi', 1, 80, '2025-04-27 05:04:35', '2025-04-27 05:04:35'),
(10, 'Vladi', 1, 0, '2025-04-27 05:19:41', '2025-04-27 05:19:41'),
(11, 'Vladi', 1, 40, '2025-04-27 05:20:53', '2025-04-27 05:20:53'),
(12, 'Vladi', 1, 80, '2025-04-27 05:42:59', '2025-04-27 05:42:59'),
(13, 'Vladi', 1, 20, '2025-04-27 05:46:23', '2025-04-27 05:46:23'),
(14, 'Vladi', 1, 20, '2025-04-27 05:48:15', '2025-04-27 05:48:15'),
(15, 'Vladi', 1, 80, '2025-04-27 17:14:28', '2025-04-27 17:14:28'),
(16, 'Vladi', 1, 40, '2025-04-27 17:16:03', '2025-04-27 17:16:03'),
(17, 'Vladi', 1, 40, '2025-04-27 17:24:17', '2025-04-27 17:24:17'),
(18, 'Vladi', 1, 20, '2025-04-27 17:27:05', '2025-04-27 17:27:05'),
(19, 'Vladi', 1, 80, '2025-04-27 18:50:54', '2025-04-27 18:50:54'),
(20, 'Vladi', 1, 20, '2025-04-27 19:29:46', '2025-04-27 19:29:46'),
(21, 'Vladi', 1, 20, '2025-04-27 19:34:46', '2025-04-27 19:34:46'),
(22, 'Vladi', 1, 60, '2025-04-27 19:36:17', '2025-04-27 19:36:17'),
(23, 'Vladi', 1, 0, '2025-04-27 19:44:01', '2025-04-27 19:44:01'),
(24, 'Vladi', 1, 20, '2025-04-27 19:58:14', '2025-04-27 19:58:14'),
(25, 'Vladi', 1, 20, '2025-04-27 20:26:31', '2025-04-27 20:26:31'),
(26, 'Vladi', 1, 20, '2025-04-27 20:27:49', '2025-04-27 20:27:49'),
(27, 'Vladi', 1, 20, '2025-04-27 21:01:00', '2025-04-27 21:01:00'),
(28, 'Vladi', 2, 80, '2025-04-27 21:02:29', '2025-04-27 21:02:29'),
(29, 'Vladi', 1, 20, '2025-04-27 21:20:50', '2025-04-27 21:20:50'),
(30, 'Vladi', 1, 20, '2025-04-27 22:02:06', '2025-04-27 22:02:06'),
(31, 'Vladi', 1, 0, '2025-04-27 22:03:39', '2025-04-27 22:03:39'),
(32, 'Vladi', 1, 20, '2025-04-27 22:04:57', '2025-04-27 22:04:57'),
(33, 'Hola', 1, 40, '2025-04-27 22:16:19', '2025-04-27 22:16:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_extra`
--

CREATE TABLE `juegos_extra` (
  `id_extra` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_quiz`
--

CREATE TABLE `juegos_quiz` (
  `id_quiz` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `juegos_quiz`
--

INSERT INTO `juegos_quiz` (`id_quiz`, `titulo`, `descripcion`, `img_referencia`) VALUES
(1, 'Educación Vial 1', 'Quiz sobre normas de tránsito 1', 'juegos/quiz/game1.jpg'),
(2, 'Epa', 'Quiz sobre normas de tránsito 2', 'juegos/quiz/game2.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_sim`
--

CREATE TABLE `juegos_sim` (
  `id_sim` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfil`
--

CREATE TABLE `perfil` (
  `username` varchar(80) NOT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  `ultima_conexion` datetime DEFAULT NULL,
  `juegos_jugados` varchar(80) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `perfil`
--

INSERT INTO `perfil` (`username`, `fecha_registro`, `ultima_conexion`, `juegos_jugados`) VALUES
('Hola', NULL, NULL, '1'),
('Vladi', '2025-04-23 18:16:04', '2025-04-23 22:14:50', '1,2,');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `quiz_preguntas`
--

CREATE TABLE `quiz_preguntas` (
  `id_pregunta` int(11) NOT NULL,
  `id_quiz` int(11) DEFAULT NULL,
  `q_pregunta` varchar(500) NOT NULL,
  `opcioncorrecta` varchar(200) NOT NULL,
  `opcion2` varchar(200) NOT NULL,
  `opcion3` varchar(200) NOT NULL,
  `opcion4` varchar(200) NOT NULL,
  `explicacion` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `quiz_preguntas`
--

INSERT INTO `quiz_preguntas` (`id_pregunta`, `id_quiz`, `q_pregunta`, `opcioncorrecta`, `opcion2`, `opcion3`, `opcion4`, `explicacion`) VALUES
(1, 1, '¿Qué significa una luz roja en un semáforo?', 'Detenerse', 'Avanzar con precaución', 'Girar a la derecha', 'Cruzar rápido', ''),
(2, 1, '¿Quién tiene prioridad en un cruce peatonal sin semáforo?', 'El peatón', 'El ciclista', 'El conductor', 'El motociclista', ''),
(3, 1, '¿Cuál es el límite de velocidad en zonas escolares?', '30 km/h', '40 km/h', '60 km/h', '20 km/h', ''),
(4, 1, '¿Qué debes hacer si escuchas una sirena de ambulancia detrás?', 'Detenerte y ceder el paso', 'Ignorarla', 'Acelerar', 'Cambiar de carril sin señalizar', ''),
(5, 1, '¿Qué indica una señal de tránsito con un triángulo rojo y un símbolo de peatón?', 'Cruce peatonal', 'Zona escolar', 'Cruce peligroso', 'Alto obligatorio', ''),
(6, 2, '¿Qué debes hacer antes de cambiar de carril?', 'Usar las luces direccionales', 'Acelerar', 'Frenar', 'Nada', 'Siempre usa las luces direccionales para indicar tus movimientos.'),
(7, 2, '¿Cuál es la distancia mínima que debes mantener con el vehículo de adelante?', '3 segundos', '1 metro', '10 metros', 'Depende del clima', 'La regla de los 3 segundos permite mantener una distancia segura en condiciones normales.'),
(8, 2, '¿Qué significa una línea continua en el centro de la carretera?', 'No puedes rebasar', 'Puedes rebasar', 'Calle cerrada', 'Solo peatones', 'Una línea continua indica que no está permitido rebasar.'),
(9, 2, '¿Qué documento necesitas para conducir legalmente?', 'Licencia de conducir', 'Pasaporte', 'CURP', 'INE', 'La licencia de conducir es obligatoria para manejar legalmente.'),
(10, 2, '¿Qué hacer si se te pincha una llanta en carretera?', 'Encender luces intermitentes y orillarte', 'Frenar de golpe', 'Seguir conduciendo', 'Salir del coche en medio del camino', 'Oríllate con precaución y enciende intermitentes para evitar accidentes.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`) VALUES
(2, 'ssssssss', 'sssss@gmail.com', '$2b$12$wFZFXHJpVhzdxzn9w/MDAea.6oqQ0YWa.f51qe8SuPZX6LksaBeP2'),
(6, 'Vladi', 'vladimirlaraalejo@gmail.com', '$2b$12$5GRxpHb5CS.BNlUHyolQzOiPIvy56ko3GZ2UvTv.yHqdEWhfcIyCe'),
(7, 'Hola', 'vladimirlaraalejo@hotmail.com', '$2b$12$AdTHUjhDOR31PHXL8TEtqORy9kBoIrsQMGBPsYarspyYVTmCL0LFa');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `intentos`
--
ALTER TABLE `intentos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`);

--
-- Indices de la tabla `juegos_extra`
--
ALTER TABLE `juegos_extra`
  ADD PRIMARY KEY (`id_extra`);

--
-- Indices de la tabla `juegos_quiz`
--
ALTER TABLE `juegos_quiz`
  ADD PRIMARY KEY (`id_quiz`);

--
-- Indices de la tabla `juegos_sim`
--
ALTER TABLE `juegos_sim`
  ADD PRIMARY KEY (`id_sim`);

--
-- Indices de la tabla `perfil`
--
ALTER TABLE `perfil`
  ADD PRIMARY KEY (`username`);

--
-- Indices de la tabla `quiz_preguntas`
--
ALTER TABLE `quiz_preguntas`
  ADD PRIMARY KEY (`id_pregunta`),
  ADD KEY `id_quiz` (`id_quiz`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `intentos`
--
ALTER TABLE `intentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `juegos_extra`
--
ALTER TABLE `juegos_extra`
  MODIFY `id_extra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=200000;

--
-- AUTO_INCREMENT de la tabla `juegos_quiz`
--
ALTER TABLE `juegos_quiz`
  MODIFY `id_quiz` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `juegos_sim`
--
ALTER TABLE `juegos_sim`
  MODIFY `id_sim` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100000;

--
-- AUTO_INCREMENT de la tabla `quiz_preguntas`
--
ALTER TABLE `quiz_preguntas`
  MODIFY `id_pregunta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `intentos`
--
ALTER TABLE `intentos`
  ADD CONSTRAINT `intentos_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`);

--
-- Filtros para la tabla `perfil`
--
ALTER TABLE `perfil`
  ADD CONSTRAINT `perfil_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`);

--
-- Filtros para la tabla `quiz_preguntas`
--
ALTER TABLE `quiz_preguntas`
  ADD CONSTRAINT `quiz_preguntas_ibfk_1` FOREIGN KEY (`id_quiz`) REFERENCES `juegos_quiz` (`id_quiz`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

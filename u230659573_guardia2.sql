-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-05-2025 a las 20:50:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `intentos`
--

INSERT INTO `intentos` (`id`, `username`, `juego_id`, `puntaje`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 'olorex12', 2, 0, '2025-05-01 22:08:38', '2025-05-01 22:08:50'),
(2, 'Vladi', 1, 0, '2025-05-01 22:18:14', '2025-05-01 22:18:27'),
(3, 'Vladi', 1, 40, '2025-05-01 22:22:54', '2025-05-01 22:23:32'),
(4, 'Vladi', 1, 40, '2025-05-01 22:26:14', '2025-05-01 22:26:52'),
(5, 'Vladi', 2, 0, '2025-05-01 22:29:16', '2025-05-01 22:29:30'),
(6, 'Vladi', 1, 20, '2025-05-01 22:29:47', '2025-05-01 22:30:00'),
(7, 'Vladi', 1, 20, '2025-05-01 22:43:16', '2025-05-01 22:43:27'),
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
(31, 'ssssssss', 1, 40, '2025-05-06 01:51:49', '2025-05-06 01:52:01'),
(32, 'Vladi', 1, 20, '2025-05-07 00:10:35', '2025-05-07 00:10:51'),
(33, 'Vladi', 100000, 0, '2025-05-07 18:28:49', '2025-05-07 18:28:56');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_extra`
--

CREATE TABLE `juegos_extra` (
  `id_extra` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `juegos_extra`
--

INSERT INTO `juegos_extra` (`id_extra`, `titulo`, `descripcion`, `img_referencia`) VALUES
(200000, 'Acompleta la frase 1', 'Se mostraran una serie de frases y el usuario tendra que acompletarlas con la palabra faltante', 'juegos/extra/game200001.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_quiz`
--

CREATE TABLE `juegos_quiz` (
  `id_quiz` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `juegos_quiz`
--

INSERT INTO `juegos_quiz` (`id_quiz`, `titulo`, `descripcion`, `img_referencia`) VALUES
(1, 'Educación Vial 1', 'Quiz sobre normas de tránsito 1', 'juegos/quiz/game1.jpg'),
(2, 'Educación Vial 2', 'Quiz sobre normas de tránsito 2', 'juegos/quiz/game1.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_sim`
--

CREATE TABLE `juegos_sim` (
  `id_sim` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `juegos_sim`
--

INSERT INTO `juegos_sim` (`id_sim`, `titulo`, `descripcion`, `img_referencia`) VALUES
(100000, 'Juego simulacion 1', 'Se presenta una serie de caidas para analizar errores', 'juegos/sim/game100000.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfil`
--

CREATE TABLE `perfil` (
  `username` varchar(80) NOT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  `ultima_conexion` datetime DEFAULT NULL,
  `juegos_jugados` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `perfil`
--

INSERT INTO `perfil` (`username`, `fecha_registro`, `ultima_conexion`, `juegos_jugados`) VALUES
('Bruhcin', '2025-05-02 00:43:58', '2025-05-02 00:50:11', '1,1,1,1,1'),
('ssssssss', '2025-05-06 01:41:52', '2025-05-06 01:55:57', '0,1'),
('ssssssss2', '2025-05-06 01:56:22', '2025-05-05 20:35:36', '0'),
('Tejuino', '2025-05-07 18:18:41', '2025-05-07 18:28:24', '0'),
('UrielYO', '2025-05-02 00:58:00', '2025-05-05 21:37:44', '0'),
('Vladi', '2025-05-01 16:45:32', '2025-05-07 18:28:56', '2,2,1,1,100000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `quiz_extra`
--

CREATE TABLE `quiz_extra` (
  `id_pregunta` int(11) NOT NULL,
  `id_extra` int(11) DEFAULT NULL,
  `q_pregunta` varchar(500) NOT NULL,
  `opcioncorrecta` varchar(200) NOT NULL,
  `opcion2` varchar(200) NOT NULL,
  `opcion3` varchar(200) NOT NULL,
  `opcion4` varchar(200) NOT NULL,
  `explicacion` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `quiz_preguntas`
--

INSERT INTO `quiz_preguntas` (`id_pregunta`, `id_quiz`, `q_pregunta`, `opcioncorrecta`, `opcion2`, `opcion3`, `opcion4`, `explicacion`) VALUES
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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `quiz_simulacion`
--

CREATE TABLE `quiz_simulacion` (
  `id_pregunta` int(11) NOT NULL,
  `id_sim` int(11) DEFAULT NULL,
  `q_pregunta` varchar(500) NOT NULL,
  `url_sim` varchar(500) NOT NULL,
  `opcioncorrecta` varchar(200) NOT NULL,
  `opcion2` varchar(200) NOT NULL,
  `opcion3` varchar(200) NOT NULL,
  `opcion4` varchar(200) NOT NULL,
  `explicacion` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `quiz_simulacion`
--

INSERT INTO `quiz_simulacion` (`id_pregunta`, `id_sim`, `q_pregunta`, `url_sim`, `opcioncorrecta`, `opcion2`, `opcion3`, `opcion4`, `explicacion`) VALUES
(1, 100000, '¿Que podrian hacer los motociclistas para evitar caer?', 'simulation/Caidas.mp4', 'No frenar tan bruscamente', 'Acelerar mas', 'Inclinarse al otro lado', 'Bajarse de la moto', 'En este tipo de casos, lo mas recomendable es tener una velocidad moderada para evitar tener que usar el freno y asi evitar un derrape');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`) VALUES
(1, 'olorex12', 'sigala@gmail.com', '$2b$12$u1e3oZ3E/N296K98FG2Yv.4f2jVh2EiNMJoq3h.fgnzGOEBMlmesu'),
(2, 'Vladi', 'vladimirlaraalejo@gmail.com', '$2b$12$ZpUUFTD10EZdT75oggrZQumFpPvCNEmYCd.Tl93eKoDMvS5vfBk5e'),
(3, 'Tejuino2', 'tejuino2@gmail.com', '$2b$12$Scf1rczQ/r3PBISwgzTphOc0DxZc647uUitxSQSPzyj3P.pRwMKii'),
(5, 'Bruhcin', 'sebastian.zuniga1376@alumnos.udg.mx', '$2b$12$dOCePEY60pUM0EuUKAQpdOJSWNi5hbzm6iWiyRAFeJNAY5vWx8Iam'),
(6, 'UrielYO', 'urielbarajas@gmail.com', '$2b$12$Nmo7uWf1qMV2lkmp5L6qGuhI34EUIhyVBfMwo2W9MAAJbSwTM3/TK'),
(7, 'ssssssss', 'sssss@gmail.com', '$2b$12$K9Ee43qmISDn0Q2uB5MIx.ZvYiIpZoXk28nZR8A8TcXXjbPdtlaR6'),
(8, 'ssssssss2', 'sssss2@gmail.com', '$2b$12$.C4BtXbvrl2vUdA8SAhyxOBhE9gyZ9t2HeGQoXVE/QdNC3BLb5jT.'),
(10, 'Tejuino', 'tejuino@gmail.com', '$2b$12$f16EKLJqfKSvuye46dR5iep0Ftd5/rS9/0F0jUJDe7oCCUFIhCmb6');

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
  ADD PRIMARY KEY (`id_extra`),
  ADD KEY `ix_juegos_extra_descripcion` (`descripcion`),
  ADD KEY `ix_juegos_extra_titulo` (`titulo`);

--
-- Indices de la tabla `juegos_quiz`
--
ALTER TABLE `juegos_quiz`
  ADD PRIMARY KEY (`id_quiz`),
  ADD KEY `ix_juegos_quiz_titulo` (`titulo`),
  ADD KEY `ix_juegos_quiz_descripcion` (`descripcion`);

--
-- Indices de la tabla `juegos_sim`
--
ALTER TABLE `juegos_sim`
  ADD PRIMARY KEY (`id_sim`),
  ADD KEY `ix_juegos_sim_descripcion` (`descripcion`),
  ADD KEY `ix_juegos_sim_titulo` (`titulo`);

--
-- Indices de la tabla `perfil`
--
ALTER TABLE `perfil`
  ADD PRIMARY KEY (`username`);

--
-- Indices de la tabla `quiz_extra`
--
ALTER TABLE `quiz_extra`
  ADD PRIMARY KEY (`id_pregunta`),
  ADD KEY `id_extra` (`id_extra`);

--
-- Indices de la tabla `quiz_preguntas`
--
ALTER TABLE `quiz_preguntas`
  ADD PRIMARY KEY (`id_pregunta`),
  ADD KEY `id_quiz` (`id_quiz`);

--
-- Indices de la tabla `quiz_simulacion`
--
ALTER TABLE `quiz_simulacion`
  ADD PRIMARY KEY (`id_pregunta`),
  ADD KEY `id_sim` (`id_sim`);

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
  MODIFY `id_extra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=200001;

--
-- AUTO_INCREMENT de la tabla `juegos_quiz`
--
ALTER TABLE `juegos_quiz`
  MODIFY `id_quiz` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `juegos_sim`
--
ALTER TABLE `juegos_sim`
  MODIFY `id_sim` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100001;

--
-- AUTO_INCREMENT de la tabla `quiz_extra`
--
ALTER TABLE `quiz_extra`
  MODIFY `id_pregunta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `quiz_preguntas`
--
ALTER TABLE `quiz_preguntas`
  MODIFY `id_pregunta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `quiz_simulacion`
--
ALTER TABLE `quiz_simulacion`
  MODIFY `id_pregunta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

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
-- Filtros para la tabla `quiz_extra`
--
ALTER TABLE `quiz_extra`
  ADD CONSTRAINT `quiz_extra_ibfk_1` FOREIGN KEY (`id_extra`) REFERENCES `juegos_extra` (`id_extra`);

--
-- Filtros para la tabla `quiz_preguntas`
--
ALTER TABLE `quiz_preguntas`
  ADD CONSTRAINT `quiz_preguntas_ibfk_1` FOREIGN KEY (`id_quiz`) REFERENCES `juegos_quiz` (`id_quiz`);

--
-- Filtros para la tabla `quiz_simulacion`
--
ALTER TABLE `quiz_simulacion`
  ADD CONSTRAINT `quiz_simulacion_ibfk_1` FOREIGN KEY (`id_sim`) REFERENCES `juegos_sim` (`id_sim`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

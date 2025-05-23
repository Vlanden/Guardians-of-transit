-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 08-05-2025 a las 07:59:52
-- Versión del servidor: 8.0.42-0ubuntu0.24.04.1
-- Versión de PHP: 8.3.6

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
  `id` int NOT NULL,
  `username` varchar(80) NOT NULL,
  `juego_id` int NOT NULL,
  `puntaje` int NOT NULL,
  `fecha_inicio` datetime DEFAULT NULL,
  `fecha_fin` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `intentos`
--

INSERT INTO `intentos` (`id`, `username`, `juego_id`, `puntaje`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 'olorex12', 2, 0, '2025-05-01 22:08:38', '2025-05-01 22:08:50'),
(11, 'Bruhcin', 1, 0, '2025-05-02 00:44:36', '2025-05-02 00:45:08'),
(12, 'Bruhcin', 1, 60, '2025-05-02 00:44:36', '2025-05-02 00:46:20'),
(13, 'Bruhcin', 1, 80, '2025-05-02 00:44:36', '2025-05-02 00:47:24'),
(14, 'Bruhcin', 1, 80, '2025-05-02 00:44:36', '2025-05-02 00:48:07'),
(15, 'Bruhcin', 1, 80, '2025-05-02 00:44:36', '2025-05-02 00:48:53'),
(16, 'Bruhcin', 1, 100, '2025-05-02 00:44:36', '2025-05-02 00:49:22'),
(17, 'Bruhcin', 1, 100, '2025-05-02 00:49:35', '2025-05-02 00:50:09'),
(19, 'olorex12', 1, 60, '2025-05-05 17:40:49', '2025-05-05 17:41:29'),
(26, 'Tejuino', 1, 20, '2025-05-05 22:25:14', '2025-05-05 22:25:27'),
(27, 'Tejuino', 2, 80, '2025-05-05 22:25:38', '2025-05-05 22:25:55'),
(28, 'Tejuino', 1, 100, '2025-05-05 22:35:24', '2025-05-05 22:36:03'),
(29, 'Tejuino', 2, 60, '2025-05-05 22:36:19', '2025-05-05 22:36:55'),
(30, 'Tejuino', 1, 60, '2025-05-05 22:40:19', '2025-05-05 22:40:38'),
(31, 'ssssssss', 1, 40, '2025-05-06 01:51:49', '2025-05-06 01:52:01'),
(32, 'Vladi', 1, 20, '2025-05-07 00:10:35', '2025-05-07 00:10:51'),
(33, 'Vladi', 8, 20, '2025-05-08 06:53:09', '2025-05-08 06:53:26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_extra`
--

CREATE TABLE `juegos_extra` (
  `id_extra` int NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `juegos_extra`
--

INSERT INTO `juegos_extra` (`id_extra`, `titulo`, `descripcion`, `img_referencia`) VALUES
(200000, 'Acompleta la frase 1', 'Se mostraran una serie de frases y el usuario tendra que acompletarlas con la palabra faltante', 'juegos/quiz/game1.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_quiz`
--

CREATE TABLE `juegos_quiz` (
  `id_quiz` int NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `juegos_quiz`
--

INSERT INTO `juegos_quiz` (`id_quiz`, `titulo`, `descripcion`, `img_referencia`) VALUES
(1, 'Educación Vial 1', 'Quiz sobre normas de tránsito 1', 'juegos/quiz/game1.jpg'),
(2, 'Educación Vial 2', 'Quiz sobre normas de tránsito 2', 'juegos/quiz/game2.jpg'),
(3, 'Educación Vial 3', 'Quiz sobre señales de advertencia', 'juegos/quiz/game3.jpg'),
(4, 'Educación Vial 4', 'Quiz sobre señalización horizontal', 'juegos/quiz/game4.jpg'),
(5, 'Educación Vial 5', 'Quiz sobre normas para ciclistas', 'juegos/quiz/game5.jpg'),
(6, 'Educación Vial 6', 'Quiz de conducción defensiva', 'juegos/quiz/game6.jpg'),
(7, 'Educación Vial 7', 'Quiz sobre comportamiento peatonal', 'juegos/quiz/game7.jpg'),
(8, 'Educación Vial 8', 'Quiz sobre prioridad de paso', 'juegos/quiz/game8.jpg'),
(9, 'Educación Vial 9', 'Quiz sobre normas para motociclistas', 'juegos/quiz/game9.jpg'),
(10, 'Educación Vial 10', 'Quiz de situaciones de emergencia vial', 'juegos/quiz/game10.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos_sim`
--

CREATE TABLE `juegos_sim` (
  `id_sim` int NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `img_referencia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `juegos_sim`
--

INSERT INTO `juegos_sim` (`id_sim`, `titulo`, `descripcion`, `img_referencia`) VALUES
(100000, 'Juego simulacion 1', 'Se presenta una serie de caidas para analizar errores', 'juegos/sim/game100000.jpg'),
(100001, 'Juego de simulacion 2', 'Se presentan una serie de vides donde se graban colisiones por invadir carriles no debidos donde el usuario tendra que evaluar cual accion fue incorrecta.', 'juegos/sim/game100001.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfil`
--

CREATE TABLE `perfil` (
  `username` varchar(80) NOT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  `ultima_conexion` datetime DEFAULT NULL,
  `juegos_jugados` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `perfil`
--

INSERT INTO `perfil` (`username`, `fecha_registro`, `ultima_conexion`, `juegos_jugados`) VALUES
('Bruhcin', '2025-05-02 00:43:58', '2025-05-02 00:50:11', '1,1,1,1,1'),
('ssssssss', '2025-05-06 01:41:52', '2025-05-06 01:55:57', '0,1'),
('ssssssss2', '2025-05-06 01:56:22', '2025-05-05 20:35:36', '0'),
('Tejuino', '2025-05-01 16:45:32', '2025-05-06 01:10:46', '1,2,1,2,1'),
('UrielYO', '2025-05-02 00:58:00', '2025-05-05 21:37:44', '0'),
('Vladi', NULL, '2025-05-08 06:53:27', '8,8');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `quiz_extra`
--

CREATE TABLE `quiz_extra` (
  `id_pregunta` int NOT NULL,
  `id_extra` int DEFAULT NULL,
  `q_pregunta` varchar(500) NOT NULL,
  `opcioncorrecta` varchar(200) NOT NULL,
  `opcion2` varchar(200) NOT NULL,
  `opcion3` varchar(200) NOT NULL,
  `opcion4` varchar(200) NOT NULL,
  `explicacion` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `quiz_preguntas`
--

CREATE TABLE `quiz_preguntas` (
  `id_pregunta` int NOT NULL,
  `id_quiz` int DEFAULT NULL,
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
(1, 1, '¿Qué significa una luz roja en un semáforo?', 'Detenerse', 'Avanzar con precaución', 'Girar a la derecha', 'Cruzar rápido', 'El rojo en semáforos indica detención obligatoria.'),
(2, 1, '¿Quién tiene prioridad en un cruce peatonal sin semáforo?', 'El peatón', 'El ciclista', 'El conductor', 'El motociclista', 'Los peatones siempre tienen prioridad en cruces no señalizados.'),
(3, 1, '¿Cuál es el límite de velocidad en zonas escolares?', '30 km/h', '40 km/h', '60 km/h', '20 km/h', 'En muchas ciudades, el límite en zonas escolares es 30 km/h para proteger a los niños.'),
(4, 1, '¿Qué debes hacer si escuchas una sirena de ambulancia detrás?', 'Detenerte y ceder el paso', 'Ignorarla', 'Acelerar', 'Cambiar de carril sin señalizar', 'Debes ceder el paso a vehículos de emergencia.'),
(5, 1, '¿Qué indica una señal de tránsito con un triángulo rojo y un símbolo de peatón?', 'Cruce peatonal', 'Zona escolar', 'Cruce peligroso', 'Alto obligatorio', 'Señal de advertencia: indica proximidad a un cruce peatonal.'),
(6, 2, '¿Qué debes hacer antes de cambiar de carril?', 'Usar las luces direccionales', 'Acelerar', 'Frenar', 'Nada', 'Siempre usa las luces direccionales para indicar tus movimientos.'),
(7, 2, '¿Cuál es la distancia mínima que debes mantener con el vehículo de adelante?', '3 segundos', '1 metro', '10 metros', 'Depende del clima', 'La regla de los 3 segundos permite mantener una distancia segura en condiciones normales.'),
(8, 2, '¿Qué significa una línea continua en el centro de la carretera?', 'No puedes rebasar', 'Puedes rebasar', 'Calle cerrada', 'Solo peatones', 'Una línea continua indica que no está permitido rebasar.'),
(9, 2, '¿Qué documento necesitas para conducir legalmente?', 'Licencia de conducir', 'Pasaporte', 'CURP', 'INE', 'La licencia de conducir es obligatoria para manejar legalmente.'),
(10, 2, '¿Qué hacer si se te pincha una llanta en carretera?', 'Encender luces intermitentes y orillarte', 'Frenar de golpe', 'Seguir conduciendo', 'Salir del coche en medio del camino', 'Oríllate con precaución y enciende intermitentes para evitar accidentes.'),
(11, 3, '¿Qué forma tiene una señal de advertencia general?', 'Triángulo equilátero con borde rojo', 'Círculo con fondo azul', 'Rectángulo con borde negro', 'Óvalo con fondo amarillo', 'Las señales de advertencia son triángulos equiláteros con borde rojo para alertar de un peligro.'),
(12, 3, '¿Qué color predomina en las señales de advertencia?', 'Amarillo', 'Rojo', 'Azul', 'Verde', 'El amarillo destaca en condiciones de poca visibilidad y advierte precaución.'),
(13, 3, '¿Qué debes hacer al ver una señal de advertencia de curva peligrosa?', 'Reducir la velocidad antes de la curva', 'Mantener velocidad', 'Acelerar para pasar rápido', 'Frenar bruscamente dentro de la curva', 'Reducir velocidad con antelación evita derrapes y pérdida de control.'),
(14, 3, '¿Qué indica una señal de advertencia con un icono de pavimento resbaladizo?', 'Superficie con baja adherencia', 'Zona de construcción', 'Paso peatonal', 'Fin de vía resbaladiza', 'Advierte que la superficie puede estar mojada o resbaladiza, reduce velocidad.'),
(15, 3, '¿Qué señal advierte de un paso de peatones próximo?', 'Triángulo con peatón caminando', 'Círculo con borde rojo', 'Rectángulo azul', 'Cuadrado amarillo', 'El triángulo con la figura de un peatón indica un paso de peatones.'),
(16, 4, '¿Qué indica una línea continua amarilla en el centro de la vía?', 'Prohibición de rebasar', 'Carril exclusivo', 'Zona peatonal', 'Fin de vía', 'La línea continua prohíbe cambiar de carril o rebasar.'),
(17, 4, '¿Qué significa una doble línea blanca continua?', 'Separación de sentidos de circulación', 'Zona de estacionamiento', 'Paso de peatones', 'Carril bici', 'Dobles líneas blancas indican separación de carriles en el mismo sentido o sentidos opuestos.'),
(18, 4, '¿Qué indica una flecha pintada en el pavimento apuntando hacia la derecha?', 'Obligación de girar a la derecha', 'Prohibido girar', 'Solo recto', 'Rotonda', 'Las flechas direccionales obligan a seguir la dirección indicada.'),
(19, 4, '¿Qué indican las franjas transversales (paso de cebra)?', 'Paso de peatones', 'Zona de carga', 'Carril bici', 'Área de estacionamiento', 'Las franjas transversales marcan el cruce reservado a peatones.'),
(20, 4, '¿Qué marca un área de no estacionar en el pavimento?', 'Líneas amarillas en zigzag', 'Línea blanca discontinua', 'Flechas blancas', 'Círculo rojo pintado', 'Los zigzags o líneas amarillas continuas prohíben el estacionamiento.'),
(21, 5, '¿Dónde deben circular los ciclistas cuando existe ciclovía?', 'Dentro de la ciclovía', 'Por el arcén', 'Por la acera', 'Por el centro de la calzada', 'La ciclovía está diseñada para la seguridad de los ciclistas.'),
(22, 5, '¿Qué elemento es obligatorio para ciclistas en la noche?', 'Luces delanteras y traseras', 'Guantes', 'Botas', 'Reflectores en la ropa solamente', 'Las luces garantizan visibilidad activa y pasiva durante la noche.'),
(23, 5, '¿Cómo señaliza un ciclista que va a girar a la izquierda?', 'Brazo izquierdo extendido horizontalmente', 'Brazo derecho hacia arriba', 'Pito', 'Luces intermitentes', 'La señal manual con el brazo izquierdo informa a otros usuarios.'),
(24, 5, '¿Cuál es la distancia mínima lateral recomendada al adelantar a un ciclista?', '1.5 metros', '0.5 metros', '3 metros', '10 centímetros', 'Mantener al menos 1.5 m reduce riesgo de colisión.'),
(25, 5, '¿Qué debe hacer un ciclista al cruzar un paso peatonal?', 'Bajar de la bicicleta y cruzar como peatón', 'Cruzar pedaleando', 'Acelerar', 'Detenerse permanentemente', 'Bajar y caminar con la bicicleta es lo más seguro.'),
(26, 6, '¿Qué significa conducción defensiva?', 'Anticiparse a los riesgos', 'Conducir muy despacio', 'Ignorar señales', 'Solo usar freno motor', 'Consiste en prever situaciones para evitar accidentes.'),
(27, 6, '¿Qué regla de separación se usa para mantener distancia segura?', 'Regla de los 2 segundos', 'Regla de 5 metros', 'Regla del punto ciego', 'Regla del semáforo', 'La regla de los 2 s garantiza tiempo para reaccionar.'),
(28, 6, '¿Cómo debes ajustar tu conducción con lluvia intensa?', 'Reducir velocidad y aumentar distancia', 'Mantener velocidad', 'Acelerar', 'Frenar bruscamente', 'Adaptar velocidad y distancia evita aquaplaning.'),
(29, 6, '¿Cuál es la mejor forma de evitar puntos ciegos?', 'Mirar por los espejos y girar la cabeza', 'Confiar en sensores', 'Usar claxon', 'Cerrar los ojos', 'La comprobación visual directa permite ver áreas no cubiertas por espejos.'),
(30, 6, '¿Por qué es útil el freno motor en bajadas?', 'Evita el sobrecalentamiento de frenos', 'Acelera el vehículo', 'Apaga el motor', 'No tiene efecto', 'El freno motor reduce velocidad sin usar frenos de fricción.'),
(31, 7, '¿Dónde debe cruzar un peatón preferentemente?', 'Por el paso de cebra', 'Por la calzada', 'Por la ciclovía', 'Donde desee', 'El paso de cebra está señalizado para peatones.'),
(32, 7, '¿Qué debes hacer al cruzar con semáforo en rojo para peatones?', 'Esperar a que se ponga en verde', 'Cruzar rápido', 'Ignorar vehículos', 'Gritar', 'Respetar la señal evita accidentes.'),
(33, 7, '¿Por dónde debe caminar un peatón si hay acera disponible?', 'Por la acera', 'Por la calzada', 'Por el arcén', 'Por la ciclovía', 'La acera ofrece protección frente al tráfico.'),
(34, 7, '¿Qué hábito reduce el riesgo al cruzar la calle?', 'Dejar el móvil y mirar el tráfico', 'Escuchar música fuerte', 'Correr sin mirar', 'Charlar', 'Estar atento al entorno mejora la seguridad.'),
(35, 7, '¿Qué debes hacer antes de cruzar en intersección sin semáforo?', 'Mirar a ambos lados', 'Cerrar los ojos', 'Tirar objetos', 'Gritar', 'Comprobar tráfico en ambas direcciones es esencial.'),
(36, 8, '¿Quién tiene prioridad en una rotonda?', 'El que ya está dentro', 'El que llega', 'Los peatones', 'Los ciclistas', 'Dentro de la rotonda, los vehículos circulan con prioridad.'),
(37, 8, 'En una intersección no señalizada, ¿a quién ceder el paso?', 'Al que viene por la derecha', 'Al que viene por la izquierda', 'Nadie', 'A los peatones solamente', 'La prioridad a la derecha es norma general.'),
(38, 8, '¿Qué hacer ante un vehículo de emergencia con sirenas?', 'Detenerse y ceder el paso', 'Seguir conduciendo', 'Acelerar', 'Bloquear la vía', 'Los vehículos de emergencia tienen prioridad absoluta.'),
(39, 8, '¿Quién tiene preferencia en un paso peatonal?', 'El peatón', 'El coche', 'La bicicleta', 'El autobús', 'El peatón siempre tiene derecho de paso en el paso.'),
(40, 8, '¿Qué señal obliga a detenerse completamente?', 'Señal de Alto (stop)', 'Ceda el paso', 'Prohibido girar', 'Velocidad máxima', 'El stop exige detención total antes de continuar.'),
(41, 9, '¿Qué equipo es obligatorio para el conductor de motocicleta?', 'Casco homologado', 'Guantes de cuero', 'Botas altas', 'Chaleco reflectante', 'El casco homologado es obligatorio por seguridad.'),
(42, 9, '¿Está permitido llevar pasajero sin reposapiés trasero?', 'No, es prohibido', 'Sí, siempre', 'Solo en ciudad', 'Solo de noche', 'El reposapiés es elemento de seguridad para el pasajero.'),
(43, 9, '¿Cuándo deben llevar encendidas las luces diurnas?', 'Siempre en marcha', 'Solo de noche', 'Solo en túneles', 'Nunca', 'Las luces diurnas mejoran la visibilidad ante otros.'),
(44, 9, '¿Qué maniobra está prohibida entre carriles?', 'Circular entre vehículos', 'Rebasar por la derecha', 'Girar en U', 'Parar en línea', 'El filtering o zigzag entre carriles está prohibido.'),
(45, 9, '¿Cuál es la distancia de seguridad mínima al seguir a otro vehículo?', '2 segundos', '0.5 segundos', '5 metros', '10 metros', 'Mantener 2 s evita colisiones en frenadas.'),
(46, 10, '¿Qué debes hacer si fallan los frenos en pendiente?', 'Usar freno motor y orillar', 'Frenar bruscamente', 'Apagar motor', 'Acelerar', 'El freno motor controla la velocidad sin sobrecargar los frenos.'),
(47, 10, '¿Cómo actuar ante aquaplaning?', 'Reducir velocidad sin frenar de golpe', 'Girar el volante rápido', 'Acelerar', 'Frenar fuerte', 'Reducir velocidad suavemente recupera adherencia.'),
(48, 10, '¿Qué hacer si pinchas una llanta en carretera?', 'Encender intermitentes y orillarte', 'Seguir conduciendo', 'Frenar de golpe', 'Salir al carril contrario', 'Señalizar y detenerse fuera de la vía principal.'),
(49, 10, '¿Cómo señalizas un obstáculo en la vía de noche?', 'Colocar triángulos reflectantes', 'Usar las luces largas', 'Tocar claxon', 'Dejar coche encendido', 'Los triángulos alertan a otros conductores del peligro.'),
(50, 10, '¿Qué hacer ante una colisión leve?', 'Intercambiar datos y fotografiar daños', 'Huir del lugar', 'Pelear con el otro', 'Ignorar lo sucedido', 'Recopilar información facilita trámites de seguro.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `quiz_simulacion`
--

CREATE TABLE `quiz_simulacion` (
  `id_pregunta` int NOT NULL,
  `id_sim` int DEFAULT NULL,
  `q_pregunta` varchar(500) NOT NULL,
  `url_sim` varchar(500) NOT NULL,
  `opcioncorrecta` varchar(200) NOT NULL,
  `opcion2` varchar(200) NOT NULL,
  `opcion3` varchar(200) NOT NULL,
  `opcion4` varchar(200) NOT NULL,
  `explicacion` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `quiz_simulacion`
--

INSERT INTO `quiz_simulacion` (`id_pregunta`, `id_sim`, `q_pregunta`, `url_sim`, `opcioncorrecta`, `opcion2`, `opcion3`, `opcion4`, `explicacion`) VALUES
(1, 100000, '¿Que podrian hacer los motociclistas para evitar caer?', 'Media/Caidas.mp4', 'No frenar tan bruscamente', 'Acelerar mas', 'Inclinarse al otro lado', 'Bajarse de la moto', 'En este tipo de casos, lo mas recomendable es tener una velocidad moderada para evitar tener que usar el freno y asi evitar un derrape'),
(2, 100000, '¿Que maniobra desato el derrape?', 'Media/Caidas2.mp4', 'Girar muy rapido mientras frenaba', 'Llevar mucha carga', 'El carro blanco se adelanto', 'El piso mojado', 'Aunque todas las anteriores pueden ser causantes de un derrape, el hecho de que haya girado bruscamente y tratara de frenar, la carga genero una fuerza lateral que hiso que la cabina se desviara.'),
(3, 100000, '¿Que ocasiono el derrape del carro rojo?', 'Media/Caidas3.mp4', 'La incorporacion al otro carril', 'El exceso de velocidad', 'La colision con el machuelo', 'El carro negro disminuyo su velocidad', 'Aunque la velocidad juega un factor muy importante, al momento de cambiar de carril debes de tener un movimiento controlado, siempre midiendo distancias para evitar perder el control'),
(4, 100001, 'Como se pudo haber prevenido principalmente el accidente.', 'Media/Caidas6.mp4', 'Si el carro prendiera las direccionales', 'Si la moto acelera mas', 'Si el carro acelera mas', 'Si el carro hubiese afrenado', 'En muchas situaciones lo carros pueden llegar a tener puntos ciegos, donde es un gran punto de cuidado para los motociclistas. El acelerar o frenar de manera repentina alguno de los 2 vehiculos puede causar un accidente. Pero el motociclista hubiese podido anticipar algun movimiento si el carro encendiera las direccionales.'),
(5, 100001, '¿Cual fue el problema principal del choque?', 'Media/Caidas7.mp4', 'Usar de retorno un cruce peatonal', 'Ir a exceso de velocidad', 'Frenarse muy rapido', 'No mirar para atras', 'Todas la anteriores son faltas graves que ponen en riesgo la vida. Pero la detonante del choque fue que el carro utilizo el cruce peatonal como un retorno invadiendo el carril de la moto.'),
(6, 100001, '¿Quién realizó una maniobra peligrosa o prohibida?', 'Media/Caidas8.mp4', 'La moto', 'El carro', 'Ninguno', 'Fue un descuido leve', 'La moto al venir cambiando de carriles no se percato de que venia el carro, ademas de querer cambiar mas 1 carril en un solo movimiento.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`) VALUES
(1, 'olorex12', 'sigala@gmail.com', '$2b$12$u1e3oZ3E/N296K98FG2Yv.4f2jVh2EiNMJoq3h.fgnzGOEBMlmesu'),
(2, 'Vladi', 'vladimirlaraalejo@gmail.com', '$2b$12$P25GJBIIwDQGCGXvos4B0OOK2OqesBhNgHPUyFOOZVP2x6x/2Yk.2'),
(3, 'Tejuino2', 'tejuino2@gmail.com', '$2b$12$Scf1rczQ/r3PBISwgzTphOc0DxZc647uUitxSQSPzyj3P.pRwMKii'),
(4, 'Tejuino', 'tejuino@gmail.com', '$2b$12$HAWuOw3chT2axYvLT7t4aOPQNUmrtQu3FKL2HcL.Wu9WO1Q81Nflm'),
(5, 'Bruhcin', 'sebastian.zuniga1376@alumnos.udg.mx', '$2b$12$dOCePEY60pUM0EuUKAQpdOJSWNi5hbzm6iWiyRAFeJNAY5vWx8Iam'),
(6, 'UrielYO', 'urielbarajas@gmail.com', '$2b$12$Nmo7uWf1qMV2lkmp5L6qGuhI34EUIhyVBfMwo2W9MAAJbSwTM3/TK'),
(7, 'ssssssss', 'sssss@gmail.com', '$2b$12$K9Ee43qmISDn0Q2uB5MIx.ZvYiIpZoXk28nZR8A8TcXXjbPdtlaR6'),
(8, 'ssssssss2', 'sssss2@gmail.com', '$2b$12$.C4BtXbvrl2vUdA8SAhyxOBhE9gyZ9t2HeGQoXVE/QdNC3BLb5jT.');

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
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `juegos_extra`
--
ALTER TABLE `juegos_extra`
  MODIFY `id_extra` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=200001;

--
-- AUTO_INCREMENT de la tabla `juegos_quiz`
--
ALTER TABLE `juegos_quiz`
  MODIFY `id_quiz` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `juegos_sim`
--
ALTER TABLE `juegos_sim`
  MODIFY `id_sim` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100003;

--
-- AUTO_INCREMENT de la tabla `quiz_extra`
--
ALTER TABLE `quiz_extra`
  MODIFY `id_pregunta` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `quiz_preguntas`
--
ALTER TABLE `quiz_preguntas`
  MODIFY `id_pregunta` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `quiz_simulacion`
--
ALTER TABLE `quiz_simulacion`
  MODIFY `id_pregunta` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

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

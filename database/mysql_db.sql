USE parrilla_argentina;

CREATE TABLE IF NOT EXISTS combos (
    id_combo        INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(30) NOT NULL,
    precio          DECIMAL(8, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario      INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(30) NOT NULL,
    contraseña      VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS combo_detalle (
    id_combo        INT NOT NULL,
    id_producto     INT NOT NULL,
    FOREIGN KEY (id_combo) REFERENCES combos(id_combo),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

CREATE TABLE IF NOT EXISTS combo_version (
    id_version      INT AUTO_INCREMENT PRIMARY KEY,
    descripcion     VARCHAR(50) NOT NULL,
    personas        INT NOT NULL,
    precio          DECIMAL(8, 2) NOT NULL,
    id_combo        INT NOT NULL,
    FOREIGN KEY (id_combo) REFERENCES combos(id_combo)
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto     INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    descripcion     TEXT,
    precio          DECIMAL(10,2) NOT NULL,
    categoria       ENUM('entrada','principal','postre','bebida') NOT NULL,
    lactosa         BOOLEAN DEFAULT FALSE,
    vegetariano     BOOLEAN DEFAULT FALSE,
    vegano          BOOLEAN DEFAULT FALSE,
    sin_tacc        BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS reservas (
    id_reserva      INT AUTO_INCREMENT PRIMARY KEY,
    cant_personas   INT NOT NULL CHECK (cant_personas > 0),
    horario         TIME NOT NULL,
    dia             DATE NOT NULL,
    mesa            INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS reseñas (
    id_reseña       INT AUTO_INCREMENT PRIMARY KEY,
    descripcion     VARCHAR(1000) NOT NULL
);

CREATE TABLE IF NOT EXISTS servicios_extra (
    id_servicio     INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    descripcion     VARCHAR(255)
);

INSERT INTO combos (nombre, precio) VALUES
('Ejecutivo', 12500),
('Infantil', 6500);

INSERT INTO usuarios (nombre, contraseña) VALUES
('Admin', 'admin1234'),
('Martina Bencardino', 'mart1234');

INSERT INTO productos (nombre, descripcion, precio, categoria, lactosa, vegetariano, vegano, sin_tacc) VALUES
('Mini hamburguesita con papas fritas', 'Hamburguesa en pan chico con queso cheddar y papas crocantes', 2500, 'principal', TRUE, FALSE, FALSE, FALSE),
('Mini Choripan', 'Chorizo suave en pan chico con papas fritas', 2200, 'principal', FALSE, FALSE, FALSE, FALSE),
('Milanesitas con Puré', 'Tiritas de milanesa de pollo con puré de papa', 2400, 'principal', TRUE, FALSE, FALSE, FALSE),
('Asado de tira', 'Corte clásico a la parrilla', 8500, 'principal', FALSE, FALSE, FALSE, TRUE),
('Vacío', 'Corte tierno con chimichurri casero', 9200, 'principal', FALSE, FALSE, FALSE, TRUE),
('Chorizo criollo', 'Chorizo artesanal a las brasas', 3200, 'entrada', FALSE, FALSE, FALSE, TRUE),
('Morcilla', 'Morcilla casera a la parrilla', 2800, 'entrada', FALSE, FALSE, FALSE, TRUE),
('Provoleta', 'Queso provolone a la parrilla con orégano', 3500, 'entrada', TRUE, TRUE, FALSE, TRUE),
('Ensalada mixta', 'Lechuga, tomate, zanahoria y choclo', 2100, 'entrada', FALSE, TRUE, TRUE, TRUE),
('Flan casero', 'Con dulce de leche y crema', 1800, 'postre', TRUE, TRUE, FALSE, FALSE),
('Agua mineral', '500ml sin gas o con gas', 900, 'bebida', FALSE, TRUE, TRUE, TRUE),
('Gaseosa', 'Coca-Cola, Sprite o Fanta 350ml', 1200, 'bebida', FALSE, TRUE, TRUE, TRUE);

INSERT INTO reservas (id_usuario, cant_personas, dia, horario, mesa) VALUES
(1, 4, '2026-06-15', '20:00:00', 1),
(2, 2, '2026-06-20', '13:00:00', 2);

INSERT INTO reseñas (descripcion) VALUES
('Excelente experiencia. La carne llegó en el punto justo, súper tierna y con mucho sabor. Sin duda volvería.'),
('La provoleta una bomba. El servicio muy atento, re recomendado.'),
('El menú infantil estuvo genial, los chicos felices con las milanesitas.');

INSERT INTO servicios_extra (nombre, descripcion) VALUES
('Acceso para discapacitados', 'Rampas y espacios adaptados para personas con movilidad reducida'),
('Estacionamiento gratuito', 'Playa de estacionamiento gratuita dentro de la Parrilla'),
('Show del asador', 'Degustación de cortes premium con show en vivo del asador');

INSERT INTO combo_detalle (id_combo, id_producto) VALUES
(1, 4),
(1, 7),
(2, 1),
(2, 3);

INSERT INTO combo_version (descripcion, personas, precio, id_combo) VALUES
('Combo ejecutivo enero 2026', 2, 12500, 1),
('Combo infantil enero 2026', 1, 6500, 2);

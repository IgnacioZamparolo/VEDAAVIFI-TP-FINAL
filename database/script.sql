USE parrilla_argentina;

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
    id_usuario      INT NOT NULL,
    total_personas  INT NOT NULL CHECK (total_personas > 0),
    fecha           DATE NOT NULL,
    hora            TIME NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS reseñas (
    id_reseña       INT AUTO_INCREMENT PRIMARY KEY,
    descripcion     VARCHAR(1000) NOT NULL
);

CREATE TABLE IF NOT EXISTS combos_version (
    id_version      INT AUTO_INCREMENT PRIMARY KEY,
    id_combo        INT NOT NULL,
    fecha_inicio    DATE NOT NULL,
    precio          DECIMAL(10,2) NOT NULL,
    activo          BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_combo) REFERENCES combos(id_combo)
);

INSERT INTO productos (nombre, descripcion, precio, categoria, lactosa, vegetariano, vegano, sin_tacc) VALUES
('Mini hamburguesita con papas fritas', 'Hamburguesa en pan chico con queso cheddar y papas crocantes', 2500, 'principal', TRUE, FALSE, FALSE, FALSE),
('Mini Choripan', 'Chorizo suave en pan chico con papas fritas', 2200, 'principal', FALSE, FALSE, FALSE, FALSE),
('Milanesitas con Puré', 'Tiritas de milanesa de pollo con puré de papa', 2400, 'principal', TRUE, FALSE, FALSE, FALSE);

INSERT INTO productos (nombre, descripcion, precio, categoria, lactosa, vegetariano, vegano, sin_tacc) VALUES
('Asado de tira', 'Corte clásico a la parrilla', 8500, 'principal', FALSE, FALSE, FALSE, TRUE),
('Vacío', 'Corte tierno con chimichurri casero', 9200, 'principal', FALSE, FALSE, FALSE, TRUE),
('Chorizo criollo', 'Chorizo artesanal a las brasas', 3200, 'entrada', FALSE, FALSE, FALSE, TRUE),
('Morcilla', 'Morcilla casera a la parrilla', 2800, 'entrada', FALSE, FALSE, FALSE, TRUE),
('Provoleta', 'Queso provolone a la parrilla con orégano', 3500, 'entrada', TRUE, TRUE, FALSE, TRUE),
('Ensalada mixta', 'Lechuga, tomate, zanahoria y choclo', 2100, 'entrada', FALSE, TRUE, TRUE, TRUE),
('Flan casero', 'Con dulce de leche y crema', 1800, 'postre', TRUE, TRUE, FALSE, FALSE),
('Agua mineral', '500ml sin gas o con gas', 900, 'bebida', FALSE, TRUE, TRUE, TRUE),
('Gaseosa', 'Coca-Cola, Sprite o Fanta 350ml', 1200, 'bebida', FALSE, TRUE, TRUE, TRUE);


INSERT INTO reservas (id_usuario, total_personas, fecha, hora) VALUES
(1, 4, '2026-06-15', '20:00:00'),
(1, 2, '2026-06-20', '13:00:00');

INSERT INTO resenias (descripcion) VALUES
('Excelente experiencia. La carne llegó en el punto justo, súper tierna y con mucho sabor. La tabla parrillera estaba muy bien servida. Sin duda volvería.'),
('La provoleta una bomba. El servicio muy atento, re recomendado.'),
('El menú infantil estuvo genial, los chicos felices con las milanesitas.');

INSERT INTO combos_version (id_combo, fecha_inicio, precio, activo) VALUES
(1, '2026-01-01', 12500, TRUE),   
(2, '2026-01-01', 6500, TRUE);    
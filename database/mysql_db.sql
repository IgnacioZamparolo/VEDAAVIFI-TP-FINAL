CREATE TABLE Combos (
    id_combo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    precio DECIMAL(8, 2) NOT NULL;
)

CREATE TABLE Combo_detalle (
    id_combo INT NOT NULL,
    id_producto INT NOT NULL,
    FOREIGN KEY (id_combo) REFERENCES Combos(id_combo),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto);
)

CREATE TABLE Combo_version (
    id_version INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL,
    personas INT NOT NULL,
    precio DECIMAL(8, 2) NOT NULL,
    id_combo INT NOT NULL,
    FOREIGN KEY (id_combo) REFERENCES Combos(id_combo);
)

CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    contraseña VARCHAR(10) NOT NULL;
)


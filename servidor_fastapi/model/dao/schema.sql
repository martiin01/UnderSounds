-- Tabla para los usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    tipo_usuario TEXT CHECK(tipo_usuario IN ('artista', 'usuario')) NOT NULL,
    nombre_banda TEXT
);

-- Tabla para los productos
CREATE TABLE IF NOT EXISTS productos (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    imagen TEXT NOT NULL,
    precio REAL NOT NULL,
    fecha TEXT NOT NULL,
    tipo TEXT NOT NULL,
    estilo TEXT NOT NULL,
    autor TEXT NOT NULL,
    FOREIGN KEY (autor) REFERENCES usuarios (id) ON DELETE CASCADE
);

-- Tabla para el carrito
CREATE TABLE IF NOT EXISTS carrito (
    idUser TEXT NOT NULL,
    idProducto TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    PRIMARY KEY (idUser, idProducto),
    FOREIGN KEY (idUser) REFERENCES usuarios (id) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES productos (id) ON DELETE CASCADE
);

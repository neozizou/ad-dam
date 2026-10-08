-- Estructura de la base de datos de la tienda.
-- Válida para MariaDB y para H2 en modo MariaDB. Se puede ejecutar varias veces.

CREATE TABLE IF NOT EXISTS categoria (
    id      INT          AUTO_INCREMENT PRIMARY KEY,
    nombre  VARCHAR(50)  NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS producto (
    codigo        VARCHAR(10)     PRIMARY KEY,
    nombre        VARCHAR(100)    NOT NULL,
    precio        DECIMAL(10, 2)  NOT NULL CHECK (precio >= 0),
    stock         INT             NOT NULL DEFAULT 0 CHECK (stock >= 0),
    categoria_id  INT             NULL,
    CONSTRAINT fk_producto_categoria FOREIGN KEY (categoria_id) REFERENCES categoria (id)
);

CREATE TABLE IF NOT EXISTS cliente (
    id          INT           AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100)  NOT NULL,
    email       VARCHAR(100)  NOT NULL UNIQUE,
    fecha_alta  DATE          NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido (
    numero      INT          AUTO_INCREMENT PRIMARY KEY,
    cliente_id  INT          NOT NULL,
    fecha       DATE         NOT NULL,
    estado      VARCHAR(10)  NOT NULL
        CHECK (estado IN ('PENDIENTE', 'PAGADO', 'ENVIADO', 'ENTREGADO', 'CANCELADO')),
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (cliente_id) REFERENCES cliente (id)
);

CREATE TABLE IF NOT EXISTS linea_pedido (
    pedido_numero    INT             NOT NULL,
    producto_codigo  VARCHAR(10)     NOT NULL,
    cantidad         INT             NOT NULL CHECK (cantidad > 0),
    precio_unitario  DECIMAL(10, 2)  NOT NULL CHECK (precio_unitario >= 0),
    PRIMARY KEY (pedido_numero, producto_codigo),
    CONSTRAINT fk_linea_pedido FOREIGN KEY (pedido_numero) REFERENCES pedido (numero) ON DELETE CASCADE,
    CONSTRAINT fk_linea_producto FOREIGN KEY (producto_codigo) REFERENCES producto (codigo)
);

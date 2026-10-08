-- Datos de ejemplo. La aplicación los carga si la tabla producto está vacía.

INSERT INTO categoria (nombre) VALUES ('Periféricos'), ('Monitores'), ('Cables');

INSERT INTO producto (codigo, nombre, precio, stock, categoria_id) VALUES
    ('TEC01', 'Teclado mecánico',    59.90, 12, 1),
    ('RAT01', 'Ratón inalámbrico',   24.50, 30, 1),
    ('MON01', 'Monitor 27 pulgadas', 219.00, 4, 2),
    ('CAB01', 'Cable USB-C 2 m',      8.95,  0, 3);

INSERT INTO cliente (nombre, email, fecha_alta) VALUES
    ('Ana Martín',   'ana@example.com',   '2026-09-01'),
    ('Luis Romero',  'luis@example.com',  '2026-09-15'),
    ('Carmen Ortiz', 'carmen@example.com', '2026-10-02');

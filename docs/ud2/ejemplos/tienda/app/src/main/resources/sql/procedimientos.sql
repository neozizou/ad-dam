-- Procedimientos almacenados. Solo para MariaDB (H2 no admite CREATE PROCEDURE).
-- Se puede ejecutar desde el cliente de MariaDB o desde Java con EjecutorScripts:
-- DELIMITER cambia el final de sentencia para que los ';' de dentro no la corten.

DELIMITER //

-- Devuelve, como resultado de una consulta, los productos con menos unidades que el mínimo
CREATE OR REPLACE PROCEDURE productos_bajo_minimo(IN p_minimo INT)
BEGIN
    SELECT codigo, nombre, stock
      FROM producto
     WHERE stock < p_minimo
     ORDER BY stock, codigo;
END //

-- Calcula en un parámetro de salida el valor (precio × stock) de una categoría
CREATE OR REPLACE PROCEDURE valor_categoria(IN p_categoria INT, OUT p_valor DECIMAL(12, 2))
BEGIN
    SELECT COALESCE(SUM(precio * stock), 0)
      INTO p_valor
      FROM producto
     WHERE categoria_id = p_categoria;
END //

DELIMITER ;

package es.dam.tienda.modelo;

import java.math.BigDecimal;

/** Una línea de un pedido: qué producto, cuántas unidades y a qué precio. */
public record LineaPedido(Producto producto, int cantidad, BigDecimal precioUnitario) {

    public LineaPedido {                          // constructor compacto: solo validaciones
        if (cantidad <= 0) {
            throw new IllegalArgumentException("Cantidad no válida: " + cantidad);
        }
    }

    public BigDecimal importe() {
        return precioUnitario.multiply(BigDecimal.valueOf(cantidad));
    }
}

package es.dam.tienda.modelo;

import java.math.BigDecimal;

/** Una fila del informe de ventas: lo vendido de una categoría. */
public record VentasCategoria(String categoria, int unidades, BigDecimal importe) {
}

package es.dam.tienda.modelo;

/** Se lanza cuando un pedido pide más unidades de las que hay en stock. */
public class StockInsuficienteException extends RuntimeException {

    public StockInsuficienteException(String codigo, int unidades) {
        super("No hay stock suficiente de " + codigo + " para servir " + unidades + " unidades");
    }
}

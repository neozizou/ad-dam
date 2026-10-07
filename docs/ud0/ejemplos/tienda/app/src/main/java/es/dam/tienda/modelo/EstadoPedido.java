package es.dam.tienda.modelo;

/** Estados por los que pasa un pedido. */
public enum EstadoPedido {
    PENDIENTE, PAGADO, ENVIADO, ENTREGADO, CANCELADO;

    /** Un pedido entregado o cancelado ya no puede cambiar de estado. */
    public boolean esFinal() {
        return this == ENTREGADO || this == CANCELADO;
    }
}

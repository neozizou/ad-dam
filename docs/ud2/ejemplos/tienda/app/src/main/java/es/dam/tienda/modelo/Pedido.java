package es.dam.tienda.modelo;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/** Un pedido de un cliente, con sus líneas. */
public class Pedido {

    private Integer numero;                  // null hasta que la base de datos lo asigna
    private final int clienteId;
    private final LocalDate fecha;
    private EstadoPedido estado;
    private final List<LineaPedido> lineas = new ArrayList<>();

    /** Crea un pedido nuevo, pendiente y todavía sin número. */
    public Pedido(int clienteId, LocalDate fecha) {
        this(null, clienteId, fecha, EstadoPedido.PENDIENTE);
    }

    /** Reconstruye un pedido leído de la base de datos. */
    public Pedido(Integer numero, int clienteId, LocalDate fecha, EstadoPedido estado) {
        this.numero = numero;
        this.clienteId = clienteId;
        this.fecha = fecha;
        this.estado = estado;
    }

    /**
     * Añade unidades de un producto al precio actual. Si el producto ya estaba
     * en el pedido, suma las unidades a su línea.
     */
    public void agregar(Producto producto, int cantidad) {
        for (int i = 0; i < lineas.size(); i++) {
            LineaPedido linea = lineas.get(i);
            if (linea.producto().equals(producto)) {
                lineas.set(i, new LineaPedido(producto, linea.cantidad() + cantidad, linea.precioUnitario()));
                return;
            }
        }
        lineas.add(new LineaPedido(producto, cantidad, producto.getPrecio()));
    }

    /** Añade una línea tal como está guardada (con su precio de entonces). */
    public void agregarLinea(LineaPedido linea) {
        lineas.add(linea);
    }

    /** @return suma de los importes de las líneas */
    public BigDecimal total() {
        return lineas.stream().map(LineaPedido::importe).reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    public Integer getNumero() { return numero; }

    /** Lo usa el repositorio cuando la base de datos ha generado el número. */
    public void asignarNumero(int numero) { this.numero = numero; }

    public int getClienteId() { return clienteId; }

    public LocalDate getFecha() { return fecha; }

    public EstadoPedido getEstado() { return estado; }

    public List<LineaPedido> getLineas() { return List.copyOf(lineas); }
}

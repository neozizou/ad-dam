package es.dam.tienda.servicio;

import es.dam.tienda.modelo.Pedido;
import es.dam.tienda.modelo.VentasCategoria;
import es.dam.tienda.repositorio.PedidoRepository;
import es.dam.tienda.repositorio.ProductoRepository;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/** Reglas de negocio sobre los pedidos. */
public class PedidoService {

    private final PedidoRepository pedidos;
    private final ProductoRepository productos;

    public PedidoService(PedidoRepository pedidos, ProductoRepository productos) {
        this.pedidos = pedidos;
        this.productos = productos;
    }

    /**
     * Registra un pedido con los precios actuales de los productos.
     *
     * @param lineas unidades pedidas de cada producto, por código
     * @return el número del pedido
     * @throws ProductoNoEncontradoException si algún código no existe
     * @throws es.dam.tienda.modelo.StockInsuficienteException si falta stock
     */
    public int registrar(int clienteId, Map<String, Integer> lineas) {
        if (lineas.isEmpty()) {
            throw new IllegalArgumentException("El pedido no tiene ninguna línea");
        }
        Pedido pedido = new Pedido(clienteId, LocalDate.now());
        lineas.forEach((codigo, cantidad) -> pedido.agregar(
                productos.buscarPorCodigo(codigo).orElseThrow(() -> new ProductoNoEncontradoException(codigo)),
                cantidad));
        return pedidos.guardar(pedido);
    }

    /** @throws IllegalArgumentException si no existe */
    public Pedido buscar(int numero) {
        return pedidos.buscarPorNumero(numero)
                .orElseThrow(() -> new IllegalArgumentException("No existe el pedido " + numero));
    }

    public List<VentasCategoria> ventasPorCategoria() {
        return pedidos.ventasPorCategoria();
    }
}

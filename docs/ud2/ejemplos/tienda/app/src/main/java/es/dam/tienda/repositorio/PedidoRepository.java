package es.dam.tienda.repositorio;

import es.dam.tienda.modelo.Pedido;
import es.dam.tienda.modelo.VentasCategoria;
import java.util.List;
import java.util.Optional;

/** Operaciones de almacenamiento de pedidos. */
public interface PedidoRepository {

    /**
     * Guarda un pedido nuevo con sus líneas y descuenta del stock las unidades
     * pedidas. Se hace todo o no se hace nada.
     *
     * @return el número que la base de datos asigna al pedido
     * @throws es.dam.tienda.modelo.StockInsuficienteException si falta stock de algún producto
     */
    int guardar(Pedido pedido);

    /** @return el pedido con sus líneas, o vacío si no existe */
    Optional<Pedido> buscarPorNumero(int numero);

    /** @return unidades e importe vendidos de cada categoría, de mayor a menor importe */
    List<VentasCategoria> ventasPorCategoria();
}

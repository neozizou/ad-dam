package es.dam.tienda.fichero;

import es.dam.tienda.modelo.Producto;
import java.io.Serializable;
import java.math.BigDecimal;

/**
 * Un producto tal como se guarda en un fichero: datos planos, sin comportamiento.
 * Separa el formato de los ficheros de la clase del modelo.
 */
public record ProductoDto(String codigo, String nombre, BigDecimal precio, int stock)
        implements Serializable {

    /** Copia los datos de un producto del modelo. */
    public static ProductoDto desde(Producto producto) {
        return new ProductoDto(producto.getCodigo(), producto.getNombre(),
                producto.getPrecio(), producto.getStock());
    }

    /** Crea un producto del modelo; su constructor valida los datos leídos. */
    public Producto aProducto() {
        return new Producto(codigo, nombre, precio, stock);
    }
}

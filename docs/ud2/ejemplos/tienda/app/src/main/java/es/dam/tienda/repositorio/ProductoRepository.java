package es.dam.tienda.repositorio;

import es.dam.tienda.modelo.Producto;
import java.util.List;
import java.util.Optional;

/**
 * Operaciones de almacenamiento de productos.
 * <p>
 * Define <em>qué</em> se puede hacer con los productos guardados, no
 * <em>cómo</em> se guardan. Cada unidad del curso añadirá una implementación
 * nueva (memoria, fichero JSON, JDBC, JPA, ObjectDB, MongoDB) sin cambiar
 * esta interfaz.
 */
public interface ProductoRepository {

    /**
     * Guarda un producto: lo da de alta si su código no existe y lo
     * reemplaza si ya existía.
     *
     * @param producto el producto a guardar; no puede ser {@code null}
     */
    void guardar(Producto producto);

    /**
     * Busca un producto por su código.
     *
     * @param codigo código del producto
     * @return el producto, o un {@code Optional} vacío si no existe
     */
    Optional<Producto> buscarPorCodigo(String codigo);

    /** @return todos los productos guardados; nunca {@code null} */
    List<Producto> buscarTodos();

    /**
     * Elimina un producto.
     *
     * @param codigo código del producto
     * @return {@code true} si existía y se ha eliminado
     */
    boolean borrar(String codigo);

    /** @return {@code true} si hay un producto con ese código */
    default boolean existe(String codigo) {
        return buscarPorCodigo(codigo).isPresent();
    }
}

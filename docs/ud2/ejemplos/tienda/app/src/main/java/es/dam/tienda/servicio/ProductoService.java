package es.dam.tienda.servicio;

import es.dam.tienda.fichero.Formatos;
import es.dam.tienda.fichero.ProductoDto;
import es.dam.tienda.modelo.Producto;
import es.dam.tienda.repositorio.AccesoDatosException;
import es.dam.tienda.repositorio.ProductoRepository;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.List;

/**
 * Reglas de negocio sobre los productos.
 * Trabaja con la interfaz {@link ProductoRepository}: no sabe ni le importa
 * dónde se guardan los datos.
 */
public class ProductoService {

    private final ProductoRepository repositorio;

    public ProductoService(ProductoRepository repositorio) {
        this.repositorio = repositorio;
    }

    /**
     * Da de alta un producto nuevo.
     *
     * @throws IllegalStateException si ya existe un producto con ese código
     */
    public void alta(Producto producto) {
        if (repositorio.existe(producto.getCodigo())) {
            throw new IllegalStateException("Ya existe un producto con código " + producto.getCodigo());
        }
        repositorio.guardar(producto);
    }

    /** @return los productos ordenados por nombre */
    public List<Producto> listar() {
        return repositorio.buscarTodos().stream()
                .sorted(Comparator.comparing(Producto::getNombre))
                .toList();
    }

    /** @throws ProductoNoEncontradoException si no existe */
    public Producto buscar(String codigo) {
        return repositorio.buscarPorCodigo(codigo)
                .orElseThrow(() -> new ProductoNoEncontradoException(codigo));
    }

    public void cambiarPrecio(String codigo, BigDecimal nuevoPrecio) {
        Producto producto = buscar(codigo);
        producto.setPrecio(nuevoPrecio);
        repositorio.guardar(producto);   // en memoria sobra; con un fichero o una BD es imprescindible
    }

    /** @throws ProductoNoEncontradoException si no existe */
    public void baja(String codigo) {
        if (!repositorio.borrar(codigo)) {
            throw new ProductoNoEncontradoException(codigo);
        }
    }

    /** @return suma de precio × stock de todos los productos */
    public BigDecimal valorInventario() {
        return repositorio.buscarTodos().stream()
                .map(p -> p.getPrecio().multiply(BigDecimal.valueOf(p.getStock())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    /**
     * Exporta el catálogo, ordenado por nombre, a un fichero cuyo formato
     * se deduce de su extensión (csv, json, xml o dat).
     *
     * @return número de productos exportados
     * @throws AccesoDatosException si no se puede escribir el fichero
     */
    public int exportar(Path destino) {
        List<ProductoDto> productos = listar().stream().map(ProductoDto::desde).toList();
        try {
            Files.createDirectories(destino.toAbsolutePath().getParent());
            Formatos.porExtension(destino).escribir(destino, productos);
        } catch (IOException e) {
            throw new AccesoDatosException("No se pudo exportar a " + destino, e);
        }
        return productos.size();
    }
}

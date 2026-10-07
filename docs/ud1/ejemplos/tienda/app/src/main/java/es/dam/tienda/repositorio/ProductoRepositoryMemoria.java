package es.dam.tienda.repositorio;

import es.dam.tienda.modelo.Producto;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/** Implementación en memoria: los datos se pierden al cerrar el programa. */
public class ProductoRepositoryMemoria implements ProductoRepository {

    private final Map<String, Producto> productos = new LinkedHashMap<>();

    @Override
    public void guardar(Producto producto) {
        productos.put(producto.getCodigo(), producto);
    }

    @Override
    public Optional<Producto> buscarPorCodigo(String codigo) {
        return Optional.ofNullable(productos.get(codigo));
    }

    @Override
    public List<Producto> buscarTodos() {
        return List.copyOf(productos.values());
    }

    @Override
    public boolean borrar(String codigo) {
        return productos.remove(codigo) != null;
    }
}

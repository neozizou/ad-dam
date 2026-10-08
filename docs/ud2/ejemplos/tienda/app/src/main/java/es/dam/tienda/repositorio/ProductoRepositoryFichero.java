package es.dam.tienda.repositorio;

import es.dam.tienda.fichero.FormatoProductos;
import es.dam.tienda.fichero.ProductoDto;
import es.dam.tienda.modelo.Producto;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Guarda los productos en un fichero. Al crearse lee el fichero completo y, tras
 * cada cambio, lo reescribe entero de forma segura (fichero temporal + movimiento atómico).
 */
public class ProductoRepositoryFichero implements ProductoRepository {

    private final Path ruta;
    private final FormatoProductos formato;
    private final Map<String, ProductoDto> datos = new LinkedHashMap<>();

    /**
     * @param ruta fichero de datos; si no existe, el repositorio empieza vacío
     * @param formato formato del fichero
     * @throws AccesoDatosException si el fichero existe pero no se puede leer
     */
    public ProductoRepositoryFichero(Path ruta, FormatoProductos formato) {
        this.ruta = ruta;
        this.formato = formato;
        cargar();
    }

    @Override
    public void guardar(Producto producto) {
        datos.put(producto.getCodigo(), ProductoDto.desde(producto));
        escribirFichero();
    }

    @Override
    public Optional<Producto> buscarPorCodigo(String codigo) {
        return Optional.ofNullable(datos.get(codigo)).map(ProductoDto::aProducto);
    }

    @Override
    public List<Producto> buscarTodos() {
        return datos.values().stream().map(ProductoDto::aProducto).toList();
    }

    @Override
    public boolean borrar(String codigo) {
        if (datos.remove(codigo) == null) {
            return false;
        }
        escribirFichero();
        return true;
    }

    private void cargar() {
        if (Files.notExists(ruta)) {
            return;                                   // primera ejecución: catálogo vacío
        }
        try {
            for (ProductoDto dto : formato.leer(ruta)) {
                dto.aProducto();                      // valida: lanza si los datos no son correctos
                datos.put(dto.codigo(), dto);
            }
        } catch (IOException | IllegalArgumentException e) {
            throw new AccesoDatosException("No se pudo cargar " + ruta, e);
        }
    }

    private void escribirFichero() {
        try {
            Files.createDirectories(ruta.toAbsolutePath().getParent());
            Path temporal = ruta.resolveSibling(ruta.getFileName() + ".tmp");   // productos.json.tmp
            try {
                formato.escribir(temporal, List.copyOf(datos.values()));
                Files.move(temporal, ruta, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);
            } finally {
                Files.deleteIfExists(temporal);       // solo queda si algo ha fallado
            }
        } catch (IOException e) {
            throw new AccesoDatosException("No se pudo guardar " + ruta, e);
        }
    }
}

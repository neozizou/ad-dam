package es.dam.tienda.fichero;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

/** Un formato de fichero capaz de leer y escribir una lista de productos. */
public interface FormatoProductos {

    /**
     * Lee todos los productos de un fichero.
     *
     * @param ruta fichero que se va a leer
     * @return los productos, en el orden en que aparecen en el fichero
     * @throws IOException si el fichero no se puede leer o su contenido no es válido
     */
    List<ProductoDto> leer(Path ruta) throws IOException;

    /**
     * Escribe los productos en un fichero, reemplazando su contenido.
     *
     * @param ruta fichero que se va a escribir
     * @param productos productos que se guardan
     * @throws IOException si el fichero no se puede escribir
     */
    void escribir(Path ruta, List<ProductoDto> productos) throws IOException;
}

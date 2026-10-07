package es.dam.tienda.fichero;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

/** Elige el formato según la extensión del fichero y convierte entre formatos. */
public final class Formatos {

    private Formatos() {
    }

    /**
     * @param ruta fichero cuya extensión decide el formato: csv, json, xml o dat
     * @throws IllegalArgumentException si la extensión no es ninguna de ellas
     */
    public static FormatoProductos porExtension(Path ruta) {
        String nombre = ruta.getFileName().toString().toLowerCase();
        String extension = nombre.substring(nombre.lastIndexOf('.') + 1);
        return switch (extension) {
            case "csv" -> new FormatoCsv();
            case "json" -> new FormatoJson();
            case "xml" -> new FormatoXml();
            case "dat" -> new FormatoBinario();
            default -> throw new IllegalArgumentException("Formato no admitido: " + nombre);
        };
    }

    /**
     * Convierte un fichero de productos a otro formato.
     *
     * @return número de productos convertidos
     */
    public static int convertir(Path origen, Path destino) throws IOException {
        List<ProductoDto> productos = porExtension(origen).leer(origen);
        porExtension(destino).escribir(destino, productos);
        return productos.size();
    }
}

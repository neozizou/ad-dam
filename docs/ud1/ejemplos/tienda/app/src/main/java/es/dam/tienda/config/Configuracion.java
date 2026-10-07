package es.dam.tienda.config;

import java.io.IOException;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

/** Configuración de la aplicación, leída de un fichero .properties. */
public class Configuracion {

    private final Properties propiedades = new Properties();

    /**
     * Carga el fichero si existe; si no existe, se usan los valores por defecto.
     *
     * @throws UncheckedIOException si el fichero existe pero no se puede leer
     */
    public Configuracion(Path fichero) {
        if (Files.exists(fichero)) {
            try (Reader lector = Files.newBufferedReader(fichero)) {   // UTF-8
                propiedades.load(lector);
            } catch (IOException e) {
                throw new UncheckedIOException("No se pudo leer " + fichero, e);
            }
        }
    }

    /** @return ruta del fichero de datos; su extensión decide el formato */
    public Path rutaDatos() {
        return Path.of(propiedades.getProperty("datos.ruta", "datos/productos.json"));
    }
}

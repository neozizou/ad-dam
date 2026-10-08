package es.dam.tienda.config;

import java.io.IOException;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

/**
 * Configuración de la aplicación, leída de un fichero .properties.
 * Ese fichero contiene credenciales: no se sube al repositorio.
 */
public class Configuracion {

    /** Base de datos que se usa si no hay configuración: H2 embebida en datos/tienda.mv.db */
    public static final String URL_POR_DEFECTO = "jdbc:h2:./datos/tienda;MODE=MariaDB;DATABASE_TO_LOWER=TRUE";

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

    /** @return URL JDBC de la base de datos */
    public String urlBaseDatos() {
        return propiedades.getProperty("db.url", URL_POR_DEFECTO);
    }

    /** @return usuario de la base de datos */
    public String usuarioBaseDatos() {
        return propiedades.getProperty("db.usuario", "sa");
    }

    /**
     * @return la clave de la variable de entorno TIENDA_DB_CLAVE si existe;
     *         si no, la del fichero; si tampoco, la cadena vacía
     */
    public String claveBaseDatos() {
        String deEntorno = System.getenv("TIENDA_DB_CLAVE");
        return deEntorno != null ? deEntorno : propiedades.getProperty("db.clave", "");
    }
}

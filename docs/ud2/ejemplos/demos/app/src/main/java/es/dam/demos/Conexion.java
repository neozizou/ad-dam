package es.dam.demos;

import java.io.IOException;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

/** Lee los datos de conexión de config.properties y abre conexiones con DriverManager. */
public final class Conexion {

    private static final Properties CONFIG = cargar(Path.of("config.properties"));

    private Conexion() {
    }

    public static String url() {
        return CONFIG.getProperty("db.url", "jdbc:mariadb://localhost:3306/tienda");
    }

    public static String usuario() {
        return CONFIG.getProperty("db.usuario", "tienda");
    }

    /** La clave, de la variable de entorno TIENDA_DB_CLAVE o, si no existe, del fichero. */
    public static String clave() {
        String deEntorno = System.getenv("TIENDA_DB_CLAVE");
        return deEntorno != null ? deEntorno : CONFIG.getProperty("db.clave", "");
    }

    /** Abre una conexión nueva. Quien la pide es responsable de cerrarla. */
    public static Connection abrir() throws SQLException {
        return DriverManager.getConnection(url(), usuario(), clave());
    }

    private static Properties cargar(Path fichero) {
        Properties propiedades = new Properties();
        if (Files.exists(fichero)) {
            try (Reader lector = Files.newBufferedReader(fichero)) {
                propiedades.load(lector);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
        return propiedades;
    }
}

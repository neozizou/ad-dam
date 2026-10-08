package es.dam.tienda.bd;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import com.zaxxer.hikari.pool.HikariPool;
import es.dam.tienda.repositorio.AccesoDatosException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.SQLException;
import javax.sql.DataSource;

/**
 * Punto de acceso a la base de datos: mantiene un pool de conexiones (HikariCP)
 * y ejecuta scripts SQL. Sirve igual para MariaDB que para H2: lo decide la URL.
 */
public final class BaseDatos implements AutoCloseable {

    private final HikariDataSource pool;

    /**
     * Abre el pool y comprueba que la base de datos responde.
     *
     * @throws AccesoDatosException si no se puede conectar
     */
    public BaseDatos(String url, String usuario, String clave) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(url);
        config.setUsername(usuario);
        config.setPassword(clave);
        config.setPoolName("tienda");
        config.setMaximumPoolSize(4);           // a una aplicación de consola le sobran
        config.setConnectionTimeout(5_000);     // ms esperando una conexión libre
        try {
            pool = new HikariDataSource(config);
        } catch (HikariPool.PoolInitializationException e) {
            throw new AccesoDatosException("No se pudo conectar con " + url, e.getCause());
        }
    }

    /** @return la fuente de conexiones que reciben los repositorios */
    public DataSource dataSource() {
        return pool;
    }

    /**
     * Ejecuta un script SQL guardado en los recursos de la aplicación (src/main/resources).
     *
     * @param recurso ruta del script dentro de los recursos, por ejemplo "/sql/schema.sql"
     * @throws AccesoDatosException si el script no existe o falla alguna sentencia
     */
    public void ejecutarScript(String recurso) {
        try (InputStream entrada = BaseDatos.class.getResourceAsStream(recurso)) {
            if (entrada == null) {
                throw new AccesoDatosException("No existe el script " + recurso, null);
            }
            try (Connection conexion = pool.getConnection();
                 Reader lector = new InputStreamReader(entrada, StandardCharsets.UTF_8)) {
                EjecutorScripts.ejecutar(conexion, lector);
            }
        } catch (IOException | SQLException e) {
            throw new AccesoDatosException("Error al ejecutar " + recurso, e);
        }
    }

    /** Cierra todas las conexiones del pool. */
    @Override
    public void close() {
        pool.close();
    }
}

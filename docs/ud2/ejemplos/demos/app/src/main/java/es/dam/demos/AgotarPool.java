package es.dam.demos;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.sql.SQLException;

/** Qué pasa si se piden conexiones a un pool y no se cierran. */
public class AgotarPool {

    public static void main(String[] args) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(Conexion.url());
        config.setUsername(Conexion.usuario());
        config.setPassword(Conexion.clave());
        config.setMaximumPoolSize(3);
        config.setConnectionTimeout(2_000);                // esperar como mucho 2 s
        try (HikariDataSource pool = new HikariDataSource(config)) {
            for (int i = 1; i <= 4; i++) {
                Connection olvidada = pool.getConnection();    // MAL: nunca se cierra
                System.out.println("Conexión " + i + " obtenida");
            }
        } catch (SQLException e) {
            System.out.println(e.getClass().getSimpleName() + ": " + e.getMessage());
        }
    }
}

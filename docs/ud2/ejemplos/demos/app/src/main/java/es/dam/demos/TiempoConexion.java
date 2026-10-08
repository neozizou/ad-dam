package es.dam.demos;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

/** Compara el tiempo de abrir 100 conexiones nuevas con el de pedirlas 100 veces a un pool. */
public class TiempoConexion {

    private static final int VECES = 100;

    public static void main(String[] args) throws SQLException {
        long inicio = System.nanoTime();
        for (int i = 0; i < VECES; i++) {
            try (Connection conexion = Conexion.abrir()) {          // conexión nueva cada vez
                consultar(conexion);
            }
        }
        System.out.printf("DriverManager: %6.2f ms por consulta%n", milisegundos(inicio) / VECES);

        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(Conexion.url());
        config.setUsername(Conexion.usuario());
        config.setPassword(Conexion.clave());
        try (HikariDataSource pool = new HikariDataSource(config)) {
            inicio = System.nanoTime();
            for (int i = 0; i < VECES; i++) {
                try (Connection conexion = pool.getConnection()) {  // la presta el pool
                    consultar(conexion);
                }                                                   // close() la devuelve al pool
            }
            System.out.printf("Pool HikariCP: %6.2f ms por consulta%n", milisegundos(inicio) / VECES);
        }
    }

    private static void consultar(Connection conexion) throws SQLException {
        try (Statement sentencia = conexion.createStatement()) {
            sentencia.executeQuery("SELECT 1").close();
        }
    }

    private static double milisegundos(long inicio) {
        return (System.nanoTime() - inicio) / 1_000_000.0;
    }
}

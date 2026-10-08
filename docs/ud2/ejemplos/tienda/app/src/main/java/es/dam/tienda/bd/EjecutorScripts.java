package es.dam.tienda.bd;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.Reader;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Ejecuta un script SQL sentencia a sentencia. Salta los comentarios de línea (--)
 * y entiende la orden DELIMITER del cliente de MariaDB, que permite crear
 * procedimientos almacenados cuyo cuerpo contiene ';'.
 */
public final class EjecutorScripts {

    private EjecutorScripts() {
    }

    /**
     * @return número de sentencias ejecutadas
     * @throws SQLException si falla una sentencia o el script termina a medias
     */
    public static int ejecutar(Connection conexion, Reader script) throws IOException, SQLException {
        BufferedReader lector = new BufferedReader(script);
        String delimitador = ";";
        StringBuilder sentencia = new StringBuilder();
        int ejecutadas = 0;
        try (Statement st = conexion.createStatement()) {
            String linea;
            while ((linea = lector.readLine()) != null) {
                String limpia = linea.strip();
                if (sentencia.isEmpty() && (limpia.isEmpty() || limpia.startsWith("--"))) {
                    continue;                                     // línea vacía o comentario
                }
                if (limpia.toUpperCase().startsWith("DELIMITER ")) {
                    delimitador = limpia.substring("DELIMITER ".length()).strip();
                    continue;                                     // orden para el lector, no para el servidor
                }
                sentencia.append(linea).append('\n');
                if (limpia.endsWith(delimitador)) {
                    String sql = sentencia.toString().strip();
                    st.execute(sql.substring(0, sql.length() - delimitador.length()));
                    ejecutadas++;
                    sentencia.setLength(0);
                }
            }
        }
        if (!sentencia.toString().isBlank()) {
            throw new SQLException("El script termina sin '" + delimitador + "'");
        }
        return ejecutadas;
    }
}

package es.dam.demos;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

/** Provoca varios errores típicos y muestra qué información trae cada SQLException. */
public class ErroresSql {

    public static void main(String[] args) throws SQLException {
        String[] sentencias = {
            "INSERT INTO producto (codigo, nombre, precio, stock) VALUES ('TEC01', 'Repetido', 1, 1)",
            "DELETE FROM categoria WHERE id = 1",
            "UPDATE producto SET precio = -5 WHERE codigo = 'RAT01'",
            "SELECT precio_venta FROM producto",
            "SELEC * FROM producto",
        };
        try (Connection conexion = Conexion.abrir();
             Statement sentencia = conexion.createStatement()) {
            for (String sql : sentencias) {
                try {
                    sentencia.execute(sql);
                } catch (SQLException e) {
                    System.out.println(sql);
                    System.out.println("  " + e.getClass().getSimpleName());
                    System.out.println("  SQLState " + e.getSQLState() + ", código " + e.getErrorCode());
                    System.out.println("  " + e.getMessage());
                }
            }
        }
    }
}

package es.dam.demos;

import java.math.BigDecimal;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Types;

/** Llama a los dos procedimientos de procedimientos.sql. Necesita MariaDB. */
public class Procedimientos {

    public static void main(String[] args) throws SQLException {
        try (Connection conexion = Conexion.abrir()) {

            // 1. Procedimiento que devuelve filas, como una consulta
            try (CallableStatement llamada = conexion.prepareCall("{call productos_bajo_minimo(?)}")) {
                llamada.setInt(1, 10);
                try (ResultSet filas = llamada.executeQuery()) {
                    System.out.println("Productos con menos de 10 unidades:");
                    while (filas.next()) {
                        System.out.printf("  %-6s %-22s %3d%n",
                                filas.getString("codigo"), filas.getString("nombre"), filas.getInt("stock"));
                    }
                }
            }

            // 2. Procedimiento con un parámetro de entrada y otro de salida
            try (CallableStatement llamada = conexion.prepareCall("{call valor_categoria(?, ?)}")) {
                llamada.setInt(1, 1);                                  // IN: categoría 1
                llamada.registerOutParameter(2, Types.DECIMAL);        // OUT: hay que declarar su tipo
                llamada.execute();
                BigDecimal valor = llamada.getBigDecimal(2);           // se lee después de ejecutar
                System.out.println("Valor del stock de la categoría 1: " + valor + " €");
            }
        }
    }
}

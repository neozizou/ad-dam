package es.dam.demos;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.Scanner;

/**
 * Ejecuta cualquier SELECT que escriba el usuario y muestra el resultado como una tabla.
 * No conoce las columnas de antemano: las descubre con ResultSetMetaData.
 */
public class ConsultaLibre {

    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        try (Connection conexion = Conexion.abrir()) {
            while (true) {
                System.out.print("SQL (vacío para salir)> ");
                String sql = teclado.nextLine().strip();
                if (sql.isEmpty()) {
                    break;
                }
                if (!sql.toUpperCase().startsWith("SELECT")) {   // comprobación ingenua: ver el texto
                    System.out.println("Solo se admiten consultas SELECT.");
                    continue;
                }
                try (PreparedStatement sentencia = conexion.prepareStatement(sql);
                     ResultSet filas = sentencia.executeQuery()) {
                    imprimir(filas);
                } catch (SQLException e) {
                    System.out.println("Error " + e.getSQLState() + ": " + e.getMessage());
                }
            }
        } catch (SQLException e) {
            System.out.println("No se pudo conectar: " + e.getMessage());
        }
    }

    private static void imprimir(ResultSet filas) throws SQLException {
        ResultSetMetaData columnas = filas.getMetaData();
        int n = columnas.getColumnCount();
        for (int i = 1; i <= n; i++) {                   // las columnas se numeran desde 1
            System.out.printf("%-22s", columnas.getColumnLabel(i) + " (" + columnas.getColumnTypeName(i) + ")");
        }
        System.out.println();
        int contador = 0;
        while (filas.next()) {
            for (int i = 1; i <= n; i++) {
                System.out.printf("%-22s", filas.getObject(i));
            }
            System.out.println();
            contador++;
        }
        System.out.println("(" + contador + " filas)");
    }
}

package es.dam.demos;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/** Muestra cómo una consulta construida concatenando texto deja atacar la base de datos. */
public class InyeccionSql {

    public static void main(String[] args) throws SQLException {
        String ataque = "x' UNION SELECT email, nombre, 0, 0 FROM cliente -- ";
        try (Connection conexion = Conexion.abrir()) {
            System.out.println("Búsqueda insegura del código «TEC01»:");
            buscarInseguro(conexion, "TEC01");
            System.out.println("Búsqueda insegura del código «" + ataque + "»:");
            buscarInseguro(conexion, ataque);
            System.out.println("Búsqueda segura del mismo texto:");
            buscarSeguro(conexion, ataque);
        }
    }

    /** MAL: el texto del usuario pasa a formar parte de la sentencia SQL. */
    static void buscarInseguro(Connection conexion, String codigo) throws SQLException {
        String sql = "SELECT codigo, nombre, precio, stock FROM producto WHERE codigo = '" + codigo + "'";
        try (Statement sentencia = conexion.createStatement();
             ResultSet filas = sentencia.executeQuery(sql)) {
            mostrar(filas);
        }
    }

    /** BIEN: la sentencia es fija y el texto del usuario viaja como un valor. */
    static void buscarSeguro(Connection conexion, String codigo) throws SQLException {
        String sql = "SELECT codigo, nombre, precio, stock FROM producto WHERE codigo = ?";
        try (PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            sentencia.setString(1, codigo);
            try (ResultSet filas = sentencia.executeQuery()) {
                mostrar(filas);
            }
        }
    }

    private static void mostrar(ResultSet filas) throws SQLException {
        int n = 0;
        while (filas.next()) {
            System.out.printf("  %-20s %-20s%n", filas.getString(1), filas.getString(2));
            n++;
        }
        System.out.println("  (" + n + " filas)");
    }
}

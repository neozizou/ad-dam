package es.dam.demos;

import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.SQLException;

/** Comprueba la conexión y muestra qué gestor y qué conector hay al otro lado. */
public class ProbarConexion {

    public static void main(String[] args) {
        System.out.println("Conectando con " + Conexion.url() + " …");
        try (Connection conexion = Conexion.abrir()) {
            DatabaseMetaData info = conexion.getMetaData();
            System.out.println("Gestor:   " + info.getDatabaseProductName() + " " + info.getDatabaseProductVersion());
            System.out.println("Conector: " + info.getDriverName() + " " + info.getDriverVersion());
            System.out.println("JDBC:     " + info.getJDBCMajorVersion() + "." + info.getJDBCMinorVersion());
            System.out.println("Usuario:  " + info.getUserName());
        } catch (SQLException e) {
            System.out.println("No se pudo conectar: " + e.getMessage());
            System.out.println("SQLState " + e.getSQLState() + ", código de error " + e.getErrorCode());
        }
    }
}

package es.dam.demos;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

/** Inserta 5.000 filas de tres formas distintas y compara el tiempo. */
public class CargaMasiva {

    private static final int FILAS = 5_000;
    private static final String INSERTAR = "INSERT INTO prueba_carga (id, texto) VALUES (?, ?)";

    public static void main(String[] args) throws SQLException {
        try (Connection conexion = Conexion.abrir();
             Statement sentencia = conexion.createStatement()) {
            sentencia.execute("CREATE TABLE prueba_carga (id INT PRIMARY KEY, texto VARCHAR(50))");
            try {
                medir("Una a una, con autocommit", () -> unaAUna(conexion));
                sentencia.execute("DELETE FROM prueba_carga");
                medir("Una a una, en una transacción", () -> enTransaccion(conexion, false));
                sentencia.execute("DELETE FROM prueba_carga");
                medir("En lote, en una transacción", () -> enTransaccion(conexion, true));
            } finally {
                sentencia.execute("DROP TABLE prueba_carga");
            }
        }
    }

    /** Cada executeUpdate es una transacción: el gestor confirma (y escribe en disco) 5.000 veces. */
    static void unaAUna(Connection conexion) throws SQLException {
        try (PreparedStatement insertar = conexion.prepareStatement(INSERTAR)) {
            for (int i = 1; i <= FILAS; i++) {
                insertar.setInt(1, i);
                insertar.setString(2, "fila " + i);
                insertar.executeUpdate();
            }
        }
    }

    /** Todas las inserciones en una sola transacción, enviadas una a una o en lotes de 500. */
    static void enTransaccion(Connection conexion, boolean enLote) throws SQLException {
        conexion.setAutoCommit(false);
        try (PreparedStatement insertar = conexion.prepareStatement(INSERTAR)) {
            for (int i = 1; i <= FILAS; i++) {
                insertar.setInt(1, i);
                insertar.setString(2, "fila " + i);
                if (enLote) {
                    insertar.addBatch();
                    if (i % 500 == 0) {
                        insertar.executeBatch();
                    }
                } else {
                    insertar.executeUpdate();
                }
            }
            conexion.commit();
        } catch (SQLException e) {
            conexion.rollback();
            throw e;
        } finally {
            conexion.setAutoCommit(true);
        }
    }

    interface Tarea {
        void ejecutar() throws SQLException;
    }

    static void medir(String nombre, Tarea tarea) throws SQLException {
        long inicio = System.nanoTime();
        tarea.ejecutar();
        System.out.printf("%-32s %7.0f ms%n", nombre, (System.nanoTime() - inicio) / 1_000_000.0);
    }
}

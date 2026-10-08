package es.dam.tienda.repositorio;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import es.dam.tienda.bd.BaseDatos;
import es.dam.tienda.modelo.Pedido;
import es.dam.tienda.modelo.Producto;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDate;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

class ProductoRepositoryJdbcTest extends ProductoRepositoryContrato {

    private BaseDatos baseDatos;

    @Override
    protected ProductoRepository crearRepositorio() {
        // Una base de datos H2 en memoria, nueva y vacía para cada prueba
        String url = "jdbc:h2:mem:" + UUID.randomUUID() + ";MODE=MariaDB;DATABASE_TO_LOWER=TRUE";
        baseDatos = new BaseDatos(url, "sa", "");
        baseDatos.ejecutarScript("/sql/schema.sql");
        return new ProductoRepositoryJdbc(baseDatos.dataSource());
    }

    @AfterEach
    void cerrarBaseDatos() {
        baseDatos.close();                     // al cerrar la última conexión, H2 borra la base de datos
    }

    @Test
    void otroRepositorioVeLosMismosDatos() {
        repositorio.guardar(new Producto("RAT01", "Ratón", new BigDecimal("24.50"), 30));

        ProductoRepository otro = new ProductoRepositoryJdbc(baseDatos.dataSource());

        assertEquals(2, otro.buscarTodos().size());
        assertEquals(new BigDecimal("24.50"), otro.buscarPorCodigo("RAT01").orElseThrow().getPrecio());
    }

    @Test
    void unCambioSinGuardarNoLlegaALaBaseDeDatos() {
        Producto teclado = repositorio.buscarPorCodigo("TEC01").orElseThrow();
        teclado.reponer(100);

        assertEquals(3, repositorio.buscarPorCodigo("TEC01").orElseThrow().getStock());
    }

    @Test
    void noSePuedeBorrarUnProductoQueApareceEnUnPedido() throws SQLException {
        try (Connection conexion = baseDatos.dataSource().getConnection();
             Statement sentencia = conexion.createStatement()) {
            sentencia.executeUpdate("INSERT INTO cliente (nombre, email, fecha_alta)"
                    + " VALUES ('Ana Martín', 'ana@example.com', '2026-09-01')");
        }
        Pedido pedido = new Pedido(1, LocalDate.of(2026, 10, 8));
        pedido.agregar(repositorio.buscarPorCodigo("TEC01").orElseThrow(), 1);
        new PedidoRepositoryJdbc(baseDatos.dataSource()).guardar(pedido);

        assertThrows(IllegalStateException.class, () -> repositorio.borrar("TEC01"));
    }
}

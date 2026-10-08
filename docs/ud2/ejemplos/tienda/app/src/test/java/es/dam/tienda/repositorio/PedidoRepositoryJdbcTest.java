package es.dam.tienda.repositorio;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import es.dam.tienda.bd.BaseDatos;
import es.dam.tienda.modelo.Pedido;
import es.dam.tienda.modelo.StockInsuficienteException;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDate;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class PedidoRepositoryJdbcTest {

    private BaseDatos baseDatos;
    private ProductoRepository productos;
    private PedidoRepository pedidos;

    @BeforeEach
    void prepararBaseDatos() {
        baseDatos = new BaseDatos("jdbc:h2:mem:" + UUID.randomUUID() + ";MODE=MariaDB;DATABASE_TO_LOWER=TRUE",
                "sa", "");
        baseDatos.ejecutarScript("/sql/schema.sql");
        baseDatos.ejecutarScript("/sql/datos-ejemplo.sql");      // TEC01: 12 uds., RAT01: 30, MON01: 4
        productos = new ProductoRepositoryJdbc(baseDatos.dataSource());
        pedidos = new PedidoRepositoryJdbc(baseDatos.dataSource());
    }

    @AfterEach
    void cerrarBaseDatos() {
        baseDatos.close();
    }

    private Pedido pedido(String... codigosYUnidades) {
        Pedido pedido = new Pedido(1, LocalDate.of(2026, 10, 8));
        for (int i = 0; i < codigosYUnidades.length; i += 2) {
            pedido.agregar(productos.buscarPorCodigo(codigosYUnidades[i]).orElseThrow(),
                    Integer.parseInt(codigosYUnidades[i + 1]));
        }
        return pedido;
    }

    private int stock(String codigo) {
        return productos.buscarPorCodigo(codigo).orElseThrow().getStock();
    }

    private int contarFilas(String tabla) throws SQLException {
        try (Connection conexion = baseDatos.dataSource().getConnection();
             Statement sentencia = conexion.createStatement();
             ResultSet fila = sentencia.executeQuery("SELECT COUNT(*) FROM " + tabla)) {
            fila.next();
            return fila.getInt(1);
        }
    }

    @Test
    void guardarAsignaNumeroYDescuentaElStock() {
        int numero = pedidos.guardar(pedido("TEC01", "2", "RAT01", "1"));

        assertTrue(numero > 0);
        assertEquals(10, stock("TEC01"));
        assertEquals(29, stock("RAT01"));
        Pedido leido = pedidos.buscarPorNumero(numero).orElseThrow();
        assertEquals(2, leido.getLineas().size());
        assertEquals(0, new BigDecimal("144.30").compareTo(leido.total()));
    }

    @Test
    void siFaltaStockNoSeGuardaNada() throws SQLException {
        // RAT01 tiene stock de sobra, pero MON01 solo 4: el pedido entero debe deshacerse
        assertThrows(StockInsuficienteException.class, () -> pedidos.guardar(pedido("RAT01", "1", "MON01", "5")));

        assertEquals(30, stock("RAT01"));                    // el UPDATE de RAT01 se ha deshecho
        assertEquals(0, contarFilas("pedido"));
        assertEquals(0, contarFilas("linea_pedido"));
    }

    @Test
    void unClienteInexistenteNoSeAdmite() throws SQLException {
        Pedido deNadie = new Pedido(99, LocalDate.of(2026, 10, 8));
        deNadie.agregar(productos.buscarPorCodigo("RAT01").orElseThrow(), 1);

        assertThrows(IllegalArgumentException.class, () -> pedidos.guardar(deNadie));
        assertEquals(30, stock("RAT01"));
    }

    @Test
    void lasVentasSeAgrupanPorCategoria() {
        pedidos.guardar(pedido("TEC01", "2", "RAT01", "1", "MON01", "1"));

        var informe = pedidos.ventasPorCategoria();

        assertEquals("Monitores", informe.get(0).categoria());       // el de mayor importe va primero
        assertEquals(3, informe.get(1).unidades());                  // Periféricos: 2 + 1
        assertEquals(0, new BigDecimal("144.30").compareTo(informe.get(1).importe()));
    }
}

package es.dam.tienda.repositorio;

import es.dam.tienda.modelo.EstadoPedido;
import es.dam.tienda.modelo.LineaPedido;
import es.dam.tienda.modelo.Pedido;
import es.dam.tienda.modelo.Producto;
import es.dam.tienda.modelo.StockInsuficienteException;
import es.dam.tienda.modelo.VentasCategoria;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.SQLIntegrityConstraintViolationException;
import java.sql.Statement;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import javax.sql.DataSource;

/** Guarda los pedidos y sus líneas mediante JDBC. */
public class PedidoRepositoryJdbc implements PedidoRepository {

    private final DataSource dataSource;

    public PedidoRepositoryJdbc(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public int guardar(Pedido pedido) {
        try (Connection conexion = dataSource.getConnection()) {
            conexion.setAutoCommit(false);                         // empieza la transacción
            try {
                int numero = insertarPedido(conexion, pedido);
                insertarLineas(conexion, numero, pedido.getLineas());
                descontarStock(conexion, pedido.getLineas());
                conexion.commit();                                 // todo ha ido bien: se confirma
                pedido.asignarNumero(numero);
                return numero;
            } catch (SQLException | RuntimeException e) {
                conexion.rollback();                               // algo ha fallado: se deshace todo
                throw e;
            } finally {
                conexion.setAutoCommit(true);
            }
        } catch (SQLIntegrityConstraintViolationException e) {
            throw new IllegalArgumentException("El cliente o algún producto del pedido no existe");
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo guardar el pedido", e);
        }
    }

    /** Inserta la cabecera del pedido y devuelve el número que genera la base de datos. */
    private static int insertarPedido(Connection conexion, Pedido pedido) throws SQLException {
        String sql = "INSERT INTO pedido (cliente_id, fecha, estado) VALUES (?, ?, ?)";
        try (PreparedStatement sentencia = conexion.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            sentencia.setInt(1, pedido.getClienteId());
            sentencia.setObject(2, pedido.getFecha());             // LocalDate → DATE
            sentencia.setString(3, pedido.getEstado().name());
            sentencia.executeUpdate();
            try (ResultSet claves = sentencia.getGeneratedKeys()) {
                claves.next();
                return claves.getInt(1);
            }
        }
    }

    /** Inserta todas las líneas en un único envío (lote). */
    private static void insertarLineas(Connection conexion, int numero, List<LineaPedido> lineas)
            throws SQLException {
        String sql = "INSERT INTO linea_pedido (pedido_numero, producto_codigo, cantidad, precio_unitario)"
                + " VALUES (?, ?, ?, ?)";
        try (PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            for (LineaPedido linea : lineas) {
                sentencia.setInt(1, numero);
                sentencia.setString(2, linea.producto().getCodigo());
                sentencia.setInt(3, linea.cantidad());
                sentencia.setBigDecimal(4, linea.precioUnitario());
                sentencia.addBatch();                              // se acumula en el lote
            }
            sentencia.executeBatch();                              // se envían todas juntas
        }
    }

    /** Resta las unidades de cada línea; falla si algún producto no tiene bastantes. */
    private static void descontarStock(Connection conexion, List<LineaPedido> lineas) throws SQLException {
        String sql = "UPDATE producto SET stock = stock - ? WHERE codigo = ? AND stock >= ?";
        try (PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            for (LineaPedido linea : lineas) {
                sentencia.setInt(1, linea.cantidad());
                sentencia.setString(2, linea.producto().getCodigo());
                sentencia.setInt(3, linea.cantidad());
                if (sentencia.executeUpdate() == 0) {              // ninguna fila cumple la condición
                    throw new StockInsuficienteException(linea.producto().getCodigo(), linea.cantidad());
                }
            }
        }
    }

    @Override
    public Optional<Pedido> buscarPorNumero(int numero) {
        String sql = """
                SELECT p.numero, p.cliente_id, p.fecha, p.estado,
                       l.cantidad, l.precio_unitario,
                       pr.codigo, pr.nombre, pr.precio, pr.stock
                  FROM pedido p
                  LEFT JOIN linea_pedido l ON l.pedido_numero = p.numero
                  LEFT JOIN producto pr ON pr.codigo = l.producto_codigo
                 WHERE p.numero = ?
                 ORDER BY pr.codigo
                """;
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            sentencia.setInt(1, numero);
            try (ResultSet filas = sentencia.executeQuery()) {
                Pedido pedido = null;
                while (filas.next()) {
                    if (pedido == null) {                          // la cabecera, de la primera fila
                        pedido = new Pedido(filas.getInt("numero"), filas.getInt("cliente_id"),
                                filas.getObject("fecha", LocalDate.class),
                                EstadoPedido.valueOf(filas.getString("estado")));
                    }
                    if (filas.getString("codigo") != null) {       // un pedido sin líneas trae NULL
                        Producto producto = new Producto(filas.getString("codigo"), filas.getString("nombre"),
                                filas.getBigDecimal("precio"), filas.getInt("stock"));
                        pedido.agregarLinea(new LineaPedido(producto, filas.getInt("cantidad"),
                                filas.getBigDecimal("precio_unitario")));
                    }
                }
                return Optional.ofNullable(pedido);
            }
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo leer el pedido " + numero, e);
        }
    }

    @Override
    public List<VentasCategoria> ventasPorCategoria() {
        String sql = """
                SELECT COALESCE(c.nombre, 'Sin categoría') AS categoria,
                       SUM(l.cantidad) AS unidades,
                       SUM(l.cantidad * l.precio_unitario) AS importe
                  FROM linea_pedido l
                  JOIN producto p ON p.codigo = l.producto_codigo
                  LEFT JOIN categoria c ON c.id = p.categoria_id
                 GROUP BY COALESCE(c.nombre, 'Sin categoría')
                 ORDER BY importe DESC
                """;
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement(sql);
             ResultSet filas = sentencia.executeQuery()) {
            List<VentasCategoria> informe = new ArrayList<>();
            while (filas.next()) {
                informe.add(new VentasCategoria(filas.getString("categoria"),
                        filas.getInt("unidades"), filas.getBigDecimal("importe")));
            }
            return informe;
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo calcular el informe de ventas", e);
        }
    }
}

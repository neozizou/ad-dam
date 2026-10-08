package es.dam.tienda.repositorio;

import es.dam.tienda.modelo.Producto;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.SQLIntegrityConstraintViolationException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import javax.sql.DataSource;

/**
 * Guarda los productos en una base de datos relacional mediante JDBC.
 * Sirve para cualquier gestor que tenga la tabla producto de schema.sql (MariaDB, H2…).
 */
public class ProductoRepositoryJdbc implements ProductoRepository {

    private static final String SELECT = "SELECT codigo, nombre, precio, stock FROM producto";

    private final DataSource dataSource;

    public ProductoRepositoryJdbc(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public void guardar(Producto producto) {
        String actualizar = "UPDATE producto SET nombre = ?, precio = ?, stock = ? WHERE codigo = ?";
        String insertar = "INSERT INTO producto (nombre, precio, stock, codigo) VALUES (?, ?, ?, ?)";
        try (Connection conexion = dataSource.getConnection()) {
            if (ejecutar(conexion, actualizar, producto) == 0) {     // no existía: se inserta
                ejecutar(conexion, insertar, producto);
            }
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo guardar el producto " + producto.getCodigo(), e);
        }
    }

    /** Ejecuta una sentencia cuyos cuatro parámetros son, en este orden, nombre, precio, stock y código. */
    private static int ejecutar(Connection conexion, String sql, Producto p) throws SQLException {
        try (PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            sentencia.setString(1, p.getNombre());
            sentencia.setBigDecimal(2, p.getPrecio());
            sentencia.setInt(3, p.getStock());
            sentencia.setString(4, p.getCodigo());
            return sentencia.executeUpdate();                       // filas afectadas
        }
    }

    @Override
    public Optional<Producto> buscarPorCodigo(String codigo) {
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement(SELECT + " WHERE codigo = ?")) {
            sentencia.setString(1, codigo);
            try (ResultSet fila = sentencia.executeQuery()) {
                return fila.next() ? Optional.of(aProducto(fila)) : Optional.empty();
            }
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo buscar el producto " + codigo, e);
        }
    }

    @Override
    public List<Producto> buscarTodos() {
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement(SELECT + " ORDER BY codigo");
             ResultSet filas = sentencia.executeQuery()) {
            List<Producto> productos = new ArrayList<>();
            while (filas.next()) {
                productos.add(aProducto(filas));
            }
            return List.copyOf(productos);
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo leer la lista de productos", e);
        }
    }

    @Override
    public boolean borrar(String codigo) {
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement("DELETE FROM producto WHERE codigo = ?")) {
            sentencia.setString(1, codigo);
            return sentencia.executeUpdate() == 1;
        } catch (SQLIntegrityConstraintViolationException e) {       // lo impide una clave ajena
            throw new IllegalStateException("El producto " + codigo + " aparece en algún pedido y no se puede borrar");
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo borrar el producto " + codigo, e);
        }
    }

    /** Convierte la fila actual en un Producto; su constructor valida los datos. */
    private static Producto aProducto(ResultSet fila) throws SQLException {
        return new Producto(fila.getString("codigo"), fila.getString("nombre"),
                fila.getBigDecimal("precio"), fila.getInt("stock"));
    }
}

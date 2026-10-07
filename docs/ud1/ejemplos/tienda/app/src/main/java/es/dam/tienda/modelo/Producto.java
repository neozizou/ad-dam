package es.dam.tienda.modelo;

import java.math.BigDecimal;

/**
 * Producto del catálogo de la tienda.
 * Dos productos son iguales si tienen el mismo código.
 */
public class Producto {

    private final String codigo;          // no cambia una vez creado
    private String nombre;
    private BigDecimal precio;
    private int stock;

    public Producto(String codigo, String nombre, BigDecimal precio, int stock) {
        if (codigo == null || codigo.isBlank()) {
            throw new IllegalArgumentException("El código es obligatorio");
        }
        if (stock < 0) {
            throw new IllegalArgumentException("Stock no válido: " + stock);
        }
        this.codigo = codigo;
        this.nombre = nombre;
        this.precio = validarPrecio(precio);
        this.stock = stock;
    }

    /** Crea un producto sin existencias. */
    public Producto(String codigo, String nombre, BigDecimal precio) {
        this(codigo, nombre, precio, 0);  // delega en el otro constructor
    }

    private static BigDecimal validarPrecio(BigDecimal precio) {
        if (precio == null || precio.signum() < 0) {
            throw new IllegalArgumentException("Precio no válido: " + precio);
        }
        return precio;
    }

    public String getCodigo() { return codigo; }

    public String getNombre() { return nombre; }

    public void setNombre(String nombre) { this.nombre = nombre; }

    public BigDecimal getPrecio() { return precio; }

    public void setPrecio(BigDecimal precio) { this.precio = validarPrecio(precio); }

    public int getStock() { return stock; }

    /** Suma unidades al stock. */
    public void reponer(int unidades) {
        if (unidades <= 0) {
            throw new IllegalArgumentException("Las unidades deben ser positivas");
        }
        stock += unidades;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Producto otro)) return false;
        return codigo.equals(otro.codigo);
    }

    @Override
    public int hashCode() {
        return codigo.hashCode();
    }

    @Override
    public String toString() {
        return "Producto[" + codigo + ", " + nombre + ", " + precio + " €, stock " + stock + "]";
    }
}

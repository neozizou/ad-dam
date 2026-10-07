package es.dam.tienda.consola;

import es.dam.tienda.modelo.Producto;
import es.dam.tienda.servicio.ProductoNoEncontradoException;
import es.dam.tienda.servicio.ProductoService;
import java.util.Locale;

/** Menú de consola para gestionar productos. Solo habla con el servicio. */
public class MenuProductos {

    private static final Locale ES = Locale.of("es", "ES");

    private final ProductoService servicio;
    private final Consola consola;

    public MenuProductos(ProductoService servicio, Consola consola) {
        this.servicio = servicio;
        this.consola = consola;
    }

    public void mostrar() {
        int opcion;
        do {
            System.out.println("""

                    === Productos ===
                    1. Listar
                    2. Buscar por código
                    3. Alta
                    4. Cambiar precio
                    5. Baja
                    0. Salir""");
            opcion = consola.leerEntero("Opción: ", 0, 5);
            try {
                switch (opcion) {
                    case 1 -> listar();
                    case 2 -> buscar();
                    case 3 -> alta();
                    case 4 -> cambiarPrecio();
                    case 5 -> baja();
                    case 0 -> System.out.println("Hasta luego.");
                }
            } catch (ProductoNoEncontradoException | IllegalArgumentException | IllegalStateException e) {
                System.out.println("  Error: " + e.getMessage());
            }
        } while (opcion != 0);
    }

    private void listar() {
        for (Producto p : servicio.listar()) {
            System.out.println(String.format(ES, "  %-6s %-22s %9.2f € %4d uds.",
                    p.getCodigo(), p.getNombre(), p.getPrecio(), p.getStock()));
        }
        System.out.println(String.format(ES, "  Valor del inventario: %,.2f €", servicio.valorInventario()));
    }

    private void buscar() {
        String codigo = consola.leerTexto("Código: ");
        System.out.println("  " + servicio.buscar(codigo));
    }

    private void alta() {
        String codigo = consola.leerTexto("Código: ");
        String nombre = consola.leerTexto("Nombre: ");
        var precio = consola.leerDecimal("Precio: ");
        int stock = consola.leerEntero("Stock: ", 0, 1_000_000);
        servicio.alta(new Producto(codigo, nombre, precio, stock));
        System.out.println("  Producto dado de alta.");
    }

    private void cambiarPrecio() {
        String codigo = consola.leerTexto("Código: ");
        var precio = consola.leerDecimal("Nuevo precio: ");
        servicio.cambiarPrecio(codigo, precio);
        System.out.println("  Precio actualizado.");
    }

    private void baja() {
        String codigo = consola.leerTexto("Código: ");
        servicio.baja(codigo);
        System.out.println("  Producto eliminado.");
    }
}

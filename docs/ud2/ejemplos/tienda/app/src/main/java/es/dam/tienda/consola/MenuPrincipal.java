package es.dam.tienda.consola;

/** Primer menú de la aplicación: elige entre productos y pedidos. */
public class MenuPrincipal {

    private final MenuProductos productos;
    private final MenuPedidos pedidos;
    private final Consola consola;

    public MenuPrincipal(MenuProductos productos, MenuPedidos pedidos, Consola consola) {
        this.productos = productos;
        this.pedidos = pedidos;
        this.consola = consola;
    }

    public void mostrar() {
        int opcion;
        do {
            System.out.println("""

                    === Tienda ===
                    1. Productos
                    2. Pedidos
                    0. Salir""");
            opcion = consola.leerEntero("Opción: ", 0, 2);
            switch (opcion) {
                case 1 -> productos.mostrar();
                case 2 -> pedidos.mostrar();
                case 0 -> System.out.println("Hasta luego.");
            }
        } while (opcion != 0);
    }
}

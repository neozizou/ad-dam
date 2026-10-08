package es.dam.tienda.consola;

import es.dam.tienda.modelo.LineaPedido;
import es.dam.tienda.modelo.Pedido;
import es.dam.tienda.modelo.StockInsuficienteException;
import es.dam.tienda.modelo.VentasCategoria;
import es.dam.tienda.repositorio.AccesoDatosException;
import es.dam.tienda.servicio.PedidoService;
import es.dam.tienda.servicio.ProductoNoEncontradoException;
import java.time.format.DateTimeFormatter;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** Menú de consola para registrar y consultar pedidos. */
public class MenuPedidos {

    private static final Locale ES = Locale.of("es", "ES");
    private static final DateTimeFormatter FECHA = DateTimeFormatter.ofPattern("dd/MM/yyyy");

    private final PedidoService servicio;
    private final Consola consola;

    public MenuPedidos(PedidoService servicio, Consola consola) {
        this.servicio = servicio;
        this.consola = consola;
    }

    public void mostrar() {
        int opcion;
        do {
            System.out.println("""

                    === Pedidos ===
                    1. Registrar pedido
                    2. Ver pedido
                    3. Ventas por categoría
                    0. Volver""");
            opcion = consola.leerEntero("Opción: ", 0, 3);
            try {
                switch (opcion) {
                    case 1 -> registrar();
                    case 2 -> ver();
                    case 3 -> ventasPorCategoria();
                }
            } catch (ProductoNoEncontradoException | StockInsuficienteException
                     | IllegalArgumentException | IllegalStateException e) {
                System.out.println("  Error: " + e.getMessage());
            } catch (AccesoDatosException e) {
                System.out.println("  Error de acceso a datos: " + e.getMessage() + " (" + e.getCause() + ")");
            }
        } while (opcion != 0);
    }

    private void registrar() {
        int cliente = consola.leerEntero("Cliente (id): ", 1, Integer.MAX_VALUE);
        Map<String, Integer> lineas = new LinkedHashMap<>();
        while (true) {
            String codigo = consola.leerTexto("  Código del producto (FIN para terminar): ");
            if (codigo.equalsIgnoreCase("FIN")) {
                break;
            }
            lineas.merge(codigo, consola.leerEntero("  Unidades: ", 1, 1_000), Integer::sum);
        }
        int numero = servicio.registrar(cliente, lineas);
        System.out.println("  Pedido " + numero + " registrado.");
    }

    private void ver() {
        Pedido pedido = servicio.buscar(consola.leerEntero("Número de pedido: ", 1, Integer.MAX_VALUE));
        System.out.printf("  Pedido %d · cliente %d · %s · %s%n", pedido.getNumero(), pedido.getClienteId(),
                pedido.getFecha().format(FECHA), pedido.getEstado());
        for (LineaPedido l : pedido.getLineas()) {
            System.out.println(String.format(ES, "    %-6s %-22s %3d × %7.2f € = %8.2f €",
                    l.producto().getCodigo(), l.producto().getNombre(), l.cantidad(), l.precioUnitario(), l.importe()));
        }
        System.out.println(String.format(ES, "  Total: %,.2f €", pedido.total()));
    }

    private void ventasPorCategoria() {
        for (VentasCategoria v : servicio.ventasPorCategoria()) {
            System.out.println(String.format(ES, "  %-14s %5d uds. %,10.2f €", v.categoria(), v.unidades(), v.importe()));
        }
    }
}

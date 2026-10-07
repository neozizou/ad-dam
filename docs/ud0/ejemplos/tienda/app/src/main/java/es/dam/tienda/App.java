package es.dam.tienda;

import es.dam.tienda.consola.Consola;
import es.dam.tienda.consola.MenuProductos;
import es.dam.tienda.modelo.Producto;
import es.dam.tienda.repositorio.ProductoRepository;
import es.dam.tienda.repositorio.ProductoRepositoryMemoria;
import es.dam.tienda.servicio.ProductoService;
import java.math.BigDecimal;

/** Punto de entrada: crea las piezas, las conecta y arranca el menú. */
public class App {

    public static void main(String[] args) {
        // El único sitio del programa que conoce la implementación concreta
        ProductoRepository repositorio = new ProductoRepositoryMemoria();
        ProductoService servicio = new ProductoService(repositorio);

        cargarDatosDeEjemplo(servicio);
        new MenuProductos(servicio, new Consola()).mostrar();
    }

    private static void cargarDatosDeEjemplo(ProductoService servicio) {
        servicio.alta(new Producto("TEC01", "Teclado mecánico", new BigDecimal("59.90"), 12));
        servicio.alta(new Producto("RAT01", "Ratón inalámbrico", new BigDecimal("24.50"), 30));
        servicio.alta(new Producto("MON01", "Monitor 27 pulgadas", new BigDecimal("219.00"), 4));
        servicio.alta(new Producto("CAB01", "Cable USB-C 2 m", new BigDecimal("8.95"), 0));
    }
}

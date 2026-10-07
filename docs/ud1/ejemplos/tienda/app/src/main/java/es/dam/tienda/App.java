package es.dam.tienda;

import es.dam.tienda.config.Configuracion;
import es.dam.tienda.consola.Consola;
import es.dam.tienda.consola.MenuProductos;
import es.dam.tienda.fichero.Formatos;
import es.dam.tienda.modelo.Producto;
import es.dam.tienda.repositorio.AccesoDatosException;
import es.dam.tienda.repositorio.ProductoRepository;
import es.dam.tienda.repositorio.ProductoRepositoryFichero;
import es.dam.tienda.servicio.ProductoService;
import java.io.UncheckedIOException;
import java.math.BigDecimal;
import java.nio.file.Path;

/** Punto de entrada: crea las piezas, las conecta y arranca el menú. */
public class App {

    public static void main(String[] args) {
        try {
            Configuracion configuracion = new Configuracion(Path.of("config.properties"));
            Path datos = configuracion.rutaDatos();

            // El único sitio del programa que conoce la implementación concreta
            ProductoRepository repositorio = new ProductoRepositoryFichero(datos, Formatos.porExtension(datos));
            ProductoService servicio = new ProductoService(repositorio);

            if (servicio.listar().isEmpty()) {
                cargarDatosDeEjemplo(servicio);
            }
            System.out.println("Datos en " + datos.toAbsolutePath());
            new MenuProductos(servicio, new Consola()).mostrar();
        } catch (AccesoDatosException | UncheckedIOException e) {
            System.err.println("No se puede arrancar: " + e.getMessage());
            System.err.println("Causa: " + e.getCause());
            System.exit(1);
        }
    }

    private static void cargarDatosDeEjemplo(ProductoService servicio) {
        servicio.alta(new Producto("TEC01", "Teclado mecánico", new BigDecimal("59.90"), 12));
        servicio.alta(new Producto("RAT01", "Ratón inalámbrico", new BigDecimal("24.50"), 30));
        servicio.alta(new Producto("MON01", "Monitor 27 pulgadas", new BigDecimal("219.00"), 4));
        servicio.alta(new Producto("CAB01", "Cable USB-C 2 m", new BigDecimal("8.95"), 0));
    }
}

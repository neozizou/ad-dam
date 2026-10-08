package es.dam.tienda;

import es.dam.tienda.bd.BaseDatos;
import es.dam.tienda.config.Configuracion;
import es.dam.tienda.consola.Consola;
import es.dam.tienda.consola.MenuPedidos;
import es.dam.tienda.consola.MenuPrincipal;
import es.dam.tienda.consola.MenuProductos;
import es.dam.tienda.repositorio.AccesoDatosException;
import es.dam.tienda.repositorio.PedidoRepository;
import es.dam.tienda.repositorio.PedidoRepositoryJdbc;
import es.dam.tienda.repositorio.ProductoRepository;
import es.dam.tienda.repositorio.ProductoRepositoryJdbc;
import es.dam.tienda.servicio.PedidoService;
import es.dam.tienda.servicio.ProductoService;
import java.io.UncheckedIOException;
import java.nio.file.Path;

/** Punto de entrada: crea las piezas, las conecta y arranca el menú. */
public class App {

    public static void main(String[] args) {
        try {
            arrancar(new Configuracion(Path.of("config.properties")));
        } catch (AccesoDatosException | UncheckedIOException e) {
            System.err.println("No se puede arrancar: " + e.getMessage());
            System.err.println("Causa: " + e.getCause());
            System.exit(1);
        }
    }

    private static void arrancar(Configuracion configuracion) {
        try (BaseDatos baseDatos = new BaseDatos(configuracion.urlBaseDatos(),
                configuracion.usuarioBaseDatos(), configuracion.claveBaseDatos())) {
            baseDatos.ejecutarScript("/sql/schema.sql");          // crea las tablas que falten

            // El único sitio del programa que conoce las implementaciones concretas
            ProductoRepository productos = new ProductoRepositoryJdbc(baseDatos.dataSource());
            PedidoRepository pedidos = new PedidoRepositoryJdbc(baseDatos.dataSource());

            ProductoService productoService = new ProductoService(productos);
            if (productoService.listar().isEmpty()) {
                baseDatos.ejecutarScript("/sql/datos-ejemplo.sql");
            }
            System.out.println("Conectado a " + configuracion.urlBaseDatos());

            Consola consola = new Consola();
            new MenuPrincipal(
                    new MenuProductos(productoService, consola),
                    new MenuPedidos(new PedidoService(pedidos, productos), consola),
                    consola).mostrar();
        }
    }
}

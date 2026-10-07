package es.dam.tienda.repositorio;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import es.dam.tienda.fichero.FormatoCsv;
import es.dam.tienda.modelo.Producto;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class ProductoRepositoryFicheroTest extends ProductoRepositoryContrato {

    @TempDir
    Path carpeta;

    private Path fichero() {
        return carpeta.resolve("productos.csv");
    }

    @Override
    protected ProductoRepository crearRepositorio() {
        return new ProductoRepositoryFichero(fichero(), new FormatoCsv());
    }

    @Test
    void losDatosSobrevivenAUnReinicio() {
        repositorio.guardar(new Producto("RAT01", "Ratón", new BigDecimal("24.50"), 30));

        ProductoRepository otro = crearRepositorio();          // como si el programa arrancara de nuevo

        assertEquals(2, otro.buscarTodos().size());
        assertEquals(new BigDecimal("24.50"), otro.buscarPorCodigo("RAT01").orElseThrow().getPrecio());
    }

    @Test
    void unCambioSinGuardarNoLlegaAlFichero() {
        Producto teclado = repositorio.buscarPorCodigo("TEC01").orElseThrow();
        teclado.reponer(100);                                  // se modifica la copia, no se guarda

        assertEquals(3, repositorio.buscarPorCodigo("TEC01").orElseThrow().getStock());
    }

    @Test
    void ficheroCorruptoLanzaAccesoDatosException() throws IOException {
        Files.writeString(fichero(), "codigo;nombre;precio;stock\nesto no es un producto\n");

        AccesoDatosException e = assertThrows(AccesoDatosException.class, this::crearRepositorio);
        assertTrue(e.getCause() instanceof IOException);
    }

    @Test
    void noQuedanFicherosTemporales() throws IOException {
        repositorio.guardar(new Producto("RAT01", "Ratón", new BigDecimal("24.50"), 30));
        try (var contenido = Files.list(carpeta)) {
            assertEquals(1, contenido.count());                 // solo productos.csv
        }
    }
}

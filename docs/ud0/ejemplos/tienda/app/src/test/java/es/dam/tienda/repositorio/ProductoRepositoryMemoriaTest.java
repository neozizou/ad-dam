package es.dam.tienda.repositorio;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import es.dam.tienda.modelo.Producto;
import java.math.BigDecimal;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ProductoRepositoryMemoriaTest {

    private ProductoRepository repositorio;

    @BeforeEach                     // se ejecuta antes de CADA prueba: cada una empieza limpia
    void prepararRepositorio() {
        repositorio = new ProductoRepositoryMemoria();
        repositorio.guardar(new Producto("TEC01", "Teclado", new BigDecimal("59.90"), 3));
    }

    @Test
    void buscarPorCodigoExistenteLoEncuentra() {
        assertTrue(repositorio.buscarPorCodigo("TEC01").isPresent());
    }

    @Test
    void buscarPorCodigoInexistenteDevuelveVacio() {
        assertTrue(repositorio.buscarPorCodigo("NOEXISTE").isEmpty());
    }

    @Test
    void guardarConCodigoRepetidoReemplaza() {
        repositorio.guardar(new Producto("TEC01", "Teclado mecánico", new BigDecimal("79.90"), 1));
        assertEquals(1, repositorio.buscarTodos().size());
        assertEquals("Teclado mecánico", repositorio.buscarPorCodigo("TEC01").orElseThrow().getNombre());
    }

    @Test
    void borrarEliminaYDevuelveTrue() {
        assertTrue(repositorio.borrar("TEC01"));
        assertFalse(repositorio.existe("TEC01"));
    }
}

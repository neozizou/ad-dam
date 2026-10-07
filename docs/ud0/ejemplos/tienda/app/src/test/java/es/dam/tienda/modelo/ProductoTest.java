package es.dam.tienda.modelo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ProductoTest {

    @Test
    @DisplayName("Reponer suma las unidades al stock")
    void reponerSumaUnidades() {
        // Preparar
        Producto teclado = new Producto("TEC01", "Teclado", new BigDecimal("59.90"), 3);
        // Actuar
        teclado.reponer(2);
        // Comprobar
        assertEquals(5, teclado.getStock());
    }

    @Test
    void precioNegativoLanzaExcepcion() {
        assertThrows(IllegalArgumentException.class,
                () -> new Producto("RAT01", "Ratón", new BigDecimal("-1")));
    }

    @Test
    void dosProductosConElMismoCodigoSonIguales() {
        var a = new Producto("TEC01", "Teclado", new BigDecimal("59.90"));
        var b = new Producto("TEC01", "Teclado mecánico", new BigDecimal("79.90"));
        assertEquals(a, b);
        assertEquals(a.hashCode(), b.hashCode());
    }
}

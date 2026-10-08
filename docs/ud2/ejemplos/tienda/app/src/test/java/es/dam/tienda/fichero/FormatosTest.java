package es.dam.tienda.fichero;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class FormatosTest {

    @TempDir
    Path carpeta;                       // JUnit crea una carpeta vacía para cada prueba y la borra después

    private final List<ProductoDto> productos = List.of(
            new ProductoDto("TEC01", "Teclado mecánico", new BigDecimal("59.90"), 12),
            new ProductoDto("HUB01", "Hub USB; 4 puertos \"Pro\"", new BigDecimal("19.99"), 7));

    @ParameterizedTest                  // la misma prueba, una vez por cada formato
    @ValueSource(strings = {"csv", "json", "xml", "dat"})
    void loQueSeEscribeSeLeeIgual(String extension) throws IOException {
        Path fichero = carpeta.resolve("productos." + extension);
        FormatoProductos formato = Formatos.porExtension(fichero);

        formato.escribir(fichero, productos);

        assertEquals(productos, formato.leer(fichero));
    }

    @Test
    void convertirDeCsvAXmlConservaLosDatos() throws IOException {
        Path csv = carpeta.resolve("origen.csv");
        Path xml = carpeta.resolve("destino.xml");
        new FormatoCsv().escribir(csv, productos);

        int convertidos = Formatos.convertir(csv, xml);

        assertEquals(2, convertidos);
        assertEquals(productos, new FormatoXml().leer(xml));
    }

    @Test
    void csvConNumeroMalFormadoLanzaIOException() throws IOException {
        Path csv = carpeta.resolve("malo.csv");
        Files.writeString(csv, "codigo;nombre;precio;stock\nTEC01;Teclado;59,90;12\n");

        assertThrows(IOException.class, () -> new FormatoCsv().leer(csv));
    }

    @Test
    void extensionDesconocidaNoSeAdmite() {
        assertThrows(IllegalArgumentException.class, () -> Formatos.porExtension(Path.of("datos.txt")));
    }
}

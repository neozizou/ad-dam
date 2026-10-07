import java.io.*;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class Serializacion {

    record ProductoDto(String codigo, String nombre, BigDecimal precio, int stock) implements Serializable {}

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Path fichero = Path.of("productos.ser");
        List<ProductoDto> productos = new ArrayList<>(List.of(
                new ProductoDto("TEC01", "Teclado mecánico", new BigDecimal("59.90"), 12),
                new ProductoDto("RAT01", "Ratón inalámbrico", new BigDecimal("24.50"), 30)));

        try (ObjectOutputStream salida = new ObjectOutputStream(Files.newOutputStream(fichero))) {
            salida.writeObject(productos);                  // la lista y todo lo que contiene
        }

        try (ObjectInputStream entrada = new ObjectInputStream(Files.newInputStream(fichero))) {
            @SuppressWarnings("unchecked")
            List<ProductoDto> leidos = (List<ProductoDto>) entrada.readObject();
            System.out.println(leidos.equals(productos) + ", " + Files.size(fichero) + " bytes");
        }
        Files.delete(fichero);
    }
}

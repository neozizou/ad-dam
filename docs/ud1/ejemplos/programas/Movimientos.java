import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Stream;

public class Movimientos {

    private static final Path REGISTRO = Path.of("movimientos.log");
    private static final DateTimeFormatter FORMATO = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    static void anotar(String codigo, int unidades) throws IOException {
        String linea = LocalDateTime.now().format(FORMATO) + ";" + codigo + ";" + unidades + System.lineSeparator();
        Files.writeString(REGISTRO, linea, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
    }

    public static void main(String[] args) throws IOException {
        anotar("TEC01", -2);
        anotar("RAT01", 10);
        anotar("TEC01", -1);

        List<String> todas = Files.readAllLines(REGISTRO);             // todo a memoria: ficheros pequeños
        System.out.println(todas.size() + " líneas");

        try (Stream<String> lineas = Files.lines(REGISTRO)) {          // línea a línea: ficheros grandes
            int vendidasTec = lineas.map(l -> l.split(";"))
                    .filter(campos -> campos[1].equals("TEC01"))
                    .mapToInt(campos -> Integer.parseInt(campos[2]))
                    .sum();
            System.out.println("Movimiento neto de TEC01: " + vendidasTec);   // -3
        }
        Files.delete(REGISTRO);
    }
}

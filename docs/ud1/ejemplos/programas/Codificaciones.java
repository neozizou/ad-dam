import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HexFormat;

public class Codificaciones {
    public static void main(String[] args) throws IOException {
        String texto = "año";
        byte[] utf8 = texto.getBytes(StandardCharsets.UTF_8);
        byte[] latin1 = texto.getBytes(StandardCharsets.ISO_8859_1);
        System.out.println(HexFormat.ofDelimiter(" ").formatHex(utf8));     // 61 c3 b1 6f
        System.out.println(HexFormat.ofDelimiter(" ").formatHex(latin1));   // 61 f1 6f

        // Leer con la codificación equivocada
        System.out.println(new String(utf8, StandardCharsets.ISO_8859_1));  // aÃ±o
        System.out.println(new String(latin1, StandardCharsets.UTF_8));     // a�o

        Path fichero = Path.of("latin1.txt");
        Files.writeString(fichero, texto, StandardCharsets.ISO_8859_1);
        try {
            Files.readString(fichero);                                      // supone UTF-8
        } catch (IOException e) {
            System.out.println(e);                                          // MalformedInputException
        }
        System.out.println(Files.readString(fichero, StandardCharsets.ISO_8859_1));   // año
        Files.delete(fichero);
    }
}

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;

public class Rutas {
    public static void main(String[] args) throws IOException {
        Path datos = Path.of("datos", "productos.json");        // ruta relativa
        System.out.println(datos);                               // datos/productos.json (datos\productos.json en Windows)
        System.out.println(datos.getFileName());                 // productos.json
        System.out.println(datos.getParent());                   // datos
        System.out.println(datos.isAbsolute());                  // false
        System.out.println(datos.toAbsolutePath());              // /home/ana/tienda/datos/productos.json

        Path copia = datos.resolveSibling("copia.json");         // datos/copia.json
        Path rara = Path.of("datos/../datos/./productos.json");
        System.out.println(copia + "  " + rara.normalize());     // datos/copia.json  datos/productos.json
        System.out.println(Path.of("datos").relativize(Path.of("export/catalogo.csv")));  // ../export/catalogo.csv

        Path carpeta = Files.createDirectories(Path.of("prueba", "sub"));   // crea las que falten
        Path fichero = carpeta.resolve("hola.txt");
        Files.writeString(fichero, "Hola, ficheros\n");
        System.out.println(Files.exists(fichero) + " " + Files.isDirectory(carpeta) + " " + Files.size(fichero));  // true true 15
        Files.copy(fichero, carpeta.resolve("copia.txt"));
        Files.move(carpeta.resolve("copia.txt"), Path.of("prueba", "movida.txt"));

        try (Stream<Path> contenido = Files.walk(Path.of("prueba"))) {       // recorre el árbol
            contenido.sorted().forEach(System.out::println);
        }
        try (Stream<Path> contenido = Files.walk(Path.of("prueba"))) {       // borrar: primero lo de dentro
            contenido.sorted(java.util.Comparator.reverseOrder()).forEach(p -> {
                try { Files.delete(p); } catch (IOException e) { throw new java.io.UncheckedIOException(e); }
            });
        }
        System.out.println(Files.exists(Path.of("prueba")));     // false
    }
}

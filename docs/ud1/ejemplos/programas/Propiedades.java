import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

public class Propiedades {
    public static void main(String[] args) throws IOException {
        Path fichero = Path.of("config.properties");
        Files.writeString(fichero, """
                # Configuración de la tienda
                datos.ruta=datos/productos.json
                tienda.nombre=Informática Alhambra
                """);

        Properties config = new Properties();
        try (Reader lector = Files.newBufferedReader(fichero)) {       // UTF-8: respeta la «á»
            config.load(lector);
        }
        System.out.println(config.getProperty("datos.ruta"));           // datos/productos.json
        System.out.println(config.getProperty("tienda.nombre"));        // Informática Alhambra
        System.out.println(config.getProperty("idioma", "es"));         // es (valor por defecto)

        config.setProperty("ultima.exportacion", "export/catalogo.csv");
        try (Writer escritor = Files.newBufferedWriter(fichero)) {
            config.store(escritor, "Configuración de la tienda");       // reescribe el fichero completo
        }
        System.out.print(Files.readString(fichero));
        Files.delete(fichero);
    }
}

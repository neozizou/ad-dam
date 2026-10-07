package es.dam.tienda.fichero;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Texto separado por punto y coma, con una línea de cabecera. Codificación UTF-8. */
public class FormatoCsv implements FormatoProductos {

    private static final char SEPARADOR = ';';
    private static final String CABECERA = "codigo;nombre;precio;stock";

    @Override
    public List<ProductoDto> leer(Path ruta) throws IOException {
        List<ProductoDto> productos = new ArrayList<>();
        try (BufferedReader lector = Files.newBufferedReader(ruta)) {
            String linea = lector.readLine();                 // la cabecera no son datos
            int numero = 1;
            while ((linea = lector.readLine()) != null) {
                numero++;
                if (linea.isBlank()) {
                    continue;
                }
                List<String> campos = dividir(linea);
                if (campos.size() != 4) {
                    throw new IOException("Línea " + numero + ": se esperaban 4 campos y hay " + campos.size());
                }
                try {
                    productos.add(new ProductoDto(campos.get(0), campos.get(1),
                            new BigDecimal(campos.get(2)), Integer.parseInt(campos.get(3))));
                } catch (NumberFormatException e) {
                    throw new IOException("Línea " + numero + ": número no válido", e);
                }
            }
        }
        return productos;
    }

    @Override
    public void escribir(Path ruta, List<ProductoDto> productos) throws IOException {
        try (BufferedWriter escritor = Files.newBufferedWriter(ruta)) {
            escritor.write(CABECERA);
            escritor.newLine();
            for (ProductoDto p : productos) {
                escritor.write(String.join(String.valueOf(SEPARADOR),
                        escapar(p.codigo()), escapar(p.nombre()),
                        p.precio().toPlainString(), String.valueOf(p.stock())));
                escritor.newLine();
            }
        }
    }

    /** Entrecomilla un campo si contiene el separador o comillas ("" representa una comilla). */
    static String escapar(String campo) {
        if (campo.indexOf(SEPARADOR) >= 0 || campo.indexOf('"') >= 0) {
            return '"' + campo.replace("\"", "\"\"") + '"';
        }
        return campo;
    }

    /** Divide una línea en campos respetando las comillas: "Cable; 2 m" es un solo campo. */
    static List<String> dividir(String linea) {
        List<String> campos = new ArrayList<>();
        StringBuilder actual = new StringBuilder();
        boolean entreComillas = false;
        for (int i = 0; i < linea.length(); i++) {
            char c = linea.charAt(i);
            if (entreComillas) {
                if (c == '"' && i + 1 < linea.length() && linea.charAt(i + 1) == '"') {
                    actual.append('"');                       // "" dentro de comillas
                    i++;
                } else if (c == '"') {
                    entreComillas = false;
                } else {
                    actual.append(c);
                }
            } else if (c == '"') {
                entreComillas = true;
            } else if (c == SEPARADOR) {
                campos.add(actual.toString());
                actual.setLength(0);
            } else {
                actual.append(c);
            }
        }
        campos.add(actual.toString());
        return campos;
    }
}

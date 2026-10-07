import java.io.IOException;
import java.io.RandomAccessFile;
import java.math.BigDecimal;

/**
 * Productos en registros de longitud fija: código (6 caracteres), nombre (30 caracteres),
 * precio en céntimos (long) y stock (int). Cada registro ocupa 84 bytes.
 */
public class CatalogoAleatorio implements AutoCloseable {

    static final int LONG_CODIGO = 6;                               // caracteres
    static final int LONG_NOMBRE = 30;                              // caracteres
    static final int TAM_REGISTRO = (LONG_CODIGO + LONG_NOMBRE) * 2 + Long.BYTES + Integer.BYTES;   // 84 bytes
    static final int DESPL_STOCK = (LONG_CODIGO + LONG_NOMBRE) * 2 + Long.BYTES;                   // 80

    private final RandomAccessFile fichero;

    public CatalogoAleatorio(String ruta) throws IOException {
        fichero = new RandomAccessFile(ruta, "rw");                 // lectura y escritura
    }

    public long numeroRegistros() throws IOException {
        return fichero.length() / TAM_REGISTRO;
    }

    /** Añade un registro al final del fichero. */
    public void agregar(String codigo, String nombre, BigDecimal precio, int stock) throws IOException {
        fichero.seek(fichero.length());
        escribirTexto(codigo, LONG_CODIGO);
        escribirTexto(nombre, LONG_NOMBRE);
        fichero.writeLong(precio.movePointRight(2).longValueExact());
        fichero.writeInt(stock);
    }

    /** Lee el registro número n (empezando en 0) sin leer los anteriores. */
    public String leer(long n) throws IOException {
        fichero.seek(n * TAM_REGISTRO);
        String codigo = leerTexto(LONG_CODIGO);
        String nombre = leerTexto(LONG_NOMBRE);
        BigDecimal precio = BigDecimal.valueOf(fichero.readLong(), 2);
        int stock = fichero.readInt();
        return codigo + " | " + nombre + " | " + precio + " | " + stock;
    }

    /** Cambia solo el stock del registro n: escribe 4 bytes en mitad del fichero. */
    public void cambiarStock(long n, int stock) throws IOException {
        fichero.seek(n * TAM_REGISTRO + DESPL_STOCK);
        fichero.writeInt(stock);
    }

    private void escribirTexto(String texto, int longitud) throws IOException {
        StringBuilder relleno = new StringBuilder(texto);
        relleno.setLength(longitud);                                // recorta o rellena con '\0'
        fichero.writeChars(relleno.toString());                     // 2 bytes por carácter
    }

    private String leerTexto(int longitud) throws IOException {
        char[] letras = new char[longitud];
        for (int i = 0; i < longitud; i++) {
            letras[i] = fichero.readChar();
        }
        return new String(letras).replace("\0", "").strip();
    }

    @Override
    public void close() throws IOException {
        fichero.close();
    }

    public static void main(String[] args) throws IOException {
        try (CatalogoAleatorio catalogo = new CatalogoAleatorio("catalogo.bin")) {
            catalogo.agregar("TEC01", "Teclado mecánico", new BigDecimal("59.90"), 12);
            catalogo.agregar("RAT01", "Ratón inalámbrico", new BigDecimal("24.50"), 30);
            catalogo.agregar("MON01", "Monitor 27 pulgadas", new BigDecimal("219.00"), 4);

            System.out.println(catalogo.numeroRegistros() + " registros");   // 3 registros
            System.out.println(catalogo.leer(2));                  // MON01 | Monitor 27 pulgadas | 219.00 | 4
            catalogo.cambiarStock(0, 9);
            System.out.println(catalogo.leer(0));                  // TEC01 | Teclado mecánico | 59.90 | 9
        }
        System.out.println(new java.io.File("catalogo.bin").length() + " bytes");   // 252 bytes
        new java.io.File("catalogo.bin").delete();
    }
}

package es.dam.tienda.fichero;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Fichero binario propio: una firma que identifica el formato, el número de
 * productos y, después, los campos de cada producto en un orden fijo.
 * El precio se guarda en céntimos.
 */
public class FormatoBinario implements FormatoProductos {

    private static final int FIRMA = 0x54445031;    // los bytes de "TDP1": Tienda, Datos de Productos, versión 1

    @Override
    public List<ProductoDto> leer(Path ruta) throws IOException {
        try (DataInputStream entrada = new DataInputStream(
                new BufferedInputStream(Files.newInputStream(ruta)))) {
            if (entrada.readInt() != FIRMA) {
                throw new IOException(ruta + " no es un fichero binario de productos");
            }
            int cantidad = entrada.readInt();
            List<ProductoDto> productos = new ArrayList<>();
            for (int i = 0; i < cantidad; i++) {
                String codigo = entrada.readUTF();
                String nombre = entrada.readUTF();
                BigDecimal precio = BigDecimal.valueOf(entrada.readLong(), 2);   // céntimos → euros
                int stock = entrada.readInt();
                productos.add(new ProductoDto(codigo, nombre, precio, stock));
            }
            return productos;
        }
    }

    @Override
    public void escribir(Path ruta, List<ProductoDto> productos) throws IOException {
        try (DataOutputStream salida = new DataOutputStream(
                new BufferedOutputStream(Files.newOutputStream(ruta)))) {
            salida.writeInt(FIRMA);
            salida.writeInt(productos.size());
            for (ProductoDto p : productos) {
                salida.writeUTF(p.codigo());
                salida.writeUTF(p.nombre());
                salida.writeLong(p.precio().movePointRight(2).longValueExact());   // euros → céntimos
                salida.writeInt(p.stock());
            }
        }
    }
}

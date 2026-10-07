package es.dam.tienda.consola;

import java.math.BigDecimal;
import java.util.Scanner;

/** Lectura validada de datos desde el teclado. */
public class Consola {

    private final Scanner teclado = new Scanner(System.in);

    /** Lee una línea no vacía, sin espacios al principio ni al final. */
    public String leerTexto(String mensaje) {
        while (true) {
            System.out.print(mensaje);
            String linea = teclado.nextLine().strip();
            if (!linea.isEmpty()) {
                return linea;
            }
            System.out.println("  El valor no puede estar vacío.");
        }
    }

    /** Lee un entero entre min y max, ambos incluidos. */
    public int leerEntero(String mensaje, int min, int max) {
        while (true) {
            String linea = leerTexto(mensaje);
            try {
                int valor = Integer.parseInt(linea);
                if (valor >= min && valor <= max) {
                    return valor;
                }
                System.out.printf("  Debe estar entre %d y %d.%n", min, max);
            } catch (NumberFormatException e) {
                System.out.println("  No es un número entero: " + linea);
            }
        }
    }

    /** Lee un decimal; admite coma o punto como separador ("12,50" o "12.50"). */
    public BigDecimal leerDecimal(String mensaje) {
        while (true) {
            String linea = leerTexto(mensaje).replace(',', '.');
            try {
                return new BigDecimal(linea);
            } catch (NumberFormatException e) {
                System.out.println("  No es un número decimal: " + linea);
            }
        }
    }
}

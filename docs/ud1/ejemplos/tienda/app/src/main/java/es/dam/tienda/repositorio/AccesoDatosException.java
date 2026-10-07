package es.dam.tienda.repositorio;

/**
 * Error al leer o guardar datos. Envuelve la excepción original (IOException,
 * SQLException…) para que las capas superiores no dependan de dónde están los datos.
 */
public class AccesoDatosException extends RuntimeException {

    public AccesoDatosException(String mensaje, Throwable causa) {
        super(mensaje, causa);
    }
}

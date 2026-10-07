package es.dam.tienda.servicio;

/** Se lanza cuando se pide un producto que no existe. */
public class ProductoNoEncontradoException extends RuntimeException {

    public ProductoNoEncontradoException(String codigo) {
        super("No existe ningún producto con código " + codigo);
    }
}

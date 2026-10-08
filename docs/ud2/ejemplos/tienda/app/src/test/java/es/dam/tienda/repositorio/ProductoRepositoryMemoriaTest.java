package es.dam.tienda.repositorio;

class ProductoRepositoryMemoriaTest extends ProductoRepositoryContrato {

    @Override
    protected ProductoRepository crearRepositorio() {
        return new ProductoRepositoryMemoria();
    }
}

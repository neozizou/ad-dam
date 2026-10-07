package es.dam.tienda.fichero;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import tools.jackson.core.JacksonException;
import tools.jackson.databind.SerializationFeature;
import tools.jackson.databind.json.JsonMapper;

/** Un array JSON de objetos, legible y con sangría. Usa Jackson 3. */
public class FormatoJson implements FormatoProductos {

    private final JsonMapper mapper = JsonMapper.builder()
            .enable(SerializationFeature.INDENT_OUTPUT)       // con sangría, para leerlo a simple vista
            .build();

    @Override
    public List<ProductoDto> leer(Path ruta) throws IOException {
        String json = Files.readString(ruta);
        if (json.isBlank()) {
            return List.of();
        }
        try {
            return List.of(mapper.readValue(json, ProductoDto[].class));
        } catch (JacksonException e) {
            throw new IOException("JSON no válido en " + ruta + ": " + e.getMessage(), e);
        }
    }

    @Override
    public void escribir(Path ruta, List<ProductoDto> productos) throws IOException {
        Files.writeString(ruta, mapper.writeValueAsString(productos));
    }
}

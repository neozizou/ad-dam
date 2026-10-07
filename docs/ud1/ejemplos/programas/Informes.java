import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;

public class Informes {

    record ProductoDto(String codigo, String nombre, BigDecimal precio, int stock) {}

    public static void main(String[] args) {
        List<ProductoDto> catalogo = List.of(
                new ProductoDto("TEC01", "Teclado mecánico", new BigDecimal("59.90"), 12),
                new ProductoDto("TEC02", "Teclado compacto", new BigDecimal("34.90"), 0),
                new ProductoDto("RAT01", "Ratón inalámbrico", new BigDecimal("24.50"), 30),
                new ProductoDto("MON01", "Monitor 27 pulgadas", new BigDecimal("219.00"), 4),
                new ProductoDto("CAB01", "Cable USB-C 2 m", new BigDecimal("8.95"), 0));

        // Agrupar por familia (las tres primeras letras del código), en orden alfabético
        Map<String, List<String>> porFamilia = catalogo.stream()
                .collect(Collectors.groupingBy(p -> p.codigo().substring(0, 3), TreeMap::new,
                        Collectors.mapping(ProductoDto::codigo, Collectors.toList())));
        System.out.println(porFamilia);       // {CAB=[CAB01], MON=[MON01], RAT=[RAT01], TEC=[TEC01, TEC02]}

        // Partir en dos grupos: con stock y agotados
        Map<Boolean, Long> conStock = catalogo.stream()
                .collect(Collectors.partitioningBy(p -> p.stock() > 0, Collectors.counting()));
        System.out.println(conStock);         // {false=2, true=3}

        // Índice por código para búsquedas rápidas
        Map<String, ProductoDto> porCodigo = catalogo.stream()
                .collect(Collectors.toMap(ProductoDto::codigo, p -> p));
        System.out.println(porCodigo.get("MON01").nombre());    // Monitor 27 pulgadas

        // Comparar dos versiones del catálogo con operaciones de conjuntos
        Set<String> ayer = Set.of("TEC01", "TEC02", "RAT01", "IMP01");
        Set<String> hoy = porCodigo.keySet();
        Set<String> altas = new TreeSet<>(hoy);
        altas.removeAll(ayer);                                  // en hoy y no en ayer
        Set<String> bajas = new TreeSet<>(ayer);
        bajas.removeAll(hoy);                                   // en ayer y no en hoy
        Set<String> comunes = new TreeSet<>(hoy);
        comunes.retainAll(ayer);                                // en los dos
        System.out.println("Altas " + altas + ", bajas " + bajas + ", comunes " + comunes);
        // Altas [CAB01, MON01], bajas [IMP01], comunes [RAT01, TEC01, TEC02]
    }
}

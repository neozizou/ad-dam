# Tienda · ejemplo de referencia del Hito 1

Gestión de productos de una tienda de informática por consola, con los datos guardados en un fichero.
Es el ejemplo que acompaña a la UD1 de Acceso a Datos (2.º DAM).

## Requisitos

- JDK 25 (si no está instalado, Gradle lo descarga gracias al *toolchain*).
- Gradle 9 instalado **solo la primera vez**, para generar el *wrapper* (este ejemplo no lo incluye): `gradle wrapper`.

## Configuración

`config.properties`, en la raíz del proyecto:

```properties
datos.ruta=datos/productos.json
```

La extensión del fichero decide el formato: `json`, `csv`, `xml` o `dat`. Si no existe `config.properties`, se usa `datos/productos.json`.

## Ejecutar y probar

| | Windows (PowerShell) | macOS y Linux |
|---|---|---|
| Ejecutar | `.\gradlew run -q --console=plain` | `./gradlew run -q --console=plain` |
| Pruebas | `.\gradlew test` | `./gradlew test` |
| Documentación | `.\gradlew javadoc` | `./gradlew javadoc` |

## Formato de los ficheros

Todos los ficheros de texto usan UTF-8. Los precios van en euros con punto decimal.

- **JSON** (`.json`): un array de objetos con `codigo`, `nombre`, `precio` (número) y `stock` (entero).
- **CSV** (`.csv`): separador `;`, primera línea de cabecera `codigo;nombre;precio;stock`. Los campos que contienen `;` o comillas van entre comillas, con `""` para representar una comilla.
- **XML** (`.xml`): elemento raíz `catalogo` con un elemento `producto` por producto; el código es el atributo `codigo` y `nombre`, `precio` y `stock` son elementos hijos.
- **Binario** (`.dat`): firma `TDP1` (4 bytes), número de productos (`int`) y, por cada producto, código y nombre (`writeUTF`), precio en céntimos (`long`) y stock (`int`).

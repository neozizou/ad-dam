# Tienda · ejemplo de referencia del Hito 0

Gestión de productos de una tienda de informática por consola, con los datos en memoria.
Es el ejemplo que acompaña a la UD0 de Acceso a Datos (2.º DAM).

## Requisitos

- JDK 25 (si no está instalado, Gradle lo descarga gracias al *toolchain*).
- Gradle 9 instalado **solo la primera vez**, para generar el *wrapper* (este ejemplo no lo incluye):

```bash
gradle wrapper
```

## Ejecutar y probar

| | Windows (PowerShell) | macOS y Linux |
|---|---|---|
| Ejecutar | `.\gradlew run -q --console=plain` | `./gradlew run -q --console=plain` |
| Pruebas | `.\gradlew test` | `./gradlew test` |
| Documentación | `.\gradlew javadoc` | `./gradlew javadoc` |

El informe de pruebas queda en `app/build/reports/tests/test/index.html`
y la documentación en `app/build/docs/javadoc/index.html`.

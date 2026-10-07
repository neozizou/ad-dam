# Materiales de Acceso a Datos · 2.º DAM (curso 2026-2027)

Este repositorio contiene los apuntes del módulo Acceso a Datos que imparte Jaime en 2.º del CFGS Desarrollo de Aplicaciones Multiplataforma, en Granada. Se publican con GitHub Pages desde la carpeta `docs/`. Responde y escribe siempre en español.

## Estructura

- `docs/`: la web. `index.md` es la portada; cada unidad está en `docs/udN/index.md`, con sus figuras en `img/` y su código en `ejemplos/`.
- `docs/_config.yml`: Jekyll con el tema Just the Docs (`remote_theme`). Cada página de unidad lleva *front matter* con `title` y `nav_order`, y un índice `{:toc}` tras la línea de versión.
- `herramientas/figuras/`: los generadores Python de las figuras SVG (ver su README).

## Decisiones del módulo (no cambiarlas sin consultarlo)

- Horario: martes 1 h, miércoles 1 h y jueves 2 h, del 16/09/2026 al 16/02/2027 (78 h reales; 72 de docencia y 6 reservadas a pruebas el 17/12, 22/12, 11/02 y 16/02).
- Unidades: UD0 Java desde C++ (8 h), UD1 Ficheros (12 h), UD2 JDBC (14 h), UD3 Hibernate/JPA (12 h), UD4 BD objeto-relacionales y orientadas a objetos (6 h), UD5 MongoDB (10 h), UD6 Componentes con Spring Boot (10 h). El RA6 es transversal: su criterio c se trabaja en la UD1, d en la UD2, e en la UD3, f en la UD4, g en la UD5 y a, b, h, i en la UD6.
- Alumnado que viene de C++ (Programación de 1.º). Recuadros «Desde C++» cuando ayuden.
- Java 25 (Temurin), Gradle 9 con Kotlin DSL, wrapper, catálogo de versiones y toolchain; VS Code. Nada de Maven ni de interfaces gráficas: consola hasta la UD5 y API REST en la UD6.
- Versiones verificadas: JUnit 6.1.1, Jackson 3.2.1 (`tools.jackson.core`), Spring Boot 4.1, Hibernate 7 con `jakarta.persistence`.
- Toda orden de terminal en dos versiones: PowerShell (Windows) y bash/zsh (macOS y Linux).
- Proyecto integrador: el ejemplo de los apuntes es una tienda (Producto, Categoria, Cliente, Pedido, LineaPedido, EstadoPedido); el alumnado elige otro dominio. La interfaz `ProductoRepository` recibe una implementación nueva en cada unidad (Memoria, Fichero, Jdbc, Jpa, ObjectDb, Mongo) y solo `App` conoce la implementación concreta.
- Referencia: los apuntes de datos.codeandcoke.com (Santiago Faci). Si están desfasados, se usan versiones actuales y se explica en la «Nota de actualización» de la bibliografía de cada unidad.

## Formato de cada unidad

Título y «*Acceso a Datos · 2.º DAM · Versión del dd/mm/aaaa*» (actualiza la fecha al cambiar una unidad). Después: presentación con horas; tabla de criterios de evaluación → apartados; temporalización por sesiones con fecha; requisitos previos; convenciones; apartados N.x; «Práctica de la unidad · Hito N del proyecto integrador» con entregables, defensa oral de 5 minutos y tabla criterio → evidencia; resumen en tabla; bibliografía con «Todas las fuentes web se consultaron el …» y nota de actualización.

- Listados numerados: `**Listado N.x.** Descripción` antes del bloque de código.
- Figuras: `![texto alternativo descriptivo](img/fig-N-x-nombre.svg)` y debajo `*Figura N.x. Pie.*`. Numeración por orden de aparición; si se insertan figuras o listados, renumera y corrige las referencias.
- Recuadros: `> **Desde C++.** …`. Ejercicios en `### Para practicar`, con (A) para los autónomos.
- Sin `<` ni `>` sueltos fuera del código en el texto o en los textos alternativos (kramdown los toma por HTML).
- Sin dobles llaves de apertura ni una llave seguida de un signo de porcentaje en ningún Markdown, tampoco dentro de bloques de código: Jekyll las interpreta como Liquid y la publicación falla. Si un ejemplo las necesita, envuélvelo en un bloque `raw` de Liquid. Esta regla vale también para este fichero y para el README.
- Tablas sin `|` dentro de las celdas.

## Figuras

Se generan con `herramientas/figuras/`. Usa `lib.py` (misma paleta y funciones) para las nuevas, fondo blanco y texto alternativo completo. Tras cambiar una, ejecuta su script y revisa la PNG con `previsualizar.py`. Para DER y diagramas de clases, la notación de las Figuras 0.8 y 0.9.

## Código

Todo el código de los apuntes debe compilar y ejecutarse con JDK 25, y las salidas que se muestran deben ser reales. El código de los ejemplos vive en `docs/udN/ejemplos/`; los listados del Markdown deben coincidir con esos ficheros. Para comprobarlo: `gradle wrapper` (una vez) y `./gradlew build` en la carpeta del ejemplo.

## Publicación

GitHub Pages publica desde la rama `main` y la carpeta **`/docs`** (Settings → Pages). Si se elige la raíz, Jekyll procesa también este fichero y el README, y la web no es la de los apuntes. Cada *push* lanza la tarea «pages build and deployment» en la pestaña Actions: si falla, el error aparece en el paso *build*.

## Git

Mensajes de *commit* en español, en imperativo y concretos («UD1: corrige la figura 1.4», «Añade la UD2»). Haz *commit* y *push* solo cuando Jaime lo pida o lo confirme.

## Pendiente

- Verificar con Jackson real el formato JSON de la UD1 (`docs/ud1/ejemplos/tienda`: `gradle wrapper` y `./gradlew test`); en el entorno donde se escribió no había acceso a Maven Central.
- Decidir si se suben los wrappers de Gradle de los ejemplos.
- Siguiente unidad: UD2 · JDBC (RA2 y RA6.d): conectores, H2 embebido frente a MariaDB (máquina e2-micro de Google Cloud), DataSource y credenciales en `config.properties`, del diagrama de clases al modelo relacional (con DER), PreparedStatement e inyección SQL, claves generadas, lotes, transacciones, procedimientos almacenados y `ProductoRepositoryJdbc`.
- Formato de las transparencias: por decidir.

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
- Versiones verificadas: JUnit 6.1.1, Jackson 3.2.1 (`tools.jackson.core`), MariaDB Connector/J 3.5.10, H2 2.5.252, HikariCP 7.1.0, SLF4J 2.0.20, Spring Boot 4.1, Hibernate 7 con `jakarta.persistence`. MariaDB: series LTS 11.8 y 12.3.
- Bases de datos (desde la UD2): H2 en modo MariaDB (`MODE=MariaDB;DATABASE_TO_LOWER=TRUE`) para las pruebas y como base de datos por defecto; MariaDB como servidor. El mismo SQL debe funcionar en los dos. Pool HikariCP; los repositorios reciben un `DataSource`. Credenciales en `config.properties` (no se sube; se sube `config.ejemplo.properties`) y la clave en la variable de entorno `TIENDA_DB_CLAVE`. Scripts SQL en `src/main/resources/sql`.
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

## Entrega de cada unidad

Al terminar una unidad, se entrega el proyecto completo en un único zip (todo el contenido del repositorio, sin la carpeta `.git`), para que Jaime lo descomprima sobre su carpeta local y lo sobrescriba todo. Si un fichero se renombra o se elimina, hay que avisarlo, porque descomprimir encima no borra los ficheros antiguos.

## Git

Mensajes de *commit* en español, en imperativo y concretos («UD1: corrige la figura 1.4», «Añade la UD2»). Haz *commit* y *push* solo cuando Jaime lo pida o lo confirme.

## Estado del ejemplo de la tienda

Cada unidad publica su estado en `docs/udN/ejemplos/tienda`. UD0: repositorio en memoria. UD1: `ProductoRepositoryFichero` con formatos CSV, JSON, XML y binario. UD2: `BaseDatos` (HikariCP), `EjecutorScripts`, `ProductoRepositoryJdbc`, `PedidoRepository` y `PedidoRepositoryJdbc` (transacción al guardar un pedido), `PedidoService`, `MenuPrincipal` y `MenuPedidos`; el `Pedido` guarda el identificador del cliente, no un objeto `Cliente` (la UD3 lo convertirá en referencia). Los programas cortos de la UD2 están en `docs/ud2/ejemplos/demos`.

## Pendiente

- Verificar con Gradle en un equipo real los ejemplos de la UD1 y la UD2 (`gradle wrapper` y `./gradlew build` en cada carpeta de ejemplos): en el entorno donde se escribieron no había acceso a Maven Central. El código JDBC se probó con MariaDB 10.11, Connector/J 2.7.6, H2 2.2.220 y HikariCP 2.7.9; el formato JSON de la UD1 no se ha podido ejecutar con Jackson 3.
- Confirmar el nombre del servidor MariaDB del aula (máquina e2-micro de Google Cloud) y cómo se crean los usuarios y las bases de datos del alumnado: la UD2 lo menciona sin dar datos.
- Decidir si se suben los wrappers de Gradle de los ejemplos.
- Siguiente unidad: UD3 · Hibernate/JPA (RA3 y RA6.e): `persistence.xml`, mapeo de entidades, relaciones y el problema N+1, ciclo de vida (`persist`, `merge`, `remove`, `find`), JPQL/HQL y SQL nativo, transacciones y bloqueo optimista con `@Version`, y `ProductoRepositoryJpa` con el mismo contrato.
- Formato de las transparencias: por decidir.

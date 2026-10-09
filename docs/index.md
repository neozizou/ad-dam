# Acceso a Datos

*CFGS Desarrollo de Aplicaciones Multiplataforma · 2.º curso · Curso 2026-2027*

Apuntes, ejemplos y prácticas del módulo. Cada unidad se publica al empezar y se actualiza durante el curso; la fecha de la versión aparece al principio de cada una.

## Cómo está organizado el módulo

Las aplicaciones se escriben en **Java 25**, se construyen con **Gradle** y se editan con **VS Code**. No hay interfaces gráficas: hasta la UD5 las aplicaciones son de consola y en la UD6 se convierten en un servicio REST.

Todo el curso gira en torno a un **proyecto integrador** que construyes tú, sobre un dominio que eliges en el Hito 0. El modelo de clases y la interfaz de usuario apenas cambian; lo que cambia en cada unidad es **dónde se guardan los datos**: en memoria, en ficheros, en una base de datos relacional, en una base de datos orientada a objetos y en MongoDB.

| Unidad | Horas | Fechas | Resultados de aprendizaje |
|---|---|---|---|
| [UD0 · Java para quien ya programa en C++](ud0/index.md) | 8 | 16/09 – 29/09 | Nivelación |
| [UD1 · Ficheros](ud1/index.md) | 12 | 30/09 – 20/10 | RA1, RA6 |
| [UD2 · Bases de datos relacionales con JDBC](ud2/index.md) | 14 | 21/10 – 12/11 | RA2, RA6 |
| UD3 · Mapeo objeto-relacional con Hibernate y JPA | 12 | 12/11 – 03/12 | RA3, RA6 |
| UD4 · Bases de datos objeto-relacionales y orientadas a objetos | 6 | 03/12 – 16/12 | RA4, RA6 |
| Prueba de la primera evaluación | 3 | 17/12 y 22/12 | |
| UD5 · Bases de datos documentales con MongoDB | 10 | 07/01 – 21/01 | RA5, RA6 |
| UD6 · Componentes de acceso a datos con Spring Boot | 10 | 26/01 – 10/02 | RA6 |
| Prueba final y recuperación | 3 | 11/02 y 16/02 | |

El módulo tiene 4 horas semanales: martes (1 h), miércoles (1 h) y jueves (2 h). Las fechas siguen el calendario escolar de Granada; las unidades sin enlace se publicarán al llegar a ellas.

## Resultados de aprendizaje

1. Desarrolla aplicaciones que gestionan información almacenada en ficheros identificando el campo de aplicación de los mismos y utilizando clases específicas.
2. Desarrolla aplicaciones que gestionan información almacenada en bases de datos relacionales identificando y utilizando mecanismos de conexión.
3. Gestiona la persistencia de los datos identificando herramientas de mapeo objeto relacional (ORM) y desarrollando aplicaciones que las utilizan.
4. Desarrolla aplicaciones que gestionan la información almacenada en bases de datos objeto relacionales y orientadas a objetos valorando sus características y utilizando los mecanismos de acceso incorporados.
5. Desarrolla aplicaciones que gestionan la información almacenada en bases de datos documentales nativas evaluando y utilizando clases específicas.
6. Programa componentes de acceso a datos identificando las características que debe poseer un componente y utilizando herramientas de desarrollo.

## Antes de empezar

Necesitas instalar el JDK 25, VS Code con las extensiones de Java y Gradle. La UD0 explica cómo hacerlo en Windows, macOS y Linux.

## Cómo leer los apuntes

- **Listado N.x**: código completo; el botón de la esquina de cada listado lo copia. El código de cada unidad está también en su carpeta de ejemplos, que puedes consultar y descargar desde el [repositorio del módulo](https://github.com/neozizou/ad-dam/tree/main/docs).
- **Windows · macOS y Linux**: cuando una orden cambia según el sistema, verás una versión para PowerShell y otra para bash o zsh. Si aparecen en pestañas, elige la tuya una vez y la web la recordará en todas las unidades.
- **Desde C++**: comparación directa con lo que ya conoces de 1.º.
- **Figura N.x**: esquemas y diagramas de lo que el código no deja ver.
- **Para practicar**: ejercicios al final de cada apartado; los marcados con (A) son autónomos.
- **Navegación**: la tabla de contenidos de la derecha marca el apartado que estás leyendo (en el móvil está dentro del menú ☰). Al desplazarte hacia arriba aparece el botón **Volver al principio**, y al pie de cada página tienes la unidad anterior y la siguiente. El icono de la luna, junto al buscador, activa el modo oscuro.

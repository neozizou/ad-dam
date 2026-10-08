# Tienda · ejemplo de referencia del Hito 2

Gestión de productos y pedidos de una tienda de informática por consola, con los datos en una base de datos relacional a través de JDBC.
Es el ejemplo que acompaña a la UD2 de Acceso a Datos (2.º DAM).

## Requisitos

- JDK 25 (si no está instalado, Gradle lo descarga gracias al *toolchain*).
- Gradle 9 instalado **solo la primera vez**, para generar el *wrapper* (este ejemplo no lo incluye): `gradle wrapper`.
- Opcional: un servidor MariaDB. Sin él, la tienda usa una base de datos H2 embebida en `datos/tienda.mv.db`.

## Base de datos

La tienda crea las tablas que falten al arrancar (`app/src/main/resources/sql/schema.sql`) y, si no hay productos, carga los datos de ejemplo (`datos-ejemplo.sql`).

Para usar MariaDB:

1. Crea la base de datos y el usuario (como administrador, con el cliente `mariadb`):

   ```sql
   CREATE DATABASE tienda CHARACTER SET utf8mb4;
   CREATE USER 'tienda'@'localhost' IDENTIFIED BY 'cambia-esta-clave';
   GRANT ALL PRIVILEGES ON tienda.* TO 'tienda'@'localhost';
   ```

2. Copia `config.ejemplo.properties` como `config.properties`.
3. Pon la clave en la variable de entorno `TIENDA_DB_CLAVE` (o en `db.clave`, solo en tu equipo):

   | Windows (PowerShell) | macOS y Linux |
   |---|---|
   | `$env:TIENDA_DB_CLAVE = "cambia-esta-clave"` | `export TIENDA_DB_CLAVE=cambia-esta-clave` |

4. Para crear los procedimientos almacenados (solo MariaDB):
   `mariadb -u tienda -p tienda -e "source app/src/main/resources/sql/procedimientos.sql"`

## Ejecutar y probar

| | Windows (PowerShell) | macOS y Linux |
|---|---|---|
| Ejecutar | `.\gradlew run -q --console=plain` | `./gradlew run -q --console=plain` |
| Pruebas | `.\gradlew test` | `./gradlew test` |
| Documentación | `.\gradlew javadoc` | `./gradlew javadoc` |

Las pruebas usan H2 en memoria: no necesitan ningún servidor.

## Modelo relacional

```text
categoria    (id PK, nombre UNIQUE)
producto     (codigo PK, nombre, precio, stock, categoria_id FK → categoria)
cliente      (id PK, nombre, email UNIQUE, fecha_alta)
pedido       (numero PK, cliente_id FK → cliente, fecha, estado)
linea_pedido (pedido_numero FK → pedido, producto_codigo FK → producto, cantidad, precio_unitario)
             PK (pedido_numero, producto_codigo)
```

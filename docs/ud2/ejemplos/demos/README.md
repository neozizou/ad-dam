# Programas de ejemplo de la UD2

Programas cortos que acompañan a los apuntes de la UD2. Se conectan a la base de datos `tienda` de MariaDB, así que antes:

1. Ejecuta una vez la tienda (`../tienda`) contra MariaDB, para que cree las tablas y cargue los datos de ejemplo.
2. Crea los procedimientos almacenados: `mariadb -u tienda -p tienda -e "source ../tienda/app/src/main/resources/sql/procedimientos.sql"`.
3. Copia `config.ejemplo.properties` como `config.properties` y define la variable de entorno `TIENDA_DB_CLAVE` con la clave.

Para ejecutar uno (por defecto, `ProbarConexion`):

| Windows (PowerShell) | macOS y Linux |
|---|---|
| `.\gradlew run -q --console=plain -Pdemo=InyeccionSql` | `./gradlew run -q --console=plain -Pdemo=InyeccionSql` |

También puedes usar el enlace **Run** que VS Code muestra encima de cada `main`.

| Programa | Apartado |
|---|---|
| `ProbarConexion` | 2.3 Conexión y metadatos |
| `TiempoConexion` | 2.3 Conexiones nuevas frente a un pool |
| `ConsultaLibre` | 2.5 `ResultSet` y `ResultSetMetaData` |
| `InyeccionSql` | 2.5 Inyección SQL |
| `CargaMasiva` | 2.6 Lotes y transacciones |
| `Procedimientos` | 2.8 Procedimientos almacenados |
| `ErroresSql` | 2.9 `SQLException` |
| `AgotarPool` | 2.9 Conexiones que no se cierran |

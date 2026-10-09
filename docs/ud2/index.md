# Unidad Didáctica 2 · Bases de datos relacionales con JDBC

*Acceso a Datos · 2.º DAM · Versión del 08/10/2026*

## Presentación de la unidad

Los ficheros de la UD1 funcionan mientras un solo programa guarda unos pocos miles de registros. Cuando varios usuarios trabajan a la vez, los datos se relacionan entre sí y una operación tiene que hacerse entera o no hacerse, se necesita un **gestor de bases de datos**. En esta unidad, de 14 horas, conectas tus programas Java a bases de datos relacionales mediante **JDBC**, la interfaz estándar de Java para hacerlo, y aprovechas lo que ya sabes de SQL de Bases de Datos de 1.º.

Trabajarás con dos gestores: **H2**, que se ejecuta dentro de tu propio programa, y **MariaDB**, un servidor independiente. El mismo código servirá para los dos. Al terminar, tu proyecto integrador guardará sus datos en una base de datos con un componente nuevo que implementa, otra vez, la misma interfaz de repositorio.

### Resultados de aprendizaje y criterios de evaluación

**RA2.** Desarrolla aplicaciones que gestionan información almacenada en bases de datos relacionales identificando y utilizando mecanismos de conexión.

**RA6.** Programa componentes de acceso a datos identificando las características que debe poseer un componente y utilizando herramientas de desarrollo (solo el criterio d en esta unidad).

| Criterio de evaluación | Apartados |
|---|---|
| 2a) Se han valorado las ventajas e inconvenientes de utilizar conectores | 2.1 |
| 2b) Se han utilizado gestores de bases de datos embebidos e independientes | 2.2 |
| 2c) Se ha utilizado el conector idóneo en la aplicación | 2.1, 2.2 |
| 2d) Se ha establecido la conexión | 2.3 |
| 2e) Se ha definido la estructura de la base de datos | 2.4 |
| 2f) Se han desarrollado aplicaciones que modifican el contenido de la base de datos | 2.6 |
| 2g) Se han definido los objetos destinados a almacenar el resultado de las consultas | 2.5 |
| 2h) Se han eliminado los objetos una vez finalizada su función | 2.9 (y en todos los apartados) |
| 2i) Se han gestionado las transacciones | 2.7 |
| 2j) Se han ejecutado procedimientos almacenados en la base de datos | 2.8 |
| 2k) Se han desarrollado aplicaciones que efectúan consultas y modificaciones | 2.5, 2.6, 2.10 |
| 6d) Se han programado componentes que gestionan mediante conectores información almacenada en bases de datos | 2.10 |

### Temporalización

| Sesión | Fecha | Horas | Contenidos |
|---|---|---|---|
| 1 | Miércoles 21/10/2026 | 1 | 2.1 Conectores y JDBC |
| 2 | Jueves 22/10/2026 | 2 | 2.2 Gestores embebidos e independientes (instalación de MariaDB) · 2.3 La conexión |
| 3 | Martes 27/10/2026 | 1 | 2.3 Credenciales, `DataSource` y pool (entrega del Hito 1) |
| 4 | Miércoles 28/10/2026 | 1 | 2.4 Del diagrama de clases al modelo relacional: actividad cooperativa |
| 5 | Jueves 29/10/2026 | 2 | 2.4 El script DDL · 2.5 Consultas y `ResultSet` |
| 6 | Martes 03/11/2026 | 1 | 2.5 `PreparedStatement` e inyección SQL |
| 7 | Miércoles 04/11/2026 | 1 | 2.6 Modificaciones, claves generadas y lotes |
| 8 | Jueves 05/11/2026 | 2 | 2.7 Transacciones · 2.8 Procedimientos almacenados |
| 9 | Martes 10/11/2026 | 1 | 2.9 Cierre de recursos y `SQLException` |
| 10 | Miércoles 11/11/2026 | 1 | 2.10 El componente JDBC |
| 11 | Jueves 12/11/2026 (primera hora) | 1 | Práctica: Hito 2 |

### Requisitos previos

- La UD1 completa y el Hito 1 entregado: el proyecto de esta unidad parte de él.
- SQL de Bases de Datos de 1.º: `CREATE TABLE` con claves primarias y ajenas, `SELECT` con `JOIN` y `GROUP BY`, `INSERT`, `UPDATE` y `DELETE`.
- Saber leer un diagrama entidad-relación y un diagrama de clases (Figuras 0.8, 0.9 y 0.12).

### Convenciones

Las mismas que en las unidades anteriores. Además, los programas cortos de esta unidad forman un proyecto de Gradle aparte, `ejemplos/demos`, que se conecta a la base de datos de la tienda; su README explica cómo ejecutar cada uno. Las salidas que verás en los listados se obtuvieron en un equipo con MariaDB 10.11, H2 2.2 y Connector/J 2.7: con las versiones del proyecto, los números de versión y algún mensaje del conector serán distintos.

---

## 2.1 Conectores y JDBC

### Qué es un conector

Un gestor de bases de datos es un programa que entiende SQL. Para usarlo desde Java hace falta algo que lleve las sentencias hasta el gestor y traiga los resultados de vuelta, convertidos en objetos de Java. Ese algo es el **conector** (o *driver*): una biblioteca que habla el protocolo de un gestor concreto.

Si cada conector tuviera sus propios métodos, cambiar de MariaDB a PostgreSQL obligaría a reescribir todo el acceso a datos. Para evitarlo, Java define **JDBC** (*Java Database Connectivity*): un conjunto de interfaces en los paquetes `java.sql` y `javax.sql`, incluidos en el JDK. Tu programa usa solo esas interfaces y cada conector las implementa para su gestor.

![Tu aplicación usa la API JDBC, con interfaces como DataSource, Connection, PreparedStatement, ResultSet y SQLException. Las implementan el conector de MariaDB, que habla con el servidor por la red en el puerto 3306, y el conector de H2, que incluye el propio gestor y escribe directamente en el fichero tienda.mv.db. Cambiar de gestor es cambiar el conector y la URL.](img/fig-2-1-jdbc.svg)

*Figura 2.1. JDBC: una interfaz común y un conector para cada gestor.*

Es la misma idea que `ProductoRepository` en tu proyecto: el resto del programa trabaja con una interfaz y la implementación concreta se elige en un único sitio. Aquí la interfaz la pone Java y las implementaciones, los fabricantes de cada gestor.

| Interfaz | Para qué |
|---|---|
| `DataSource` | Fábrica de conexiones; lo que reciben los repositorios |
| `Connection` | Una sesión abierta con la base de datos; también controla las transacciones |
| `Statement` y `PreparedStatement` | Una sentencia SQL que se envía al gestor; la segunda, con parámetros |
| `CallableStatement` | La llamada a un procedimiento almacenado |
| `ResultSet` | Las filas que devuelve una consulta |
| `SQLException` | Cualquier error del gestor o de la conexión |

> **Desde C++.** No hay un equivalente en la biblioteca estándar de C++: se usa la biblioteca de cliente de cada gestor (por ejemplo, la de MariaDB en C) o una capa común como ODBC, que es la inspiración directa de JDBC.

### Ventajas e inconvenientes de usar conectores

| Ventajas | Inconvenientes |
|---|---|
| El código usa una API estándar: cambiar de gestor cambia una dependencia y una URL | Hay que escribir el SQL a mano y convertir cada fila en un objeto (el «desajuste» entre objetos y tablas que resolverá la UD3) |
| Acceso completo al SQL del gestor: consultas complejas, procedimientos, funciones propias | El SQL va dentro de cadenas de texto: el compilador no detecta los errores, aparecen al ejecutar |
| Control fino del rendimiento: qué se consulta, cuándo, en qué transacción | Cada gestor tiene su dialecto de SQL: la portabilidad no es total |
| Es la base de todo lo demás: Hibernate (UD3) y Spring Data (UD6) usan JDBC por debajo | Hay que gestionar a mano las conexiones, las transacciones y el cierre de recursos |

Las alternativas son un **mapeo objeto-relacional** (ORM), que genera el SQL a partir de las clases y lo verás en la UD3, o las bibliotecas nativas de cada gestor, que atan el programa a ese gestor.

### Añadir los conectores al proyecto

Los conectores son dependencias de Gradle, como Jackson en la UD1. La tienda usa dos (MariaDB y H2) y una tercera biblioteca, HikariCP, que verás en el apartado 2.3:

**Listado 2.1.** Las dependencias de la UD2 en `gradle/libs.versions.toml` y en `app/build.gradle.kts`

```toml
[versions]
junit-jupiter = "6.1.1"
jackson = "3.2.1"
hikaricp = "7.1.0"
mariadb = "3.5.10"
h2 = "2.5.252"
slf4j = "2.0.20"

[libraries]
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit-jupiter" }
jackson-databind = { module = "tools.jackson.core:jackson-databind", version.ref = "jackson" }
hikaricp = { module = "com.zaxxer:HikariCP", version.ref = "hikaricp" }
mariadb-java-client = { module = "org.mariadb.jdbc:mariadb-java-client", version.ref = "mariadb" }
h2 = { module = "com.h2database:h2", version.ref = "h2" }
slf4j-simple = { module = "org.slf4j:slf4j-simple", version.ref = "slf4j" }
```

```kotlin
dependencies {
    implementation(libs.jackson.databind)                           // JSON (UD1)
    implementation(libs.hikaricp)                                   // pool de conexiones (UD2)
    runtimeOnly(libs.mariadb.java.client)                           // conector JDBC de MariaDB (UD2)
    runtimeOnly(libs.h2)                                            // gestor embebido H2 (UD2)
    runtimeOnly(libs.slf4j.simple)                                  // mensajes de HikariCP
    testImplementation(libs.junit.jupiter)
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
```

Fíjate en que los conectores son `runtimeOnly`: tu código no escribe nunca el nombre de una clase de MariaDB ni de H2, solo usa las interfaces de `java.sql`. Gradle no los pone en el *classpath* de compilación, así que si por error importaras una clase del conector, el programa no compilaría. Al ejecutar, JDBC busca entre los conectores disponibles el que reconoce la URL de conexión. En materiales antiguos verás una línea `Class.forName("com.mysql.jdbc.Driver")` para «cargar el driver»: desde JDBC 4.0 (Java 6) ya no hace falta.

`slf4j-simple` es la biblioteca con la que HikariCP escribe sus mensajes. El fichero `src/main/resources/simplelogger.properties` los limita a avisos y errores.

### Para practicar

1. Busca en Maven Central (<https://central.sonatype.com>) el conector JDBC de PostgreSQL y el de SQLite. Anota sus coordenadas y su última versión.
2. Cambia `runtimeOnly(libs.h2)` por `implementation(libs.h2)`, ejecuta `./gradlew :app:dependencies --configuration compileClasspath` y busca H2 en la salida. Vuelve a dejarlo como estaba y explica la diferencia.
3. (A) Compara la tabla de ventajas e inconvenientes con lo que hiciste en la UD1: ¿qué problemas del repositorio en fichero resuelve una base de datos y cuáles quedan igual?

---

## 2.2 Gestores embebidos e independientes

### Dos formas de ejecutar un gestor

Un gestor **embebido** es una biblioteca que se ejecuta dentro del proceso de tu programa y guarda los datos en un fichero: no hay que instalar ni arrancar nada. Un gestor **independiente** (o servidor) es otro programa, normalmente en otra máquina, al que se conectan por la red todos los clientes que lo necesiten.

![A la izquierda, un gestor embebido: tu código y el motor de H2 comparten la JVM y escriben en el fichero tienda.mv.db; no hay nada que instalar, pero solo un programa puede usarlo a la vez. A la derecha, un servidor independiente: tu programa con su conector y otros clientes, como el cliente mariadb o HeidiSQL, se conectan por la red al proceso mariadbd, que gestiona los datos, usuarios y permisos.](img/fig-2-2-embebido-servidor.svg)

*Figura 2.2. Gestor embebido y servidor independiente.*

| | Embebido | Independiente |
|---|---|---|
| Ejemplos | H2, SQLite, Apache Derby | MariaDB, MySQL, PostgreSQL, Oracle, SQL Server |
| Instalación | Ninguna: una dependencia más | Instalar, arrancar y administrar el servidor |
| Usuarios a la vez | Un programa (H2 admite un modo servidor, pero no es su uso habitual) | Muchos programas y usuarios |
| Seguridad | La del fichero | Usuarios, contraseñas y permisos por tabla |
| Usos típicos | Pruebas automáticas, aplicaciones de escritorio y móviles (SQLite en Android), prototipos | Aplicaciones con varios usuarios, servidores web, datos compartidos |

En este módulo usarás los dos, cada uno donde encaja: **H2** para las pruebas automáticas y para que la tienda funcione sin instalar nada, y **MariaDB** como gestor de la aplicación. Para que el mismo SQL sirva en ambos, H2 se abre en **modo MariaDB**, en el que imita el dialecto de MariaDB.

### Elegir el conector idóneo

El conector depende del gestor y debe ser compatible con tu versión de Java:

| Gestor | Conector | Coordenadas en Maven Central |
|---|---|---|
| MariaDB | MariaDB Connector/J 3.5 | `org.mariadb.jdbc:mariadb-java-client` |
| H2 | El propio H2 | `com.h2database:h2` |
| MySQL | MySQL Connector/J | `com.mysql:mysql-connector-j` |
| PostgreSQL (UD4) | PostgreSQL JDBC | `org.postgresql:postgresql` |

MariaDB nació como una bifurcación de MySQL y sigue entendiendo casi todo su SQL y su protocolo, pero conviene usar el conector de cada uno con su gestor: el de MariaDB conoce las particularidades de MariaDB.

### Instalar MariaDB

En clase usarás el servidor MariaDB del módulo: el profesor te dará el nombre de la máquina, tu usuario y tu base de datos. Para trabajar en casa, o sin conexión, instálalo también en tu equipo. Cualquier versión actual sirve; las de soporte largo son la 11.8 y la 12.3.

**Listado 2.2.** Instalación de MariaDB

=== "Windows (PowerShell)"

    ```powershell
    # El instalador pide la contraseña de root: apúntala.
    winget install MariaDB.Server
    # Si prefieres el asistente gráfico, descarga el .msi de https://mariadb.org/download/
    ```

=== "macOS y Linux (bash/zsh)"

    ```bash
    # macOS (Homebrew)
    brew install mariadb
    brew services start mariadb       # arranca ahora y en cada inicio de sesión

    # Ubuntu o Debian
    sudo apt install mariadb-server
    sudo systemctl status mariadb     # comprueba que está en marcha
    ```

Si usas Docker, también puedes arrancarlo en un contenedor: `docker run --name mariadb -e MARIADB_ROOT_PASSWORD=una-clave -p 3306:3306 -d mariadb:lts`.

Para administrarlo se usa el cliente de consola `mariadb`. Cómo se entra como administrador depende de la instalación: en Windows, `mariadb -u root -p` con la contraseña que elegiste; en macOS con Homebrew, `mariadb` sin más (tu usuario del sistema es administrador); en Linux, `sudo mariadb`. Si prefieres una herramienta gráfica, DBeaver Community es gratuita y funciona en los tres sistemas.

### Una base de datos y un usuario para la aplicación

Una aplicación nunca debe conectarse como `root`. Se crea un usuario con permisos solo sobre su base de datos:

**Listado 2.3.** Base de datos y usuario de la tienda (como administrador, en el cliente `mariadb`)

```sql
CREATE DATABASE tienda CHARACTER SET utf8mb4;
CREATE USER 'tienda'@'localhost' IDENTIFIED BY 'cambia-esta-clave';
GRANT ALL PRIVILEGES ON tienda.* TO 'tienda'@'localhost';
```

`utf8mb4` es la codificación UTF-8 completa (en MariaDB, `utf8` a secas solo admite caracteres de hasta 3 bytes). `'tienda'@'localhost'` significa «el usuario tienda cuando se conecta desde esta misma máquina». Comprueba que funciona con `mariadb -u tienda -p tienda`.

### Para practicar

1. Instala MariaDB, crea la base de datos y el usuario del Listado 2.3 y entra con `mariadb -u tienda -p tienda`. Ejecuta `SELECT VERSION();` y `SHOW TABLES;`.
2. Entra como `tienda` e intenta `CREATE DATABASE otra;`. Lee el error: ¿por qué es una buena noticia?
3. (A) Crea un segundo usuario, `consulta`, que solo pueda leer: `GRANT SELECT ON tienda.* TO 'consulta'@'localhost'`. Lo usarás en el apartado 2.5.

---

## 2.3 La conexión

### La URL de conexión

JDBC identifica la base de datos con una **URL**. Su primera parte dice qué conector debe atenderla; el resto lo interpreta ese conector.

![Partes de tres URL. jdbc:mariadb://localhost:3306/tienda?connectTimeout=5000 tiene el prefijo jdbc, el conector mariadb, la máquina, el puerto, la base de datos y opciones tras la interrogación. jdbc:h2:./datos/tienda;MODE=MariaDB;DATABASE_TO_LOWER=TRUE tiene el fichero, relativo al directorio de trabajo, y opciones separadas por punto y coma. jdbc:h2:mem:pruebas es una base de datos en memoria.](img/fig-2-3-url.svg)

*Figura 2.3. Anatomía de una URL JDBC.*

### `DriverManager`: la forma más directa

`DriverManager.getConnection(url, usuario, clave)` busca un conector que acepte la URL y abre una conexión. Los programas de ejemplo de la unidad la usan a través de esta clase auxiliar, que lee los datos de conexión de un fichero:

**Listado 2.4.** `demos/.../Conexion.java`

```java
package es.dam.demos;

import java.io.IOException;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

/** Lee los datos de conexión de config.properties y abre conexiones con DriverManager. */
public final class Conexion {

    private static final Properties CONFIG = cargar(Path.of("config.properties"));

    private Conexion() {
    }

    public static String url() {
        return CONFIG.getProperty("db.url", "jdbc:mariadb://localhost:3306/tienda");
    }

    public static String usuario() {
        return CONFIG.getProperty("db.usuario", "tienda");
    }

    /** La clave, de la variable de entorno TIENDA_DB_CLAVE o, si no existe, del fichero. */
    public static String clave() {
        String deEntorno = System.getenv("TIENDA_DB_CLAVE");
        return deEntorno != null ? deEntorno : CONFIG.getProperty("db.clave", "");
    }

    /** Abre una conexión nueva. Quien la pide es responsable de cerrarla. */
    public static Connection abrir() throws SQLException {
        return DriverManager.getConnection(url(), usuario(), clave());
    }

    private static Properties cargar(Path fichero) {
        Properties propiedades = new Properties();
        if (Files.exists(fichero)) {
            try (Reader lector = Files.newBufferedReader(fichero)) {
                propiedades.load(lector);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
        return propiedades;
    }
}
```

**Listado 2.5.** `ProbarConexion.java`: comprobar la conexión y ver qué hay al otro lado

```java
package es.dam.demos;

import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.SQLException;

/** Comprueba la conexión y muestra qué gestor y qué conector hay al otro lado. */
public class ProbarConexion {

    public static void main(String[] args) {
        System.out.println("Conectando con " + Conexion.url() + " …");
        try (Connection conexion = Conexion.abrir()) {
            DatabaseMetaData info = conexion.getMetaData();
            System.out.println("Gestor:   " + info.getDatabaseProductName() + " " + info.getDatabaseProductVersion());
            System.out.println("Conector: " + info.getDriverName() + " " + info.getDriverVersion());
            System.out.println("JDBC:     " + info.getJDBCMajorVersion() + "." + info.getJDBCMinorVersion());
            System.out.println("Usuario:  " + info.getUserName());
        } catch (SQLException e) {
            System.out.println("No se pudo conectar: " + e.getMessage());
            System.out.println("SQLState " + e.getSQLState() + ", código de error " + e.getErrorCode());
        }
    }
}
```

```text
Conectando con jdbc:mariadb://localhost:3306/tienda …
Gestor:   MariaDB 10.11.14-MariaDB-0ubuntu0.24.04.1
Conector: MariaDB Connector/J 2.7.6
JDBC:     4.2
Usuario:  tienda
```

`getMetaData()` devuelve un `DatabaseMetaData` con información del gestor: su nombre y versión, las tablas que contiene, sus columnas… La conexión se abre en el `try-with-resources` y se cierra al salir, pase lo que pase.

### Las credenciales, fuera del código

Una contraseña escrita en el código acaba en GitHub, en los ficheros compilados y en las manos de cualquiera que los lea. Las reglas son sencillas:

- La URL, el usuario y la clave van en un **fichero de configuración** que **no se sube** al repositorio: `config.properties` aparece en el `.gitignore`.
- En el repositorio se sube una **plantilla** sin datos reales, `config.ejemplo.properties`, para que quien clone el proyecto sepa qué tiene que rellenar.
- La clave, mejor aún, en una **variable de entorno**, que no se guarda en ningún fichero del proyecto.

**Listado 2.6.** `config.ejemplo.properties` de la tienda

```properties
# Copia este fichero como config.properties y ajusta los valores.
# config.properties no se sube al repositorio: está en .gitignore.
# Si no existe config.properties, la tienda usa una base de datos H2 embebida en datos/.

# Servidor MariaDB
db.url=jdbc:mariadb://localhost:3306/tienda
db.usuario=tienda
# La clave, mejor en la variable de entorno TIENDA_DB_CLAVE. Si no existe, se usa esta:
db.clave=

# H2 embebida (descomenta estas dos líneas y comenta las de MariaDB)
#db.url=jdbc:h2:./datos/tienda;MODE=MariaDB;DATABASE_TO_LOWER=TRUE
#db.usuario=sa
```

**Listado 2.7.** Definir la variable de entorno para la sesión actual de la terminal

=== "Windows (PowerShell)"

    ```powershell
    $env:TIENDA_DB_CLAVE = "cambia-esta-clave"
    .\gradlew run -q --console=plain
    ```

=== "macOS y Linux (bash/zsh)"

    ```bash
    export TIENDA_DB_CLAVE=cambia-esta-clave
    ./gradlew run -q --console=plain
    ```

La variable dura lo que dura la terminal. El botón **Run** de VS Code no la ve si la defines después de abrir VS Code; en ese caso, usa `db.clave` en tu `config.properties` local, que nunca se sube.

La clase `Configuracion` de la UD1 cambia para ofrecer los datos de conexión. Si no existe `config.properties`, la tienda usa una base de datos H2 embebida, así que funciona sin instalar nada:

**Listado 2.8.** `config/Configuracion.java`

```java
package es.dam.tienda.config;

import java.io.IOException;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

/**
 * Configuración de la aplicación, leída de un fichero .properties.
 * Ese fichero contiene credenciales: no se sube al repositorio.
 */
public class Configuracion {

    /** Base de datos que se usa si no hay configuración: H2 embebida en datos/tienda.mv.db */
    public static final String URL_POR_DEFECTO = "jdbc:h2:./datos/tienda;MODE=MariaDB;DATABASE_TO_LOWER=TRUE";

    private final Properties propiedades = new Properties();

    /**
     * Carga el fichero si existe; si no existe, se usan los valores por defecto.
     *
     * @throws UncheckedIOException si el fichero existe pero no se puede leer
     */
    public Configuracion(Path fichero) {
        if (Files.exists(fichero)) {
            try (Reader lector = Files.newBufferedReader(fichero)) {   // UTF-8
                propiedades.load(lector);
            } catch (IOException e) {
                throw new UncheckedIOException("No se pudo leer " + fichero, e);
            }
        }
    }

    /** @return URL JDBC de la base de datos */
    public String urlBaseDatos() {
        return propiedades.getProperty("db.url", URL_POR_DEFECTO);
    }

    /** @return usuario de la base de datos */
    public String usuarioBaseDatos() {
        return propiedades.getProperty("db.usuario", "sa");
    }

    /**
     * @return la clave de la variable de entorno TIENDA_DB_CLAVE si existe;
     *         si no, la del fichero; si tampoco, la cadena vacía
     */
    public String claveBaseDatos() {
        String deEntorno = System.getenv("TIENDA_DB_CLAVE");
        return deEntorno != null ? deEntorno : propiedades.getProperty("db.clave", "");
    }
}
```

### `DataSource` y el pool de conexiones

Abrir una conexión es caro: hay que establecer la comunicación con el servidor, identificarse y preparar la sesión. Una aplicación que abre una conexión para cada consulta pasa buena parte del tiempo haciendo eso. La solución es un **pool de conexiones**: un conjunto de conexiones que se abren una vez y se prestan a quien las pide.

![Sin pool, cada operación abre la conexión (comunicación e identificación), hace su consulta y la cierra. Con un pool como HikariCP, las conexiones están abiertas desde el arranque; los repositorios piden una con getConnection y, al hacer close, la devuelven al pool en lugar de cerrarla.](img/fig-2-4-pool.svg)

*Figura 2.4. Conexiones nuevas frente a un pool.*

JDBC representa cualquier fuente de conexiones con la interfaz `DataSource`, que tiene un método principal: `getConnection()`. Los repositorios reciben un `DataSource` y no saben si detrás hay un pool, una conexión simple o una base de datos en memoria para las pruebas. Es la misma inversión de dependencias que ya practicas con los repositorios.

**Listado 2.9.** `bd/BaseDatos.java`: el pool de la tienda

```java
package es.dam.tienda.bd;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import com.zaxxer.hikari.pool.HikariPool;
import es.dam.tienda.repositorio.AccesoDatosException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.SQLException;
import javax.sql.DataSource;

/**
 * Punto de acceso a la base de datos: mantiene un pool de conexiones (HikariCP)
 * y ejecuta scripts SQL. Sirve igual para MariaDB que para H2: lo decide la URL.
 */
public final class BaseDatos implements AutoCloseable {

    private final HikariDataSource pool;

    /**
     * Abre el pool y comprueba que la base de datos responde.
     *
     * @throws AccesoDatosException si no se puede conectar
     */
    public BaseDatos(String url, String usuario, String clave) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(url);
        config.setUsername(usuario);
        config.setPassword(clave);
        config.setPoolName("tienda");
        config.setMaximumPoolSize(4);           // a una aplicación de consola le sobran
        config.setConnectionTimeout(5_000);     // ms esperando una conexión libre
        try {
            pool = new HikariDataSource(config);
        } catch (HikariPool.PoolInitializationException e) {
            throw new AccesoDatosException("No se pudo conectar con " + url, e.getCause());
        }
    }

    /** @return la fuente de conexiones que reciben los repositorios */
    public DataSource dataSource() {
        return pool;
    }

    /**
     * Ejecuta un script SQL guardado en los recursos de la aplicación (src/main/resources).
     *
     * @param recurso ruta del script dentro de los recursos, por ejemplo "/sql/schema.sql"
     * @throws AccesoDatosException si el script no existe o falla alguna sentencia
     */
    public void ejecutarScript(String recurso) {
        try (InputStream entrada = BaseDatos.class.getResourceAsStream(recurso)) {
            if (entrada == null) {
                throw new AccesoDatosException("No existe el script " + recurso, null);
            }
            try (Connection conexion = pool.getConnection();
                 Reader lector = new InputStreamReader(entrada, StandardCharsets.UTF_8)) {
                EjecutorScripts.ejecutar(conexion, lector);
            }
        } catch (IOException | SQLException e) {
            throw new AccesoDatosException("Error al ejecutar " + recurso, e);
        }
    }

    /** Cierra todas las conexiones del pool. */
    @Override
    public void close() {
        pool.close();
    }
}
```

Usamos **HikariCP**, el pool más extendido en Java y el que usa Spring Boot por defecto (UD6). Sus opciones principales:

| Opción | Significado | Por defecto |
|---|---|---|
| `maximumPoolSize` | Número máximo de conexiones abiertas | 10 |
| `connectionTimeout` | Milisegundos que `getConnection()` espera una conexión libre antes de lanzar una excepción | 30 000 |
| `idleTimeout` y `maxLifetime` | Cuándo se retira y se renueva una conexión | 10 y 30 minutos |
| `poolName` | Nombre que aparece en los mensajes | `HikariPool-1` |

¿Cuánto se gana? El programa `TiempoConexion` hace 100 consultas sencillas abriendo una conexión cada vez y otras 100 pidiendo la conexión al pool:

**Listado 2.10.** `TiempoConexion.java`

```java
package es.dam.demos;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

/** Compara el tiempo de abrir 100 conexiones nuevas con el de pedirlas 100 veces a un pool. */
public class TiempoConexion {

    private static final int VECES = 100;

    public static void main(String[] args) throws SQLException {
        long inicio = System.nanoTime();
        for (int i = 0; i < VECES; i++) {
            try (Connection conexion = Conexion.abrir()) {          // conexión nueva cada vez
                consultar(conexion);
            }
        }
        System.out.printf("DriverManager: %6.2f ms por consulta%n", milisegundos(inicio) / VECES);

        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(Conexion.url());
        config.setUsername(Conexion.usuario());
        config.setPassword(Conexion.clave());
        try (HikariDataSource pool = new HikariDataSource(config)) {
            inicio = System.nanoTime();
            for (int i = 0; i < VECES; i++) {
                try (Connection conexion = pool.getConnection()) {  // la presta el pool
                    consultar(conexion);
                }                                                   // close() la devuelve al pool
            }
            System.out.printf("Pool HikariCP: %6.2f ms por consulta%n", milisegundos(inicio) / VECES);
        }
    }

    private static void consultar(Connection conexion) throws SQLException {
        try (Statement sentencia = conexion.createStatement()) {
            sentencia.executeQuery("SELECT 1").close();
        }
    }

    private static double milisegundos(long inicio) {
        return (System.nanoTime() - inicio) / 1_000_000.0;
    }
}
```

```text
DriverManager:   2.25 ms por consulta
Pool HikariCP:   0.34 ms por consulta
```

Con el servidor en la misma máquina, el pool es unas siete veces más rápido. Con el servidor en otra máquina, donde cada viaje por la red cuesta milisegundos, la diferencia es mucho mayor.

> **Desde C++.** El pool recuerda a reservar memoria una vez y reutilizarla en lugar de llamar a `new` y `delete` en cada operación: lo caro es crear y destruir, no usar.

### Para practicar

1. Ejecuta `ProbarConexion` contra tu MariaDB. Después, provoca tres errores (clave equivocada, base de datos inexistente y puerto 3307) y anota el `SQLState` de cada uno.
2. Cambia la URL a `jdbc:h2:./datos/prueba` y vuelve a ejecutarlo. ¿Qué fichero aparece en la carpeta `datos`?
3. Ejecuta `TiempoConexion` y compara tus resultados con los del listado. Si tienes acceso al servidor del aula, repítelo contra él.
4. (A) Lee en la documentación de HikariCP qué hace la opción `leakDetectionThreshold` y por qué es útil mientras desarrollas.

---

## 2.4 Del diagrama de clases al modelo relacional

### Tres vistas de los mismos datos

En la UD0 dibujaste el diagrama de clases de la tienda (Figura 0.12). En Bases de Datos de 1.º aprendiste a modelar los mismos datos con un **diagrama entidad-relación** (DER) y a transformarlo en un **modelo relacional**. Ahora necesitas las tres vistas a la vez: el diagrama de clases para el código, el modelo relacional para la base de datos y el DER como puente entre ambos.

![Diagrama entidad-relación: CLIENTE realiza PEDIDO (1:N, un cliente realiza de 0 a n pedidos y un pedido lo realiza un cliente); PEDIDO contiene PRODUCTO (N:M, con los atributos cantidad y precio_unitario); PRODUCTO pertenece a CATEGORÍA (N:1, un producto pertenece a 0 o 1 categorías). Cada entidad tiene sus atributos y su identificador marcado.](img/fig-2-5-der.svg)

*Figura 2.5. Diagrama entidad-relación de la tienda.*

![Modelo relacional con cinco tablas: cliente, pedido, linea_pedido, producto y categoria. pedido.cliente_id apunta a cliente.id; linea_pedido.pedido_numero apunta a pedido.numero y linea_pedido.producto_codigo a producto.codigo; producto.categoria_id apunta a categoria.id. linea_pedido tiene una clave primaria compuesta por sus dos claves ajenas.](img/fig-2-6-modelo-relacional.svg)

*Figura 2.6. Modelo relacional de la tienda.*

### Reglas de transformación

| En el diagrama de clases | En el modelo relacional | En la tienda |
|---|---|---|
| Clase | Tabla, con un nombre en minúscula y singular | `Producto` → `producto` |
| Atributo | Columna; los nombres compuestos, separados por guiones bajos | `fechaAlta` → `fecha_alta` |
| Atributo que identifica al objeto | Clave primaria natural | `codigo` |
| Objeto sin identificador propio | Clave primaria artificial, generada por el gestor (`AUTO_INCREMENT`) | `cliente.id`, `pedido.numero` |
| Asociación 1:N | Clave ajena en la tabla del lado N | `pedido.cliente_id` |
| Composición (las partes no existen sin el todo) | Clave ajena `NOT NULL` y `ON DELETE CASCADE` | `linea_pedido.pedido_numero` |
| Relación N:M | Tabla intermedia con dos claves ajenas que forman su clave primaria, más los atributos de la relación | `linea_pedido` |
| Asociación opcional (multiplicidad 0..1) | Clave ajena que admite `NULL` | `producto.categoria_id` |
| Enumerado | Columna de texto con su `name()` y una restricción `CHECK` con los valores posibles | `pedido.estado` |
| Herencia | Una tabla para toda la jerarquía, una por clase o una por clase concreta (lo resuelve la UD3) | — |
| Validaciones del constructor | `NOT NULL`, `UNIQUE` y `CHECK` | `precio >= 0`, `email` único |

| Tipo de Java | Tipo de SQL | Observaciones |
|---|---|---|
| `String` | `VARCHAR(n)` | Elige `n` según el dato real |
| `int`, `long` | `INT`, `BIGINT` | |
| `BigDecimal` | `DECIMAL(p, s)` | `p` dígitos en total, `s` decimales: `DECIMAL(10, 2)` llega a 99 999 999,99 |
| `double` | `DOUBLE` | Nunca para dinero |
| `boolean` | `BOOLEAN` | En MariaDB es un sinónimo de `TINYINT(1)` |
| `LocalDate` | `DATE` | |
| `LocalDateTime` | `DATETIME` o `TIMESTAMP` | |
| `enum` | `VARCHAR` + `CHECK` | Se guarda el nombre, nunca el ordinal (UD0) |

La relación entre clases y tablas no es exacta. En Java, un `Pedido` contiene una lista de objetos `LineaPedido`, y cada línea, una referencia a un `Producto`. En la base de datos no hay listas ni referencias: hay filas en tablas distintas unidas por el valor de sus claves. Convertir de una forma a la otra es trabajo de tu repositorio en esta unidad, y será trabajo de Hibernate en la UD3.

### Actividad cooperativa: el modelo relacional de tu dominio

Antes de escribir una sola línea de SQL, transforma el diagrama de clases de tu proyecto (el `docs/dominio.md` del Hito 0) en su modelo relacional. Se trabaja en grupos de cuatro, con este orden:

| Fase | Tiempo | Qué se hace |
|---|---|---|
| 1. Individual | 15 min | Cada uno dibuja el DER y el modelo relacional de su propio dominio, aplicando las tablas de reglas de este apartado |
| 2. Por parejas | 10 min | Intercambiáis los modelos. Cada uno revisa el del compañero con la tabla de reglas como lista de comprobación y anota los fallos al margen, sin corregirlos |
| 3. En grupo | 15 min | Cada miembro explica cómo ha resuelto su relación N:M y su composición. El grupo elige el caso más difícil y lo resuelve en la pizarra |
| 4. Puesta en común | 10 min | Un portavoz por grupo cuenta el error más habitual que han encontrado |

Roles del grupo, que rotan en cada actividad: **portavoz** (presenta en la fase 4), **secretario** (anota los errores encontrados), **guardián de las reglas** (comprueba que cada decisión se apoya en una regla de la tabla) y **controlador del tiempo**. El resultado de la actividad es el `docs/modelo.md` del Hito 2.

### El script de definición de datos (DDL)

La estructura de la base de datos se escribe en un **script SQL** que forma parte del proyecto, igual que el código: se sube al repositorio, se revisa y se puede ejecutar en cualquier máquina para crear la base de datos desde cero.

**Listado 2.11.** `src/main/resources/sql/schema.sql`

```sql
-- Estructura de la base de datos de la tienda.
-- Válida para MariaDB y para H2 en modo MariaDB. Se puede ejecutar varias veces.

CREATE TABLE IF NOT EXISTS categoria (
    id      INT          AUTO_INCREMENT PRIMARY KEY,
    nombre  VARCHAR(50)  NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS producto (
    codigo        VARCHAR(10)     PRIMARY KEY,
    nombre        VARCHAR(100)    NOT NULL,
    precio        DECIMAL(10, 2)  NOT NULL CHECK (precio >= 0),
    stock         INT             NOT NULL DEFAULT 0 CHECK (stock >= 0),
    categoria_id  INT             NULL,
    CONSTRAINT fk_producto_categoria FOREIGN KEY (categoria_id) REFERENCES categoria (id)
);

CREATE TABLE IF NOT EXISTS cliente (
    id          INT           AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100)  NOT NULL,
    email       VARCHAR(100)  NOT NULL UNIQUE,
    fecha_alta  DATE          NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido (
    numero      INT          AUTO_INCREMENT PRIMARY KEY,
    cliente_id  INT          NOT NULL,
    fecha       DATE         NOT NULL,
    estado      VARCHAR(10)  NOT NULL
        CHECK (estado IN ('PENDIENTE', 'PAGADO', 'ENVIADO', 'ENTREGADO', 'CANCELADO')),
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (cliente_id) REFERENCES cliente (id)
);

CREATE TABLE IF NOT EXISTS linea_pedido (
    pedido_numero    INT             NOT NULL,
    producto_codigo  VARCHAR(10)     NOT NULL,
    cantidad         INT             NOT NULL CHECK (cantidad > 0),
    precio_unitario  DECIMAL(10, 2)  NOT NULL CHECK (precio_unitario >= 0),
    PRIMARY KEY (pedido_numero, producto_codigo),
    CONSTRAINT fk_linea_pedido FOREIGN KEY (pedido_numero) REFERENCES pedido (numero) ON DELETE CASCADE,
    CONSTRAINT fk_linea_producto FOREIGN KEY (producto_codigo) REFERENCES producto (codigo)
);
```

Detalles que merecen atención:

- **`IF NOT EXISTS`** hace que el script se pueda ejecutar varias veces: la tienda lo ejecuta cada vez que arranca y solo crea las tablas que faltan. La contrapartida es que no modifica las tablas que ya existen; para cambiar una tabla con datos hace falta `ALTER TABLE`.
- **El orden importa.** Una tabla solo puede tener una clave ajena hacia otra que ya exista, así que se crean primero las tablas sin claves ajenas.
- **Las restricciones repiten las validaciones del modelo.** El constructor de `Producto` ya rechaza los precios negativos, pero la base de datos puede recibir datos de otros programas o de alguien que escribe SQL a mano. La base de datos es la última línea de defensa.
- **Es SQL portable** entre MariaDB y H2 en modo MariaDB. Por eso no aparecen opciones exclusivas de MariaDB como `ENGINE=InnoDB` (en MariaDB es el motor por defecto, el que admite transacciones y claves ajenas).

Con el script de estructura va otro con los datos iniciales:

**Listado 2.12.** `src/main/resources/sql/datos-ejemplo.sql`

```sql
-- Datos de ejemplo. La aplicación los carga si la tabla producto está vacía.

INSERT INTO categoria (nombre) VALUES ('Periféricos'), ('Monitores'), ('Cables');

INSERT INTO producto (codigo, nombre, precio, stock, categoria_id) VALUES
    ('TEC01', 'Teclado mecánico',    59.90, 12, 1),
    ('RAT01', 'Ratón inalámbrico',   24.50, 30, 1),
    ('MON01', 'Monitor 27 pulgadas', 219.00, 4, 2),
    ('CAB01', 'Cable USB-C 2 m',      8.95,  0, 3);

INSERT INTO cliente (nombre, email, fecha_alta) VALUES
    ('Ana Martín',   'ana@example.com',   '2026-09-01'),
    ('Luis Romero',  'luis@example.com',  '2026-09-15'),
    ('Carmen Ortiz', 'carmen@example.com', '2026-10-02');
```

### Ejecutar los scripts desde Java

Los scripts están en `src/main/resources`, así que Gradle los incluye en la aplicación y se leen con `getResourceAsStream`, que funciona igual desde VS Code, desde `./gradlew run` y desde el JAR. JDBC no tiene un método para ejecutar un script entero, de modo que hay que partirlo en sentencias:

**Listado 2.13.** `bd/EjecutorScripts.java`

```java
package es.dam.tienda.bd;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.Reader;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Ejecuta un script SQL sentencia a sentencia. Salta los comentarios de línea (--)
 * y entiende la orden DELIMITER del cliente de MariaDB, que permite crear
 * procedimientos almacenados cuyo cuerpo contiene ';'.
 */
public final class EjecutorScripts {

    private EjecutorScripts() {
    }

    /**
     * @return número de sentencias ejecutadas
     * @throws SQLException si falla una sentencia o el script termina a medias
     */
    public static int ejecutar(Connection conexion, Reader script) throws IOException, SQLException {
        BufferedReader lector = new BufferedReader(script);
        String delimitador = ";";
        StringBuilder sentencia = new StringBuilder();
        int ejecutadas = 0;
        try (Statement st = conexion.createStatement()) {
            String linea;
            while ((linea = lector.readLine()) != null) {
                String limpia = linea.strip();
                if (sentencia.isEmpty() && (limpia.isEmpty() || limpia.startsWith("--"))) {
                    continue;                                     // línea vacía o comentario
                }
                if (limpia.toUpperCase().startsWith("DELIMITER ")) {
                    delimitador = limpia.substring("DELIMITER ".length()).strip();
                    continue;                                     // orden para el lector, no para el servidor
                }
                sentencia.append(linea).append('\n');
                if (limpia.endsWith(delimitador)) {
                    String sql = sentencia.toString().strip();
                    st.execute(sql.substring(0, sql.length() - delimitador.length()));
                    ejecutadas++;
                    sentencia.setLength(0);
                }
            }
        }
        if (!sentencia.toString().isBlank()) {
            throw new SQLException("El script termina sin '" + delimitador + "'");
        }
        return ejecutadas;
    }
}
```

La orden `DELIMITER` no es SQL: la entiende el cliente `mariadb` y sirve para cambiar el carácter que marca el final de una sentencia. La necesitarás en el apartado 2.8, cuando el cuerpo de un procedimiento contenga varios `;`. Este ejecutor la entiende igual que el cliente, de modo que el mismo script sirve desde la consola y desde Java.

### El modelo Java, completo

Para trabajar con pedidos, el modelo de la tienda incorpora la clase `Pedido`, una excepción para la falta de stock y un *record* para el informe de ventas:

**Listado 2.14.** `modelo/Pedido.java`, `modelo/StockInsuficienteException.java` y `modelo/VentasCategoria.java`

```java
package es.dam.tienda.modelo;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/** Un pedido de un cliente, con sus líneas. */
public class Pedido {

    private Integer numero;                  // null hasta que la base de datos lo asigna
    private final int clienteId;
    private final LocalDate fecha;
    private EstadoPedido estado;
    private final List<LineaPedido> lineas = new ArrayList<>();

    /** Crea un pedido nuevo, pendiente y todavía sin número. */
    public Pedido(int clienteId, LocalDate fecha) {
        this(null, clienteId, fecha, EstadoPedido.PENDIENTE);
    }

    /** Reconstruye un pedido leído de la base de datos. */
    public Pedido(Integer numero, int clienteId, LocalDate fecha, EstadoPedido estado) {
        this.numero = numero;
        this.clienteId = clienteId;
        this.fecha = fecha;
        this.estado = estado;
    }

    /**
     * Añade unidades de un producto al precio actual. Si el producto ya estaba
     * en el pedido, suma las unidades a su línea.
     */
    public void agregar(Producto producto, int cantidad) {
        for (int i = 0; i < lineas.size(); i++) {
            LineaPedido linea = lineas.get(i);
            if (linea.producto().equals(producto)) {
                lineas.set(i, new LineaPedido(producto, linea.cantidad() + cantidad, linea.precioUnitario()));
                return;
            }
        }
        lineas.add(new LineaPedido(producto, cantidad, producto.getPrecio()));
    }

    /** Añade una línea tal como está guardada (con su precio de entonces). */
    public void agregarLinea(LineaPedido linea) {
        lineas.add(linea);
    }

    /** @return suma de los importes de las líneas */
    public BigDecimal total() {
        return lineas.stream().map(LineaPedido::importe).reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    public Integer getNumero() { return numero; }

    /** Lo usa el repositorio cuando la base de datos ha generado el número. */
    public void asignarNumero(int numero) { this.numero = numero; }

    public int getClienteId() { return clienteId; }

    public LocalDate getFecha() { return fecha; }

    public EstadoPedido getEstado() { return estado; }

    public List<LineaPedido> getLineas() { return List.copyOf(lineas); }
}
```

```java
package es.dam.tienda.modelo;

/** Se lanza cuando un pedido pide más unidades de las que hay en stock. */
public class StockInsuficienteException extends RuntimeException {

    public StockInsuficienteException(String codigo, int unidades) {
        super("No hay stock suficiente de " + codigo + " para servir " + unidades + " unidades");
    }
}
```

```java
package es.dam.tienda.modelo;

import java.math.BigDecimal;

/** Una fila del informe de ventas: lo vendido de una categoría. */
public record VentasCategoria(String categoria, int unidades, BigDecimal importe) {
}
```

Observa dos diferencias con el diagrama de la Figura 0.12. El `numero` es un `Integer` que vale `null` hasta que la base de datos lo genera. Y el pedido guarda el **identificador** del cliente, no un objeto `Cliente`: con JDBC, cargar el cliente entero cada vez que se lee un pedido sería trabajo extra que nadie ha pedido. En la UD3 verás cómo un ORM permite tener la referencia al objeto sin pagar ese precio.

### Para practicar

1. Escribe en el cliente `mariadb` las consultas que respondan a estas preguntas: ¿cuántos productos hay de cada categoría?, ¿qué clientes no han hecho ningún pedido?, ¿cuál es el importe de cada pedido?
2. Intenta insertar a mano un producto con precio negativo, un pedido de un cliente que no existe y una línea con cantidad 0. Anota qué restricción salta en cada caso.
3. Añade a `schema.sql` una tabla `valoracion` (un cliente valora un producto con una nota de 1 a 5 y un comentario; cada cliente solo puede valorar una vez cada producto). Decide la clave primaria y las restricciones.
4. (A) Dibuja el DER y el modelo relacional de tu dominio siguiendo las Figuras 2.5 y 2.6.

---

## 2.5 Consultas

### `Statement` y `PreparedStatement`

Con una conexión abierta se crean **sentencias**. Hay dos tipos para SQL normal:

| | `Statement` | `PreparedStatement` |
|---|---|---|
| Cómo se crea | `conexion.createStatement()` | `conexion.prepareStatement(sql)` |
| El SQL | Se pasa al ejecutar, completo | Se pasa al crearla, con un `?` en lugar de cada valor |
| Los valores | Escritos dentro del texto del SQL | Con `setString(1, …)`, `setInt(2, …)`… |
| Seguridad | Vulnerable a la inyección SQL si el texto incluye datos del usuario | Inmune: los valores nunca se interpretan como SQL |
| Cuándo usarla | Solo para SQL fijo sin datos variables (por ejemplo, un script) | Siempre que haya un valor variable |

Los parámetros se numeran **desde 1**, en el orden en que aparecen los `?`. Una sentencia se ejecuta con uno de estos métodos:

| Método | Para | Devuelve |
|---|---|---|
| `executeQuery()` | `SELECT` | Un `ResultSet` con las filas |
| `executeUpdate()` | `INSERT`, `UPDATE`, `DELETE` y DDL | El número de filas afectadas |
| `execute()` | Cualquier sentencia | `true` si el resultado es un `ResultSet` |
| `executeBatch()` | Un lote de sentencias (apartado 2.6) | Las filas afectadas por cada una |

### `ResultSet`: el resultado de una consulta

Un `ResultSet` no es una lista: es un **cursor** que apunta a una fila del resultado. Al principio está antes de la primera; cada llamada a `next()` lo avanza una fila y devuelve `false` cuando ya no quedan.

![Resultado de SELECT codigo, nombre, precio, stock FROM producto. El cursor empieza antes de la primera fila; tras el segundo next() apunta a la fila de MON01, la fila actual; después de la última, next() devuelve false. Al lado, el bucle while (filas.next()) con getString, getBigDecimal y getInt, que leen columnas de la fila actual por nombre o por posición.](img/fig-2-7-resultset.svg)

*Figura 2.7. Un `ResultSet` es un cursor.*

Los métodos `get` leen una columna de la fila actual, por su nombre o por su posición (desde 1):

| Tipo de SQL | Método | Si la columna vale `NULL` |
|---|---|---|
| `VARCHAR`, `CHAR` | `getString` | `null` |
| `INT` | `getInt` | `0` (compruébalo con `wasNull()` o usa `getObject(col, Integer.class)`) |
| `BIGINT` | `getLong` | `0` |
| `DECIMAL` | `getBigDecimal` | `null` |
| `DATE` | `getObject(col, LocalDate.class)` | `null` |
| `DATETIME`, `TIMESTAMP` | `getObject(col, LocalDateTime.class)` | `null` |
| `BOOLEAN` | `getBoolean` | `false` |

Las fechas se leen con `getObject` indicando la clase de `java.time`. En código antiguo verás `getDate`, que devuelve un `java.sql.Date`, una clase anterior a `java.time` que ya no conviene usar.

### Del `ResultSet` a los objetos

Un `ResultSet` depende de su conexión: cuando la conexión se cierra, el `ResultSet` deja de servir. Por eso un repositorio nunca devuelve un `ResultSet`. Copia cada fila en un objeto del modelo y devuelve esos objetos, que siguen existiendo cuando la conexión ya se ha cerrado. Esos objetos son, en palabras del criterio 2g, «los objetos destinados a almacenar el resultado de las consultas».

**Listado 2.15.** `repositorio/ProductoRepositoryJdbc.java`

```java
package es.dam.tienda.repositorio;

import es.dam.tienda.modelo.Producto;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.SQLIntegrityConstraintViolationException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import javax.sql.DataSource;

/**
 * Guarda los productos en una base de datos relacional mediante JDBC.
 * Sirve para cualquier gestor que tenga la tabla producto de schema.sql (MariaDB, H2…).
 */
public class ProductoRepositoryJdbc implements ProductoRepository {

    private static final String SELECT = "SELECT codigo, nombre, precio, stock FROM producto";

    private final DataSource dataSource;

    public ProductoRepositoryJdbc(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public void guardar(Producto producto) {
        String actualizar = "UPDATE producto SET nombre = ?, precio = ?, stock = ? WHERE codigo = ?";
        String insertar = "INSERT INTO producto (nombre, precio, stock, codigo) VALUES (?, ?, ?, ?)";
        try (Connection conexion = dataSource.getConnection()) {
            if (ejecutar(conexion, actualizar, producto) == 0) {     // no existía: se inserta
                ejecutar(conexion, insertar, producto);
            }
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo guardar el producto " + producto.getCodigo(), e);
        }
    }

    /** Ejecuta una sentencia cuyos cuatro parámetros son, en este orden, nombre, precio, stock y código. */
    private static int ejecutar(Connection conexion, String sql, Producto p) throws SQLException {
        try (PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            sentencia.setString(1, p.getNombre());
            sentencia.setBigDecimal(2, p.getPrecio());
            sentencia.setInt(3, p.getStock());
            sentencia.setString(4, p.getCodigo());
            return sentencia.executeUpdate();                       // filas afectadas
        }
    }

    @Override
    public Optional<Producto> buscarPorCodigo(String codigo) {
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement(SELECT + " WHERE codigo = ?")) {
            sentencia.setString(1, codigo);
            try (ResultSet fila = sentencia.executeQuery()) {
                return fila.next() ? Optional.of(aProducto(fila)) : Optional.empty();
            }
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo buscar el producto " + codigo, e);
        }
    }

    @Override
    public List<Producto> buscarTodos() {
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement(SELECT + " ORDER BY codigo");
             ResultSet filas = sentencia.executeQuery()) {
            List<Producto> productos = new ArrayList<>();
            while (filas.next()) {
                productos.add(aProducto(filas));
            }
            return List.copyOf(productos);
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo leer la lista de productos", e);
        }
    }

    @Override
    public boolean borrar(String codigo) {
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement("DELETE FROM producto WHERE codigo = ?")) {
            sentencia.setString(1, codigo);
            return sentencia.executeUpdate() == 1;
        } catch (SQLIntegrityConstraintViolationException e) {       // lo impide una clave ajena
            throw new IllegalStateException("El producto " + codigo + " aparece en algún pedido y no se puede borrar");
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo borrar el producto " + codigo, e);
        }
    }

    /** Convierte la fila actual en un Producto; su constructor valida los datos. */
    private static Producto aProducto(ResultSet fila) throws SQLException {
        return new Producto(fila.getString("codigo"), fila.getString("nombre"),
                fila.getBigDecimal("precio"), fila.getInt("stock"));
    }
}
```

En las consultas, fíjate en el patrón que se repite:

1. Se pide una conexión al `DataSource`, en un `try-with-resources`.
2. Se prepara la sentencia con sus `?` y se asignan los valores.
3. Se ejecuta y se recorre el `ResultSet`, también en un `try-with-resources`.
4. El método privado `aProducto` convierte la fila actual en un objeto. Al pasar por el constructor de `Producto`, los datos se validan también al leerlos.
5. Cualquier `SQLException` se envuelve en la `AccesoDatosException` de la UD1.

`buscarTodos` devuelve una lista ordenada por código: sin `ORDER BY`, el orden de las filas de un `SELECT` no está garantizado.

Las consultas con varias tablas siguen el mismo patrón. Estos dos métodos de `PedidoRepositoryJdbc` reconstruyen un pedido con sus líneas a partir de un `JOIN` y calculan un informe agrupado, que se guarda en objetos del *record* `VentasCategoria`:

**Listado 2.16.** Las consultas de `repositorio/PedidoRepositoryJdbc.java`

```java
    @Override
    public Optional<Pedido> buscarPorNumero(int numero) {
        String sql = """
                SELECT p.numero, p.cliente_id, p.fecha, p.estado,
                       l.cantidad, l.precio_unitario,
                       pr.codigo, pr.nombre, pr.precio, pr.stock
                  FROM pedido p
                  LEFT JOIN linea_pedido l ON l.pedido_numero = p.numero
                  LEFT JOIN producto pr ON pr.codigo = l.producto_codigo
                 WHERE p.numero = ?
                 ORDER BY pr.codigo
                """;
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            sentencia.setInt(1, numero);
            try (ResultSet filas = sentencia.executeQuery()) {
                Pedido pedido = null;
                while (filas.next()) {
                    if (pedido == null) {                          // la cabecera, de la primera fila
                        pedido = new Pedido(filas.getInt("numero"), filas.getInt("cliente_id"),
                                filas.getObject("fecha", LocalDate.class),
                                EstadoPedido.valueOf(filas.getString("estado")));
                    }
                    if (filas.getString("codigo") != null) {       // un pedido sin líneas trae NULL
                        Producto producto = new Producto(filas.getString("codigo"), filas.getString("nombre"),
                                filas.getBigDecimal("precio"), filas.getInt("stock"));
                        pedido.agregarLinea(new LineaPedido(producto, filas.getInt("cantidad"),
                                filas.getBigDecimal("precio_unitario")));
                    }
                }
                return Optional.ofNullable(pedido);
            }
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo leer el pedido " + numero, e);
        }
    }
```

```java
    @Override
    public List<VentasCategoria> ventasPorCategoria() {
        String sql = """
                SELECT COALESCE(c.nombre, 'Sin categoría') AS categoria,
                       SUM(l.cantidad) AS unidades,
                       SUM(l.cantidad * l.precio_unitario) AS importe
                  FROM linea_pedido l
                  JOIN producto p ON p.codigo = l.producto_codigo
                  LEFT JOIN categoria c ON c.id = p.categoria_id
                 GROUP BY COALESCE(c.nombre, 'Sin categoría')
                 ORDER BY importe DESC
                """;
        try (Connection conexion = dataSource.getConnection();
             PreparedStatement sentencia = conexion.prepareStatement(sql);
             ResultSet filas = sentencia.executeQuery()) {
            List<VentasCategoria> informe = new ArrayList<>();
            while (filas.next()) {
                informe.add(new VentasCategoria(filas.getString("categoria"),
                        filas.getInt("unidades"), filas.getBigDecimal("importe")));
            }
            return informe;
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo calcular el informe de ventas", e);
        }
    }
```

En `buscarPorNumero`, la consulta devuelve una fila por línea del pedido, con los datos de la cabecera repetidos en todas. El bucle crea el `Pedido` con la primera fila y le añade una línea por cada fila. El `LEFT JOIN` hace que un pedido sin líneas también se encuentre: sus columnas de línea llegan como `NULL`. En `ventasPorCategoria`, `COALESCE` sustituye el `NULL` de los productos sin categoría por un texto.

### Inyección SQL

Construir una consulta pegando trozos de texto con los datos del usuario es el error de seguridad más conocido de la programación web, y uno de los más graves. Este programa lo demuestra:

**Listado 2.17.** `InyeccionSql.java`

```java
package es.dam.demos;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/** Muestra cómo una consulta construida concatenando texto deja atacar la base de datos. */
public class InyeccionSql {

    public static void main(String[] args) throws SQLException {
        String ataque = "x' UNION SELECT email, nombre, 0, 0 FROM cliente -- ";
        try (Connection conexion = Conexion.abrir()) {
            System.out.println("Búsqueda insegura del código «TEC01»:");
            buscarInseguro(conexion, "TEC01");
            System.out.println("Búsqueda insegura del código «" + ataque + "»:");
            buscarInseguro(conexion, ataque);
            System.out.println("Búsqueda segura del mismo texto:");
            buscarSeguro(conexion, ataque);
        }
    }

    /** MAL: el texto del usuario pasa a formar parte de la sentencia SQL. */
    static void buscarInseguro(Connection conexion, String codigo) throws SQLException {
        String sql = "SELECT codigo, nombre, precio, stock FROM producto WHERE codigo = '" + codigo + "'";
        try (Statement sentencia = conexion.createStatement();
             ResultSet filas = sentencia.executeQuery(sql)) {
            mostrar(filas);
        }
    }

    /** BIEN: la sentencia es fija y el texto del usuario viaja como un valor. */
    static void buscarSeguro(Connection conexion, String codigo) throws SQLException {
        String sql = "SELECT codigo, nombre, precio, stock FROM producto WHERE codigo = ?";
        try (PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            sentencia.setString(1, codigo);
            try (ResultSet filas = sentencia.executeQuery()) {
                mostrar(filas);
            }
        }
    }

    private static void mostrar(ResultSet filas) throws SQLException {
        int n = 0;
        while (filas.next()) {
            System.out.printf("  %-20s %-20s%n", filas.getString(1), filas.getString(2));
            n++;
        }
        System.out.println("  (" + n + " filas)");
    }
}
```

```text
Búsqueda insegura del código «TEC01»:
  TEC01                Teclado mecánico
  (1 filas)
Búsqueda insegura del código «x' UNION SELECT email, nombre, 0, 0 FROM cliente -- »:
  ana@example.com      Ana Martín
  luis@example.com     Luis Romero
  carmen@example.com   Carmen Ortiz
  (3 filas)
Búsqueda segura del mismo texto:
  (0 filas)
```

Una búsqueda de productos ha devuelto los correos de todos los clientes. La Figura 2.8 explica por qué:

![Arriba, concatenando: el código une un texto fijo con lo que escribe el usuario; la comilla del usuario cierra el texto y UNION SELECT email, nombre, 0, 0 FROM cliente se convierte en parte de la consulta, con dos guiones que anulan la comilla sobrante. Abajo, con PreparedStatement: primero se envía la sentencia con un hueco y después el valor, que solo puede ocupar ese hueco como dato, así que se busca un código igual a todo ese texto y no hay ninguna fila.](img/fig-2-8-inyeccion.svg)

*Figura 2.8. Inyección SQL y cómo la evita `PreparedStatement`.*

Con otras entradas, el atacante podría saltarse una comprobación de contraseña (`' OR '1'='1`) o leer cualquier tabla a la que tenga acceso el usuario de la aplicación. La regla no tiene excepciones: **todo valor que no sea fijo en el código va en un parámetro `?`**. Los parámetros solo sirven para valores, no para nombres de tablas o columnas; si necesitas que el usuario elija una columna para ordenar, compárala con una lista de nombres permitidos.

Que el usuario de la aplicación tenga solo los permisos que necesita es una segunda capa de defensa: si la tienda solo tuviera permiso de lectura sobre `producto`, el ataque no habría podido leer `cliente`.

### Consultas cuyo resultado no se conoce de antemano

`ResultSetMetaData` describe las columnas de un resultado: cuántas hay, cómo se llaman y de qué tipo son. Con él se puede escribir un programa que muestre cualquier consulta, como hacen los clientes de bases de datos:

**Listado 2.18.** `ConsultaLibre.java`

```java
package es.dam.demos;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.Scanner;

/**
 * Ejecuta cualquier SELECT que escriba el usuario y muestra el resultado como una tabla.
 * No conoce las columnas de antemano: las descubre con ResultSetMetaData.
 */
public class ConsultaLibre {

    public static void main(String[] args) {
        Scanner teclado = new Scanner(System.in);
        try (Connection conexion = Conexion.abrir()) {
            while (true) {
                System.out.print("SQL (vacío para salir)> ");
                String sql = teclado.nextLine().strip();
                if (sql.isEmpty()) {
                    break;
                }
                if (!sql.toUpperCase().startsWith("SELECT")) {   // comprobación ingenua: ver el texto
                    System.out.println("Solo se admiten consultas SELECT.");
                    continue;
                }
                try (PreparedStatement sentencia = conexion.prepareStatement(sql);
                     ResultSet filas = sentencia.executeQuery()) {
                    imprimir(filas);
                } catch (SQLException e) {
                    System.out.println("Error " + e.getSQLState() + ": " + e.getMessage());
                }
            }
        } catch (SQLException e) {
            System.out.println("No se pudo conectar: " + e.getMessage());
        }
    }

    private static void imprimir(ResultSet filas) throws SQLException {
        ResultSetMetaData columnas = filas.getMetaData();
        int n = columnas.getColumnCount();
        for (int i = 1; i <= n; i++) {                   // las columnas se numeran desde 1
            System.out.printf("%-22s", columnas.getColumnLabel(i) + " (" + columnas.getColumnTypeName(i) + ")");
        }
        System.out.println();
        int contador = 0;
        while (filas.next()) {
            for (int i = 1; i <= n; i++) {
                System.out.printf("%-22s", filas.getObject(i));
            }
            System.out.println();
            contador++;
        }
        System.out.println("(" + contador + " filas)");
    }
}
```

```text
SQL (vacío para salir)> SELECT c.nombre AS categoria, COUNT(*) AS productos, SUM(p.stock) AS unidades FROM producto p JOIN categoria c ON c.id = p.categoria_id GROUP BY c.nombre
categoria (VARCHAR)   productos (BIGINT)    unidades (DECIMAL)
Cables                1                     0
Monitores             1                     4
Periféricos           2                     39
(3 filas)
SQL (vacío para salir)> delete from producto
Solo se admiten consultas SELECT.
```

Observa los tipos: `COUNT(*)` devuelve un `BIGINT` y `SUM` de un `INT`, un `DECIMAL` en MariaDB.

La comprobación de que la sentencia empieza por `SELECT` está ahí por una razón. Al probar una versión anterior de este programa, que no la hacía y llamaba a `conexion.setReadOnly(true)` confiando en que bastaría, un `DELETE FROM producto` tecleado en ella llegó a ejecutarse: `executeQuery` no impide que una sentencia modifique datos y, con el conector de MariaDB, `setReadOnly` es solo una indicación. Solo la clave ajena de `linea_pedido` evitó que se borrara la tabla. Aun así, la comprobación es ingenua y fácil de burlar: la protección de verdad es conectarse con un usuario que solo tenga permiso de lectura, como el `consulta` del apartado 2.2.

### Para practicar

1. Añade a `ProductoRepositoryJdbc` un método `List<Producto> buscarPorNombre(String texto)` que encuentre los productos cuyo nombre contenga el texto (`LIKE ?`, con el parámetro `"%" + texto + "%"`). ¿Por qué el `%` va en el valor y no en el SQL?
2. Prueba `InyeccionSql` con la entrada `x' OR '1'='1` y explica el resultado.
3. Ejecuta `ConsultaLibre` conectado con el usuario `consulta` e intenta modificar algo con una sentencia que empiece por `SELECT`, por ejemplo `SELECT 1; DELETE FROM producto`. ¿Qué lo impide?
4. (A) Escribe un método que devuelva los cinco clientes que más han gastado, con su nombre y el importe total, en un *record* `ClienteGasto`.

---

## 2.6 Modificaciones, claves generadas y lotes

### `executeUpdate` y las filas afectadas

`INSERT`, `UPDATE` y `DELETE` se ejecutan con `executeUpdate()`, que devuelve cuántas filas ha afectado. Ese número es información útil, no un detalle:

- En `guardar` (Listado 2.15), un `UPDATE` que afecta a 0 filas significa que el producto no existía, así que se inserta. Las dos sentencias reciben los mismos cuatro valores en el mismo orden, por eso las comparte el método `ejecutar`.
- En `borrar`, `executeUpdate() == 1` indica si el producto existía, que es justo lo que pide la interfaz.

MariaDB tiene una sentencia que hace las dos cosas a la vez (`INSERT … ON DUPLICATE KEY UPDATE`), y H2 otra distinta (`MERGE INTO`). La pareja `UPDATE` más `INSERT` es más larga, pero funciona en cualquier gestor.

### Claves generadas por el gestor

Cuando la clave primaria es `AUTO_INCREMENT`, el valor lo decide el gestor al insertar. Para conocerlo, se pide al preparar la sentencia y se lee después:

**Listado 2.19.** `insertarPedido`, en `PedidoRepositoryJdbc`

```java
    /** Inserta la cabecera del pedido y devuelve el número que genera la base de datos. */
    private static int insertarPedido(Connection conexion, Pedido pedido) throws SQLException {
        String sql = "INSERT INTO pedido (cliente_id, fecha, estado) VALUES (?, ?, ?)";
        try (PreparedStatement sentencia = conexion.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            sentencia.setInt(1, pedido.getClienteId());
            sentencia.setObject(2, pedido.getFecha());             // LocalDate → DATE
            sentencia.setString(3, pedido.getEstado().name());
            sentencia.executeUpdate();
            try (ResultSet claves = sentencia.getGeneratedKeys()) {
                claves.next();
                return claves.getInt(1);
            }
        }
    }
```

`getGeneratedKeys()` devuelve un `ResultSet` con una fila por cada fila insertada. Fíjate también en cómo se guardan la fecha y el estado: `setObject` con un `LocalDate` y el nombre del enumerado, que la restricción `CHECK` de la tabla comprueba.

### Lotes

Enviar muchas sentencias parecidas una a una obliga a ir y volver del servidor por cada una. Un **lote** (*batch*) las acumula con `addBatch()` y las envía juntas con `executeBatch()`:

**Listado 2.20.** `insertarLineas`, en `PedidoRepositoryJdbc`

```java
    /** Inserta todas las líneas en un único envío (lote). */
    private static void insertarLineas(Connection conexion, int numero, List<LineaPedido> lineas)
            throws SQLException {
        String sql = "INSERT INTO linea_pedido (pedido_numero, producto_codigo, cantidad, precio_unitario)"
                + " VALUES (?, ?, ?, ?)";
        try (PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            for (LineaPedido linea : lineas) {
                sentencia.setInt(1, numero);
                sentencia.setString(2, linea.producto().getCodigo());
                sentencia.setInt(3, linea.cantidad());
                sentencia.setBigDecimal(4, linea.precioUnitario());
                sentencia.addBatch();                              // se acumula en el lote
            }
            sentencia.executeBatch();                              // se envían todas juntas
        }
    }
```

En un pedido de tres líneas la diferencia es pequeña. En una carga de miles de filas, no. `CargaMasiva` inserta 5.000 filas de tres maneras:

**Listado 2.21.** `CargaMasiva.java`

```java
package es.dam.demos;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

/** Inserta 5.000 filas de tres formas distintas y compara el tiempo. */
public class CargaMasiva {

    private static final int FILAS = 5_000;
    private static final String INSERTAR = "INSERT INTO prueba_carga (id, texto) VALUES (?, ?)";

    public static void main(String[] args) throws SQLException {
        try (Connection conexion = Conexion.abrir();
             Statement sentencia = conexion.createStatement()) {
            sentencia.execute("CREATE TABLE prueba_carga (id INT PRIMARY KEY, texto VARCHAR(50))");
            try {
                medir("Una a una, con autocommit", () -> unaAUna(conexion));
                sentencia.execute("DELETE FROM prueba_carga");
                medir("Una a una, en una transacción", () -> enTransaccion(conexion, false));
                sentencia.execute("DELETE FROM prueba_carga");
                medir("En lote, en una transacción", () -> enTransaccion(conexion, true));
            } finally {
                sentencia.execute("DROP TABLE prueba_carga");
            }
        }
    }

    /** Cada executeUpdate es una transacción: el gestor confirma (y escribe en disco) 5.000 veces. */
    static void unaAUna(Connection conexion) throws SQLException {
        try (PreparedStatement insertar = conexion.prepareStatement(INSERTAR)) {
            for (int i = 1; i <= FILAS; i++) {
                insertar.setInt(1, i);
                insertar.setString(2, "fila " + i);
                insertar.executeUpdate();
            }
        }
    }

    /** Todas las inserciones en una sola transacción, enviadas una a una o en lotes de 500. */
    static void enTransaccion(Connection conexion, boolean enLote) throws SQLException {
        conexion.setAutoCommit(false);
        try (PreparedStatement insertar = conexion.prepareStatement(INSERTAR)) {
            for (int i = 1; i <= FILAS; i++) {
                insertar.setInt(1, i);
                insertar.setString(2, "fila " + i);
                if (enLote) {
                    insertar.addBatch();
                    if (i % 500 == 0) {
                        insertar.executeBatch();
                    }
                } else {
                    insertar.executeUpdate();
                }
            }
            conexion.commit();
        } catch (SQLException e) {
            conexion.rollback();
            throw e;
        } finally {
            conexion.setAutoCommit(true);
        }
    }

    interface Tarea {
        void ejecutar() throws SQLException;
    }

    static void medir(String nombre, Tarea tarea) throws SQLException {
        long inicio = System.nanoTime();
        tarea.ejecutar();
        System.out.printf("%-32s %7.0f ms%n", nombre, (System.nanoTime() - inicio) / 1_000_000.0);
    }
}
```

```text
Una a una, con autocommit            879 ms
Una a una, en una transacción        279 ms
En lote, en una transacción          221 ms
```

![Tres formas de insertar 5.000 filas. Una a una con autocommit: 5.000 envíos y 5.000 confirmaciones, 879 ms. Una a una en una transacción: 5.000 envíos y una confirmación, 279 ms. En lote en una transacción: 10 envíos de 500 sentencias y una confirmación, 221 ms.](img/fig-2-9-lotes.svg)

*Figura 2.9. Envíos y confirmaciones en una carga masiva.*

La mayor ganancia viene de la transacción: con *autocommit*, el gestor confirma cada fila por separado y en cada confirmación se asegura de que el dato queda escrito en el disco. El lote reduce además los viajes al servidor; con el servidor en la misma máquina se nota poco, pero con el servidor del aula, a varios milisegundos de distancia, 5.000 viajes son segundos de espera. Las transacciones son el tema del apartado siguiente.

### Para practicar

1. Añade a la tienda una opción que suba un porcentaje el precio de todos los productos de una categoría con un solo `UPDATE` y muestre cuántos productos han cambiado.
2. Modifica `CargaMasiva` para que use lotes de 50, 500 y 5.000 sentencias. ¿Cambia el tiempo?
3. Escribe un programa que importe a la base de datos un CSV de productos de la UD1 (usa `FormatoCsv`) en un lote y una transacción.
4. (A) Comprueba qué devuelve `executeBatch()` en tu programa del ejercicio 3 y qué significa cada valor del array.

---

## 2.7 Transacciones

### Todo o nada

Registrar un pedido son varias operaciones: insertar la cabecera, insertar las líneas y descontar el stock de cada producto. Si falla la tercera, las dos primeras no pueden quedarse hechas: habría un pedido con productos que no se han descontado del almacén. Una **transacción** es un grupo de operaciones que el gestor trata como una sola: o se confirman todas o no se aplica ninguna.

Las transacciones de un gestor relacional cumplen cuatro propiedades, conocidas por sus siglas:

| Propiedad | Significado |
|---|---|
| Atomicidad | Se hacen todas las operaciones o ninguna |
| Consistencia | La base de datos pasa de un estado válido a otro: se cumplen todas las restricciones |
| Aislamiento (*isolation*) | Las transacciones que se ejecutan a la vez no ven los cambios a medias de las otras |
| Durabilidad | Lo confirmado sobrevive a una caída del servidor |

### Transacciones en JDBC

Por defecto, una conexión JDBC está en modo ***autocommit***: cada sentencia es una transacción y se confirma al terminar. Para agrupar varias:

1. `conexion.setAutoCommit(false)` empieza la transacción.
2. Se ejecutan las sentencias con esa misma conexión.
3. `conexion.commit()` confirma todos los cambios, o `conexion.rollback()` los deshace.

**Listado 2.22.** `guardar` y `descontarStock`, en `PedidoRepositoryJdbc`

```java
    @Override
    public int guardar(Pedido pedido) {
        try (Connection conexion = dataSource.getConnection()) {
            conexion.setAutoCommit(false);                         // empieza la transacción
            try {
                int numero = insertarPedido(conexion, pedido);
                insertarLineas(conexion, numero, pedido.getLineas());
                descontarStock(conexion, pedido.getLineas());
                conexion.commit();                                 // todo ha ido bien: se confirma
                pedido.asignarNumero(numero);
                return numero;
            } catch (SQLException | RuntimeException e) {
                conexion.rollback();                               // algo ha fallado: se deshace todo
                throw e;
            } finally {
                conexion.setAutoCommit(true);
            }
        } catch (SQLIntegrityConstraintViolationException e) {
            throw new IllegalArgumentException("El cliente o algún producto del pedido no existe");
        } catch (SQLException e) {
            throw new AccesoDatosException("No se pudo guardar el pedido", e);
        }
    }
```

```java
    /** Resta las unidades de cada línea; falla si algún producto no tiene bastantes. */
    private static void descontarStock(Connection conexion, List<LineaPedido> lineas) throws SQLException {
        String sql = "UPDATE producto SET stock = stock - ? WHERE codigo = ? AND stock >= ?";
        try (PreparedStatement sentencia = conexion.prepareStatement(sql)) {
            for (LineaPedido linea : lineas) {
                sentencia.setInt(1, linea.cantidad());
                sentencia.setString(2, linea.producto().getCodigo());
                sentencia.setInt(3, linea.cantidad());
                if (sentencia.executeUpdate() == 0) {              // ninguna fila cumple la condición
                    throw new StockInsuficienteException(linea.producto().getCodigo(), linea.cantidad());
                }
            }
        }
    }
```

Lo esencial está en la estructura de `guardar`:

- **Todas las operaciones usan la misma conexión.** Una transacción pertenece a una conexión: si `insertarLineas` pidiera otra al `DataSource`, sus cambios irían en una transacción distinta.
- **El `catch` deshace y relanza.** Captura tanto `SQLException` como cualquier `RuntimeException`, como `StockInsuficienteException`: sea cual sea el fallo, primero `rollback()` y después la excepción sigue su camino hacia el servicio y la consola.
- **El `finally` restablece el *autocommit*.** La conexión vuelve al pool y la siguiente operación que la reciba espera encontrarla en su estado normal. Cuidado con el orden: según la especificación de JDBC, llamar a `setAutoCommit(true)` en mitad de una transacción la **confirma**. Si faltara el `rollback()` del `catch`, el `finally` guardaría la mitad del pedido (lo comprobarás en el ejercicio 2).
- **`descontarStock` usa el número de filas afectadas.** `UPDATE … WHERE codigo = ? AND stock >= ?` solo modifica la fila si hay unidades suficientes. Si devuelve 0, falta stock y la transacción entera se deshace. La restricción `CHECK (stock >= 0)` de la tabla lo habría impedido de todos modos, pero con un error menos claro.

La Figura 2.10 sigue la transacción de un pedido que pide más monitores de los que hay:

![Pasos de la transacción: setAutoCommit(false); INSERT del pedido, al que el gestor asigna el número 2; INSERT de las líneas en un lote; UPDATE de RAT01, que afecta a una fila y deja el stock en 28; UPDATE de MON01, que no afecta a ninguna porque no hay 5 monitores. Si todas hubieran afectado a una fila, commit; como no, rollback y StockInsuficienteException. Una tabla muestra el estado: el stock de RAT01 pasa de 29 a 28 dentro de la transacción y vuelve a 29; las filas de pedido pasan de 1 a 2 y vuelven a 1; el siguiente AUTO_INCREMENT pasa de 2 a 3 y se queda en 3.](img/fig-2-10-transaccion.svg)

*Figura 2.10. La transacción de un pedido que no puede servirse.*

Dos detalles de la tabla de estado. Mientras la transacción está abierta, los demás programas no ven el pedido nuevo ni el stock rebajado: eso es el aislamiento. Y el contador `AUTO_INCREMENT` no retrocede con el `rollback`: el siguiente pedido será el número 3 y el 2 no existirá nunca. Los huecos en la numeración son normales; si una aplicación necesita números consecutivos sin huecos, como las facturas, tiene que generarlos de otra forma.

Una prueba automática comprueba exactamente este comportamiento:

**Listado 2.23.** La prueba de la transacción, en `PedidoRepositoryJdbcTest`

```java
    @Test
    void siFaltaStockNoSeGuardaNada() throws SQLException {
        // RAT01 tiene stock de sobra, pero MON01 solo 4: el pedido entero debe deshacerse
        assertThrows(StockInsuficienteException.class, () -> pedidos.guardar(pedido("RAT01", "1", "MON01", "5")));

        assertEquals(30, stock("RAT01"));                    // el UPDATE de RAT01 se ha deshecho
        assertEquals(0, contarFilas("pedido"));
        assertEquals(0, contarFilas("linea_pedido"));
    }
```

### Niveles de aislamiento

El aislamiento completo tiene un coste: si cada transacción tuviera que esperar a que terminaran las demás, el gestor atendería a un usuario detrás de otro. Por eso SQL define **niveles de aislamiento** que permiten ciertas anomalías a cambio de más concurrencia:

| Nivel | ¿Puede leer cambios no confirmados? | ¿Puede leer dos veces lo mismo y obtener valores distintos? | Gestores que lo usan por defecto |
|---|---|---|---|
| `READ UNCOMMITTED` | Sí | Sí | — |
| `READ COMMITTED` | No | Sí | H2, PostgreSQL, Oracle |
| `REPEATABLE READ` | No | No | MariaDB, MySQL |
| `SERIALIZABLE` | No | No (y además evita las filas fantasma) | — |

Se cambia con `conexion.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE)`. Para este módulo basta con saber que existen y que el valor por defecto de cada gestor es razonable.

Dos cosas más que conviene saber:

- En MariaDB, las sentencias de definición (`CREATE`, `ALTER`, `DROP`) **confirman automáticamente** la transacción en curso. No mezcles DDL con modificaciones de datos en una transacción.
- Un `Savepoint` (`conexion.setSavepoint()` y `rollback(savepoint)`) permite deshacer solo una parte de la transacción.

### Para practicar

1. Registra en la tienda un pedido que pida más unidades de las que hay y comprueba en el cliente `mariadb` que no queda rastro de él. Mira el valor de `AUTO_INCREMENT` con `SHOW TABLE STATUS LIKE 'pedido'`.
2. Comenta la línea `conexion.rollback()` de `guardar` y pasa las pruebas. ¿Cuál falla, con qué mensaje y por qué? Pista: lee en la documentación de `Connection` qué hace `setAutoCommit`.
3. Abre dos clientes `mariadb`. En el primero, `START TRANSACTION;` y un `UPDATE` del stock de un producto, sin confirmar. En el segundo, consulta ese producto. Confirma en el primero con `COMMIT;` y vuelve a consultar.
4. (A) Añade a la tienda la operación «cancelar pedido»: cambia su estado a `CANCELADO` y devuelve al stock las unidades de sus líneas, todo en una transacción. Un pedido ya entregado no se puede cancelar.

---

## 2.8 Procedimientos almacenados

### Código que vive en la base de datos

Un **procedimiento almacenado** es un programa escrito en el lenguaje procedimental del gestor y guardado en la propia base de datos. Se invoca por su nombre, puede recibir y devolver parámetros y devolver filas, como una consulta.

| Ventajas | Inconvenientes |
|---|---|
| Se ejecuta junto a los datos: una operación compleja no necesita ir y volver por la red | Cada gestor tiene su propio lenguaje: el procedimiento no es portable |
| Varias aplicaciones comparten la misma lógica | La lógica queda repartida entre el código Java y la base de datos |
| Se puede dar permiso para ejecutar el procedimiento sin dárselo sobre las tablas | Es más difícil de probar, depurar y versionar que el código Java |

En la práctica se usan para operaciones muy ligadas a los datos o cuando la base de datos ya los tiene porque la comparten varias aplicaciones. En este módulo los usarás desde Java; escribirlos a fondo es materia de Bases de Datos.

**Listado 2.24.** `src/main/resources/sql/procedimientos.sql`

```sql
-- Procedimientos almacenados. Solo para MariaDB (H2 no admite CREATE PROCEDURE).
-- Se puede ejecutar desde el cliente de MariaDB o desde Java con EjecutorScripts:
-- DELIMITER cambia el final de sentencia para que los ';' de dentro no la corten.

DELIMITER //

-- Devuelve, como resultado de una consulta, los productos con menos unidades que el mínimo
CREATE OR REPLACE PROCEDURE productos_bajo_minimo(IN p_minimo INT)
BEGIN
    SELECT codigo, nombre, stock
      FROM producto
     WHERE stock < p_minimo
     ORDER BY stock, codigo;
END //

-- Calcula en un parámetro de salida el valor (precio × stock) de una categoría
CREATE OR REPLACE PROCEDURE valor_categoria(IN p_categoria INT, OUT p_valor DECIMAL(12, 2))
BEGIN
    SELECT COALESCE(SUM(precio * stock), 0)
      INTO p_valor
      FROM producto
     WHERE categoria_id = p_categoria;
END //

DELIMITER ;
```

`productos_bajo_minimo` devuelve filas, como una consulta. `valor_categoria` calcula un valor y lo deja en un parámetro de salida (`OUT`). H2 no admite `CREATE PROCEDURE`, así que este script solo sirve para MariaDB. Créalos con el cliente `mariadb`, desde la carpeta de la tienda (la orden es la misma en PowerShell, bash y zsh):

```bash
mariadb -u tienda -p tienda -e "source app/src/main/resources/sql/procedimientos.sql"
```

### `CallableStatement`

Un procedimiento se llama con un `CallableStatement`, que se crea con `prepareCall` y una sintaxis de escape propia de JDBC, `{call nombre(?, ?)}`, que cada conector traduce a la de su gestor:

**Listado 2.25.** `Procedimientos.java`

```java
package es.dam.demos;

import java.math.BigDecimal;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Types;

/** Llama a los dos procedimientos de procedimientos.sql. Necesita MariaDB. */
public class Procedimientos {

    public static void main(String[] args) throws SQLException {
        try (Connection conexion = Conexion.abrir()) {

            // 1. Procedimiento que devuelve filas, como una consulta
            try (CallableStatement llamada = conexion.prepareCall("{call productos_bajo_minimo(?)}")) {
                llamada.setInt(1, 10);
                try (ResultSet filas = llamada.executeQuery()) {
                    System.out.println("Productos con menos de 10 unidades:");
                    while (filas.next()) {
                        System.out.printf("  %-6s %-22s %3d%n",
                                filas.getString("codigo"), filas.getString("nombre"), filas.getInt("stock"));
                    }
                }
            }

            // 2. Procedimiento con un parámetro de entrada y otro de salida
            try (CallableStatement llamada = conexion.prepareCall("{call valor_categoria(?, ?)}")) {
                llamada.setInt(1, 1);                                  // IN: categoría 1
                llamada.registerOutParameter(2, Types.DECIMAL);        // OUT: hay que declarar su tipo
                llamada.execute();
                BigDecimal valor = llamada.getBigDecimal(2);           // se lee después de ejecutar
                System.out.println("Valor del stock de la categoría 1: " + valor + " €");
            }
        }
    }
}
```

```text
Productos con menos de 10 unidades:
  CAB01  Cable USB-C 2 m          0
  MON01  Monitor 27 pulgadas      4
Valor del stock de la categoría 1: 1309.50 €
```

| Tipo de parámetro | En Java |
|---|---|
| `IN` | Se asigna con `setInt`, `setString`… como en `PreparedStatement` |
| `OUT` | Se declara su tipo antes de ejecutar con `registerOutParameter(n, Types.DECIMAL)` y se lee después con `getBigDecimal(n)`… |
| `INOUT` | Las dos cosas |

Si el procedimiento devuelve filas, se ejecuta con `executeQuery()` y se recorre el `ResultSet` como siempre; si no, con `execute()`. Las funciones almacenadas, que devuelven un único valor, se llaman con `{? = call nombre(?)}`.

### Para practicar

1. Crea los procedimientos en tu MariaDB y ejecuta `Procedimientos`. Después llama a los dos desde el cliente `mariadb`: `CALL productos_bajo_minimo(10);` y `CALL valor_categoria(1, @v); SELECT @v;`.
2. Escribe un procedimiento `reponer(IN p_codigo VARCHAR(10), IN p_unidades INT, OUT p_stock INT)` que sume unidades al stock y devuelva el stock final, y llámalo desde Java.
3. (A) Escribe una función almacenada `importe_pedido(p_numero INT)` que devuelva el importe de un pedido y úsala en un `SELECT` desde Java.

---

## 2.9 Cierre de recursos y `SQLException`

### Qué hay que cerrar y en qué orden

`Connection`, `Statement`, `PreparedStatement`, `CallableStatement` y `ResultSet` ocupan recursos en tu programa y en el servidor: memoria, cursores abiertos, conexiones. Todos implementan `AutoCloseable` y se abren en un `try-with-resources`, que los cierra en orden inverso al de apertura aunque se produzca una excepción.

![A la izquierda, tres recursos anidados: la Connection se abre primero y se cierra la tercera; el PreparedStatement, segundo y segundo; el ResultSet, tercero y primero. Cerrar un objeto cierra los que contiene. A la derecha, un pool de tres conexiones que nunca se cierran: la cuarta petición espera y, pasados 2 segundos, falla con SQLTransientConnectionException.](img/fig-2-11-recursos.svg)

*Figura 2.11. El orden de cierre y lo que pasa si no se cierra.*

Cerrar una sentencia cierra su `ResultSet`, y cerrar una conexión cierra sus sentencias, pero no te apoyes en ello: con un pool, `close()` no cierra de verdad la conexión, la devuelve, y un `ResultSet` olvidado puede seguir ocupando recursos en el servidor. Cada objeto se cierra en cuanto termina su función, que es lo que pide el criterio 2h.

¿Y si no se cierra? Este programa pide conexiones a un pool de tres y no las devuelve nunca:

**Listado 2.26.** `AgotarPool.java`

```java
package es.dam.demos;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.sql.SQLException;

/** Qué pasa si se piden conexiones a un pool y no se cierran. */
public class AgotarPool {

    public static void main(String[] args) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(Conexion.url());
        config.setUsername(Conexion.usuario());
        config.setPassword(Conexion.clave());
        config.setMaximumPoolSize(3);
        config.setConnectionTimeout(2_000);                // esperar como mucho 2 s
        try (HikariDataSource pool = new HikariDataSource(config)) {
            for (int i = 1; i <= 4; i++) {
                Connection olvidada = pool.getConnection();    // MAL: nunca se cierra
                System.out.println("Conexión " + i + " obtenida");
            }
        } catch (SQLException e) {
            System.out.println(e.getClass().getSimpleName() + ": " + e.getMessage());
        }
    }
}
```

```text
Conexión 1 obtenida
Conexión 2 obtenida
Conexión 3 obtenida
SQLTransientConnectionException: HikariPool-1 - Connection is not available, request timed out after 2000ms.
```

En una aplicación real, el síntoma es que todo va bien durante un rato y de pronto cada operación tarda exactamente lo que vale `connectionTimeout` y luego falla. La opción `leakDetectionThreshold` de HikariCP avisa cuando una conexión lleva demasiado tiempo prestada.

### La información de una `SQLException`

Cualquier error de JDBC llega como una `SQLException` o una de sus subclases. Además del mensaje, trae dos códigos:

| Método | Qué devuelve | Ejemplo |
|---|---|---|
| `getMessage()` | Descripción del error, normalmente la del gestor | `Duplicate entry 'TEC01' for key 'PRIMARY'` |
| `getSQLState()` | Código de cinco caracteres del estándar SQL, igual en todos los gestores | `23000` |
| `getErrorCode()` | Código propio del gestor | `1062` en MariaDB |
| `getCause()` y `getNextException()` | Excepciones relacionadas | |

**Listado 2.27.** `ErroresSql.java`

```java
package es.dam.demos;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

/** Provoca varios errores típicos y muestra qué información trae cada SQLException. */
public class ErroresSql {

    public static void main(String[] args) throws SQLException {
        String[] sentencias = {
            "INSERT INTO producto (codigo, nombre, precio, stock) VALUES ('TEC01', 'Repetido', 1, 1)",
            "DELETE FROM categoria WHERE id = 1",
            "UPDATE producto SET precio = -5 WHERE codigo = 'RAT01'",
            "SELECT precio_venta FROM producto",
            "SELEC * FROM producto",
        };
        try (Connection conexion = Conexion.abrir();
             Statement sentencia = conexion.createStatement()) {
            for (String sql : sentencias) {
                try {
                    sentencia.execute(sql);
                } catch (SQLException e) {
                    System.out.println(sql);
                    System.out.println("  " + e.getClass().getSimpleName());
                    System.out.println("  SQLState " + e.getSQLState() + ", código " + e.getErrorCode());
                    System.out.println("  " + e.getMessage());
                }
            }
        }
    }
}
```

```text
INSERT INTO producto (codigo, nombre, precio, stock) VALUES ('TEC01', 'Repetido', 1, 1)
  SQLIntegrityConstraintViolationException
  SQLState 23000, código 1062
  (conn=19) Duplicate entry 'TEC01' for key 'PRIMARY'
DELETE FROM categoria WHERE id = 1
  SQLIntegrityConstraintViolationException
  SQLState 23000, código 1451
  (conn=19) Cannot delete or update a parent row: a foreign key constraint fails (`tienda`.`producto`, CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`))
UPDATE producto SET precio = -5 WHERE codigo = 'RAT01'
  SQLIntegrityConstraintViolationException
  SQLState 23000, código 4025
  (conn=19) CONSTRAINT `producto.precio` failed for `tienda`.`producto`
SELECT precio_venta FROM producto
  SQLSyntaxErrorException
  SQLState 42S22, código 1054
  (conn=19) Unknown column 'precio_venta' in 'SELECT'
SELEC * FROM producto
  SQLSyntaxErrorException
  SQLState 42000, código 1064
  (conn=19) You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near 'SELEC * FROM producto' at line 1
```

Los dos primeros caracteres del `SQLState` indican la clase de error, y JDBC elige la subclase de `SQLException` a partir de ellos:

| Clase de `SQLState` | Significado | Subclase de `SQLException` | ¿Qué hacer? |
|---|---|---|---|
| `08` | Conexión: el servidor no responde, se ha cortado | `SQLNonTransientConnectionException` | Avisar de que la base de datos no está disponible |
| `28` | Usuario o contraseña incorrectos | `SQLInvalidAuthorizationSpecException` | Revisar la configuración |
| `42` | Sintaxis, tabla o columna inexistente, falta de permisos | `SQLSyntaxErrorException` | Es un error de programación: corregir el SQL |
| `23` | Restricción de integridad: clave repetida, clave ajena, `CHECK` | `SQLIntegrityConstraintViolationException` | Traducirlo a un mensaje que el usuario entienda |
| `40` | La transacción se ha deshecho (por ejemplo, un interbloqueo) | `SQLTransactionRollbackException` | Reintentar la transacción |

Para decidir qué hacer con un error, usa la subclase o el `SQLState`, que son estándar, y no el texto del mensaje, que cambia con el gestor, su versión y su idioma.

### Cada capa trata sus errores

En la tienda, las excepciones siguen el mismo esquema que en la UD1, con un paso nuevo: algunos errores del gestor son en realidad errores del usuario y se traducen a una excepción que la consola sabe mostrar.

| Situación | Dónde se detecta | Qué ve el usuario |
|---|---|---|
| Borrar un producto que aparece en un pedido | `borrar` captura `SQLIntegrityConstraintViolationException` | `Error: El producto TEC01 aparece en algún pedido y no se puede borrar` |
| Pedido de un cliente que no existe | `guardar` captura la misma excepción tras el `rollback` | `Error: El cliente o algún producto del pedido no existe` |
| Falta de stock | `descontarStock` lanza `StockInsuficienteException` | `Error: No hay stock suficiente de MON01 para servir 5 unidades` |
| Cualquier otro fallo de SQL | Se envuelve en `AccesoDatosException` | `Error de acceso a datos: …` con la causa |
| No se puede conectar al arrancar | `BaseDatos` envuelve el error del pool | La aplicación termina con un mensaje |

**Listado 2.28.** Tres errores de conexión al arrancar la tienda

```text
No se puede arrancar: No se pudo conectar con jdbc:mariadb://localhost:3306/tienda
Causa: java.sql.SQLInvalidAuthorizationSpecException: Could not connect to address=(host=localhost)(port=3306)(type=master) : (conn=12) Access denied for user 'tienda'@'localhost' (using password: NO)

No se puede arrancar: No se pudo conectar con jdbc:mariadb://localhost:3306/tiendaa
Causa: java.sql.SQLSyntaxErrorException: Could not connect to address=(host=localhost)(port=3306)(type=master) : (conn=13) Access denied for user 'tienda'@'localhost' to database 'tiendaa'

No se puede arrancar: No se pudo conectar con jdbc:mariadb://localhost:3307/tienda
Causa: java.sql.SQLNonTransientConnectionException: Could not connect to address=(host=localhost)(port=3307)(type=master) : Socket fail to connect to host:localhost, port:3307. Connection refused (connect failed)
```

El primero se debe a que no se definió `TIENDA_DB_CLAVE` (`using password: NO`), el segundo a un nombre de base de datos mal escrito y el tercero a un puerto equivocado o a un servidor parado.

### Para practicar

1. Ejecuta `ErroresSql` y añade dos sentencias más: un `INSERT` en `linea_pedido` con un pedido que no existe y un `SELECT` sobre una tabla inexistente. Anota su `SQLState`.
2. Quita el `try-with-resources` de `buscarTodos` en `ProductoRepositoryJdbc` (abre la conexión con una variable normal y no la cierres), reduce el pool a 2 conexiones y lista los productos tres veces desde el menú. Describe lo que pasa.
3. Haz que la consola, ante una `AccesoDatosException` cuya causa sea de la clase `08`, muestre «La base de datos no está disponible; inténtalo más tarde» en lugar del mensaje técnico.
4. (A) Escribe una prueba que compruebe que `guardar` traduce un error de clave ajena en `IllegalArgumentException`.

---

## 2.10 El componente JDBC

### La pieza completa

Con todo lo anterior, el componente de acceso a datos de la tienda queda así:

![Diagrama de clases. ProductoService usa la interfaz ProductoRepository y PedidoService usa PedidoRepository y ProductoRepository. ProductoRepositoryJdbc y PedidoRepositoryJdbc implementan esas interfaces, usan la interfaz DataSource de javax.sql y lanzan AccesoDatosException. HikariDataSource implementa DataSource. BaseDatos tiene un HikariDataSource, usa EjecutorScripts y ejecuta los scripts schema.sql, datos-ejemplo.sql y procedimientos.sql.](img/fig-2-12-componente.svg)

*Figura 2.12. Diagrama de clases del componente JDBC.*

Comparado con el de la UD1 (Figura 1.10), el esquema es el mismo: una interfaz que no cambia y una implementación nueva. Los repositorios JDBC solo dependen de interfaces de Java (`DataSource`) y del modelo; `BaseDatos` es la única clase que conoce HikariCP, y `App`, la única que sabe qué implementaciones se usan.

### El servicio de pedidos

**Listado 2.29.** `servicio/PedidoService.java`

```java
package es.dam.tienda.servicio;

import es.dam.tienda.modelo.Pedido;
import es.dam.tienda.modelo.VentasCategoria;
import es.dam.tienda.repositorio.PedidoRepository;
import es.dam.tienda.repositorio.ProductoRepository;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/** Reglas de negocio sobre los pedidos. */
public class PedidoService {

    private final PedidoRepository pedidos;
    private final ProductoRepository productos;

    public PedidoService(PedidoRepository pedidos, ProductoRepository productos) {
        this.pedidos = pedidos;
        this.productos = productos;
    }

    /**
     * Registra un pedido con los precios actuales de los productos.
     *
     * @param lineas unidades pedidas de cada producto, por código
     * @return el número del pedido
     * @throws ProductoNoEncontradoException si algún código no existe
     * @throws es.dam.tienda.modelo.StockInsuficienteException si falta stock
     */
    public int registrar(int clienteId, Map<String, Integer> lineas) {
        if (lineas.isEmpty()) {
            throw new IllegalArgumentException("El pedido no tiene ninguna línea");
        }
        Pedido pedido = new Pedido(clienteId, LocalDate.now());
        lineas.forEach((codigo, cantidad) -> pedido.agregar(
                productos.buscarPorCodigo(codigo).orElseThrow(() -> new ProductoNoEncontradoException(codigo)),
                cantidad));
        return pedidos.guardar(pedido);
    }

    /** @throws IllegalArgumentException si no existe */
    public Pedido buscar(int numero) {
        return pedidos.buscarPorNumero(numero)
                .orElseThrow(() -> new IllegalArgumentException("No existe el pedido " + numero));
    }

    public List<VentasCategoria> ventasPorCategoria() {
        return pedidos.ventasPorCategoria();
    }
}
```

El servicio busca cada producto para tomar su precio actual y deja que el repositorio se encargue de la transacción. Si un código no existe, el error salta antes de abrir la transacción.

### Conectar las piezas

**Listado 2.30.** `App.java`

```java
package es.dam.tienda;

import es.dam.tienda.bd.BaseDatos;
import es.dam.tienda.config.Configuracion;
import es.dam.tienda.consola.Consola;
import es.dam.tienda.consola.MenuPedidos;
import es.dam.tienda.consola.MenuPrincipal;
import es.dam.tienda.consola.MenuProductos;
import es.dam.tienda.repositorio.AccesoDatosException;
import es.dam.tienda.repositorio.PedidoRepository;
import es.dam.tienda.repositorio.PedidoRepositoryJdbc;
import es.dam.tienda.repositorio.ProductoRepository;
import es.dam.tienda.repositorio.ProductoRepositoryJdbc;
import es.dam.tienda.servicio.PedidoService;
import es.dam.tienda.servicio.ProductoService;
import java.io.UncheckedIOException;
import java.nio.file.Path;

/** Punto de entrada: crea las piezas, las conecta y arranca el menú. */
public class App {

    public static void main(String[] args) {
        try {
            arrancar(new Configuracion(Path.of("config.properties")));
        } catch (AccesoDatosException | UncheckedIOException e) {
            System.err.println("No se puede arrancar: " + e.getMessage());
            System.err.println("Causa: " + e.getCause());
            System.exit(1);
        }
    }

    private static void arrancar(Configuracion configuracion) {
        try (BaseDatos baseDatos = new BaseDatos(configuracion.urlBaseDatos(),
                configuracion.usuarioBaseDatos(), configuracion.claveBaseDatos())) {
            baseDatos.ejecutarScript("/sql/schema.sql");          // crea las tablas que falten

            // El único sitio del programa que conoce las implementaciones concretas
            ProductoRepository productos = new ProductoRepositoryJdbc(baseDatos.dataSource());
            PedidoRepository pedidos = new PedidoRepositoryJdbc(baseDatos.dataSource());

            ProductoService productoService = new ProductoService(productos);
            if (productoService.listar().isEmpty()) {
                baseDatos.ejecutarScript("/sql/datos-ejemplo.sql");
            }
            System.out.println("Conectado a " + configuracion.urlBaseDatos());

            Consola consola = new Consola();
            new MenuPrincipal(
                    new MenuProductos(productoService, consola),
                    new MenuPedidos(new PedidoService(pedidos, productos), consola),
                    consola).mostrar();
        }
    }
}
```

`App` crea la base de datos con su pool, ejecuta el script de estructura y carga los datos de ejemplo si la tabla de productos está vacía. El `try-with-resources` cierra el pool al salir. Los menús de la consola cambian poco: un `MenuPrincipal` permite elegir entre productos y pedidos, `MenuProductos` cambia su opción «Salir» por «Volver» y el nuevo `MenuPedidos` registra pedidos, los muestra y presenta el informe de ventas. Están completos en la carpeta de ejemplos.

**Listado 2.31.** Una sesión con la tienda conectada a MariaDB (se han quitado las opciones de los menús que se repiten)

```text
Conectado a jdbc:mariadb://localhost:3306/tienda

=== Tienda ===
1. Productos
2. Pedidos
0. Salir
Opción: 1

=== Productos ===
1. Listar
2. Buscar por código
3. Alta
4. Cambiar precio
5. Baja
6. Exportar catálogo
0. Volver
Opción: 1
  CAB01  Cable USB-C 2 m             8,95 €    0 uds.
  MON01  Monitor 27 pulgadas       219,00 €    4 uds.
  RAT01  Ratón inalámbrico          24,50 €   30 uds.
  TEC01  Teclado mecánico           59,90 €   12 uds.
  Valor del inventario: 2.329,80 €

=== Productos ===
Opción: 0

=== Tienda ===
Opción: 2

=== Pedidos ===
1. Registrar pedido
2. Ver pedido
3. Ventas por categoría
0. Volver
Opción: 1
Cliente (id): 2
  Código del producto (FIN para terminar): TEC01
  Unidades: 2
  Código del producto (FIN para terminar): RAT01
  Unidades: 1
  Código del producto (FIN para terminar): FIN
  Pedido 1 registrado.

=== Pedidos ===
Opción: 2
Número de pedido: 1
  Pedido 1 · cliente 2 · 08/10/2026 · PENDIENTE
    RAT01  Ratón inalámbrico        1 ×   24,50 € =    24,50 €
    TEC01  Teclado mecánico         2 ×   59,90 € =   119,80 €
  Total: 144,30 €

=== Pedidos ===
Opción: 1
Cliente (id): 1
  Código del producto (FIN para terminar): RAT01
  Unidades: 1
  Código del producto (FIN para terminar): MON01
  Unidades: 5
  Código del producto (FIN para terminar): FIN
  Error: No hay stock suficiente de MON01 para servir 5 unidades

=== Pedidos ===
Opción: 3
  Periféricos        3 uds.     144,30 €

=== Pedidos ===
Opción: 0

=== Tienda ===
Opción: 1

=== Productos ===
Opción: 5
Código: TEC01
  Error: El producto TEC01 aparece en algún pedido y no se puede borrar

=== Productos ===
Opción: 0

=== Tienda ===
Opción: 0
Hasta luego.
```

### Las pruebas: el mismo contrato, otra implementación

Las pruebas usan H2 en memoria: cada una crea una base de datos nueva y vacía, con una URL distinta, y la destruye al terminar. No necesitan ningún servidor, así que funcionan en cualquier equipo y en servicios de integración continua como GitHub Actions. El contrato de la UD1 se reutiliza sin cambios:

**Listado 2.32.** `src/test/java/es/dam/tienda/repositorio/ProductoRepositoryJdbcTest.java`

```java
package es.dam.tienda.repositorio;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import es.dam.tienda.bd.BaseDatos;
import es.dam.tienda.modelo.Pedido;
import es.dam.tienda.modelo.Producto;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDate;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

class ProductoRepositoryJdbcTest extends ProductoRepositoryContrato {

    private BaseDatos baseDatos;

    @Override
    protected ProductoRepository crearRepositorio() {
        // Una base de datos H2 en memoria, nueva y vacía para cada prueba
        String url = "jdbc:h2:mem:" + UUID.randomUUID() + ";MODE=MariaDB;DATABASE_TO_LOWER=TRUE";
        baseDatos = new BaseDatos(url, "sa", "");
        baseDatos.ejecutarScript("/sql/schema.sql");
        return new ProductoRepositoryJdbc(baseDatos.dataSource());
    }

    @AfterEach
    void cerrarBaseDatos() {
        baseDatos.close();                     // al cerrar la última conexión, H2 borra la base de datos
    }

    @Test
    void otroRepositorioVeLosMismosDatos() {
        repositorio.guardar(new Producto("RAT01", "Ratón", new BigDecimal("24.50"), 30));

        ProductoRepository otro = new ProductoRepositoryJdbc(baseDatos.dataSource());

        assertEquals(2, otro.buscarTodos().size());
        assertEquals(new BigDecimal("24.50"), otro.buscarPorCodigo("RAT01").orElseThrow().getPrecio());
    }

    @Test
    void unCambioSinGuardarNoLlegaALaBaseDeDatos() {
        Producto teclado = repositorio.buscarPorCodigo("TEC01").orElseThrow();
        teclado.reponer(100);

        assertEquals(3, repositorio.buscarPorCodigo("TEC01").orElseThrow().getStock());
    }

    @Test
    void noSePuedeBorrarUnProductoQueApareceEnUnPedido() throws SQLException {
        try (Connection conexion = baseDatos.dataSource().getConnection();
             Statement sentencia = conexion.createStatement()) {
            sentencia.executeUpdate("INSERT INTO cliente (nombre, email, fecha_alta)"
                    + " VALUES ('Ana Martín', 'ana@example.com', '2026-09-01')");
        }
        Pedido pedido = new Pedido(1, LocalDate.of(2026, 10, 8));
        pedido.agregar(repositorio.buscarPorCodigo("TEC01").orElseThrow(), 1);
        new PedidoRepositoryJdbc(baseDatos.dataSource()).guardar(pedido);

        assertThrows(IllegalStateException.class, () -> repositorio.borrar("TEC01"));
    }
}
```

Las cinco pruebas del contrato se ejecutan ahora contra tres implementaciones: memoria, fichero y JDBC. La clase de pruebas de los pedidos (en los ejemplos) añade cuatro más: un pedido correcto, el `rollback` del Listado 2.23, un cliente inexistente y el informe de ventas.

¿Basta con probar con H2 si la aplicación usa MariaDB? Casi siempre, porque el SQL es el mismo y H2 lo ejecuta en modo MariaDB, pero no siempre: los procedimientos almacenados no se pueden probar así, y algún detalle de comportamiento puede diferir. Los proyectos profesionales añaden pruebas de integración contra el gestor real, a menudo arrancándolo en un contenedor de Docker durante las pruebas.

### Para practicar

1. Cambia `config.properties` entre MariaDB y H2 y comprueba que la tienda funciona igual con los dos. ¿Dónde están los datos en cada caso?
2. Crea un `ClienteRepository` con su implementación JDBC y haz que `MenuPedidos` muestre la lista de clientes antes de pedir el identificador.
3. Añade a `PedidoRepositoryJdbcTest` una prueba que guarde dos pedidos del mismo producto y compruebe que el stock se descuenta dos veces.
4. (A) Dibuja el diagrama de secuencia de «registrar pedido»: desde `MenuPedidos` hasta las tres sentencias SQL y el `commit`.

---

## Práctica de la unidad · Hito 2 del proyecto integrador

Tu proyecto pasa de los ficheros a una base de datos relacional: diseñarás la base de datos de tu dominio y escribirás el componente JDBC que la usa, con las mismas interfaces de repositorio de los hitos anteriores.

### Lo que tienes que hacer

**1. Modelo de datos.** En `docs/modelo.md`, el DER y el modelo relacional de tu dominio, resultado de la actividad cooperativa, con al menos cuatro tablas, una relación 1:N y una N:M resuelta con una tabla intermedia.

**2. Scripts SQL** en `src/main/resources/sql`:

- `schema.sql`, ejecutable varias veces y válido para MariaDB y para H2 en modo MariaDB, con claves primarias y ajenas y las restricciones `NOT NULL`, `UNIQUE` y `CHECK` que correspondan a las validaciones de tu modelo.
- `datos-ejemplo.sql` con datos para probar la aplicación.
- `procedimientos.sql` con al menos un procedimiento almacenado útil para tu dominio.

**3. Conexión.** Una clase como `BaseDatos`, con un pool de HikariCP. La URL, el usuario y la clave se leen de `config.properties` (que no se sube al repositorio) o de variables de entorno. Sube una plantilla `config.ejemplo.properties`. Sin configuración, la aplicación funciona con H2 embebida.

**4. Repositorios JDBC.**

- `XxxRepositoryJdbc` para tu entidad principal, que implementa la interfaz del Hito 0 y supera las pruebas de contrato.
- Un segundo repositorio con al menos una **operación que modifique varias tablas en una transacción**, con `commit`, `rollback` y una regla de negocio que pueda hacerla fallar.
- Al menos una consulta con `JOIN` y `GROUP BY` cuyo resultado se guarde en un *record*.
- Al menos una llamada a un procedimiento almacenado con `CallableStatement`, que funcione con MariaDB e informe con un mensaje claro si se usa H2.
- Todas las sentencias con valores variables, con `PreparedStatement`.

**5. Errores.** Ninguna traza para el usuario. Los errores de integridad (clave repetida, clave ajena) se traducen a mensajes comprensibles.

**6. Pruebas y documentación.**

- Las pruebas de contrato ejecutadas también contra la implementación JDBC, con H2 en memoria.
- Una prueba que demuestre el `rollback` de tu operación transaccional.
- Al menos **seis pruebas nuevas**, todas en verde con `./gradlew build`.
- Javadoc en las interfaces nuevas y en los repositorios, y un README que explique cómo crear la base de datos y el usuario en MariaDB y cómo configurar la conexión en Windows y en macOS o Linux.

### Entregables

- El enlace al repositorio de GitHub con la etiqueta `hito-2` en el *commit* que se entrega.
- Una defensa oral breve (5 minutos): ejecutarás la aplicación contra MariaDB, provocarás un fallo en tu operación transaccional y mostrarás en el cliente `mariadb` que no ha quedado rastro, y explicarás por qué tu código es inmune a la inyección SQL.

Se propone entregarlo el **jueves 19/11/2026**.

### Qué se evalúa

| Criterio | Evidencia en el Hito 2 |
|---|---|
| 2a | Justificación en el README de por qué se usa JDBC y qué limitaciones tiene frente a un ORM |
| 2b | La aplicación funciona con H2 embebida y con MariaDB; las pruebas usan H2 en memoria |
| 2c | Conectores como dependencias `runtimeOnly` adecuadas a cada gestor |
| 2d | Conexión con pool y credenciales fuera del código |
| 2e | `schema.sql` con claves, restricciones y una N:M bien resuelta, coherente con `docs/modelo.md` |
| 2f | Altas, modificaciones y bajas con `executeUpdate`, claves generadas y al menos un lote |
| 2g | Las filas se convierten en objetos del modelo o en *records*; ningún `ResultSet` sale del repositorio |
| 2h | Todos los recursos en `try-with-resources`; el pool se cierra al terminar |
| 2i | Operación transaccional con `commit` y `rollback`, demostrada con una prueba |
| 2j | Llamada a un procedimiento con `CallableStatement` |
| 2k | Consultas con `JOIN` y `GROUP BY` y modificaciones desde el menú |
| 6d | El repositorio JDBC sustituye al de fichero cambiando solo `App` y la configuración, y supera el mismo contrato |

---

## Resumen de la unidad

| Apartado | Lo esencial |
|---|---|
| 2.1 Conectores y JDBC | JDBC es una interfaz estándar; cada gestor aporta su conector, que se añade como dependencia `runtimeOnly` |
| 2.2 Embebidos e independientes | H2 se ejecuta dentro del programa; MariaDB es un servidor. H2 en modo MariaDB permite usar el mismo SQL en los dos |
| 2.3 La conexión | La URL elige el conector y la base de datos. Credenciales fuera del código. Los repositorios reciben un `DataSource`; HikariCP reutiliza las conexiones |
| 2.4 Modelo relacional | Del diagrama de clases al DER y a las tablas: claves ajenas para las asociaciones, tabla intermedia para las N:M, restricciones para las validaciones. Un `schema.sql` versionado |
| 2.5 Consultas | Siempre `PreparedStatement`. El `ResultSet` es un cursor; las filas se copian en objetos antes de cerrar la conexión |
| 2.6 Modificaciones | `executeUpdate` devuelve las filas afectadas; `getGeneratedKeys` para las claves `AUTO_INCREMENT`; lotes para muchas sentencias parecidas |
| 2.7 Transacciones | `setAutoCommit(false)`, una sola conexión, `commit` o `rollback` en el `catch`; propiedades ACID y niveles de aislamiento |
| 2.8 Procedimientos | Código en la base de datos, poco portable. `CallableStatement` con parámetros `IN` y `OUT` |
| 2.9 Recursos y errores | `try-with-resources` para todo; una conexión no devuelta agota el pool. El `SQLState` clasifica los errores |
| 2.10 Componente | `ProductoRepositoryJdbc` y `PedidoRepositoryJdbc` cumplen las mismas interfaces; pruebas con H2 en memoria |

---

## Bibliografía de la UD2

Todas las fuentes web se consultaron el 8 de octubre de 2026.

### JDBC

- Oracle. *Java SE 25 API*: paquetes `java.sql` y `javax.sql`. <https://docs.oracle.com/en/java/javase/25/docs/api/java.sql/module-summary.html>
- Oracle. *The Java Tutorials: JDBC Database Access* (escrito para versiones antiguas de Java, pero vigente en los conceptos). <https://docs.oracle.com/javase/tutorial/jdbc/>

### Gestores y conectores

- MariaDB Foundation. *MariaDB Server Documentation*: `CREATE TABLE`, procedimientos almacenados, transacciones y `DELIMITER`. <https://mariadb.com/docs/server/>
- MariaDB plc. *MariaDB Connector/J*, notas de versión (3.5.10, julio de 2026). <https://mariadb.com/docs/release-notes/connectors/java/all-releases>
- MariaDB Foundation (2026). *MariaDB Server 12.3, 11.8, 11.4 and 10.11 – Q3 2026 Maintenance Releases* (series con soporte largo). <https://mariadb.org/?p=41784>
- MariaDB plc. *Installing MariaDB Server Guide*. <https://mariadb.com/docs/server/mariadb-quickstart-guides/installing-mariadb-server-guide>
- H2 Database Engine. *Features* (modos de compatibilidad, URL de conexión, bases de datos en memoria). <https://h2database.com/html/features.html>
- Maven Central. `com.h2database:h2` (versión 2.5.252). <https://central.sonatype.com/artifact/com.h2database/h2>

### Pool de conexiones

- Wooldridge, B. *HikariCP* (documentación y opciones de configuración). <https://github.com/brettwooldridge/HikariCP>
- Maven Central. `com.zaxxer:HikariCP` (versión 7.1.0). <https://central.sonatype.com/artifact/com.zaxxer/HikariCP>

### Seguridad

- OWASP. *SQL Injection Prevention Cheat Sheet*. <https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html>

### Material de referencia del módulo

- Faci, S. *Acceso a Datos: Acceso a bases de datos relacionales* (CC BY-NC-SA 4.0). <https://datos.codeandcoke.com/apuntes:jdbc>

### Nota de actualización

Respecto a los apuntes de referencia del módulo, esta unidad:

- Usa **MariaDB** con su propio conector y **H2** como gestor embebido y para las pruebas, con el mismo SQL en los dos.
- Añade los conectores como dependencias **`runtimeOnly` de Gradle** y prescinde de `Class.forName`, innecesario desde JDBC 4.0.
- Introduce **`DataSource`** y un **pool de conexiones** (HikariCP, el mismo que usa Spring Boot) en lugar de abrir una conexión con `DriverManager` en cada operación.
- Saca las **credenciales del código** a un fichero de configuración que no se sube y a variables de entorno.
- Usa **`PreparedStatement` en todas las sentencias** con valores variables, demuestra la inyección SQL y cierra todos los recursos con **`try-with-resources`** en lugar de `finally`.
- Lee y escribe fechas con **`java.time`** (`getObject(col, LocalDate.class)`) y dinero con **`BigDecimal`**.
- Organiza el código en **repositorios** que implementan las interfaces de las unidades anteriores, con **pruebas de contrato** sobre H2 en memoria, y usa la consola en lugar de Swing.
- Añade el **diseño del modelo relacional** a partir del diagrama de clases, los **lotes**, las **claves generadas**, los niveles de aislamiento y la clasificación de errores por **`SQLState`**.

plugins {
    // Permite a Gradle descargar el JDK que pida el toolchain si no está instalado
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

rootProject.name = "demos-ud2"
include("app")

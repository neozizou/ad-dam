plugins {
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(libs.hikaricp)
    runtimeOnly(libs.mariadb.java.client)
    runtimeOnly(libs.h2)
    runtimeOnly(libs.slf4j.simple)
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
}

application {
    // Programa que se ejecuta: ./gradlew run -Pdemo=InyeccionSql (por defecto, ProbarConexion)
    mainClass = "es.dam.demos." + (findProperty("demo") ?: "ProbarConexion")
}

tasks.named<JavaExec>("run") {
    standardInput = System.`in`
    workingDir = rootProject.projectDir
}

plugins {
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation(libs.jackson.databind)                           // JSON (UD1)
    testImplementation(libs.junit.jupiter)
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(25)
    }
}

application {
    mainClass = "es.dam.tienda.App"
}

tasks.named<Test>("test") {
    useJUnitPlatform()
}

tasks.named<JavaExec>("run") {
    standardInput = System.`in`           // conecta el teclado
    workingDir = rootProject.projectDir   // las rutas relativas parten de la raíz del proyecto
}

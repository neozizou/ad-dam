plugins {
    application
}

repositories {
    mavenCentral()
}

dependencies {
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

// Conecta el teclado al programa cuando se lanza con ./gradlew run
tasks.named<JavaExec>("run") {
    standardInput = System.`in`
}

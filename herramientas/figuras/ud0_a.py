"""Figuras 0.1 (compilación), 0.2 (JDK), 0.4 (tareas de Gradle) y 0.5 (wrapper).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud0_a.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud0" / "img") + "/"

# ---------- Figura 0.1: compilación C++ frente a Java ----------
b = []
# carriles
b.append(rect(15, 15, 930, 190, AMBER_T, AMBER, rx=12, sw=1.2, opacity=0.55))
b.append(rect(15, 225, 930, 200, TEAL_T, TEAL, rx=12, sw=1.2, opacity=0.55))
b.append(text(32, 42, "C++", 16, AMBER, "start", 700))
b.append(text(32, 252, "Java", 16, TEAL, "start", 700))
# C++
b.append(file_icon(60, 85, 120, 56, "main.cpp", "código fuente"))
b.append(box(240, 88, 170, 50, "compilador", "g++, clang, MSVC", stroke=AMBER))
b.append(path([(180, 113), (236, 113)], "amber"))
ys = [50, 96, 142]
names = [("app.exe", "Windows"), ("app", "macOS"), ("app", "Linux")]
for yy, (n, so) in zip(ys, names):
    b.append(box(480, yy, 200, 38, None, None, stroke=AMBER))
    b.append(text(496, yy + 24, n, 13, INK, "start", 600, mono=True))
    b.append(text(664, yy + 24, "binario nativo", 11.5, MUTED, "end"))
    b.append(path([(410, 113), (445, 113), (445, yy + 19), (476, yy + 19)], "amber"))
    b.append(box(745, yy, 160, 38, so, None, fill=WHITE, stroke=LINE, tsize=13))
    b.append(path([(680, yy + 19), (741, yy + 19)], "amber"))
b.append(text(480, 198, "Un ejecutable por sistema: hay que compilar para cada uno.", 12.5, AMBER, "start", italic=True))
# Java
b.append(file_icon(60, 300, 120, 56, "Hola.java", "código fuente"))
b.append(box(240, 303, 170, 50, "javac", "compilador de Java", stroke=TEAL, tmono=True))
b.append(path([(180, 328), (236, 328)], "teal"))
b.append(file_icon(470, 300, 130, 56, "Hola.class", "bytecode", fill=WHITE, stroke=TEAL))
b.append(path([(410, 328), (466, 328)], "teal"))
ys2 = [262, 308, 354]
for yy, so in zip(ys2, ["Windows", "macOS", "Linux"]):
    b.append(box(745, yy, 160, 38, "JVM · " + so, None, fill=WHITE, stroke=TEAL, tsize=13))
    b.append(path([(600, 328), (680, 328), (680, yy + 19), (741, yy + 19)], "teal"))
b.append(text(470, 412, "El mismo .class se ejecuta en cualquier sistema con JVM.", 12.5, TEAL, "start", italic=True))
open(OUT + "fig-0-1-compilacion.svg", "w").write(svg(960, 440, "".join(b), "Modelo de compilación y ejecución de C++ frente a Java"))

# ---------- Figura 0.2: qué contiene el JDK ----------
b = []
b.append(rect(15, 15, 790, 345, WHITE, TEAL, rx=14, sw=2))
b.append(text(35, 45, "JDK (Java Development Kit)", 17, TEAL, "start", 700))
b.append(text(785, 45, "lo que instalas para programar", 12.5, MUTED, "end", italic=True))
# herramientas
b.append(rect(35, 65, 268, 275, TEAL_T, TEAL, rx=10, sw=1.2))
b.append(text(169, 92, "Herramientas de desarrollo", 14, INK, "middle", 600))
tools = [("javac", "compila .java → .class"), ("java", "lanza la JVM"), ("jshell", "intérprete interactivo"),
         ("javadoc", "genera documentación"), ("jar", "empaqueta en .jar"), ("javap", "muestra el bytecode")]
for i, (t, d) in enumerate(tools):
    yy = 108 + i * 37
    b.append(pill(50, yy, 80, 28, t, fill=WHITE, stroke=TEAL, size=13))
    b.append(text(140, yy + 19, d, 12.5, INK, "start"))
# runtime
b.append(rect(318, 65, 467, 275, NEUTRAL_T, LINE, rx=10, sw=1.2))
b.append(text(551, 92, "Lo necesario para ejecutar", 14, INK, "middle", 600))
b.append(rect(335, 108, 432, 105, WHITE, TEAL, rx=8))
b.append(text(350, 132, "JVM (máquina virtual de Java)", 14, INK, "start", 600))
b.append(lines(350, 156, ["• carga las clases y verifica el bytecode",
                          "• lo interpreta y compila al vuelo (JIT) lo que más se usa",
                          "• libera la memoria con el recolector de basura"], 12.5, gap=18, anchor="start"))
b.append(rect(335, 225, 432, 100, WHITE, INDIGO, rx=8))
b.append(text(350, 249, "Biblioteca estándar (módulos)", 14, INK, "start", 600))
mods = [("java.base", "String, colecciones, java.time, ficheros…"), ("java.sql", "JDBC (UD2)"), ("java.xml", "DOM y StAX (UD1)")]
for i, (m, d) in enumerate(mods):
    yy = 270 + i * 19
    b.append(text(350, yy, m, 12.5, INDIGO, "start", 600, mono=True))
    b.append(text(445, yy, d, 12.5, INK, "start"))
open(OUT + "fig-0-2-jdk.svg", "w").write(svg(820, 375, "".join(b), "Contenido del JDK: herramientas de desarrollo, JVM y biblioteca estándar"))

# ---------- Figura 0.3: el Gradle Wrapper ----------
b = []
b.append(box(20, 165, 170, 56, "./gradlew build", "lo que tú escribes", fill=NEUTRAL_T, stroke=INK, tmono=True))
b.append(box(240, 165, 165, 56, "gradlew", "gradlew.bat en Windows", stroke=TEAL, tmono=True))
b.append(path([(190, 193), (236, 193)], "ink"))
b.append(file_icon(225, 25, 195, 78, "gradle-wrapper.properties", ["distributionUrl=…/", "gradle-9.x-bin.zip"], tsize=11.5, ssize=11, smono=True))
b.append(path([(322, 103), (322, 161)], "teal", dash=True))
b.append(text(330, 137, "lee qué versión usar", 12, TEAL, "start", halo=True))
# rombo
cx, cy = 530, 193
b.append(f'<path d="M{cx},{cy-58} L{cx+88},{cy} L{cx},{cy+58} L{cx-88},{cy} z" fill="{WHITE}" stroke="{INK}" stroke-width="1.5"/>')
b.append(lines(cx, cy - 8, ["¿Está esa versión", "en la caché?"], 12.5, gap=17))
b.append(path([(405, 193), (438, 193)], "ink"))
# caché
b.append(cylinder(675, 150, 165, 86, "Caché local", ["~/.gradle/wrapper/dists"], tsize=13))
b.append(path([(618, 193), (671, 193)], "ink"))
b.append(text(642, 185, "sí", 12.5, INK, "middle", 600))
# descarga
b.append(box(445, 305, 170, 56, "services.gradle.org", "distribución oficial", fill=INDIGO_T, stroke=INDIGO))
b.append(path([(530, 251), (530, 301)], "ink"))
b.append(text(538, 282, "no", 12.5, INK, "start", 600))
b.append(path([(615, 333), (757, 333), (757, 240)], "indigo"))
b.append(lines(770, 290, ["descarga y descomprime", "(solo la primera vez)"], 12, gap=16, fill=INDIGO, anchor="start"))
# ejecutar
b.append(box(880, 165, 165, 56, "Gradle 9.x", "ejecuta la tarea build", fill=TEAL_T, stroke=TEAL))
b.append(path([(840, 193), (876, 193)], "teal"))
open(OUT + "fig-0-5-gradle-wrapper.svg", "w").write(svg(1065, 380, "".join(b), "Funcionamiento del Gradle Wrapper"))

# ---------- Figura 0.4: grafo de tareas del plugin Java ----------
b = []
def task(x, y, name, hl=False, w=None):
    w = w or max(120, tw(name, 13, True) + 28)
    return pill(x, y, w, 32, name, fill=TEAL_T if hl else WHITE, stroke=TEAL if hl else LINE, size=13,
                weight=700 if hl else 500), (x, y, w, 32)
P = {}
def add(key, x, y, name, hl=False, w=None):
    s, geo = task(x, y, name, hl, w); b.append(s); P[key] = geo
def c(k, side):
    x, y, w, h = P[k]
    return {"t": (x + w / 2, y), "b": (x + w / 2, y + h), "l": (x, y + h / 2), "r": (x + w, y + h / 2)}[side]
add("cj", 30, 30, "compileJava", w=150)
add("pr", 200, 30, "processResources", w=170)
add("cl", 120, 110, "classes", w=130)
add("jar", 30, 200, "jar", True, w=110)
add("as", 30, 290, "assemble", w=110)
add("run", 215, 200, "run", True, w=100)
add("ctj", 380, 200, "compileTestJava", w=165)
add("ptr", 565, 200, "processTestResources", w=200)
add("tc", 470, 290, "testClasses", w=145)
add("te", 487.5, 370, "test", True, w=110)
add("ch", 487.5, 450, "check", w=110)
add("bu", 210, 450, "build", True, w=110)
add("clean", 650, 30, "clean", True, w=100)
add("jd", 650, 110, "javadoc", True, w=110)
def arr(a, sa, z, sz, via=None, color="ink"):
    pts = [c(a, sa)] + (via or []) + [c(z, sz)]
    b.append(path(pts, color))
arr("cj", "b", "cl", "t", [(105, 90), (185, 90)])
arr("pr", "b", "cl", "t", [(285, 90), (185, 90)])
arr("cl", "b", "jar", "t", [(185, 165), (85, 165)])
arr("cl", "b", "run", "t", [(185, 165), (265, 165)], color="teal")
arr("cl", "b", "ctj", "t", [(185, 165), (462, 165)])
arr("ctj", "b", "tc", "t", [(462, 260), (542, 260)])
arr("ptr", "b", "tc", "t", [(665, 260), (542, 260)])
arr("jar", "b", "as", "t")
arr("tc", "b", "te", "t")
arr("te", "b", "ch", "t")
arr("as", "b", "bu", "t", [(85, 420), (265, 420)])
arr("ch", "l", "bu", "r")
b.append(text(700, 166, "no forman parte de build:", 12, MUTED, "middle", italic=True))
b.append(text(700, 182, "se lanzan cuando las pides", 12, MUTED, "middle", italic=True))
# leyenda
b.append(rect(640, 330, 230, 92, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(pill(655, 345, 64, 26, "tarea", fill=TEAL_T, stroke=TEAL, size=12, weight=700))
b.append(text(728, 363, "la escribirás a mano", 12, INK, "start"))
b.append(path([(655, 398), (712, 398)], "ink"))
b.append(text(728, 402, "A → B: B espera a A", 12, INK, "start"))
open(OUT + "fig-0-4-tareas-gradle.svg", "w").write(svg(890, 500, "".join(b), "Grafo de tareas de los plugins java y application de Gradle"))
print("ok")

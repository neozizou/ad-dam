"""Figuras 0.3 (dependencias), 0.6 (memoria), 0.7 (igualdad), 0.8 (clase UML) y 0.9 (relaciones UML).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud0_b.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud0" / "img") + "/"

# ---------- Figura 0.5: resolución de dependencias ----------
b = []
b.append(file_icon(20, 20, 330, 92, "gradle/libs.versions.toml",
                   ['junit-jupiter = { module =', '"org.junit.jupiter:junit-jupiter",', 'version.ref = "junit-jupiter" }'],
                   tsize=12.5, ssize=11, smono=True))
b.append(file_icon(20, 160, 330, 80, "app/build.gradle.kts",
                   ['testImplementation(libs.junit.jupiter)', 'testRuntimeOnly("org.junit.platform:…")'], tsize=12.5, ssize=11, smono=True))
b.append(path([(185, 112), (185, 156)], "teal", dash=True))
b.append(text(195, 139, "el alias libs.junit.jupiter", 12, TEAL, "start", halo=True))
b.append(box(410, 150, 200, 100, "Gradle", ["resuelve la dependencia", "y las de ella (transitivas)"], fill=TEAL_T, stroke=TEAL))
b.append(path([(350, 200), (406, 200)], "ink"))
b.append(box(680, 25, 210, 64, "Maven Central", "repo.maven.apache.org", fill=INDIGO_T, stroke=INDIGO))
b.append(cylinder(690, 150, 190, 92, "Caché local", ["~/.gradle/caches", "se descarga una sola vez"]))
b.append(path([(560, 150), (560, 57), (676, 57)], "indigo"))
b.append(text(570, 110, "si no está", 12, INDIGO, "start", halo=True))
b.append(text(570, 125, "en la caché", 12, INDIGO, "start", halo=True))
b.append(path([(785, 89), (785, 146)], "indigo"))
b.append(path([(686, 200), (614, 200)], "ink"))
# classpaths
cps = [("compileClasspath", "compilar src/main", "implementation, compileOnly"),
       ("runtimeClasspath", "ejecutar (run, jar)", "implementation, runtimeOnly"),
       ("testRuntimeClasspath", "pasar las pruebas", "todo lo anterior + testImplementation, testRuntimeOnly")]
for i, (n, uso, conf) in enumerate(cps):
    yy = 300 + i * 46
    b.append(rect(20, yy, 870, 38, WHITE, LINE, rx=6, sw=1.2))
    b.append(text(34, yy + 24, n, 13, TEAL, "start", 700, mono=True))
    b.append(text(250, yy + 24, uso, 12.5, INK, "start"))
    b.append(text(430, yy + 24, conf, 12.5, MUTED, "start", mono=True))
b.append(path([(510, 250), (510, 296)], "teal"))
b.append(text(520, 278, "monta los classpath", 12, TEAL, "start", halo=True))
open(OUT + "fig-0-3-dependencias.svg", "w").write(svg(910, 445, "".join(b), "Cómo resuelve Gradle las dependencias del proyecto"))

# ---------- Figura 0.6: pila, montículo y recolector ----------
b = []
code = ['int stock = 12;', 'Producto p = new Producto("TEC01", …);', 'Producto q = p;            // alias',
        'Producto r = null;', 'new Producto("RAT01", …);  // nadie lo guarda']
b.append(rect(20, 20, 370, 150, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(text(34, 44, "Código", 13, MUTED, "start", 600))
b.append(lines(34, 70, code, 12, gap=22, anchor="start", mono=True))
# pila
b.append(rect(20, 200, 250, 210, WHITE, INK, rx=8))
b.append(text(145, 226, "Pila (marco de main)", 13.5, INK, "middle", 700))
vars_ = [("int stock", "12"), ("Producto p", None), ("Producto q", None), ("Producto r", "null")]
slots = {}
for i, (n, v) in enumerate(vars_):
    yy = 242 + i * 40
    b.append(text(36, yy + 22, n, 12.5, INK, "start", mono=True))
    b.append(rect(165, yy + 4, 85, 28, TEAL_T if v == "12" else WHITE, LINE, rx=4, sw=1.2))
    if v:
        b.append(text(207, yy + 23, v, 12.5, INK if v == "12" else MUTED, "middle", 600 if v == "12" else 400, mono=True))
    else:
        b.append(f'<circle cx="207" cy="{yy+18}" r="4.5" fill="{TEAL}"/>')
    slots[n] = (207, yy + 18)
# montículo
b.append(rect(320, 200, 600, 240, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(text(620, 226, "Montículo (heap): aquí viven todos los objetos", 13.5, INK, "middle", 700))
o1, h1 = uml_class(420, 250, 230, "Producto", ['codigo = "TEC01"', 'nombre = "Teclado…"', 'precio = 59.90', 'stock = 12'],
                   fill=WHITE, stroke=TEAL, head_fill=TEAL_T, size=12)
b.append(o1)
o2, h2 = uml_class(690, 250, 210, "Producto", ['codigo = "RAT01"', '…'], fill=WHITE, stroke=LINE, size=12, dash=True)
b.append(o2)
b.append(lines(795, 360, ["sin ninguna referencia:", "inalcanzable, el recolector", "de basura puede liberarlo"], 12, gap=16, fill=ROSE, italic=True))
# flechas referencias
px, py = slots["Producto p"]; qx, qy = slots["Producto q"]
b.append(path([(px, py), (300, py), (300, 268), (416, 268)], "teal"))
b.append(path([(qx, qy), (310, qy), (310, 290), (416, 290)], "teal"))
b.append(text(340, 425, "p y q apuntan al MISMO objeto: modificarlo desde p se ve desde q", 12, TEAL, "start", italic=True))
open(OUT + "fig-0-6-memoria.svg", "w").write(svg(940, 460, "".join(b), "Variables en la pila, objetos en el montículo y objetos inalcanzables"))

# ---------- Figura 0.7: == frente a equals ----------
b = []
b.append(rect(20, 20, 360, 70, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(lines(34, 48, ['String a = "hola";', 'String b = new String("hola");'], 13, gap=22, anchor="start", mono=True))
b.append(rect(20, 110, 200, 120, WHITE, INK, rx=8))
b.append(text(120, 134, "Pila", 13.5, INK, "middle", 700))
for i, n in enumerate(["String a", "String b"]):
    yy = 150 + i * 38
    b.append(text(36, yy + 20, n, 12.5, INK, "start", mono=True))
    b.append(rect(140, yy + 3, 60, 26, WHITE, LINE, rx=4, sw=1.2))
    b.append(f'<circle cx="170" cy="{yy+16}" r="4.5" fill="{TEAL}"/>')
b.append(rect(270, 110, 330, 170, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(text(435, 134, "Montículo", 13.5, INK, "middle", 700))
b.append(box(300, 144, 130, 44, '"hola"', "objeto 1", stroke=TEAL, tmono=True))
b.append(box(300, 214, 130, 44, '"hola"', "objeto 2", stroke=TEAL, tmono=True))
b.append(path([(170, 166), (296, 166)], "teal"))
b.append(path([(170, 204), (240, 204), (240, 236), (296, 236)], "teal"))
b.append(text(445, 175, "dos objetos distintos", 12, MUTED, "start", italic=True))
b.append(text(445, 191, "con el mismo contenido", 12, MUTED, "start", italic=True))
# resultados
b.append(rect(630, 110, 290, 72, ROSE_T, ROSE, rx=8))
b.append(text(645, 138, "a == b       → false", 13, INK, "start", 700, mono=True))
b.append(text(645, 162, "¿son el mismo objeto?", 12.5, INK, "start"))
b.append(rect(630, 198, 290, 72, TEAL_T, TEAL, rx=8))
b.append(text(645, 226, "a.equals(b)  → true", 13, INK, "start", 700, mono=True))
b.append(text(645, 250, "¿tienen el mismo contenido?", 12.5, INK, "start"))
b.append(text(470, 305, "Regla: los objetos se comparan con equals; == solo para primitivos (y para saber si es el mismo objeto).", 12.5, INK, "middle", italic=True))
open(OUT + "fig-0-7-igualdad.svg", "w").write(svg(940, 325, "".join(b), "Diferencia entre == y equals con cadenas"))

# ---------- Figura 0.8: notación UML de una clase ----------
b = []
cls, h = uml_class(40, 30, 470, "Producto",
                   ["- codigo: String {readOnly}", "- nombre: String", "- precio: BigDecimal", "- stock: int"],
                   ["+ Producto(codigo: String, nombre: String,", "           precio: BigDecimal, stock: int)",
                    "+ getCodigo(): String", "+ setPrecio(precio: BigDecimal): void", "+ reponer(unidades: int): void",
                    ("- validarPrecio(precio: BigDecimal): BigDecimal", {"u": True}), "+ equals(o: Object): boolean"],
                   head_fill=TEAL_T, stroke=TEAL, size=12.5)
b.append(cls)
notes = [(49, "Nombre de la clase (compartimento superior)"),
         (77, "{readOnly}: no cambia tras crearse (final)"),
         (113, "Atributos:  visibilidad nombre: tipo"),
         (196, "Métodos:  visibilidad nombre(parámetros): tipo devuelto"),
         (251, "Subrayado: miembro static (de la clase, no del objeto)")]
for yy, t in notes:
    b.append(path([(590, yy - 4), (520, yy - 4)], "muted", marker_end="a"))
    b.append(text(600, yy, t, 12.5, INK, "start"))
# visibilidad
b.append(rect(600, 280, 330, 56, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(text(615, 303, "+ public     - private", 13, INK, "start", mono=True))
b.append(text(615, 325, "# protected  ~ paquete", 13, INK, "start", mono=True))
open(OUT + "fig-0-8-uml-clase.svg", "w").write(svg(1010, 355, "".join(b), "Notación UML de una clase: la clase Producto"))

# ---------- Figura 0.9: relaciones UML ----------
b = []
rows = [
    ("Generalización", "«es un»: herencia", "class Tarjeta extends MetodoPago", "Tarjeta", "MetodoPago", "gen"),
    ("Realización", "«implementa» una interfaz", "class …Memoria implements …Repository", "…Memoria", "«interface»\nProductoRepository", "real"),
    ("Asociación", "«conoce a»: un atributo que apunta a otro objeto", "private Cliente cliente;", "Pedido", "Cliente", "asoc"),
    ("Composición", "«se compone de»: las partes no existen sin el todo", "private List<LineaPedido> lineas;", "Pedido", "LineaPedido", "comp"),
    ("Dependencia", "«usa»: parámetro, variable local o excepción", "throw new ProductoNoEncontradoException(…)", "ProductoService", "ProductoNo-\nEncontradoException", "dep"),
]
b.append(text(30, 30, "Notación", 13, MUTED, "start", 600))
b.append(text(490, 30, "Significado", 13, MUTED, "start", 600))
b.append(text(450, 30 + 0, "", 13))
for i, (nom, sig, ej, a, z, kind) in enumerate(rows):
    y = 48 + i * 84
    if i:
        b.append(f'<line x1="20" y1="{y-8}" x2="1000" y2="{y-8}" stroke="#E1E5EA" stroke-width="1"/>')
    # cajas mini
    def mini(x, s, dashed=False):
        parts = s.split("\n")
        w = 172
        r = rect(x, y + 8, w, 50, WHITE, INK, rx=2, sw=1.3, dash=dashed)
        if len(parts) == 1:
            r += text(x + w / 2, y + 38, parts[0], 12.5, INK, "middle", 600)
        else:
            r += text(x + w / 2, y + 28, parts[0], 11.5, MUTED, "middle")
            r += text(x + w / 2, y + 45, parts[1], 12, INK, "middle", 600)
        return r
    b.append(mini(20, a)); b.append(mini(282, z))
    yy = y + 33
    if kind == "gen":
        b.append(path([(192, yy), (280, yy)], "ink", marker_end="t"))
    elif kind == "real":
        b.append(path([(192, yy), (280, yy)], "ink", marker_end="t", dash=True))
    elif kind == "asoc":
        b.append(path([(192, yy), (280, yy)], "ink", marker_end="o"))
        b.append(text(200, yy - 7, "*", 13, INK, "start", 700)); b.append(text(270, yy - 7, "1", 13, INK, "end", 700))
    elif kind == "comp":
        b.append(path([(192, yy), (282, yy)], "ink", marker_end=None, marker_start="d"))
        b.append(text(212, yy - 9, "1", 13, INK, "start", 700)); b.append(text(274, yy - 9, "1..*", 13, INK, "end", 700))
    elif kind == "dep":
        b.append(path([(192, yy), (280, yy)], "ink", marker_end="o", dash=True))
    b.append(text(490, y + 26, nom, 14, TEAL, "start", 700))
    b.append(text(490, y + 46, sig, 12.5, INK, "start"))
    b.append(text(490, y + 64, ej, 12, MUTED, "start", mono=True))
open(OUT + "fig-0-9-relaciones-uml.svg", "w").write(svg(1020, 470, "".join(b), "Relaciones en un diagrama de clases UML"))
print("ok")

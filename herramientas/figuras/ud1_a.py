"""Figuras 1.1 (rutas), 1.2 (flujos), 1.3 (codificación) y 1.4 (acceso secuencial y aleatorio).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud1_a.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud1" / "img") + "/"

# ---------- Figura 1.1: rutas relativas y directorio de trabajo ----------
b = []
b.append(rect(15, 15, 330, 370, NEUTRAL_T, LINE, rx=10, sw=1))
b.append(text(30, 42, "Carpetas del proyecto", 13.5, MUTED, "start", 700))
tree = [("tienda/", 0, True, "root"), ("config.properties", 1, False, None), ("datos/", 1, True, None),
        ("productos.json", 2, False, "ok"), ("app/", 1, True, "app"), ("build.gradle.kts", 2, False, None),
        ("datos/", 2, True, None), ("productos.json", 3, False, "ko"), ("src/…", 2, True, None)]
ys = {}
for i, (n, lvl, d, tag) in enumerate(tree):
    y = 72 + i * 34
    x = 35 + lvl * 26
    if lvl:
        b.append(f'<path d="M{x-14},{y-24} L{x-14},{y-5} L{x-4},{y-5}" fill="none" stroke="{LINE}" stroke-width="1.2"/>')
    fill = {"ok": TEAL_T, "ko": ROSE_T}.get(tag, WHITE)
    stroke = {"ok": TEAL, "ko": ROSE}.get(tag, LINE)
    w = tw(n, 12.5, True) + 16
    b.append(rect(x, y - 19, w, 26, fill, stroke, rx=4, sw=1.2))
    b.append(text(x + 8, y - 1, n, 12.5, INK, "start", 700 if d else 400, mono=True))
    ys[tag] = (x + w, y - 6)
# casos
b.append(rect(385, 15, 560, 175, TEAL_T, TEAL, rx=10, sw=1.2))
b.append(text(400, 42, "Directorio de trabajo: tienda/", 14, TEAL, "start", 700))
b.append(lines(400, 66, ["Terminal abierta en tienda/, Run de VS Code, o ./gradlew run",
                          "con workingDir = rootProject.projectDir"], 12.5, gap=18, anchor="start"))
b.append(text(400, 116, 'Path.of("datos/productos.json")', 12.5, INK, "start", 600, mono=True))
b.append(text(400, 140, "→ tienda/datos/productos.json", 12.5, TEAL, "start", 700, mono=True))
b.append(text(400, 168, "Es el fichero que esperas.", 12.5, INK, "start", italic=True))
b.append(rect(385, 210, 560, 175, ROSE_T, ROSE, rx=10, sw=1.2))
b.append(text(400, 237, "Directorio de trabajo: tienda/app/", 14, ROSE, "start", 700))
b.append(lines(400, 261, ["./gradlew run sin configurar: Gradle ejecuta el programa",
                          "desde la carpeta del subproyecto"], 12.5, gap=18, anchor="start"))
b.append(text(400, 311, 'Path.of("datos/productos.json")', 12.5, INK, "start", 600, mono=True))
b.append(text(400, 335, "→ tienda/app/datos/productos.json", 12.5, ROSE, "start", 700, mono=True))
b.append(text(400, 363, "Otro fichero distinto: «¡mis datos han desaparecido!»", 12.5, INK, "start", italic=True))
xo, yo = ys["ok"]; xk, yk = ys["ko"]
b.append(path([(xo + 4, yo), (381, 128)], "teal"))
b.append(path([(xk + 4, yk), (381, 323)], "rose"))
open(OUT + "fig-1-1-rutas.svg", "w").write(svg(960, 400, "".join(b), "Cómo se resuelve una ruta relativa según el directorio de trabajo"))

# ---------- Figura 1.2: flujos y su composición ----------
b = []
def stage(x, y, w, title, sub, fill=WHITE, stroke=LINE, mono=True):
    return box(x, y, w, 62, title, sub, fill=fill, stroke=stroke, tmono=mono, tsize=13, ssize=11.5)
y = 50
b.append(text(20, 30, "Leer un fichero de texto", 14, INK, "start", 700))
b.append(cylinder(20, y - 4, 95, 70, "Disco", None, tsize=12.5))
b.append(stage(160, y, 190, "InputStream", ["lee bytes"], stroke=INDIGO))
b.append(stage(395, y, 210, "InputStreamReader", ["bytes → caracteres (UTF-8)"], stroke=TEAL))
b.append(stage(650, y, 190, "BufferedReader", ["por bloques; readLine()"], stroke=TEAL))
b.append(box(885, y, 95, 62, "Tu código", None, fill=NEUTRAL_T, stroke=INK, tsize=12.5))
for x1, x2, lab, col in [(115, 156, "bytes", "indigo"), (350, 391, "bytes", "indigo"), (605, 646, "chars", "teal"), (840, 881, "líneas", "teal")]:
    b.append(path([(x1, y + 31), (x2, y + 31)], col))
    b.append(text((x1 + x2) / 2, y + 22, lab, 11, COLORS[col], "middle"))
y2 = 190
b.append(text(20, y2 - 20, "Escribir un fichero de texto", 14, INK, "start", 700))
b.append(box(20, y2, 95, 62, "Tu código", None, fill=NEUTRAL_T, stroke=INK, tsize=12.5))
b.append(stage(160, y2, 190, "BufferedWriter", ["acumula; newLine()"], stroke=TEAL))
b.append(stage(395, y2, 210, "OutputStreamWriter", ["caracteres → bytes (UTF-8)"], stroke=TEAL))
b.append(stage(650, y2, 190, "OutputStream", ["escribe bytes"], stroke=INDIGO))
b.append(cylinder(885, y2 - 4, 95, 70, "Disco", None, tsize=12.5))
for x1, x2, lab, col in [(115, 156, "texto", "teal"), (350, 391, "chars", "teal"), (605, 646, "bytes", "indigo"), (840, 881, "bytes", "indigo")]:
    b.append(path([(x1, y2 + 31), (x2, y2 + 31)], col))
    b.append(text((x1 + x2) / 2, y2 + 22, lab, 11, COLORS[col], "middle"))
b.append(rect(20, 290, 960, 74, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(text(36, 316, "Cada flujo envuelve al anterior. Files lo monta por ti, siempre en UTF-8:", 12.5, INK, "start"))
b.append(text(36, 342, "Files.newBufferedReader(ruta)  ≡  new BufferedReader(new InputStreamReader(Files.newInputStream(ruta), UTF_8))", 12, TEAL, "start", 600, mono=True))
open(OUT + "fig-1-2-flujos.svg", "w").write(svg(1000, 380, "".join(b), "Composición de flujos para leer y escribir texto"))

# ---------- Figura 1.3: codificaciones ----------
b = []
def bytes_row(x, y, items, color, fill):
    out = []
    for i, (bt, ch) in enumerate(items):
        xx = x + i * 58
        out.append(rect(xx, y, 52, 34, fill, color, rx=4, sw=1.2))
        out.append(text(xx + 26, y + 22, bt, 13, INK, "middle", 700, mono=True))
    return "".join(out)
b.append(text(30, 40, 'El texto "año" (3 caracteres)', 14, INK, "start", 700))
for i, ch in enumerate("año"):
    b.append(rect(30 + i * 58, 55, 52, 40, NEUTRAL_T, INK, rx=4, sw=1.2))
    b.append(text(56 + i * 58, 82, ch, 18, INK, "middle", 600))
b.append(text(400, 40, "UTF-8: la ñ ocupa 2 bytes", 14, TEAL, "start", 700))
b.append(bytes_row(400, 58, [("61", "a"), ("C3", ""), ("B1", ""), ("6F", "o")], TEAL, TEAL_T))
b.append(f'<path d="M458,98 L458,106 L568,106 L568,98" fill="none" stroke="{TEAL}" stroke-width="1.4"/>')
b.append(text(513, 122, "ñ", 13, TEAL, "middle", 700))
b.append(text(400, 160, "ISO-8859-1: 1 byte por carácter", 14, AMBER, "start", 700))
b.append(bytes_row(400, 178, [("61", "a"), ("F1", "ñ"), ("6F", "o")], AMBER, AMBER_T))
b.append(path([(200, 75), (392, 75)], "teal"))
b.append(path([(200, 85), (300, 85), (300, 195), (392, 195)], "amber"))
b.append(text(296, 70, "getBytes(UTF_8)", 11.5, TEAL, "middle", mono=True))
b.append(text(300, 215, "getBytes(ISO_8859_1)", 11.5, AMBER, "middle", mono=True))
# errores
b.append(rect(660, 30, 300, 75, ROSE_T, ROSE, rx=8, sw=1.2))
b.append(text(675, 54, "Bytes UTF-8 leídos como Latin-1", 12.5, INK, "start", 600))
b.append(text(675, 84, "aÃ±o", 20, ROSE, "start", 700, mono=True))
b.append(text(760, 84, "cada byte, un carácter", 11.5, MUTED, "start", italic=True))
b.append(rect(660, 150, 300, 75, ROSE_T, ROSE, rx=8, sw=1.2))
b.append(text(675, 174, "Bytes Latin-1 leídos como UTF-8", 12.5, INK, "start", 600))
b.append(text(675, 204, "a\ufffdo", 20, ROSE, "start", 700, mono=True))
b.append(text(740, 204, "o MalformedInputException", 11.5, MUTED, "start", italic=True))
b.append(path([(632, 75), (656, 67)], "rose"))
b.append(path([(574, 195), (656, 188)], "rose"))
b.append(text(30, 262, "Regla del módulo: escribe y lee siempre en UTF-8 (lo que hace Files por defecto) y dilo en la documentación del formato.", 12.5, INK, "start", italic=True))
open(OUT + "fig-1-3-codificacion.svg", "w").write(svg(980, 280, "".join(b), "El mismo texto en UTF-8 y en ISO-8859-1, y lo que pasa al leer con la codificación equivocada"))

# ---------- Figura 1.4: acceso secuencial frente a aleatorio ----------
b = []
b.append(text(20, 30, "Acceso secuencial: para llegar al tercer producto hay que leer los anteriores", 14, INK, "start", 700))
xs = 20
widths = [150, 210, 120, 180, 160]
names = ["TEC01;Teclado…", "RAT01;Ratón inalámbrico…", "MON01;Mon…", "CAB01;Cable USB-C…", "HUB01;Hub…"]
x = xs
for i, (w, n) in enumerate(zip(widths, names)):
    fill = TEAL_T if i == 2 else WHITE
    st = TEAL if i == 2 else LINE
    b.append(rect(x, 45, w, 40, fill, st, rx=0, sw=1.2))
    b.append(text(x + w / 2, 70, n, 12, INK, "middle", mono=True))
    x += w
b.append(path([(20, 105), (365, 105), (395, 105)], "amber"))
b.append(text(25, 125, "lectura de principio a fin: no se sabe dónde empieza cada producto porque cada uno mide distinto", 12, AMBER, "start", italic=True))
y = 215
b.append(text(20, y - 50, "Acceso aleatorio: registros de longitud fija (84 bytes); el registro n empieza en n × 84", 14, INK, "start", 700))
for i in range(5):
    xx = 20 + i * 165
    fill = TEAL_T if i == 2 else WHITE
    st = TEAL if i == 2 else INDIGO
    b.append(rect(xx, y, 165, 40, fill, st, rx=0, sw=1.2))
    b.append(text(xx + 82, y + 25, f"registro {i}", 12.5, INK, "middle", 600 if i == 2 else 400))
    b.append(text(xx, y + 58, str(i * 84), 11.5, MUTED, "middle", mono=True))
b.append(text(845, y + 58, "420", 11.5, MUTED, "middle", mono=True))
b.append(f'<path d="M20,{y-4} C120,{y-40} 250,{y-40} 350,{y-4}" fill="none" stroke="{TEAL}" stroke-width="1.6" marker-end="url(#a-teal)"/>')
b.append(text(186, y + 90, "seek(2 × 84) salta directamente al byte 168", 12.5, TEAL, "middle", 700, mono=True))
# estructura de un registro
y3 = 360
b.append(text(20, y3 - 12, "Dentro de cada registro", 13.5, INK, "start", 700))
segs = [("código", "6 chars = 12 B", 12, NEUTRAL_T), ("nombre", "30 chars = 60 B", 60, NEUTRAL_T), ("precio", "long = 8 B", 8, AMBER_T), ("stock", "int = 4 B", 4, INDIGO_T)]
x = 20
scale = 7
offs = [0, 12, 72, 80, 84]
for i, (n, sub, sz, f) in enumerate(segs):
    w = max(sz * scale, 95)
    b.append(rect(x, y3, w, 46, f, INK, rx=0, sw=1.2))
    b.append(text(x + w / 2, y3 + 20, n, 13, INK, "middle", 700))
    b.append(text(x + w / 2, y3 + 37, sub, 11, MUTED, "middle"))
    b.append(text(x, y3 + 62, str(offs[i]), 11.5, MUTED, "middle", mono=True))
    x += w
b.append(text(x, y3 + 62, "84", 11.5, MUTED, "middle", mono=True))
b.append(text(x + 20, y3 + 28, "cambiar el stock del registro n:", 12, INK, "start"))
b.append(text(x + 20, y3 + 46, "seek(n × 84 + 80) y writeInt", 12, TEAL, "start", 600, mono=True))
open(OUT + "fig-1-4-acceso.svg", "w").write(svg(1000, 445, "".join(b), "Acceso secuencial frente a acceso aleatorio con registros de longitud fija"))
print("ok")

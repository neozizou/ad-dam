"""Figuras 1.9 (conversiones), 1.10 (componente) y 1.11 (escritura segura).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud1_c.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud1" / "img") + "/"

# ---------- Figura 1.9: conversión a través del modelo ----------
b = []
b.append(rect(330, 150, 260, 90, TEAL_T, TEAL, rx=12, sw=1.8))
b.append(text(460, 185, "List<ProductoDto>", 15, INK, "middle", 700, mono=True))
b.append(text(460, 210, "los datos, sin formato", 12.5, MUTED, "middle", italic=True))
files = [("productos.csv", "FormatoCsv", 40, 30, AMBER), ("productos.json", "FormatoJson", 640, 30, TEAL),
         ("productos.xml", "FormatoXml", 40, 290, INDIGO), ("productos.dat", "FormatoBinario", 640, 290, ROSE)]
for name, cls, x, y, col in files:
    b.append(file_icon(x, y, 200, 70, name, [cls], fill=WHITE, stroke=col, ssize=12, smono=True))
for (name, cls, x, y, col), (px, py) in zip(files, [(330, 160), (590, 160), (330, 230), (590, 230)]):
    fx = x + 200 if x < 300 else x
    fy = y + 35
    cn = {AMBER: "amber", TEAL: "teal", INDIGO: "indigo", ROSE: "rose"}[col]
    b.append(path([(fx, fy - 8), (px, py - 8)], cn))
    b.append(path([(px, py + 8), (fx, fy + 8)], cn, dash=True))
b.append(path([(40, 400), (80, 400)], "ink"))
b.append(text(90, 404, "leer(ruta)", 12.5, INK, "start", mono=True))
b.append(path([(250, 400), (290, 400)], "ink", dash=True))
b.append(text(300, 404, "escribir(ruta, productos)", 12.5, INK, "start", mono=True))
b.append(text(460, 440, "Convertir = leer con un formato + escribir con otro:  Formatos.convertir(origen, destino)", 12.5, TEAL, "middle", 600))
open(OUT + "fig-1-9-conversiones.svg", "w").write(svg(880, 460, "".join(b), "Conversión entre formatos a través de una representación común"))

# ---------- Figura 1.10: escritura segura ----------
b = []
b.append(text(20, 30, "Guardar sin riesgo de dejar el fichero a medias", 14.5, INK, "start", 700))
steps = [("1", "Escribir todo en un temporal", "productos.json.tmp", TEAL, TEAL_T),
         ("2", "Mover el temporal encima", "Files.move(…, ATOMIC_MOVE)", TEAL, TEAL_T)]
b.append(file_icon(20, 60, 170, 70, "productos.json", ["versión anterior,", "intacta"], ssize=11.5))
b.append(box(250, 60, 230, 70, "1. Escribir el temporal", ["productos.json.tmp"], stroke=TEAL, fill=TEAL_T, smono=True))
b.append(box(540, 60, 230, 70, "2. Mover encima", ["Files.move(…, ATOMIC_MOVE)"], stroke=TEAL, fill=TEAL_T, smono=True))
b.append(file_icon(830, 60, 170, 70, "productos.json", ["versión nueva,", "completa"], fill=TEAL_T, stroke=TEAL, ssize=11.5))
b.append(path([(480, 95), (536, 95)], "teal"))
b.append(path([(770, 95), (826, 95)], "teal"))
# fallo
b.append(rect(250, 170, 520, 80, ROSE_T, ROSE, rx=8, sw=1.2))
b.append(text(265, 195, "Si algo falla en el paso 1 (disco lleno, se va la luz, excepción…)", 12.5, INK, "start", 600))
b.append(text(265, 218, "el temporal se borra y productos.json conserva la versión anterior completa.", 12.5, INK, "start"))
b.append(text(265, 239, "Escribiendo directamente encima, quedaría un fichero cortado e ilegible.", 12.5, ROSE, "start", italic=True))
b.append(path([(365, 130), (365, 166)], "rose"))
b.append(text(20, 285, "El movimiento atómico ocurre de una vez: quien lea el fichero ve la versión vieja o la nueva, nunca una mezcla.", 12.5, MUTED, "start", italic=True))
open(OUT + "fig-1-11-escritura-segura.svg", "w").write(svg(1020, 300, "".join(b), "Escritura segura de un fichero mediante un temporal y un movimiento atómico"))

# ---------- Figura 1.11: diagrama de clases del componente de ficheros ----------
b = []
svc, hs = uml_class(30, 30, 230, "ProductoService", [], ["+ exportar(destino: Path): int", "…"], size=12)
b.append(svc)
rep, hr = uml_class(330, 30, 300, "ProductoRepository", [], ["+ guardar(p: Producto)", "+ buscarPorCodigo(c): Optional<…>", "+ buscarTodos(): List<Producto>", "+ borrar(c: String): boolean"],
                    stereo="«interface»", head_fill=TEAL_T, stroke=TEAL, italic=True, size=12)
b.append(rep)
b.append(path([(260, 70), (326, 70)], "ink", marker_end="o", dash=True))
mem, hm = uml_class(225, 260, 245, "…Memoria", ["- datos: Map<String, Producto>"], [], size=11.5, stroke=LINE)
b.append(mem)
fic, hf = uml_class(500, 260, 300, "ProductoRepositoryFichero", ["- ruta: Path", "- formato: FormatoProductos", "- datos: Map<String, ProductoDto>"],
                    ["- cargar()", "- escribirFichero()"], head_fill=TEAL_T, stroke=TEAL, size=12)
b.append(fic)
yb = 30 + hr
b.append(path([(347, 260), (347, 230), (650, 230)], "ink", marker_end=None, dash=True))
b.append(path([(650, 260), (650, 230)], "ink", marker_end=None, dash=True))
b.append(path([(480, 230), (480, yb + 2)], "ink", marker_end="t", dash=True))
fmt, hfm = uml_class(870, 30, 270, "FormatoProductos", [], ["+ leer(ruta): List<ProductoDto>", "+ escribir(ruta, productos)"],
                     stereo="«interface»", head_fill=AMBER_T, stroke=AMBER, italic=True, size=12)
b.append(fmt)
b.append(path([(800, 290), (840, 290), (840, 70), (866, 70)], "ink", marker_end="o"))
b.append(text(848, 285, "1", 13, INK, "start", 700))
names = ["FormatoCsv", "FormatoJson", "FormatoXml", "FormatoBinario"]
fy = 30 + hfm + 60
for i, n in enumerate(names):
    yy = fy + i * 48
    b.append(box(960, yy, 160, 34, n, None, stroke=AMBER, tmono=True, tsize=12.5))
    b.append(path([(960, yy + 17), (935, yy + 17)], "ink", marker_end=None, dash=True))
b.append(path([(935, fy + 3 * 48 + 17), (935, 30 + hfm + 2)], "ink", marker_end="t", dash=True))
dto, hd = uml_class(500, 470, 300, "ProductoDto", ["codigo, nombre, precio, stock"], ["+ desde(p: Producto): ProductoDto", "+ aProducto(): Producto"],
                    stereo="«record»", head_fill=NEUTRAL_T, size=12)
b.append(dto)
b.append(path([(650, 260 + hf), (650, 466)], "ink", marker_end="o", dash=True))
b.append(path([(1040, fy + 3 * 48 + 34), (1040, 520), (804, 520)], "ink", marker_end="o", dash=True))
exc, he = uml_class(150, 470, 250, "AccesoDatosException", [], [], stereo="RuntimeException", size=12, stroke=ROSE, head_fill=ROSE_T)
b.append(exc)
b.append(path([(560, 260 + hf), (560, 440), (275, 440), (275, 466)], "ink", marker_end="o", dash=True))
b.append(text(420, 434, "lanza", 12, MUTED, "middle", italic=True))
b.append(text(30, 600, "Las flechas discontinuas con punta abierta indican «usa»; las de triángulo hueco, «implementa».", 12.5, MUTED, "start", italic=True))
open(OUT + "fig-1-10-componente.svg", "w").write(svg(1160, 620, "".join(b), "Diagrama de clases del componente de acceso a ficheros"))
print("ok")

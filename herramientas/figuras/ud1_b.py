"""Figuras 1.5 (binario), 1.6 (serialización), 1.7 (formatos) y 1.8 (DOM).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud1_b.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud1" / "img") + "/"

# ---------- Figura 1.5: estructura del fichero binario ----------
b = []
fields = [("firma «TDP1»", ["54", "44", "50", "31"], INDIGO_T, INDIGO),
          ("cantidad = 4", ["00", "00", "00", "04"], NEUTRAL_T, INK),
          ("long. 5", ["00", "05"], AMBER_T, AMBER),
          ("«TEC01»", ["54", "45", "43", "30", "31"], TEAL_T, TEAL),
          ("long. 17", ["00", "11"], AMBER_T, AMBER),
          ("«Teclado mecánico» en UTF-8 (la á ocupa 2 bytes)", ["54", "65", "63", "6C", "61", "64", "6F", "20", "6D", "65", "63", "C3", "A1", "6E", "69", "63", "6F"], TEAL_T, TEAL),
          ("precio: 5990 céntimos", ["00", "00", "00", "00", "00", "00", "17", "66"], ROSE_T, ROSE),
          ("stock = 12", ["00", "00", "00", "0C"], NEUTRAL_T, INK)]
CW, PER = 39, 23
cells = []
for name, bs, f, s in fields:
    for i, bt in enumerate(bs):
        cells.append((bt, f, s, name, i == 0, i == len(bs) - 1))
X0, Y0, RH = 30, 60, 130
b.append(text(30, 30, "Un producto dentro de catalogo.dat (FormatoBinario): 46 bytes, sin separadores ni nombres de campo", 13.5, INK, "start", 700))
groups = []
for idx, (bt, f, s, name, first, last) in enumerate(cells):
    row, col = divmod(idx, PER)
    x, y = X0 + col * CW, Y0 + row * RH
    b.append(rect(x, y, CW - 3, 32, f, s, rx=3, sw=1.1))
    b.append(text(x + (CW - 3) / 2, y + 21, bt, 12.5, INK, "middle", 600, mono=True))
    b.append(text(x + (CW - 3) / 2, y - 6, str(idx), 9.5, MUTED, "middle", mono=True))
    if first or col == 0:
        groups.append([name, s, x, y, x + CW - 3, first])
    else:
        groups[-1][4] = x + CW - 3
for name, s, x1, y, x2, first in groups:
    b.append(f'<path d="M{x1},{y+40} L{x1},{y+46} L{x2},{y+46} L{x2},{y+40}" fill="none" stroke="{s}" stroke-width="1.3"/>')
    if not first:
        b.append(text((x1 + x2) / 2, y + 62, "(continúa el nombre)", 11.5, s, "middle", italic=True))
    if first:
        lbl_lines = [name] if tw(name, 11.5) < (x2 - x1) + 30 else [name[:name.find(" en ")], name[name.find(" en ") + 1:]] if " en " in name else [name]
        b.append(lines((x1 + x2) / 2, y + 62, lbl_lines, 11.5, gap=15, fill=s))
b.append(text(30, 320, "writeUTF guarda primero la longitud en 2 bytes; writeLong ocupa siempre 8 bytes y writeInt, 4. Para leer hay que conocer el orden exacto.", 12.5, INK, "start", italic=True))
open(OUT + "fig-1-5-binario.svg", "w").write(svg(940, 340, "".join(b), "Bytes de un producto en el fichero binario"))

# ---------- Figura 1.6: serialización ----------
b = []
def graph(x0, y0, title, col, fill):
    out = [text(x0 + 135, y0 - 10, title, 13.5, INK, "middle", 700)]
    out.append(box(x0 + 75, y0, 120, 36, "ArrayList", None, fill=fill, stroke=col, tmono=True, tsize=12.5))
    out.append(box(x0, y0 + 75, 125, 36, "ProductoDto", None, fill=fill, stroke=col, tmono=True, tsize=12))
    out.append(box(x0 + 145, y0 + 75, 125, 36, "ProductoDto", None, fill=fill, stroke=col, tmono=True, tsize=12))
    out.append(box(x0 - 10, y0 + 150, 80, 32, '"TEC01"', None, fill=WHITE, stroke=LINE, tmono=True, tsize=11.5))
    out.append(box(x0 + 78, y0 + 150, 80, 32, "59.90", None, fill=WHITE, stroke=LINE, tmono=True, tsize=11.5))
    out.append(text(x0 + 208, y0 + 170, "…", 14, MUTED, "middle"))
    cn = "teal" if col == TEAL else "indigo"
    out.append(path([(x0 + 120, y0 + 36), (x0 + 62, y0 + 71)], cn))
    out.append(path([(x0 + 150, y0 + 36), (x0 + 207, y0 + 71)], cn))
    out.append(path([(x0 + 45, y0 + 111), (x0 + 30, y0 + 146)], cn))
    out.append(path([(x0 + 80, y0 + 111), (x0 + 113, y0 + 146)], cn))
    return "".join(out)
b.append(graph(40, 50, "Objetos en memoria", TEAL, TEAL_T))
b.append(box(345, 95, 150, 50, "ObjectOutputStream", "writeObject(lista)", stroke=TEAL, tmono=True, tsize=12, ssize=11))
b.append(path([(315, 120), (341, 120)], "teal"))
b.append(file_icon(530, 75, 150, 90, "productos.ser", ["descripción de las clases", "+ valores de los campos"], ssize=11))
b.append(path([(495, 120), (526, 120)], "teal"))
b.append(box(715, 95, 150, 50, "ObjectInputStream", "readObject()", stroke=INDIGO, tmono=True, tsize=12, ssize=11))
b.append(path([(680, 120), (711, 120)], "indigo"))
b.append(graph(900, 50, "Objetos nuevos (copias)", INDIGO, INDIGO_T))
b.append(path([(865, 120), (906, 120)], "indigo"))
b.append(rect(40, 265, 1130, 92, ROSE_T, ROSE, rx=8, sw=1))
warn = ["• Solo lo puede leer un programa Java que tenga esas mismas clases: no sirve para intercambiar datos.",
        "• Si cambias la clase (añades o quitas atributos), los ficheros antiguos pueden dejar de leerse.",
        "• Nunca deserialices un fichero de origen desconocido: puede crear objetos que ejecuten código malicioso."]
b.append(lines(58, 290, warn, 12.5, gap=22, anchor="start"))
open(OUT + "fig-1-6-serializacion.svg", "w").write(svg(1190, 375, "".join(b), "Serialización: un grafo de objetos se convierte en bytes y se reconstruye"))

# ---------- Figura 1.7: los mismos datos en tres formatos ----------
b = []
panels = [
    ("CSV", AMBER, AMBER_T, ["codigo;nombre;precio;stock", "TEC01;Teclado mecánico;59.90;12", "RAT01;Ratón inalámbrico;24.50;30"]),
    ("JSON", TEAL, TEAL_T, ["[", "  {", '    "codigo": "TEC01",', '    "nombre": "Teclado mecánico",', '    "precio": 59.90,', '    "stock": 12', "  },", "  {", '    "codigo": "RAT01",', "    …", "  }", "]"]),
    ("XML", INDIGO, INDIGO_T, ['<?xml version="1.0" encoding="UTF-8"?>', "<catalogo>", '  <producto codigo="TEC01">', "    <nombre>Teclado mecánico</nombre>", "    <precio>59.90</precio>", "    <stock>12</stock>", "  </producto>", '  <producto codigo="RAT01">', "    …", "</catalogo>"]),
]
x = 20
widths = [300, 280, 360]
for (name, col, fill, txt), w in zip(panels, widths):
    b.append(rect(x, 20, w, 320, WHITE, col, rx=8, sw=1.4))
    b.append(rect(x, 20, w, 36, fill, col, rx=8, sw=1.4))
    b.append(f'<rect x="{x+1}" y="44" width="{w-2}" height="12" fill="{fill}"/>')
    b.append(text(x + 14, 44, name, 14, col, "start", 700))
    b.append(lines(x + 14, 80, txt, 11.5, gap=20, anchor="start", mono=True))
    x += w + 20
foot = [("tabla plana: una línea por registro", 170), ("objetos y listas anidados", 470), ("árbol de elementos y atributos", 810)]
for t, cx in foot:
    b.append(text(cx, 365, t, 12.5, MUTED, "middle", italic=True))
open(OUT + "fig-1-7-formatos.svg", "w").write(svg(1000, 380, "".join(b), "Los mismos productos en CSV, JSON y XML"))

# ---------- Figura 1.8: árbol DOM ----------
b = []
def node(x, y, w, t, kind):
    f, s, mono = {"doc": (NEUTRAL_T, INK, False), "el": (TEAL_T, TEAL, True), "at": (AMBER_T, AMBER, True), "tx": (WHITE, LINE, True)}[kind]
    r = 4 if kind != "at" else 14
    return rect(x, y, w, 32, f, s, rx=r, sw=1.3) + text(x + w / 2, y + 21, t, 12.5, INK, "middle", 600 if kind != "tx" else 400, mono=mono)
def link(x1, y1, x2, y2):
    return path([(x1, y1), (x1, (y1 + y2) / 2), (x2, (y1 + y2) / 2), (x2, y2)], "line", marker_end=None)
b.append(node(380, 20, 130, "Document", "doc"))
b.append(node(370, 90, 150, "<catalogo>", "el"))
b.append(link(445, 52, 445, 90))
b.append(node(150, 165, 190, "<producto>", "el"))
b.append(node(560, 165, 190, "<producto>", "el"))
b.append(link(445, 122, 245, 165)); b.append(link(445, 122, 655, 165))
b.append(node(20, 245, 150, 'codigo="TEC01"', "at"))
b.append(node(190, 245, 120, "<nombre>", "el"))
b.append(node(340, 245, 110, "<precio>", "el"))
b.append(node(480, 245, 100, "<stock>", "el"))
for cx in (95, 250, 395, 530):
    b.append(link(245, 197, cx, 245))
b.append(node(160, 325, 180, '"Teclado mecánico"', "tx"))
b.append(node(355, 325, 80, '"59.90"', "tx"))
b.append(node(500, 325, 60, '"12"', "tx"))
b.append(link(250, 277, 250, 325)); b.append(link(395, 277, 395, 325)); b.append(link(530, 277, 530, 325))
b.append(node(640, 245, 170, 'codigo="RAT01"', "at"))
b.append(text(860, 266, "…", 16, MUTED, "middle"))
b.append(link(655, 197, 725, 245))
# leyenda
lg = [("doc", "documento (raíz invisible)"), ("el", "elemento: getElementsByTagName, getAttribute"), ("at", "atributo"), ("tx", "nodo de texto: getTextContent()")]
for i, (k, t) in enumerate(lg):
    y = 400 + i * 26
    f, s = {"doc": (NEUTRAL_T, INK), "el": (TEAL_T, TEAL), "at": (AMBER_T, AMBER), "tx": (WHITE, LINE)}[k]
    b.append(rect(30, y, 30, 18, f, s, rx=3 if k != "at" else 9, sw=1.2))
    b.append(text(72, y + 14, t, 12.5, INK, "start"))
open(OUT + "fig-1-8-dom.svg", "w").write(svg(900, 510, "".join(b), "Árbol DOM del catálogo en XML"))
print("ok")

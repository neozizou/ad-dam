"""Figuras 2.5 (diagrama entidad-relación) y 2.6 (modelo relacional).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud2_b.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud2" / "img") + "/"

# ---------- Figura 2.5: diagrama entidad-relación de la tienda ----------
b = []
EW, EH = 140, 50

def entidad(x, y, nombre):
    return rect(x, y, EW, EH, TEAL_T, TEAL, rx=2, sw=1.8) + text(x + EW / 2, y + 31, nombre, 14, INK, "middle", 700)

def rombo(cx, cy, nombre, tipo, w=124, h=70):
    d = f"M{cx},{cy-h/2} L{cx+w/2},{cy} L{cx},{cy+h/2} L{cx-w/2},{cy} z"
    return (f'<path d="{d}" fill="{AMBER_T}" stroke="{AMBER}" stroke-width="1.6"/>'
            + text(cx, cy - 2, nombre, 12.5, INK, "middle", 700) + text(cx, cy + 15, tipo, 12, AMBER, "middle", 700))

def atributos(cx, y0, nombres, clave=0, arriba=True, sep=62, ancho=EW - 24):
    """Atributos en abanico: cada línea sale del borde de la entidad y acaba en un círculo."""
    out = []
    n = len(nombres)
    paso_borde = min(sep, ancho / max(n - 1, 1))
    for i, nom in enumerate(nombres):
        x0 = cx + (i - (n - 1) / 2) * paso_borde
        x = cx + (i - (n - 1) / 2) * sep
        alto = 40 if i % 2 == 0 else 72
        y = y0 - alto if arriba else y0 + alto
        out.append(f'<line x1="{x0}" y1="{y0}" x2="{x}" y2="{y + (6 if arriba else -6)}" stroke="{INK}" stroke-width="1.2"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{INK if i == clave else WHITE}" stroke="{INK}" stroke-width="1.4"/>')
        ty = y - 12 if arriba else y + 22
        out.append(text(x, ty, nom, 12, INK, "middle", 700 if i == clave else 400, mono=True))
    return "".join(out)

def card(x, y, t, anchor="middle"):
    return text(x, y, t, 12.5, ROSE, anchor, 700, halo=True)

CY = 160
cli_x, ped_x, pro_x = 40, 420, 820
b.append(atributos(cli_x + EW / 2, CY - EH / 2, ["id", "nombre", "email", "fecha_alta"]))
b.append(atributos(ped_x + EW / 2, CY - EH / 2, ["numero", "fecha", "estado"]))
b.append(atributos(pro_x + EW / 2, CY - EH / 2, ["codigo", "nombre", "precio", "stock"]))
b.append(f'<line x1="{cli_x+EW}" y1="{CY}" x2="{ped_x}" y2="{CY}" stroke="{INK}" stroke-width="1.5"/>')
b.append(f'<line x1="{ped_x+EW}" y1="{CY}" x2="{pro_x}" y2="{CY}" stroke="{INK}" stroke-width="1.5"/>')
b.append(entidad(cli_x, CY - EH / 2, "CLIENTE"))
b.append(entidad(ped_x, CY - EH / 2, "PEDIDO"))
b.append(entidad(pro_x, CY - EH / 2, "PRODUCTO"))
b.append(rombo(300, CY, "REALIZA", "1:N"))
b.append(rombo(700, CY, "CONTIENE", "N:M"))
b.append(card(cli_x + EW + 26, CY - 10, "(1,1)"))
b.append(card(ped_x - 26, CY - 10, "(0,n)"))
b.append(card(ped_x + EW + 26, CY - 10, "(0,n)"))
b.append(card(pro_x - 26, CY - 10, "(1,n)"))
b.append(atributos(700, CY + 35, ["cantidad", "precio_unitario"], clave=-1, arriba=False, sep=110, ancho=0))
# categoria
cat_y = 380
b.append(f'<line x1="{pro_x+EW/2}" y1="{CY+EH/2}" x2="{pro_x+EW/2}" y2="{cat_y}" stroke="{INK}" stroke-width="1.5"/>')
b.append(rombo(pro_x + EW / 2, 290, "PERTENECE", "N:1", w=140))
b.append(card(pro_x + EW / 2 + 12, CY + EH / 2 + 22, "(0,n)", "start"))
b.append(card(pro_x + EW / 2 + 12, cat_y - 10, "(0,1)", "start"))
b.append(entidad(pro_x, cat_y, "CATEGORÍA"))
b.append(atributos(pro_x + EW + 70, cat_y + EH / 2, [], arriba=False))
for i, nom in enumerate(["id", "nombre"]):
    x0, y = pro_x + EW, cat_y + 14 + i * 22
    b.append(f'<line x1="{x0}" y1="{y}" x2="{x0+34}" y2="{y}" stroke="{INK}" stroke-width="1.2"/>')
    b.append(f'<circle cx="{x0+40}" cy="{y}" r="6" fill="{INK if i == 0 else WHITE}" stroke="{INK}" stroke-width="1.4"/>')
    b.append(text(x0 + 52, y + 4, nom, 12, INK, "start", 700 if i == 0 else 400, mono=True))
# leyenda
b.append(rect(30, 330, 640, 140, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(f'<circle cx="52" cy="356" r="6" fill="{INK}" stroke="{INK}"/>')
b.append(text(66, 360, "identificador (clave)", 12.5, INK, "start"))
b.append(f'<circle cx="252" cy="356" r="6" fill="{WHITE}" stroke="{INK}" stroke-width="1.4"/>')
b.append(text(266, 360, "atributo", 12.5, INK, "start"))
b.append(text(380, 360, "(mín,máx) en rojo: participación", 12.5, ROSE, "start", 700))
b.append(lines(46, 392, ["Se lee de una entidad a la otra pasando por la relación:",
                         "un cliente realiza (0,n) pedidos; un pedido lo realiza (1,1) cliente.",
                         "Un pedido contiene (1,n) productos; un producto está en (0,n) pedidos.",
                         "Una relación N:M puede tener atributos propios: cantidad y precio_unitario."], 12.5, gap=19, anchor="start"))
open(OUT + "fig-2-5-der.svg", "w").write(svg(1080, 490, "".join(b), "Diagrama entidad-relación de la tienda"))

# ---------- Figura 2.6: modelo relacional ----------
b = []
RH = 24

def tabla(x, y, w, nombre, columnas):
    """columnas: (marca, nombre, tipo). Devuelve (svg, función y_de(fila))."""
    h = 34 + RH * len(columnas) + 6
    out = [rect(x, y, w, h, WHITE, INDIGO, rx=6, sw=1.5),
           f'<path d="M{x},{y+6} a6,6 0 0 1 6,-6 h{w-12} a6,6 0 0 1 6,6 v28 h{-w} z" fill="{INDIGO_T}" stroke="{INDIGO}" stroke-width="1.5"/>',
           text(x + w / 2, y + 23, nombre, 14, INK, "middle", 700, mono=True)]
    for i, (marca, col, tipo) in enumerate(columnas):
        yy = y + 34 + i * RH + 17
        if marca:
            colores = {"PK": (AMBER_T, AMBER), "FK": (TEAL_T, TEAL), "PK FK": (AMBER_T, AMBER)}
            f, s = colores[marca]
            out.append(rect(x + 6, yy - 13, 38, 18, f, s, rx=3, sw=1))
            out.append(text(x + 25, yy, "PK" if marca == "PK FK" else marca, 10.5, s, "middle", 700))
            if marca == "PK FK":
                out.append(rect(x + 46, yy - 13, 26, 18, TEAL_T, TEAL, rx=3, sw=1))
                out.append(text(x + 59, yy, "FK", 10.5, TEAL, "middle", 700))
        out.append(text(x + 78, yy, col, 12.5, INK, "start", 700 if marca and "PK" in marca else 400, mono=True))
        out.append(text(x + w - 8, yy, tipo, 11.5, MUTED, "end", mono=True))
    return "".join(out), (lambda fila: y + 34 + fila * RH + 12), h

T = {}
s, f, h = tabla(20, 40, 270, "cliente", [("PK", "id", "INT AUTO_INC"), ("", "nombre", "VARCHAR(100)"), ("", "email", "VARCHAR(100) UQ"), ("", "fecha_alta", "DATE")])
b.append(s); T["cliente"] = (20, 270, f)
s, f, h = tabla(330, 40, 260, "pedido", [("PK", "numero", "INT AUTO_INC"), ("FK", "cliente_id", "INT"), ("", "fecha", "DATE"), ("", "estado", "VARCHAR(10) CHK")])
b.append(s); T["pedido"] = (330, 260, f)
s, f, h = tabla(630, 40, 300, "linea_pedido", [("PK FK", "pedido_numero", "INT"), ("PK FK", "producto_codigo", "VARCHAR(10)"), ("", "cantidad", "INT CHK"), ("", "precio_unitario", "DECIMAL(10,2)")])
b.append(s); T["linea"] = (630, 300, f)
s, f, h = tabla(970, 40, 280, "producto", [("PK", "codigo", "VARCHAR(10)"), ("", "nombre", "VARCHAR(100)"), ("", "precio", "DECIMAL(10,2) CHK"), ("", "stock", "INT CHK"), ("FK", "categoria_id", "INT NULL")])
b.append(s); T["producto"] = (970, 280, f)
s, f, h = tabla(970, 290, 280, "categoria", [("PK", "id", "INT AUTO_INC"), ("", "nombre", "VARCHAR(50) UQ")])
b.append(s); T["categoria"] = (970, 280, f)

def fila_y(t, i):
    return T[t][2](i)

# pedido.cliente_id -> cliente.id
b.append(path([(330, fila_y("pedido", 1)), (310, fila_y("pedido", 1)), (310, fila_y("cliente", 0)), (290, fila_y("cliente", 0))], "teal"))
# linea.pedido_numero -> pedido.numero
b.append(path([(630, fila_y("linea", 0)), (590, fila_y("pedido", 0))], "teal"))
# linea.producto_codigo -> producto.codigo
b.append(path([(930, fila_y("linea", 1)), (950, fila_y("linea", 1)), (950, fila_y("producto", 0)), (970, fila_y("producto", 0))], "teal"))
# producto.categoria_id -> categoria.id
b.append(path([(1250, fila_y("producto", 4)), (1272, fila_y("producto", 4)), (1272, fila_y("categoria", 0)), (1250, fila_y("categoria", 0))], "teal"))
# leyenda
b.append(rect(20, 230, 910, 148, NEUTRAL_T, LINE, rx=8, sw=1))
leg = [("PK", AMBER_T, AMBER, "clave primaria: identifica cada fila; no se repite ni es NULL"),
       ("FK", TEAL_T, TEAL, "clave ajena: su valor debe existir como clave primaria en la tabla a la que apunta la flecha")]
for i, (m, fl, st, t) in enumerate(leg):
    yy = 258 + i * 26
    b.append(rect(36, yy - 13, 30, 18, fl, st, rx=3, sw=1))
    b.append(text(51, yy, m, 10.5, st, "middle", 700))
    b.append(text(78, yy, t, 12.5, INK, "start"))
b.append(text(36, 314, "UQ: valor único (UNIQUE)  ·  CHK: restricción CHECK  ·  AUTO_INC: el gestor genera el valor", 12.5, INK, "start"))
b.append(text(36, 340, "linea_pedido resuelve la relación N:M: su clave primaria está formada por sus dos claves ajenas.", 12.5, INK, "start", italic=True))
b.append(text(36, 362, "Su clave ajena hacia pedido lleva ON DELETE CASCADE: al borrar un pedido se borran sus líneas.", 12.5, INK, "start", italic=True))
open(OUT + "fig-2-6-modelo-relacional.svg", "w").write(svg(1290, 395, "".join(b), "Modelo relacional de la tienda: tablas, claves primarias y claves ajenas"))
print("ok")

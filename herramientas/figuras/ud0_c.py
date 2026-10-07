"""Figuras 0.10 (interfaz e implementaciones), 0.11 (excepciones), 0.12 (modelo de la tienda) y 0.13 (capas).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud0_c.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud0" / "img") + "/"

# ---------- Figura 0.10: una interfaz, muchas implementaciones ----------
b = []
svc, hs = uml_class(390, 20, 220, "ProductoService", [], [], stroke=INK, size=12)
b.append(svc)
itf, hi = uml_class(305, 120, 390, "ProductoRepository",
                    [], ["+ guardar(p: Producto): void", "+ buscarPorCodigo(c: String): Optional<Producto>",
                         "+ buscarTodos(): List<Producto>", "+ borrar(c: String): boolean"],
                    stereo="«interface»", head_fill=TEAL_T, stroke=TEAL, size=12, italic=True)
b.append(itf)
b.append(path([(500, 20 + hs), (500, 116)], "ink", marker_end="o", dash=True))
b.append(text(510, 20 + hs + 22, "usa", 12, MUTED, "start", italic=True))
impls = [("Memoria", "UD0", "colección en memoria", False),
         ("Fichero", "UD1", "JSON, CSV, XML…", True),
         ("Jdbc", "UD2", "MariaDB · JDBC", True),
         ("Jpa", "UD3", "Hibernate / JPA", True),
         ("ObjectDb", "UD4", "BD orientada a objetos", True),
         ("Mongo", "UD5", "MongoDB", True)]
top = 120 + hi
by = top + 70
W, G, X0 = 150, 14, 23
bus = top + 32
for i, (suf, ud, sto, fut) in enumerate(impls):
    x = X0 + i * (W + G)
    b.append(rect(x, by, W, 74, TEAL_T if not fut else WHITE, TEAL if not fut else LINE, rx=4, dash=fut))
    b.append(text(x + W / 2, by + 20, "ProductoRepository", 10.5, MUTED, "middle"))
    b.append(text(x + W / 2, by + 39, suf, 14, INK, "middle", 700))
    b.append(text(x + W / 2, by + 60, sto, 11.5, MUTED, "middle"))
    b.append(pill(x + W / 2 - 22, by + 84, 44, 22, ud, fill=WHITE, stroke=TEAL if not fut else LINE, size=11.5, weight=700, mono=False,
                  color=TEAL if not fut else MUTED))
    b.append(path([(x + W / 2, by), (x + W / 2, bus)], "ink", marker_end=None, dash=True))
b.append(path([(X0 + W / 2, bus), (X0 + 5 * (W + G) + W / 2, bus)], "ink", marker_end=None, dash=True))
b.append(path([(500, bus), (500, top + 3)], "ink", marker_end="t", dash=True))
b.append(text(500, by + 130, "UD6: Spring Data genera la implementación a partir de la interfaz", 12.5, TEAL, "middle", italic=True))
open(OUT + "fig-0-10-interfaz-implementaciones.svg", "w").write(svg(1000, by + 145, "".join(b), "Una interfaz de repositorio con una implementación por unidad"))

# ---------- Figura 0.11: jerarquía de excepciones ----------
b = []
def node(x, y, w, name, kind, note=None):
    fill, stroke = {"top": (WHITE, INK), "err": (NEUTRAL_T, LINE), "chk": (AMBER_T, AMBER), "unc": (INDIGO_T, INDIGO), "own": (TEAL_T, TEAL)}[kind]
    h = 34 if not note else 48
    s = rect(x, y, w, h, fill, stroke, rx=4)
    s += text(x + w / 2, y + 22, name, 12.5, INK, "middle", 600, mono=True)
    if note:
        s += text(x + w / 2, y + 39, note, 11, MUTED, "middle")
    return s, (x, y, w, h)
G = {}
def add(k, *a, **kw):
    s, g = node(*a, **kw); b.append(s); G[k] = g
def top_(k): x, y, w, h = G[k]; return (x + w / 2, y)
def bot(k): x, y, w, h = G[k]; return (x + w / 2, y + h)
def tree(parent, children, ybus):
    px, py = bot(parent)
    b.append(path([(px, ybus), (px, py + 1)], "ink", marker_end="t"))
    xs = [top_(c)[0] for c in children]
    b.append(path([(min(xs + [px]), ybus), (max(xs + [px]), ybus)], "ink", marker_end=None))
    for c in children:
        cx, cy = top_(c)
        b.append(path([(cx, ybus), (cx, cy)], "ink", marker_end=None))
add("thr", 400, 20, 180, "Throwable", "top")
add("err", 90, 110, 160, "Error", "err", "no se capturan")
add("exc", 535, 110, 230, "Exception", "chk", "comprobadas (salvo RuntimeException)")
tree("thr", ["err", "exc"], 80)
add("oom", 20, 205, 175, "OutOfMemoryError", "err")
add("soe", 205, 205, 185, "StackOverflowError", "err")
tree("err", ["oom", "soe"], 185)
add("ioe", 420, 210, 135, "IOException", "chk", "UD1")
add("sql", 575, 210, 135, "SQLException", "chk", "UD2")
add("rte", 760, 210, 190, "RuntimeException", "unc", "no comprobadas")
tree("exc", ["ioe", "sql", "rte"], 185)
add("fnf", 392.5, 300, 190, "FileNotFoundException", "chk")
tree("ioe", ["fnf"], 282)
subs = [("NullPointerException", "unc"), ("IllegalArgumentException", "unc"), ("IllegalStateException", "unc"),
        ("ArithmeticException", "unc"), ("IndexOutOfBoundsException", "unc"), ("ProductoNoEncontradoException", "own")]
sx = 700
spine = sx + 10
yb = bot("rte")[1]
b.append(path([(855, yb + 22), (855, yb + 1)], "ink", marker_end="t"))
b.append(path([(spine, yb + 22), (855, yb + 22)], "ink", marker_end=None))
last = 0
for i, (n, k) in enumerate(subs):
    y = yb + 40 + i * 42
    add("s%d" % i, spine + 22, y, 255, n, k)
    b.append(path([(spine, y + 17), (spine + 22, y + 17)], "ink", marker_end=None))
    last = y + 17
b.append(path([(spine, yb + 22), (spine, last)], "ink", marker_end=None))
# leyenda
lg = [("chk", "comprobada: el compilador obliga a capturarla o declararla con throws"),
      ("unc", "no comprobada: suele indicar un error de programación"),
      ("err", "error grave de la JVM: no se trata"),
      ("own", "excepción propia del proyecto")]
fills = {"chk": (AMBER_T, AMBER), "unc": (INDIGO_T, INDIGO), "err": (NEUTRAL_T, LINE), "own": (TEAL_T, TEAL)}
for i, (k, t) in enumerate(lg):
    y = 395 + i * 26
    f, s = fills[k]
    b.append(rect(30, y, 26, 18, f, s, rx=3))
    b.append(text(66, y + 14, t, 12.5, INK, "start"))
open(OUT + "fig-0-11-excepciones.svg", "w").write(svg(1000, last + 40, "".join(b), "Jerarquía de excepciones de Java"))

# ---------- Figura 0.12: modelo de clases de la tienda ----------
b = []
est, he = uml_class(30, 60, 220, "EstadoPedido", ["PENDIENTE", "PAGADO", "ENVIADO", "ENTREGADO", "CANCELADO"],
                    stereo="«enumeration»", head_fill=NEUTRAL_T, size=12)
cli, hc = uml_class(340, 60, 250, "Cliente", ["- id: int", "- nombre: String", "- email: String", "- fechaAlta: LocalDate"],
                    head_fill=TEAL_T, stroke=TEAL, size=12)
ped, hp = uml_class(680, 60, 260, "Pedido", ["- numero: int", "- fecha: LocalDate", "- estado: EstadoPedido"], ["+ total(): BigDecimal"],
                    head_fill=TEAL_T, stroke=TEAL, size=12)
cat, hct = uml_class(30, 330, 220, "Categoria", ["- id: int", "- nombre: String"], head_fill=TEAL_T, stroke=TEAL, size=12)
pro, hpr = uml_class(340, 330, 250, "Producto", ["- codigo: String", "- nombre: String", "- precio: BigDecimal", "- stock: int"],
                     head_fill=TEAL_T, stroke=TEAL, size=12)
lin, hl = uml_class(680, 330, 260, "LineaPedido", ["- cantidad: int", "- precioUnitario: BigDecimal"], ["+ importe(): BigDecimal"],
                    head_fill=TEAL_T, stroke=TEAL, size=12)
for s in (est, cli, ped, cat, pro, lin):
    b.append(s)
# Cliente 1 —— * Pedido
y = 60 + 45
b.append(path([(680, y), (590, y)], "ink", marker_end="o"))
b.append(text(600, y - 8, "1", 13, INK, "start", 700)); b.append(text(670, y - 8, "*", 13, INK, "end", 700))
b.append(text(635, y + 18, "realiza", 12, MUTED, "middle", italic=True))
# Pedido ◆ 1 —— 1..* LineaPedido
x = 905
b.append(path([(x, 60 + hp), (x, 330)], "ink", marker_end=None, marker_start="d"))
b.append(text(x + 8, 60 + hp + 26, "1", 13, INK, "start", 700)); b.append(text(x + 8, 322, "1..*", 13, INK, "start", 700))
b.append(text(x - 10, (60 + hp + 330) / 2 + 4, "lineas", 12, MUTED, "end", italic=True))
# LineaPedido * —— 1 Producto
y = 330 + 45
b.append(path([(680, y), (590, y)], "ink", marker_end="o"))
b.append(text(600, y - 8, "1", 13, INK, "start", 700)); b.append(text(670, y - 8, "*", 13, INK, "end", 700))
b.append(text(635, y + 18, "producto", 12, MUTED, "middle", italic=True))
# Producto * —— 1 Categoria
b.append(path([(340, y), (250, y)], "ink", marker_end="o"))
b.append(text(260, y - 8, "1", 13, INK, "start", 700)); b.append(text(330, y - 8, "*", 13, INK, "end", 700))
b.append(text(295, y + 18, "categoria", 12, MUTED, "middle", italic=True))
# Pedido - - > EstadoPedido (por encima)
b.append(path([(760, 60), (760, 30), (140, 30), (140, 56)], "muted", marker_end="o", dash=True))
b.append(text(450, 24, "el atributo estado toma uno de estos valores", 12, MUTED, "middle", italic=True))
# nota N:M
ny = 330 + max(hpr, hl) + 30
b.append(rect(30, ny, 910, 46, AMBER_T, AMBER, rx=6, sw=1))
b.append(text(45, ny + 19, "Pedido y Producto mantienen una relación N:M: un pedido incluye muchos productos", 12.5, INK, "start"))
b.append(text(45, ny + 37, "y un producto aparece en muchos pedidos. LineaPedido la resuelve y guarda cantidad y precio.", 12.5, INK, "start"))
open(OUT + "fig-0-12-modelo-tienda.svg", "w").write(svg(970, ny + 66, "".join(b), "Diagrama de clases del ejemplo de la tienda"))

# ---------- Figura 0.13: arquitectura en capas ----------
b = []
L = [("Presentación", 20, 95), ("Servicio", 135, 80), ("Acceso a datos", 235, 150), ("Almacenamiento", 405, 95)]
for name, y, h in L:
    b.append(rect(20, y, 760, h, NEUTRAL_T, LINE, rx=10, sw=1))
    b.append(text(34, y + h / 2 + 5, name, 13, MUTED, "start", 700))
# presentación
b.append(box(170, 42, 250, 56, "MenuProductos + Consola", "UD0 – UD5: menú de texto", stroke=TEAL, fill=WHITE))
b.append(box(460, 42, 280, 56, "ProductoController", "UD6: API REST con Spring Boot", stroke=LINE, dash=True))
# servicio
b.append(box(300, 150, 280, 52, "ProductoService", "reglas de negocio", stroke=TEAL, fill=WHITE))
b.append(path([(295, 98), (295, 120), (440, 120), (440, 146)], "teal"))
b.append(path([(600, 98), (600, 120), (440, 120)], "muted", marker_end=None, dash=True))
# acceso a datos
b.append(box(300, 252, 280, 46, "«interface» ProductoRepository", None, stroke=TEAL, fill=TEAL_T, tsize=13.5))
b.append(path([(440, 202), (440, 248)], "teal"))
names = ["…Memoria", "…Fichero", "…Jdbc", "…Jpa", "…ObjectDb", "…Mongo"]
W, G0, X0 = 94, 9, 166
for i, n in enumerate(names):
    x = X0 + i * (W + G0)
    b.append(box(x, 330, W, 38, n, None, stroke=TEAL if i == 0 else LINE, fill=WHITE, dash=i > 0, tsize=12.5))
    b.append(path([(x + W / 2, 330), (x + W / 2, 314)], "ink", marker_end=None, dash=True))
b.append(path([(X0 + W / 2, 314), (X0 + 5 * (W + G0) + W / 2, 314)], "ink", marker_end=None, dash=True))
b.append(path([(440, 314), (440, 301)], "ink", marker_end="t", dash=True))
# almacenamiento
st = [("memoria", None, False), ("ficheros", ["JSON, CSV…"], True), ("MariaDB", None, True), ("MariaDB o", ["PostgreSQL"], True), ("ObjectDB", None, True), ("MongoDB", None, True)]
for i, (n, sub, fut) in enumerate(st):
    x = X0 + i * (W + G0)
    b.append(cylinder(x + 4, 430, W - 8, 56, n, sub,
                      fill=INDIGO_T if not fut else WHITE, stroke=INDIGO if not fut else LINE, tsize=11.5, ssize=11, dash=fut))
    b.append(path([(x + W / 2, 368), (x + W / 2, 426)], "indigo" if not fut else "line", dash=fut))
# modelo y App
b.append(rect(800, 20, 170, 480, TEAL_T, TEAL, rx=10, sw=1.2))
b.append(text(885, 46, "Modelo", 14, TEAL, "middle", 700))
b.append(lines(885, 72, ["Producto", "Categoria", "Cliente", "Pedido", "LineaPedido", "EstadoPedido"], 12.5, gap=21, mono=True))
b.append(lines(885, 222, ["lo usan todas", "las capas"], 12, gap=16, fill=MUTED, italic=True))
b.append(rect(815, 300, 140, 120, WHITE, INK, rx=8))
b.append(text(885, 324, "App", 14, INK, "middle", 700, mono=True))
b.append(lines(885, 348, ["crea las piezas", "y las conecta;", "único sitio que", "elige la", "implementación"], 11.5, gap=15, fill=MUTED))
b.append(text(400, 520, "Cada capa solo habla con la de debajo, y a través de interfaces.", 12.5, INK, "middle", italic=True))
open(OUT + "fig-0-13-capas.svg", "w").write(svg(990, 535, "".join(b), "Arquitectura en capas del proyecto integrador"))
print("ok")

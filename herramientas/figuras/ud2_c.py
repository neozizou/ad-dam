"""Figuras 2.7 (cursor de ResultSet), 2.8 (inyección SQL), 2.9 (lotes), 2.10 (transacción),
2.11 (cierre de recursos) y 2.12 (componente JDBC).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud2_c.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
from xml.sax.saxutils import escape
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud2" / "img") + "/"

# ---------- Figura 2.7: el cursor de un ResultSet ----------
b = []
cols = [("codigo", 90), ("nombre", 190), ("precio", 90), ("stock", 70)]
filas = [("CAB01", "Cable USB-C 2 m", "8.95", "0"), ("MON01", "Monitor 27 pulgadas", "219.00", "4"),
         ("RAT01", "Ratón inalámbrico", "24.50", "29"), ("TEC01", "Teclado mecánico", "59.90", "10")]
X0, Y0, RH = 210, 60, 34
x = X0
for c, w in cols:
    b.append(rect(x, Y0, w, RH, INDIGO_T, INDIGO, rx=0, sw=1.2))
    b.append(text(x + w / 2, Y0 + 22, c, 12.5, INK, "middle", 700, mono=True))
    x += w
for i, f in enumerate(filas):
    x = X0
    y = Y0 + RH * (i + 1) + 12
    for (c, w), v in zip(cols, f):
        hl = i == 1
        b.append(rect(x, y, w, RH, TEAL_T if hl else WHITE, TEAL if hl else LINE, rx=0, sw=1.2 if hl else 1))
        b.append(text(x + 8, y + 22, v, 12.5, INK, "start", 600 if hl else 400, mono=True))
        x += w
b.append(text(X0, 40, "SELECT codigo, nombre, precio, stock FROM producto ORDER BY codigo", 12.5, MUTED, "start", mono=True))
# posiciones del cursor
pos = [("antes de la primera fila", Y0 + RH + 6, "al ejecutar la consulta"), ("fila actual", Y0 + RH * 2 + 12 + RH / 2, "tras el segundo next()"),
       ("después de la última", Y0 + RH * 5 + 22, "next() devuelve false")]
for i, (t, y, sub) in enumerate(pos):
    col = "teal" if i == 1 else "muted"
    b.append(path([(170, y), (204, y)], col))
    b.append(text(162, y - 2, t, 12, COLORS[col], "end", 700 if i == 1 else 400))
    b.append(text(162, y + 13, sub, 11, MUTED, "end", italic=True))
# código
b.append(rect(700, 60, 330, 190, NEUTRAL_T, LINE, rx=8, sw=1))
code = ["while (filas.next()) {", "    String c = filas.getString(\"codigo\");", "    BigDecimal p =", "        filas.getBigDecimal(\"precio\");", "    int s = filas.getInt(4);", "}"]
b.append(lines(714, 88, code, 12, gap=21, anchor="start", mono=True))
b.append(lines(714, 222, ["Los get leen columnas de la fila actual,", "por nombre o por posición (desde 1)."], 11.5, gap=15, fill=MUTED, anchor="start", italic=True))
open(OUT + "fig-2-7-resultset.svg", "w").write(svg(1050, 270, "".join(b), "Un ResultSet es un cursor que avanza fila a fila con next()"))

# ---------- Figura 2.8: inyección SQL ----------
b = []
M = 7.2    # anchura de un carácter monoespaciado a 12 px; textLength la impone en cualquier fuente
def trozos(x, y, partes, size=12):
    out = []
    for t, tipo in partes:
        w = len(t) * M
        if tipo == "ataque":
            out.append(rect(x - 1, y - 14, w + 2, 20, ROSE_T, ROSE, rx=2, sw=1))
        elif tipo == "valor":
            out.append(rect(x - 1, y - 14, w + 2, 20, TEAL_T, TEAL, rx=2, sw=1))
        peso = 600 if tipo else 400
        out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{INK}" font-weight="{peso}" '
                   f'font-family="{MONO}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" '
                   f'xml:space="preserve">{escape(t)}</text>')
        x += w + 3
    return "".join(out)
b.append(rect(20, 20, 1000, 200, ROSE_T, ROSE, rx=10, sw=1.2, opacity=0.35))
b.append(text(36, 46, "Concatenando texto: lo que escribe el usuario pasa a formar parte de la sentencia", 14, ROSE, "start", 700))
b.append(text(36, 76, "Código:", 12.5, MUTED, "start", 700))
b.append(trozos(120, 76, [("\"SELECT … FROM producto WHERE codigo = '\" + ", None), ("codigo", "ataque"), (" + \"'\"", None)]))
b.append(text(36, 108, "Usuario:", 12.5, MUTED, "start", 700))
b.append(trozos(120, 108, [("x' UNION SELECT email, nombre, 0, 0 FROM cliente -- ", "ataque")]))
b.append(text(36, 140, "Se envía:", 12.5, MUTED, "start", 700))
b.append(trozos(120, 140, [("SELECT codigo, nombre, precio, stock FROM producto WHERE codigo = '", None),
                            ("x' UNION SELECT email, nombre, 0, 0 FROM cliente -- ", "ataque"), ("'", None)]))
b.append(lines(120, 172, ["La comilla del usuario cierra el texto y el resto se convierte en SQL: la consulta devuelve",
                          "los correos de todos los clientes. El -- final convierte en comentario la comilla que sobraba."], 12.5, gap=19, anchor="start"))
b.append(rect(20, 240, 1000, 190, TEAL_T, TEAL, rx=10, sw=1.2, opacity=0.35))
b.append(text(36, 266, "Con PreparedStatement: la sentencia y los valores viajan por separado", 14, TEAL, "start", 700))
b.append(pill(36, 284, 26, 26, "1", fill=WHITE, stroke=TEAL, size=12.5, mono=False, weight=700))
b.append(text(74, 302, "prepareStatement: el gestor recibe y analiza la sentencia, con un hueco ? para cada valor", 12.5, INK, "start"))
b.append(trozos(120, 330, [("SELECT codigo, nombre, precio, stock FROM producto WHERE codigo = ", None), ("?", "valor")]))
b.append(pill(36, 348, 26, 26, "2", fill=WHITE, stroke=TEAL, size=12.5, mono=False, weight=700))
b.append(text(74, 366, "setString(1, …): el valor llega después y solo puede ocupar el hueco, como dato", 12.5, INK, "start"))
b.append(trozos(120, 394, [("?", "valor"), ("  =  ", None), ("\"x' UNION SELECT email, nombre, 0, 0 FROM cliente -- \"", "valor")]))
b.append(text(120, 418, "Se busca un producto cuyo código sea literalmente ese texto: 0 filas.", 12.5, INK, "start", italic=True))
open(OUT + "fig-2-8-inyeccion.svg", "w").write(svg(1040, 448, "".join(b), "Inyección SQL al concatenar texto y cómo la evita PreparedStatement"))

# ---------- Figura 2.9: envíos y confirmaciones en una carga masiva ----------
b = []
b.append(text(30, 30, "Insertar 5.000 filas: cuántas veces se va al servidor y cuántas se confirma", 14, INK, "start", 700))
lanes = [("Una a una, con autocommit", "5.000 envíos  ·  5.000 confirmaciones", 879, ROSE, ROSE_T, 14, True),
         ("Una a una, en una transacción", "5.000 envíos  ·  1 confirmación", 279, AMBER, AMBER_T, 14, False),
         ("En lote, en una transacción", "10 envíos de 500  ·  1 confirmación", 221, TEAL, TEAL_T, 3, False)]
for i, (t, sub, ms, col, fill, n, commit_each) in enumerate(lanes):
    y = 62 + i * 92
    b.append(text(30, y + 18, t, 13, INK, "start", 700))
    b.append(text(30, y + 38, sub, 12, MUTED, "start"))
    x = 300
    for k in range(n):
        w = 22 if n > 5 else 110
        b.append(rect(x, y + 6, w, 30, fill, col, rx=3, sw=1))
        if n <= 5:
            b.append(text(x + w / 2, y + 26, "500 INSERT", 11, INK, "middle"))
        x += w + 4
        if commit_each:
            b.append(rect(x, y + 6, 8, 30, col, col, rx=1, sw=1))
            x += 12
    b.append(text(x + 6, y + 26, "…", 14, MUTED, "start"))
    x += 26
    if not commit_each:
        b.append(rect(x, y + 6, 8, 30, col, col, rx=1, sw=1))
        x += 14
    b.append(text(x + 8, y + 26, f"{ms} ms", 13, col, "start", 700))
b.append(rect(300, 336, 22, 18, ROSE_T, ROSE, rx=3, sw=1))
b.append(text(330, 350, "envío al servidor", 12, INK, "start"))
b.append(rect(470, 336, 8, 18, ROSE, ROSE, rx=1, sw=1))
b.append(text(486, 350, "confirmación (commit: escribir en disco)", 12, INK, "start"))
b.append(text(30, 384, "Tiempos medidos con CargaMasiva y el servidor en el mismo equipo. Por la red, cada envío cuesta mucho más.", 12, MUTED, "start", italic=True))
open(OUT + "fig-2-9-lotes.svg", "w").write(svg(1000, 400, "".join(b), "Envíos al servidor y confirmaciones al insertar 5.000 filas de tres formas"))

# ---------- Figura 2.10: la transacción de un pedido ----------
b = []
b.append(text(30, 30, "PedidoRepositoryJdbc.guardar: RAT01 × 1 y MON01 × 5 (solo hay 4 monitores)", 14, INK, "start", 700))
steps = [("setAutoCommit(false)", "empieza la transacción", INK, NEUTRAL_T),
         ("INSERT pedido", "el gestor asigna el nº 2", TEAL, TEAL_T),
         ("INSERT líneas", "en un lote", TEAL, TEAL_T),
         ("UPDATE RAT01", "1 fila: stock 29 → 28", TEAL, TEAL_T),
         ("UPDATE MON01", "0 filas: no hay 5", ROSE, ROSE_T)]
x = 30
for i, (t, sub, s, f) in enumerate(steps):
    w = 176
    b.append(box(x, 50, w, 58, t, [sub], fill=f, stroke=s, tmono=True, tsize=12.5, ssize=11.5))
    if i:
        b.append(path([(x - 18, 79), (x - 2, 79)], "ink"))
    x += w + 18
# dos salidas desde el último paso
b.append(path([(850, 108), (850, 124), (640, 124), (640, 150)], "teal", dash=True))
b.append(text(745, 118, "si todas afectan a 1 fila", 11.5, TEAL, "middle", italic=True, halo=True))
b.append(box(520, 154, 240, 56, "commit()", ["se confirman todos los cambios"], fill=WHITE, stroke=TEAL, tmono=True, dash=True))
b.append(path([(930, 108), (930, 150)], "rose"))
b.append(box(810, 154, 210, 56, "rollback()", ["se deshace todo lo anterior"], fill=ROSE_T, stroke=ROSE, tmono=True))
b.append(text(915, 228, "lanza StockInsuficienteException", 11, ROSE, "middle", mono=True))
# estado
b.append(text(30, 258, "Estado de la base de datos", 13.5, INK, "start", 700))
heads = ["", "Antes", "Dentro de la transacción", "Después del rollback"]
rows = [("stock de RAT01", "29", "28", "29"), ("filas en pedido", "1", "2", "1"), ("siguiente AUTO_INCREMENT", "2", "3", "3")]
cw = [240, 150, 240, 230]
y = 268
x = 30
for h, w in zip(heads, cw):
    b.append(rect(x, y, w, 30, INDIGO_T if h else WHITE, INDIGO if h else WHITE, rx=0, sw=1))
    b.append(text(x + w / 2, y + 20, h, 12.5, INK, "middle", 700))
    x += w
for r, row in enumerate(rows):
    x = 30
    y2 = y + 30 + r * 30
    for c, (v, w) in enumerate(zip(row, cw)):
        destacado = r == 2 and c == 3
        b.append(rect(x, y2, w, 30, AMBER_T if destacado else WHITE, AMBER if destacado else LINE, rx=0, sw=1))
        b.append(text(x + (12 if c == 0 else w / 2), y2 + 20, v, 12.5, INK, "start" if c == 0 else "middle", 700 if destacado else 400, mono=c > 0))
        x += w
b.append(text(30, 412, "Los demás programas no ven los cambios de dentro hasta el commit. El contador AUTO_INCREMENT no retrocede: el nº 2 queda sin usar.", 12, MUTED, "start", italic=True))
open(OUT + "fig-2-10-transaccion.svg", "w").write(svg(1050, 430, "".join(b), "Pasos de la transacción que guarda un pedido y estado de la base de datos antes, durante y después del rollback"))

# ---------- Figura 2.11: recursos anidados y pool agotado ----------
b = []
b.append(text(30, 30, "try-with-resources: se abren de fuera adentro y se cierran al revés", 14, INK, "start", 700))
b.append(rect(30, 46, 440, 210, INDIGO_T, INDIGO, rx=10, sw=1.4))
b.append(text(46, 70, "Connection", 13, INDIGO, "start", 700, mono=True))
b.append(text(454, 70, "abre 1.º · cierra 3.º", 11.5, INDIGO, "end"))
b.append(rect(54, 84, 392, 152, TEAL_T, TEAL, rx=10, sw=1.4))
b.append(text(70, 108, "PreparedStatement", 13, TEAL, "start", 700, mono=True))
b.append(text(430, 108, "abre 2.º · cierra 2.º", 11.5, TEAL, "end"))
b.append(rect(78, 122, 344, 96, WHITE, AMBER, rx=10, sw=1.4))
b.append(text(94, 146, "ResultSet", 13, AMBER, "start", 700, mono=True))
b.append(text(406, 146, "abre 3.º · cierra 1.º", 11.5, AMBER, "end"))
b.append(lines(94, 172, ["Cerrar un objeto cierra también", "los que contiene."], 12, gap=17, fill=MUTED, anchor="start", italic=True))
b.append(text(30, 286, "Cerrar la conexión de un pool la devuelve; olvidarla la deja ocupada para siempre.", 12.5, INK, "start"))
# pool agotado
X = 540
b.append(text(X, 30, "Conexiones olvidadas (AgotarPool, pool de 3)", 14, INK, "start", 700))
b.append(rect(X, 46, 300, 120, INDIGO_T, INDIGO, rx=10, sw=1.4))
for i in range(3):
    b.append(rect(X + 20 + i * 92, 70, 80, 50, ROSE_T, ROSE, rx=6, sw=1.3))
    b.append(text(X + 60 + i * 92, 92, f"conexión {i+1}", 11.5, INK, "middle", 600))
    b.append(text(X + 60 + i * 92, 108, "sin cerrar", 11, ROSE, "middle"))
b.append(text(X + 150, 150, "el pool no tiene ninguna libre", 12, MUTED, "middle", italic=True))
b.append(box(X + 330, 66, 160, 60, "4.ª petición", ["espera…"], stroke=ROSE, fill=WHITE))
b.append(path([(X + 330, 96), (X + 304, 96)], "rose"))
b.append(rect(X, 188, 490, 70, ROSE_T, ROSE, rx=8, sw=1))
b.append(text(X + 14, 212, "Pasados 2 s (connectionTimeout):", 12.5, INK, "start", 700))
b.append(text(X + 14, 236, "SQLTransientConnectionException: HikariPool-1 -", 12, INK, "start", mono=True))
b.append(text(X + 14, 252, "Connection is not available, request timed out after 2000ms", 12, INK, "start", mono=True))
open(OUT + "fig-2-11-recursos.svg", "w").write(svg(1050, 300, "".join(b), "Orden de apertura y cierre de los objetos JDBC y efecto de no cerrar las conexiones de un pool"))

# ---------- Figura 2.12: el componente de acceso con JDBC ----------
b = []
ps, h1 = uml_class(260, 20, 230, "ProductoService", [], [], size=12)
ds, h2 = uml_class(560, 20, 230, "PedidoService", [], [], size=12)
b += [ps, ds]
pr, h3 = uml_class(220, 120, 290, "ProductoRepository", [], ["+ guardar(p)", "+ buscarPorCodigo(c)", "+ buscarTodos()", "+ borrar(c)"],
                   stereo="«interface»", head_fill=TEAL_T, stroke=TEAL, italic=True, size=12)
pe, h4 = uml_class(560, 120, 300, "PedidoRepository", [], ["+ guardar(pedido): int", "+ buscarPorNumero(n)", "+ ventasPorCategoria()"],
                   stereo="«interface»", head_fill=TEAL_T, stroke=TEAL, italic=True, size=12)
b += [pr, pe]
b.append(path([(375, 20 + h1), (375, 116)], "ink", marker_end="o", dash=True))
b.append(path([(675, 20 + h2), (675, 116)], "ink", marker_end="o", dash=True))
b.append(path([(600, 20 + h2), (600, 80), (480, 80), (480, 116)], "ink", marker_end="o", dash=True))
pj, h5 = uml_class(220, 340, 290, "ProductoRepositoryJdbc", ["- dataSource: DataSource"], ["- aProducto(fila): Producto"], head_fill=TEAL_T, stroke=TEAL, size=12)
pej, h6 = uml_class(560, 340, 300, "PedidoRepositoryJdbc", ["- dataSource: DataSource"], ["- insertarPedido(…): int", "- insertarLineas(…)", "- descontarStock(…)"], head_fill=TEAL_T, stroke=TEAL, size=12)
b += [pj, pej]
b.append(path([(365, 340), (365, 120 + h3 + 2)], "ink", marker_end="t", dash=True))
b.append(path([(710, 340), (710, 120 + h4 + 2)], "ink", marker_end="t", dash=True))
dsrc, h7 = uml_class(940, 340, 220, "DataSource", [], ["+ getConnection(): Connection"], stereo="«interface» javax.sql", italic=True, size=12, head_fill=INDIGO_T, stroke=INDIGO)
b.append(dsrc)
b.append(path([(860, 372), (936, 372)], "ink", marker_end="o", dash=True))
b.append(path([(470, 340 + h5), (470, 500), (900, 500), (900, 400), (936, 400)], "ink", marker_end="o", dash=True))
hk, h8 = uml_class(940, 530, 220, "HikariDataSource", [], [], stereo="HikariCP", size=12, head_fill=INDIGO_T, stroke=INDIGO)
b.append(hk)
b.append(path([(1050, 530), (1050, 340 + h7 + 2)], "ink", marker_end="t", dash=True))
bd, h9 = uml_class(900, 120, 300, "BaseDatos", ["- pool: HikariDataSource"], ["+ dataSource(): DataSource", "+ ejecutarScript(recurso)", "+ close()"], size=12, head_fill=AMBER_T, stroke=AMBER)
b.append(bd)
b.append(path([(1200, 160), (1230, 160), (1230, 580), (1164, 580)], "ink", marker_end="o"))
b.append(text(1236, 300, "1", 13, INK, "start", 700))
ej, h10 = uml_class(900, 20, 300, "EjecutorScripts", [], [("+ ejecutar(conexión, script): int", {"u": True})], size=12, head_fill=AMBER_T, stroke=AMBER)
b.append(ej)
b.append(path([(1050, 120), (1050, 20 + h10 + 2)], "ink", marker_end="o", dash=True))
exc, h11 = uml_class(220, 560, 290, "AccesoDatosException", [], [], stereo="RuntimeException", size=12, stroke=ROSE, head_fill=ROSE_T)
b.append(exc)
b.append(path([(365, 340 + h5), (365, 556)], "ink", marker_end="o", dash=True))
b.append(text(375, 545, "lanza", 12, MUTED, "start", italic=True))
b.append(path([(640, 340 + h6), (640, 590), (514, 590)], "ink", marker_end="o", dash=True))
b.append(file_icon(30, 120, 150, 56, "schema.sql", ["estructura"], ssize=11))
b.append(file_icon(30, 196, 150, 56, "datos-ejemplo.sql", ["datos iniciales"], tsize=11.5, ssize=11))
b.append(file_icon(30, 272, 150, 56, "procedimientos.sql", ["solo MariaDB"], tsize=11.5, ssize=11))
b.append(text(105, 352, "src/main/resources/sql", 11.5, MUTED, "middle", mono=True))
b.append(text(105, 370, "los ejecuta BaseDatos", 11.5, MUTED, "middle", italic=True))
b.append(text(30, 640, "Flechas discontinuas con punta abierta: «usa». Con triángulo hueco: «implementa». Continua: atributo.", 12, MUTED, "start", italic=True))
open(OUT + "fig-2-12-componente.svg", "w").write(svg(1260, 660, "".join(b), "Diagrama de clases del componente de acceso a datos con JDBC"))
print("ok")

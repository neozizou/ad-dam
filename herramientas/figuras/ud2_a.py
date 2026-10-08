"""Figuras 2.1 (capas de JDBC), 2.2 (gestor embebido y servidor), 2.3 (URL JDBC) y 2.4 (pool de conexiones).

Ejecutar desde cualquier carpeta: python herramientas/figuras/ud2_a.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib import *
OUT = str(Path(__file__).resolve().parents[2] / "docs" / "ud2" / "img") + "/"

# ---------- Figura 2.1: JDBC, una interfaz y un conector por gestor ----------
b = []
b.append(box(300, 20, 340, 62, "Tu aplicación", ["ProductoRepositoryJdbc, PedidoRepositoryJdbc…"], fill=NEUTRAL_T, stroke=INK))
b.append(path([(470, 82), (470, 116)], "ink"))
b.append(text(482, 104, "usa solo interfaces de java.sql", 12, MUTED, "start", italic=True))
b.append(rect(220, 120, 500, 92, TEAL_T, TEAL, rx=10, sw=1.6))
b.append(text(470, 146, "API JDBC  (java.sql y javax.sql, incluida en el JDK)", 14, TEAL, "middle", 700))
apis = ["DataSource", "Connection", "PreparedStatement", "ResultSet", "SQLException"]
x = 236
for a in apis:
    w = tw(a, 12, True) + 18
    b.append(pill(x, 162, w, 28, a, fill=WHITE, stroke=TEAL, size=12))
    x += w + 8
b.append(path([(360, 212), (220, 262)], "teal"))
b.append(path([(580, 212), (720, 262)], "teal"))
b.append(text(470, 246, "las implementa", 12, MUTED, "middle", italic=True))
b.append(box(80, 266, 280, 66, "Conector de MariaDB", ["mariadb-java-client.jar"], fill=WHITE, stroke=AMBER, smono=True))
b.append(box(580, 266, 280, 66, "Conector de H2", ["h2.jar (incluye el propio gestor)"], fill=WHITE, stroke=AMBER))
b.append(path([(220, 332), (220, 386)], "indigo"))
b.append(text(230, 365, "protocolo de MariaDB por la red (puerto 3306)", 12, INDIGO, "start", halo=True))
b.append(cylinder(140, 390, 160, 76, "Servidor MariaDB", ["otro programa"], tsize=13))
b.append(path([(720, 332), (720, 386)], "indigo"))
b.append(text(730, 365, "lectura y escritura directa", 12, INDIGO, "start", halo=True))
b.append(file_icon(650, 392, 140, 70, "tienda.mv.db", ["fichero de H2"]))
b.append(rect(30, 490, 880, 46, AMBER_T, AMBER, rx=8, sw=1))
b.append(text(470, 518, "Cambiar de gestor = cambiar el conector (una dependencia) y la URL. El código que usa java.sql no cambia.", 12.5, INK, "middle"))
open(OUT + "fig-2-1-jdbc.svg", "w").write(svg(940, 552, "".join(b), "Arquitectura de JDBC: la aplicación usa la API JDBC y cada gestor aporta su conector"))

# ---------- Figura 2.2: gestor embebido frente a servidor independiente ----------
b = []
# embebido
b.append(text(30, 32, "Gestor embebido (H2)", 15, TEAL, "start", 700))
b.append(rect(30, 48, 360, 196, TEAL_T, TEAL, rx=12, sw=1.4, dash=True))
b.append(text(46, 72, "Un solo proceso: la JVM de tu programa", 12.5, MUTED, "start", italic=True))
b.append(box(56, 88, 140, 56, "Tu código", None, stroke=INK))
b.append(box(226, 88, 140, 56, "Motor de H2", ["(una biblioteca)"], stroke=TEAL))
b.append(path([(196, 116), (222, 116)], "ink"))
b.append(file_icon(236, 166, 120, 62, "tienda.mv.db", ["en datos/"], fill=WHITE))
b.append(path([(296, 144), (296, 162)], "teal"))
pros1 = ["+ nada que instalar ni arrancar", "+ ideal para pruebas y aplicaciones", "   de un solo usuario", "– un único programa a la vez", "– los datos viven en ese equipo"]
b.append(lines(36, 274, pros1, 12.5, gap=19, anchor="start"))
# servidor
X = 450
b.append(text(X, 32, "Servidor independiente (MariaDB)", 15, INDIGO, "start", 700))
b.append(rect(X, 48, 200, 100, NEUTRAL_T, LINE, rx=12, sw=1.2, dash=True))
b.append(text(X + 12, 70, "Proceso de tu programa", 12, MUTED, "start", italic=True))
b.append(box(X + 24, 82, 152, 52, "Tu código", ["+ conector"], stroke=INK))
b.append(rect(X, 166, 200, 76, NEUTRAL_T, LINE, rx=12, sw=1.2, dash=True))
b.append(text(X + 12, 188, "Otros clientes", 12, MUTED, "start", italic=True))
b.append(pill(X + 16, 200, 80, 28, "mariadb", fill=WHITE, stroke=LINE, size=12))
b.append(pill(X + 104, 200, 84, 28, "HeidiSQL", fill=WHITE, stroke=LINE, size=12, mono=False))
b.append(rect(X + 290, 48, 230, 194, INDIGO_T, INDIGO, rx=12, sw=1.4, dash=True))
b.append(text(X + 302, 70, "Otro proceso, quizá otra máquina", 12, MUTED, "start", italic=True))
b.append(box(X + 316, 82, 180, 52, "mariadbd", ["el servidor"], stroke=INDIGO, tmono=True))
b.append(cylinder(X + 346, 154, 120, 74, "datos", ["usuarios, permisos…"], tsize=12.5, ssize=10.5))
b.append(path([(X + 406, 134), (X + 406, 150)], "indigo"))
b.append(path([(X + 200, 108), (X + 312, 108)], "indigo", marker_start="a"))
b.append(path([(X + 200, 204), (X + 256, 204), (X + 256, 120), (X + 312, 120)], "indigo", marker_start="a"))
b.append(text(X + 256, 98, "red", 12, INDIGO, "middle", halo=True))
pros2 = ["+ muchos programas y usuarios a la vez", "+ usuarios, permisos, copias de seguridad", "– hay que instalarlo, arrancarlo y administrarlo", "– cada operación viaja por la red"]
b.append(lines(X + 6, 274, pros2, 12.5, gap=19, anchor="start"))
open(OUT + "fig-2-2-embebido-servidor.svg", "w").write(svg(990, 370, "".join(b), "Gestor de bases de datos embebido frente a servidor independiente"))

# ---------- Figura 2.3: anatomía de una URL JDBC ----------
b = []
def url_parts(y, parts, title):
    out = [text(30, y - 24, title, 13.5, INK, "start", 700)]
    x = 30
    for txt, lab, col in parts:
        w = tw(txt, 15, True) + 4
        if col:
            out.append(rect(x, y - 2, w, 30, {"teal": TEAL_T, "amber": AMBER_T, "indigo": INDIGO_T, "rose": ROSE_T, "ink": NEUTRAL_T}[col], COLORS[col], rx=4, sw=1.2))
        out.append(text(x + 2, y + 19, txt, 15, INK, "start", 600, mono=True))
        if lab:
            out.append(path([(x + w / 2, y + 30), (x + w / 2, y + 44)], col or "line", marker_end=None))
            out.append(lines(x + w / 2, y + 60, lab.split("\n"), 11.5, gap=15, fill=COLORS[col] if col else MUTED))
        x += w + 4
    return "".join(out)
b.append(url_parts(52, [("jdbc", "siempre", "ink"), (":", None, None), ("mariadb", "conector\nque la atiende", "amber"), ("://", None, None),
                        ("localhost", "máquina del\nservidor", "indigo"), (":", None, None), ("3306", "puerto", "indigo"), ("/", None, None),
                        ("tienda", "base de\ndatos", "teal"), ("?", None, None), ("connectTimeout=5000", "opciones del conector,\nseparadas por &", "rose")],
                   "Servidor MariaDB"))
b.append(url_parts(186, [("jdbc", None, "ink"), (":", None, None), ("h2", None, "amber"), (":", None, None),
                         ("./datos/tienda", "fichero, relativo al directorio\nde trabajo (sin .mv.db)", "teal"), (";", None, None),
                         ("MODE=MariaDB;DATABASE_TO_LOWER=TRUE", "opciones: imitar el SQL de MariaDB\ny nombres en minúscula", "rose")],
                    "H2 embebida en un fichero"))
b.append(url_parts(320, [("jdbc", None, "ink"), (":", None, None), ("h2", None, "amber"), (":", None, None), ("mem:pruebas", "en memoria: desaparece al cerrar la última\nconexión (ideal para las pruebas)", "teal")],
                    "H2 en memoria"))
open(OUT + "fig-2-3-url.svg", "w").write(svg(900, 410, "".join(b), "Partes de una URL JDBC para MariaDB y para H2"))

# ---------- Figura 2.4: pool de conexiones ----------
b = []
b.append(text(30, 30, "Sin pool: cada operación abre y cierra su propia conexión", 14, INK, "start", 700))
steps = [("abrir conexión", "TCP + identificación", ROSE_T, ROSE, 270), ("consulta", None, TEAL_T, TEAL, 90), ("cerrar", None, ROSE_T, ROSE, 80)]
for row in range(2):
    x, y = 30, 48 + row * 44
    b.append(text(x, y + 22, f"operación {row + 1}", 12, MUTED, "start"))
    x += 92
    for t, sub, f, s, w in steps:
        b.append(rect(x, y, w, 30, f, s, rx=4, sw=1.1))
        b.append(text(x + w / 2, y + 20, t if not sub else t + "  ·  " + sub, 12, INK, "middle"))
        x += w + 4
b.append(text(30, 160, "Con un pool: las conexiones se abren una vez y se prestan", 14, INK, "start", 700))
PX = 400
b.append(rect(PX, 180, 300, 168, INDIGO_T, INDIGO, rx=12, sw=1.4))
b.append(text(PX + 150, 204, "Pool (HikariCP)", 14, INDIGO, "middle", 700))
for i in range(4):
    busy = i < 2
    b.append(rect(PX + 20 + i * 68, 220, 58, 44, TEAL_T if busy else WHITE, TEAL if busy else INDIGO, rx=6, sw=1.3))
    b.append(text(PX + 49 + i * 68, 247, "en uso" if busy else "libre", 11.5, INK, "middle", 600 if busy else 400))
b.append(text(PX + 150, 290, "abiertas al arrancar y siempre listas", 12, MUTED, "middle", italic=True))
b.append(path([(PX + 150, 348), (PX + 150, 372)], "indigo", marker_start="a"))
b.append(cylinder(PX + 80, 376, 140, 62, "MariaDB", None, tsize=13))
for lab, yy in [("ProductoRepositoryJdbc", 196), ("PedidoRepositoryJdbc", 262)]:
    b.append(box(30, yy, 220, 46, lab, None, stroke=INK, tmono=True, tsize=12))
b.append(path([(250, 219), (PX - 4, 232)], "teal"))
b.append(text(262, 214, "getConnection()", 11.5, TEAL, "start", mono=True))
b.append(path([(PX - 4, 262), (254, 285)], "teal"))
b.append(text(262, 298, "close()", 11.5, TEAL, "start", mono=True))
b.append(rect(730, 196, 290, 150, NEUTRAL_T, LINE, rx=8, sw=1))
b.append(lines(746, 222, ["close() no cierra: devuelve la", "conexión al pool para otro uso.", "", "Medido con la tienda (servidor local):", "conexión nueva    ≈ 2,3 ms", "conexión del pool ≈ 0,35 ms"], 12.5, gap=19, anchor="start"))
open(OUT + "fig-2-4-pool.svg", "w").write(svg(1040, 455, "".join(b), "Sin pool, cada operación abre y cierra su conexión; con un pool, las conexiones se reutilizan"))
print("ok")

"""Pequeña biblioteca para dibujar las figuras SVG de los apuntes con un estilo común."""
from xml.sax.saxutils import escape

INK, MUTED, LINE = "#1E2933", "#5C6B7A", "#8795A3"
TEAL, TEAL_T = "#0E6F72", "#E3F1F1"
AMBER, AMBER_T = "#A35F00", "#FBEFD9"
INDIGO, INDIGO_T = "#3949A0", "#E7E9F6"
ROSE, ROSE_T = "#A83A3A", "#F8E3E3"
NEUTRAL_T = "#F2F4F7"
WHITE = "#FFFFFF"

SANS = "'Segoe UI', 'Helvetica Neue', Arial, 'DejaVu Sans', sans-serif"
MONO = "Consolas, 'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"

COLORS = {"ink": INK, "muted": MUTED, "line": LINE, "teal": TEAL, "amber": AMBER,
          "indigo": INDIGO, "rose": ROSE}


def tw(s, size=14, mono=False, bold=False):
    """Anchura aproximada de un texto (conservadora)."""
    f = 0.61 if mono else (0.6 if bold else 0.56)
    return len(s) * size * f


def defs():
    out = ["<defs>"]
    for name, c in COLORS.items():
        out.append(f'<marker id="a-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
        out.append(f'<marker id="o-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10" fill="none" stroke="{c}" stroke-width="1.6" stroke-dasharray="none"/></marker>')
        out.append(f'<marker id="t-{name}" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path d="M0,0 L11,6 L0,12 z" fill="#FFFFFF" stroke="{c}" stroke-width="1.4" stroke-dasharray="none"/></marker>')
        out.append(f'<marker id="d-{name}" viewBox="0 0 16 10" refX="1" refY="5" markerWidth="16" markerHeight="10" orient="auto-start-reverse"><path d="M1,5 L8,1 L15,5 L8,9 z" fill="{c}"/></marker>')
    out.append("</defs>")
    return "".join(out)


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(label)}" font-family="{SANS}">'
            f'<title>{escape(label)}</title>'
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>' + defs() + body + "</svg>\n")


def text(x, y, s, size=14, fill=INK, anchor="middle", weight=400, mono=False, italic=False, halo=False):
    fam = f' font-family="{MONO}"' if mono else ""
    st = ' font-style="italic"' if italic else ""
    bg = ""
    if halo:
        w = tw(s, size, mono, weight >= 600) * 0.95 + 8
        x0 = {"start": x - 4, "middle": x - w / 2, "end": x - w + 4}[anchor]
        bg = f'<rect x="{x0}" y="{y - size * 0.95}" width="{w}" height="{size * 1.3}" fill="#FFFFFF"/>'
    hl = ""
    s = s.replace("  ", "\u00a0\u00a0") if "  " in s else s
    return bg + (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{fam}{st}{hl}>{escape(s)}</text>')


def lines(x, y, items, size=14, gap=None, **kw):
    """Varias líneas de texto; items es lista de str o de (str, dict)."""
    gap = gap or size * 1.35
    out = []
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            s, extra = it
            k = dict(kw); k.update(extra)
        else:
            s, k = it, kw
        out.append(text(x, y + i * gap, s, size=size, **k))
    return "".join(out)


def rect(x, y, w, h, fill=WHITE, stroke=LINE, rx=8, sw=1.5, dash=False, opacity=None):
    d = ' stroke-dasharray="6 4"' if dash else ""
    op = f' fill-opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{op} stroke="{stroke}" stroke-width="{sw}"{d}/>'


def box(x, y, w, h, title=None, sub=None, fill=WHITE, stroke=LINE, rx=8, dash=False,
        tsize=14, ssize=12, tmono=False, smono=False, tcolor=INK, scolor=MUTED, bold=True, sw=1.5):
    """Caja con título y subtítulo (lista de líneas) centrados."""
    out = [rect(x, y, w, h, fill, stroke, rx, sw, dash)]
    sub = sub or []
    if isinstance(sub, str):
        sub = [sub]
    n_lines = (1 if title else 0) + len(sub)
    total = (tsize if title else 0) + len(sub) * ssize * 1.3 + (4 if title and sub else 0)
    cy = y + h / 2 - total / 2
    cx = x + w / 2
    if title:
        out.append(text(cx, cy + tsize * 0.8, title, size=tsize, fill=tcolor, weight=600 if bold else 400, mono=tmono))
        cy += tsize + 4
    for i, s in enumerate(sub):
        out.append(text(cx, cy + ssize * 0.95 + i * ssize * 1.3, s, size=ssize, fill=scolor, mono=smono))
    return "".join(out)


def path(points, color="ink", marker_end="a", marker_start=None, dash=False, sw=1.5):
    c = COLORS[color]
    if dash and (marker_end or marker_start):
        # línea discontinua sin puntas + tramos finales continuos con las puntas
        out = path(points, color, None, None, True, sw)
        def tip(p, q):
            dx, dy = q[0] - p[0], q[1] - p[1]
            n = max((dx * dx + dy * dy) ** 0.5, 1e-6)
            return [(q[0] - dx / n * 3, q[1] - dy / n * 3), q]
        if marker_end:
            out += path(tip(points[-2], points[-1]), color, marker_end, None, False, sw)
        if marker_start:
            out += path(tip(points[1], points[0]), color, marker_start, None, False, sw)
        return out
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    me = f' marker-end="url(#{marker_end}-{color})"' if marker_end else ""
    ms = f' marker-start="url(#{marker_start}-{color})"' if marker_start else ""
    da = ' stroke-dasharray="6 4"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}"{da}{me}{ms} stroke-linejoin="round"/>'


def file_icon(x, y, w, h, title, sub=None, fill=WHITE, stroke=LINE, tmono=True, tsize=13, ssize=11.5, smono=False):
    f = 14
    d = f"M{x},{y} L{x+w-f},{y} L{x+w},{y+f} L{x+w},{y+h} L{x},{y+h} z"
    fold = f"M{x+w-f},{y} L{x+w-f},{y+f} L{x+w},{y+f}"
    out = [f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/>',
           f'<path d="{fold}" fill="none" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/>']
    sub = sub or []
    if isinstance(sub, str):
        sub = [sub]
    total = tsize + len(sub) * ssize * 1.3 + (4 if sub else 0)
    cy = y + h / 2 - total / 2 + 2
    out.append(text(x + w / 2, cy + tsize * 0.8, title, size=tsize, weight=600, mono=tmono))
    for i, s in enumerate(sub):
        out.append(text(x + w / 2, cy + tsize + 4 + ssize * 0.95 + i * ssize * 1.3, s, size=ssize, fill=MUTED, mono=smono))
    return "".join(out)


def cylinder(x, y, w, h, title, sub=None, fill=INDIGO_T, stroke=INDIGO, tmono=False, tsize=13, ssize=11.5, dash=False):
    ry = 9
    da = ' stroke-dasharray="6 4"' if dash else ""
    body = (f'<path d="M{x},{y+ry} L{x},{y+h-ry} A{w/2},{ry} 0 0 0 {x+w},{y+h-ry} L{x+w},{y+ry}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"{da}/>')
    top = f'<ellipse cx="{x+w/2}" cy="{y+ry}" rx="{w/2}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{da}/>'
    out = [body, top]
    sub = sub or []
    if isinstance(sub, str):
        sub = [sub]
    total = tsize + len(sub) * ssize * 1.3 + (4 if sub else 0)
    cy = y + ry + (h - ry) / 2 - total / 2
    out.append(text(x + w / 2, cy + tsize * 0.8, title, size=tsize, weight=600, mono=tmono))
    for i, s in enumerate(sub):
        out.append(text(x + w / 2, cy + tsize + 4 + ssize * 0.95 + i * ssize * 1.3, s, size=ssize, fill=MUTED))
    return "".join(out)


def uml_class(x, y, w, name, attrs=(), ops=(), stereo=None, fill=WHITE, stroke=INK, head_fill=None,
              italic=False, size=12.5, dash=False, name_size=14):
    """Clase UML con tres compartimentos. Devuelve (svg, alto). Un elemento de attrs/ops
    puede ser una tupla (texto, {'u': True}) para subrayarlo (miembro static)."""
    lh = size * 1.45
    head_h = (name_size + 14) + (size + 2 if stereo else 0)
    a_h = (len(attrs) * lh + 10) if attrs else 10
    o_h = (len(ops) * lh + 10) if ops else 0
    h = head_h + a_h + o_h
    da = ' stroke-dasharray="6 4"' if dash else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{da}/>']
    if head_fill:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{head_h}" fill="{head_fill}" stroke="{stroke}" stroke-width="1.5"{da}/>')
    cy = y + 6
    if stereo:
        out.append(text(x + w / 2, cy + size, stereo, size=size, fill=MUTED))
        cy += size + 2
    out.append(text(x + w / 2, cy + name_size + 2, name, size=name_size, weight=700, italic=italic))
    yy = y + head_h
    out.append(f'<line x1="{x}" y1="{yy}" x2="{x+w}" y2="{yy}" stroke="{stroke}" stroke-width="1.2"/>')
    for i, a in enumerate(attrs):
        s, opt = (a if isinstance(a, tuple) else (a, {}))
        ty = yy + 5 + (i + 1) * lh - 4
        out.append(text(x + 8, ty, s, size=size, anchor="start", mono=True))
        if opt.get("u"):
            out.append(f'<line x1="{x+8}" y1="{ty+2}" x2="{x+8+tw(s,size,True)*0.98}" y2="{ty+2}" stroke="{INK}" stroke-width="1"/>')
    yy += a_h
    if ops:
        out.append(f'<line x1="{x}" y1="{yy}" x2="{x+w}" y2="{yy}" stroke="{stroke}" stroke-width="1.2"/>')
        for i, a in enumerate(ops):
            s, opt = (a if isinstance(a, tuple) else (a, {}))
            ty = yy + 5 + (i + 1) * lh - 4
            out.append(text(x + 8, ty, s, size=size, anchor="start", mono=True, italic=opt.get("i", False)))
            if opt.get("u"):
                out.append(f'<line x1="{x+8}" y1="{ty+2}" x2="{x+8+tw(s,size,True)*0.98}" y2="{ty+2}" stroke="{INK}" stroke-width="1"/>')
    return "".join(out), h


def pill(x, y, w, h, s, fill=WHITE, stroke=LINE, mono=True, size=13, color=INK, weight=500, dash=False):
    return rect(x, y, w, h, fill, stroke, rx=h / 2, dash=dash) + text(x + w / 2, y + h / 2 + size * 0.35, s, size=size, mono=mono, fill=color, weight=weight)

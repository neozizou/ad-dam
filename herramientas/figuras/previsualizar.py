"""Convierte las figuras SVG en PNG para revisarlas (necesita: pip install cairosvg pillow).

Uso: python herramientas/figuras/previsualizar.py [ud1]   → crea herramientas/figuras/previas/*.png
Las PNG se generan con fuentes del sistema; el resultado final es el del navegador.
"""
import sys
from pathlib import Path

import cairosvg

raiz = Path(__file__).resolve().parents[2]
destino = Path(__file__).parent / "previas"
destino.mkdir(exist_ok=True)
filtro = sys.argv[1] if len(sys.argv) > 1 else ""
for svg in sorted((raiz / "docs").glob(f"{filtro}*/img/*.svg")):
    png = destino / (svg.stem + ".png")
    cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=1000)
    print(png.relative_to(raiz))

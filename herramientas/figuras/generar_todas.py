"""Regenera todas las figuras SVG de los apuntes (docs/udN/img/)."""
import runpy
import sys
from pathlib import Path

carpeta = Path(__file__).parent
sys.path.insert(0, str(carpeta))
for script in sorted(carpeta.glob("ud*_*.py")):
    print("·", script.name)
    runpy.run_path(str(script), run_name="__main__")

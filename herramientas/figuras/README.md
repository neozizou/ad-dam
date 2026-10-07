# Figuras de los apuntes

Las figuras de `docs/udN/img/` se generan con estos programas de Python (sin dependencias externas), para que todas compartan estilo y se puedan corregir con facilidad.

- `lib.py`: paleta de colores, tipografías y funciones de dibujo (cajas, flechas, ficheros, cilindros, clases UML…).
- `ud0_a.py`, `ud0_b.py`…: cada uno genera varias figuras de una unidad; la cabecera indica cuáles.
- `generar_todas.py`: las regenera todas.
- `previsualizar.py`: crea PNG en `previas/` para revisarlas (necesita `cairosvg` y `pillow`).

Para cambiar una figura, edita su script, ejecútalo y comprueba el resultado:

```bash
python herramientas/figuras/ud1_a.py
python herramientas/figuras/previsualizar.py ud1
```

Paleta: tinta `#1E2933`; verde azulado `#0E6F72` (Java, nuestro código); ámbar `#A35F00` (C++, avisos, formatos); índigo `#3949A0` (almacenamiento y datos externos); rosa `#A83A3A` (errores). Fondo blanco siempre, para que se vean bien también en modo oscuro.

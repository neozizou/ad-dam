"""Traduce los recuadros de los apuntes a avisos de MkDocs Material.

En el Markdown se escribe de forma que también se lea bien en GitHub:

    > **Desde C++.** Las plantillas generan una versión del código...

    > [!TIP]
    > **Buena práctica.** ...

y al construir la web se convierten en avisos («admonitions») de Material:

    !!! cpp "Desde C++"
        Las plantillas generan una versión del código...

    !!! tip
        **Buena práctica.** ...

El estilo del aviso «cpp» está en docs/css/apuntes.css. MkDocs carga este
fichero porque aparece en la sección «hooks» de mkdocs.yml.
"""

import re

ALERTAS = {
    "NOTE": "note",
    "TIP": "tip",
    "IMPORTANT": "info",
    "WARNING": "warning",
    "CAUTION": "danger",
}

PATRON_ALERTA = re.compile(
    r"^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n((?:^>.*\n?)*)",
    re.MULTILINE,
)

# Un recuadro «Desde C++» ocupa una cita de una o varias líneas seguidas
PATRON_CPP = re.compile(
    r"^> \*\*Desde C\+\+\.\*\* ?(.*\n?(?:^>.*\n?)*)",
    re.MULTILINE,
)


def _cuerpo_de_cita(texto: str) -> list[str]:
    return [linea[2:] if linea.startswith("> ") else linea.lstrip(">")
            for linea in texto.splitlines()]


def _sangrar(lineas: list[str]) -> str:
    return "\n".join(f"    {linea}".rstrip() for linea in lineas)


def _alerta(coincidencia: re.Match) -> str:
    tipo = ALERTAS[coincidencia.group(1)]
    return f"!!! {tipo}\n{_sangrar(_cuerpo_de_cita(coincidencia.group(2)))}\n"


def _desde_cpp(coincidencia: re.Match) -> str:
    lineas = coincidencia.group(1).splitlines()
    cuerpo = [lineas[0]] + _cuerpo_de_cita("\n".join(lineas[1:]))
    return f'!!! cpp "Desde C++"\n{_sangrar(cuerpo)}\n'


def _fuera_de_codigo(markdown: str, transformar) -> str:
    """Aplica la transformación solo a los trozos que no son bloques de código."""
    trozos = re.split(r"(^```.*?^```[ \t]*$)", markdown, flags=re.MULTILINE | re.DOTALL)
    return "".join(t if t.startswith("```") else transformar(t) for t in trozos)


def on_page_markdown(markdown: str, **kwargs) -> str:
    """MkDocs llama a esta función con el Markdown de cada página."""
    def transformar(texto: str) -> str:
        texto = PATRON_ALERTA.sub(_alerta, texto)
        return PATRON_CPP.sub(_desde_cpp, texto)
    return _fuera_de_codigo(markdown, transformar)

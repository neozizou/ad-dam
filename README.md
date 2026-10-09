# Acceso a Datos · 2.º DAM

Apuntes, ejemplos y prácticas del módulo Acceso a Datos (CFGS Desarrollo de Aplicaciones Multiplataforma), curso 2026-2027. La web (https://neozizou.github.io/ad-dam/) se genera con MkDocs y el tema Material a partir de la carpeta `docs/`, y se publica con GitHub Actions.

## Estructura

```text
ad-dam/
├── .github/workflows/       publicar-sitio.yml: construye y publica la web
├── docs/                    la web
│   ├── index.md             portada del módulo
│   ├── css/apuntes.css      ajustes de estilo (recuadro «Desde C++», figuras)
│   ├── ud0/                 una carpeta por unidad: index.md, img/ y ejemplos/
│   ├── ud1/
│   └── ud2/
├── herramientas/
│   ├── figuras/             generadores de las figuras SVG
│   └── web/                 requirements.txt (MkDocs) y hooks.py
├── mkdocs.yml               configuración de la web y menú
├── CLAUDE.md                contexto y normas del proyecto para Claude Code
└── README.md
```

## Primera publicación

1. En GitHub, crea un repositorio **vacío** (sin README ni licencia) llamado, por ejemplo, `ad-dam`. Para publicar con Pages desde una cuenta gratuita, el repositorio debe ser público.
2. Desde la carpeta del proyecto (igual en PowerShell, bash y zsh; sustituye `USUARIO`):

   ```bash
   git init -b main
   git add .
   git commit -m "Publica la portada, la UD0 y la UD1"
   git remote add origin https://github.com/USUARIO/ad-dam.git
   git push -u origin main
   ```

   Si es la primera vez que usas Git en este ordenador, antes: `git config --global user.name "Tu nombre"` y `git config --global user.email "tu@correo"`.

3. En GitHub, en **Settings → Pages**, elige en **Source** la opción **GitHub Actions**.
4. Cada *push* a `main` lanza el flujo «Publicar el sitio en GitHub Pages» (pestaña **Actions**). En uno o dos minutos la web estará en `https://USUARIO.github.io/ad-dam/` (cambia `site_url` y `repo_url` en `mkdocs.yml` si usas otro usuario o nombre).

## Trabajo diario

```bash
git status                      # qué ha cambiado
git add .
git commit -m "UD1: amplía los ejercicios de CSV"
git push                        # GitHub Actions vuelve a publicar la web
```

## Vista previa de la web en tu ordenador

Con Python 3 instalado, desde la raíz del repositorio (igual en PowerShell, bash y zsh):

```bash
pip install -r herramientas/web/requirements.txt
mkdocs serve                    # abre http://127.0.0.1:8000/ad-dam/ y recarga al guardar
mkdocs build --strict           # la misma comprobación que hace GitHub antes de publicar
```

## Figuras

Ver `herramientas/figuras/README.md`. Para regenerarlas todas: `python herramientas/figuras/generar_todas.py`.

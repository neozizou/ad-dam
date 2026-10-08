# Acceso a Datos · 2.º DAM

Apuntes, ejemplos y prácticas del módulo Acceso a Datos (CFGS Desarrollo de Aplicaciones Multiplataforma), curso 2026-2027. La web se genera con GitHub Pages a partir de la carpeta `docs/`.

## Estructura

```text
acceso-a-datos-dam/
├── docs/                    la web
│   ├── _config.yml          configuración de Jekyll y del tema
│   ├── index.md             portada del módulo
│   ├── ud0/                 una carpeta por unidad: index.md, img/ y ejemplos/
│   ├── ud1/
│   └── ud2/
├── herramientas/figuras/    generadores de las figuras SVG
├── CLAUDE.md                contexto y normas del proyecto para Claude Code
└── README.md
```

## Primera publicación

1. En GitHub, crea un repositorio **vacío** (sin README ni licencia) llamado, por ejemplo, `acceso-a-datos-dam`. Para publicar con Pages desde una cuenta gratuita, el repositorio debe ser público.
2. Desde la carpeta del proyecto (igual en PowerShell, bash y zsh; sustituye `USUARIO`):

   ```bash
   git init -b main
   git add .
   git commit -m "Publica la portada, la UD0 y la UD1"
   git remote add origin https://github.com/USUARIO/acceso-a-datos-dam.git
   git push -u origin main
   ```

   Si es la primera vez que usas Git en este ordenador, antes: `git config --global user.name "Tu nombre"` y `git config --global user.email "tu@correo"`.

3. En GitHub, en **Settings → Pages**, elige **Deploy from a branch**, la rama `main` y la carpeta `/docs`, y guarda.
4. En uno o dos minutos la web estará en `https://USUARIO.github.io/acceso-a-datos-dam/`. El progreso de cada publicación se ve en la pestaña **Actions**.

## Trabajo diario

```bash
git status                      # qué ha cambiado
git add .
git commit -m "UD1: amplía los ejercicios de CSV"
git push                        # GitHub Pages republica la web automáticamente
```

## Figuras

Ver `herramientas/figuras/README.md`. Para regenerarlas todas: `python herramientas/figuras/generar_todas.py`.

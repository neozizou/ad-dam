/*
 * Navegación de las unidades (Acceso a Datos · 2.º DAM)
 *
 * En las páginas que tienen el índice "Contenido de la unidad" (#markdown-toc):
 *   - construye el índice "En esta unidad" con los apartados (h2) y subapartados (h3);
 *   - marca el apartado que se está leyendo mientras se hace scroll;
 *   - en pantallas estrechas lo ofrece como panel desplegable con un botón flotante.
 * En todas las páginas del menú principal añade al final los enlaces
 * a la unidad anterior y a la siguiente, tomados del propio menú lateral.
 *
 * El diseño (anchos, colores, cuándo se ve cada cosa) está en assets/css/indice-lateral.css.
 */
(function () {
  'use strict';

  var MARGEN_SUPERIOR = 40; // px: un título pasa a ser el "actual" cuando sube por encima de esta línea

  function textoDe(titulo) {
    return titulo.textContent.replace(/\s+/g, ' ').trim();
  }

  function rutaNormalizada(url) {
    var ruta = new URL(url, location.href).pathname.replace(/index\.html$/, '');
    return ruta.endsWith('/') ? ruta : ruta + '/';
  }

  /* ---------- Índice "En esta unidad" ---------- */

  function construirIndice(contenido) {
    var titulos = Array.prototype.filter.call(
      contenido.querySelectorAll('h2[id], h3[id]'),
      function (h) { return !h.classList.contains('no_toc') && !h.closest('details'); }
    );
    if (titulos.length === 0) return;

    var panel = document.createElement('nav');
    panel.className = 'indice-lateral';
    panel.id = 'indice-lateral';
    panel.setAttribute('aria-labelledby', 'indice-lateral-titulo');

    var cabecera = document.createElement('div');
    cabecera.className = 'indice-cabecera';
    var titulo = document.createElement('p');
    titulo.className = 'indice-titulo';
    titulo.id = 'indice-lateral-titulo';
    titulo.textContent = 'En esta unidad';
    var cerrar = document.createElement('button');
    cerrar.type = 'button';
    cerrar.className = 'indice-cerrar';
    cerrar.setAttribute('aria-label', 'Cerrar el índice');
    cerrar.textContent = '×';
    cabecera.appendChild(titulo);
    cabecera.appendChild(cerrar);
    panel.appendChild(cabecera);

    var lista = document.createElement('ol');
    lista.className = 'indice-lista';
    var enlaces = [];          // en el mismo orden que "titulos"
    var apartadoDe = [];       // <li> del h2 al que pertenece cada título
    var liActual = null;
    var subLista = null;

    titulos.forEach(function (h) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + encodeURIComponent(h.id);
      a.textContent = textoDe(h);
      li.appendChild(a);
      if (h.tagName === 'H2' || liActual === null) {
        lista.appendChild(li);
        liActual = li;
        subLista = null;
      } else {
        if (subLista === null) {
          subLista = document.createElement('ol');
          liActual.appendChild(subLista);
          liActual.classList.add('con-subapartados');
        }
        subLista.appendChild(li);
      }
      enlaces.push(a);
      apartadoDe.push(liActual);
    });
    panel.appendChild(lista);

    var arriba = document.createElement('a');
    arriba.className = 'indice-arriba';
    arriba.href = '#top';
    arriba.textContent = '↑ Volver arriba';
    panel.appendChild(arriba);

    document.body.appendChild(panel);

    /* Botón flotante y fondo para pantallas estrechas */
    var boton = document.createElement('button');
    boton.type = 'button';
    boton.className = 'indice-boton';
    boton.setAttribute('aria-controls', 'indice-lateral');
    boton.setAttribute('aria-expanded', 'false');
    boton.innerHTML = '<span aria-hidden="true">☰</span> Índice';
    var fondo = document.createElement('div');
    fondo.className = 'indice-fondo';
    document.body.appendChild(fondo);
    document.body.appendChild(boton);

    function abrir(si) {
      document.body.classList.toggle('indice-abierto', si);
      boton.setAttribute('aria-expanded', si ? 'true' : 'false');
      if (si) {
        mantenerVisible(true);
        cerrar.focus();
      }
    }
    boton.addEventListener('click', function () {
      abrir(!document.body.classList.contains('indice-abierto'));
    });
    cerrar.addEventListener('click', function () { abrir(false); boton.focus(); });
    fondo.addEventListener('click', function () { abrir(false); });
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a')) abrir(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('indice-abierto')) {
        abrir(false);
        boton.focus();
      }
    });

    /* Apartado actual mientras se hace scroll */
    var indiceActivo = -1;

    function mantenerVisible(centrar) {
      if (indiceActivo < 0) return;
      var a = enlaces[indiceActivo];
      var arribaA = a.offsetTop;
      var abajoA = arribaA + a.offsetHeight;
      var margen = 48;
      if (centrar) {
        panel.scrollTop = arribaA - panel.clientHeight / 2;
      } else if (arribaA < panel.scrollTop + margen) {
        panel.scrollTop = arribaA - margen;
      } else if (abajoA > panel.scrollTop + panel.clientHeight - margen) {
        panel.scrollTop = abajoA - panel.clientHeight + margen;
      }
    }

    function actualizar() {
      var nuevo = 0;
      var alFinal = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;
      if (alFinal) {
        nuevo = titulos.length - 1;
      } else {
        for (var i = 0; i < titulos.length; i++) {
          if (titulos[i].getBoundingClientRect().top <= MARGEN_SUPERIOR) nuevo = i;
          else break;
        }
      }
      if (nuevo === indiceActivo) return;
      if (indiceActivo >= 0) {
        enlaces[indiceActivo].removeAttribute('aria-current');
        apartadoDe[indiceActivo].classList.remove('abierto');
      }
      indiceActivo = nuevo;
      enlaces[nuevo].setAttribute('aria-current', 'location');
      apartadoDe[nuevo].classList.add('abierto');
      mantenerVisible(false);
    }

    var pendiente = false;
    function alDesplazar() {
      if (pendiente) return;
      pendiente = true;
      window.requestAnimationFrame(function () {
        pendiente = false;
        actualizar();
      });
    }
    window.addEventListener('scroll', alDesplazar, { passive: true });
    window.addEventListener('resize', alDesplazar);
    actualizar();
  }

  /* ---------- Unidad anterior y siguiente ---------- */

  function construirVecinas(contenido) {
    var enlacesMenu = Array.prototype.slice.call(
      document.querySelectorAll('#site-nav > .nav-list > .nav-list-item > .nav-list-link')
    );
    var aqui = rutaNormalizada(location.href);
    var pos = enlacesMenu.findIndex(function (a) { return rutaNormalizada(a.href) === aqui; });
    if (pos < 0) return;

    var anterior = enlacesMenu[pos - 1];
    var siguiente = enlacesMenu[pos + 1];
    if (!anterior && !siguiente) return;

    var nav = document.createElement('nav');
    nav.className = 'unidades-vecinas';
    nav.setAttribute('aria-label', 'Unidad anterior y siguiente');

    function tarjeta(a, clase, etiqueta) {
      var enlace = document.createElement('a');
      enlace.className = 'unidad-vecina ' + clase;
      enlace.href = a.href;
      var e = document.createElement('span');
      e.className = 'unidad-vecina-etiqueta';
      e.textContent = etiqueta;
      var t = document.createElement('span');
      t.className = 'unidad-vecina-titulo';
      t.textContent = textoDe(a);
      enlace.appendChild(e);
      enlace.appendChild(t);
      return enlace;
    }
    if (anterior) nav.appendChild(tarjeta(anterior, 'anterior', '← Anterior'));
    if (siguiente) nav.appendChild(tarjeta(siguiente, 'siguiente', 'Siguiente →'));
    contenido.appendChild(nav);
  }

  function iniciar() {
    var contenido = document.querySelector('#main-content > main');
    if (!contenido) return;
    if (contenido.querySelector('#markdown-toc')) construirIndice(contenido);
    construirVecinas(contenido);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();

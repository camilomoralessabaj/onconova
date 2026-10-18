# Revisión editorial y navegación · 18/10/2026

Rama local `feat/revision-contenidos-navegacion`, base `main` / `76c818f36021b07e3277096215bb769e029b4c00`.
El checkout estaba limpio; fetch confirmó esa misma base. Se conservan los cambios
integrados de paleta, relato S11, comprobante PDF, transiciones y guía local.
No hay issue confirmado. No se hizo push, PR, merge ni publicación.

## Matriz de aceptación

Las capturas enlazadas corresponden al render local final. Sus variantes `-390`
y `-320` están en la misma carpeta. Los informes crudos permanecen en `.local/`.

| Requisito | Implementación | Captura | Verificación efectuada |
| --- | --- | --- | --- |
| R1 | `site/index.html`, `site/assets/styles.css`, `site/assets/busqueda-apoyo.svg` | [Desafío 1440](revision-2026-10-18/editorial/desafio-1440.png), [390](revision-2026-10-18/editorial/desafio-390.png), [320](revision-2026-10-18/editorial/desafio-320.png) | Párrafo y problema de estudio literales conservados; ilustración conceptual junto al texto y después en móvil; contraste y reflujo inspeccionados. S01/S07 intactas. |
| R2 | `.pivot-comparison` en `site/index.html` | [Historia 1440](revision-2026-10-18/editorial/historia-1440.png), [390](revision-2026-10-18/editorial/historia-390.png) | 43→26 y 48→42 palabras, sin cambiar tamaño. Cinco ámbitos, cuatro componentes, conector y S02/S08/S10/S11 conservados. Comparación literal abajo. |
| R3 | `.proposal-section .section-heading`, `.proposal-attributes` | [Propuesta 1440](revision-2026-10-18/editorial/propuesta-1440.png), [390](revision-2026-10-18/editorial/propuesta-390.png), [320](revision-2026-10-18/editorial/propuesta-320.png) | Intro 391,4→636 px de ancho y 116,1→58,0 px de alto a 1440; mismo texto, 17,6 px y 29,04 px de interlineado. Tarjetas sin alturas fijas, responsabilidades pendientes y límites íntegros. |
| R4 | `site/assets/mark.svg`, consumido por ambos encabezados y ambos favicon | [Lazo 16–96 px](revision-2026-10-18/editorial/lazo-tamanos.png) | Vector propio local, bucle y dos cintas cruzadas reconocibles a 16/24/34 px; imagen decorativa `alt=""` dentro de enlace con nombre único «OncoNova, inicio». Rutas relativas comprobadas. |
| R5 | `.research-context`, `site/assets/entrevista-conceptual.svg` | [Evidencia 1440](revision-2026-10-18/editorial/validacion-1440.png), [390](revision-2026-10-18/editorial/validacion-390.png), [320](revision-2026-10-18/editorial/validacion-320.png) | Cinco entrevistas, cuatro mujeres/una profesional, perfiles diversos, muestra no representativa y ausencia de validación permanecen visibles con S01/S07. Pie distingue diseño de evidencia. |
| R6 | `.section-index`, `initSectionIndex()` en `site/assets/app.js`, ajuste de offsets de guía | [Índice 1440](revision-2026-10-18/editorial/indice-1440.png), [390](revision-2026-10-18/editorial/indice-390.png), [320](revision-2026-10-18/editorial/indice-320.png), [zoom200%](revision-2026-10-18/editorial/zoom-200.png) | Usuario eligió explícitamente «Índice de capítulos» tras comparar las dos variantes. Ocho escenarios automatizados, anclas/alias, scroll en ambos sentidos, historial, teclado, cambio de tamaño/orientación, ampliación, zoom nativo200 %, sin JS, reducción de movimiento y caché de medidas. |
| R7 | `.iteration-table` en `site/assets/styles.css` | [Tabla 1440](revision-2026-10-18/editorial/proximos-pasos-1440.png), [390](revision-2026-10-18/editorial/proximos-pasos-390.png), [320](revision-2026-10-18/editorial/proximos-pasos-320.png) | Contorno y separaciones burdeo con `--primary`; tres filas y caption/encabezados/roles conservados. Móvil agrupa cada acción con responsables y plazo completo; semanas relativas propuestas. |

## Comparación editorial

Conteo por palabras separadas por espacios, cuerpos sin títulos ni etiquetas.

### App Integral Multifunción

| Antes (43 palabras) | Después (26 palabras) |
| --- | --- |
| Reunir en una aplicación el seguimiento clínico, la salud mental, la rehabilitación, la orientación laboral y la gestión GES. Ese alcance concentraba múltiples necesidades y servicios en una misma propuesta. Es el punto de partida conceptual; no representa funciones construidas ni integraciones disponibles. | Una app para reunir seguimiento clínico, salud mental, rehabilitación, orientación laboral y gestión GES. Fue una idea de partida: esas funciones e integraciones no se construyeron. |

### Servicio Acotado de Transición

| Antes (48 palabras) | Después (42 palabras) |
| --- | --- |
| Una exploración breve no diagnóstica, una decisión voluntaria, una derivación prioritaria acompañada y una confirmación de acceso compatible. La propuesta busca utilizar canales institucionales existentes. El prototipo actual ensaya la coordinación de una primera hora de apoyo psicológico; todavía no realiza derivaciones ni confirma acceso a atención real. | Servicio propuesto: exploración breve sin diagnóstico, decisión voluntaria, una derivación prioritaria acompañada y confirmación de acceso compatible por canales institucionales existentes. Hoy el prototipo solo simula coordinar una primera hora de apoyo psicológico: sin derivaciones ni confirmación de acceso a atención real. |

La segunda síntesis conserva explícitamente servicio **propuesto**, exploración
sin diagnóstico, decisión voluntaria, **una** derivación prioritaria acompañada,
confirmación compatible y uso propuesto de canales existentes. La frase final
limita el prototipo a coordinar una primera hora simulada, sin derivaciones ni
confirmación de acceso real. No se modificaron `project.json` ni `docs/evidencia.md`:
no hay datos nuevos, originales ni resultados que registrar.

## Composición, navegación y biblioteca

Se preservaron portada, fuente de sistema, paleta y composición general.
Marcos de 12 px de radio y espaciado de 24–26 px continúan las figuras existentes.
Las tarjetas de Propuesta usan `--page` sobre sección `--primary`, títulos burdeo
con cuerpo oscuro. Pares medidos: burdeo/fondo 5,90:1; cuerpo/fondo 14,56:1;
secundario/fondo 7,22:1; burdeo/pastel 4,89:1. Son cálculos de pares y un muestreo
renderizado, no una certificación completa del sitio.

Los bocetos quedaron en `.local/wireframes/barra.md`. Se construyeron dos variantes
funcionales aisladas con relato real: enlaces directos frente a ubicación+select
nativo+botón Ir. Cada una pasó teclado y ausencia de overflow a 1440/390/320; se
mostraron capturas de escritorio/móvil. El usuario solicitó aclarar la diferencia
y eligió luego **Índice de capítulos**. La superficie temporal se retiró tras la
promoción; evidencia y comprobación se conservaron en `.local/revision-editorial/`.

El índice reemplaza los tres accesos redundantes de la cabecera en la landing.
La cabecera del prototipo independiente mantiene su navegación. Cada enlace
sigue siendo un ancla nativa, con `aria-current="location"` y señal de borde,
peso y subrayado. No se escribe historial al hacer scroll, se mueve foco ni se
usa aria-live. Se conservan `#resultados` dentro de Evidencia y `#proximos-pasos`
dentro de Aprendizajes. La tira horizontal se centra en el capítulo actual,
salvo cuando contiene foco de teclado; el foco permanece visible. El hint móvil
explica que hay más capítulos al deslizar. Un gesto táctil sintetizado movió
la tira 0→452 px sin cambiar scrollY de página.

Solo se miden capítulos al cambiar layout; scroll consulta posiciones cacheadas.
La prueba instrumenta getBoundingClientRect y confirma cero lecturas durante
cuatro movimientos dentro del mismo capítulo. ResizeObserver actualiza límites
por cambios de dimensiones; resize/pageshow cubren orientación y restauración.
Los offsets descuentan cabecera+índice una vez, con 24 px de aire. En móvil,
texto grande de la app o altura≤520 px se deja cabecera/guía local en flujo;
el índice pasa también a flujo si supera28 % de la altura visible. Sin JS
queda la lista real, sin una sección activa inventada. Reflujo extremo mejora
con ajuste de palabras y flex-wrap, sin ocultar overflow ni achicar controles.

Consultas `ui-ux-pro-max` verificadas: current location navigation, responsive
navigation y focus not obscured (dominio ux). Active State, Sticky Navigation y
Keyboard Navigation aportan patrones pertinentes. Breadcrumbs se descartó porque
el relato es plano; el ejemplo de padding fijo se reemplaza por offsets medidos.
La referencia de foco AAA se distingue del mínimo AA; el encargo busca foco entero.

`pick-ui-library`: para un índice de enlaces nativos no se necesita biblioteca.
La recomendación genérica Base UI de la lista sirve a primitivas personalizadas
en React; incorporarla exigiría otro stack sin aportar valor aquí. Se mantienen
anclas y scroll nativos, cero paquetes de producción y ninguna instalación.
`animate-expo` se consultó por petición expresa: no aplica a esta web HTML/CSS/JS;
no hay aplicación React Native/Expo, migración, gestos ni paquetes móviles.

## Procedencia y carga de imágenes

Se inspeccionaron `acompanamiento.svg` y `escucha.svg`: el primero aporta las
figuras adultas y colores de portada; el segundo es un pictograma de escucha y
no describe una entrevista. Se conservaron ambos originales sin alteración.
Los nuevos SVG adaptan las figuras del arte propio en 76c818f a dos composiciones:
búsqueda de apoyo con información/reloj/coordinación, y conversación de entrevista
con cuaderno. No derivan de fotografías ni de identidades reales. El lazo es
geometría original dibujada para esta revisión, sin emoji ni marca externa.
No representa aval, convenio ni alianza institucional.

| Recurso | ViewBox/dimensiones reservadas | Bytes | Gzip orientativo |
| --- | --- | ---: | ---: |
| `busqueda-apoyo.svg` |640×400|2731|1254|
| `entrevista-conceptual.svg` |640×400|4259|1767|
| `mark.svg` |48×48; encabezado34/27/24|448|295|

Las dos escenas usan img local con width/height, loading=lazy, decoding=async,
alternativa descriptiva y pie conceptual visible. Su ausencia simulada conserva
la lectura factual y el espacio reservado. Las cifras gzip son compresión local,
no una medición de la respuesta de Pages. No se añaden peticiones de terceros.

## Movimiento y refinamiento

No se añadieron animaciones. La señal global cambia instantáneamente porque
acompaña lectura y navegación frecuentes. Las nuevas ilustraciones son estáticas.
Se retiró la entrada vertical de 8 px de las tarjetas de Propuesta para cumplir
la petición de texto quieto durante lectura. Se conservan el token
`--ease-out:cubic-bezier(0.23,1,0.32,1)`, el marco local de 250 ms y la opacidad
del prototipo de 150 ms, incluidos cambio instantáneo por teclado/reducción.
La ilustración de portada y su decisión existente se preservan.

Plan acotado en `.local/animation-plans/editorial-20261018.md`: no hay una
corrección animada nueva que implementar. Las ocho categorías se revisaron contra
fuente y pruebas: propósito/frecuencia, tiempos, origen, interrupción, rendimiento,
reducción, tokens y oportunidades. Se rechazaron movimiento del texto académico,
entradas de ilustraciones nuevas y deslizamiento del activo global. Ninguno
mejora la comprensión en el recorrido de lectura. No se reportó la opacidad sola
como defecto. La intención es respuesta y orientación inmediata, no decoración.

| Antes | Después | Motivo |
| --- | --- | --- |
| Tarjetas de propuesta entraban con transform8 px | Tarjetas estáticas, contenido idéntico | Texto estable durante lectura. |
| Nuevo índice podía ocultar un enlace enfocado al centrar activo | Centrado suspendido mientras la tira contiene foco | Conservar foco visible sin moverlo. |
| Marco local250 ms y prototipo150 ms | Conservados y probados | Indican estado sin bloquear acciones; reducido/teclado instantáneos. |

Revisión `review-animations`: aprobada dentro del diff comprobado, sin hallazgos
bloqueantes confirmados. Fuente: `site/assets/app.js` para límites/foco y
`site/assets/styles.css` para señal/ausencia de animación global; los 13 casos de
`test-step-motion.py` y 11 de guía revalidan tiempos exactos y alternativas.

## Comandos y resultados reales

- `node scripts/check.mjs`: aprobado; 8 etapas, 11 fuentes, 3 metas sin resultados,
 2 páginas y 15 archivos públicos.
- `node scripts/build.mjs`: aprobado; únicamente `site/` a `dist/`.
- `git diff --check` y `node --check site/assets/app.js`: aprobados.
- `node scripts/serve.mjs`: servidor4173 iniciado; `/`, `/prototipo/` y recursos
 relativos comprobados. `work/check-pages-prefix.py` aprobó `/onconova/` y `/onconova/prototipo/`,
 incluidas marca, imágenes, imports y semántica de tabla móvil, sin errores.
- Comando exacto solicitado de smoke en `.agents/skills/revision-landing/scripts/smoke.py`:
 ejecutado; **0/6** por selectores históricos ausentes (`[data-choice]`, `#support`).
 Es un defecto previo del test, reproducible en 76c818f. No se editaron skills.
 Reporte original en `.local/revision-landing/report.json`.
- Adaptador de solo QA `work/smoke-current.py`: reutiliza runner/reportes del
 smoke y cambia únicamente sus acciones a la interfaz vigente; **6/6 aprobados**, resultado en
 `.local/revision-editorial/smoke-current.json`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-section-index.py --base-url http://127.0.0.1:4173 --output .local/revision-editorial/section-index`:
 **8 escenarios aprobados**, cinco geometrías 1440×900,390×800,320×800,844×390,320×256
 y casos sin JS, sin medición continua/movimiento reducido y zoom nativo200 %.
 La preferencia de zoom real de Chromium devolvió innerWidth720, outerWidth1440,
 devicePixelRatio2 y visualViewport.scale1; no es CSS zoom ni pinch emulado.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-reading-guide.py --base-url http://127.0.0.1:4173 --output .local/revision-editorial/reading-guide`:
 **11 casos aprobados**. Se adaptaron dos expectativas a guía móvil en flujo y
 ancho interior de fila con padding; se mantienen teclado,250 ms y fallbacks.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-step-motion.py --base-url http://127.0.0.1:4173 --output .local/revision-editorial/step-motion-final`:
 **13 casos aprobados**, dos rutas,150 ms y curva exacta, toque/teclado,
 interrupciones, validación, reducción y foco.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --base-url http://127.0.0.1:4173 --output .local/revision-editorial/booking`:
 **6 casos aprobados y 78 PDFs**; cuatro combinaciones de canal/modalidad por
 ruta/ancho, postergación, rechazo, pendiente, reinicio, fallos/reintentos,
 lectura sin JS y enlace a fuente. Sin mensajes ni reservas reales.
- `PYTHONDONTWRITEBYTECODE=1 python3 work/test-break-fixtures.py`:
 **64 combinaciones aprobadas** de cuatro fixtures, cuatro anchos 1440/390/320/256
 y texto raíz 100/200 %. Fixtures rotulados en `.local/break-ui/editorial/`,
 sin tocar project.json. Imagen fallida genera404 deliberado, con alt y lectura
 disponibles; sin overflow. El fixture ausente es un fallo de autoría simulado.
- `work/capture-final.py`: capturas y medida comparativa de R3, peso y contraste.

Las primeras pruebas de integración permitieron corregir expectativas y errores
del harness antes del resultado final; no se presentan como pasadas aquellas
corridas fallidas. El smoke original se conserva como fallo conocido.

## Segunda revisión separada

Se volvió sobre el diff después de implementar: textos contra76c818f y S01–S11,
privacidad, problema íntegro, títulos/tabla, solicitudes ficticias, ARIA/foco,
scroll, offsets, nativo sin JS y composición1440/390/320. Los límites de evidencia,
metas y planificación no cambiaron; no hay originales privados ni datos de salud.

Impeccable corrió contexto una vez sobre la vista existente (sin PRODUCT.md o
DESIGN.md, autoridad del CSS/arte vigente y permiso para refinamiento acotado).
Se leyeron referencias de composición, crítica, auditoría y pulido, y se realizó
crítica con dos assessments aislados. A terminó antes de incorporar el detector
B a la síntesis. A: 27/32 heurísticas aplicables; B: 18/20 técnico, ambos orientativos.
El detector CLI se ejecutó una vez: cuatro warnings, sin bloqueantes confirmados;
el overlay de prueba corrió en Chromium headless y **no fue visible al usuario**.
Su servidor exclusivo se cerró. No se instalaron hooks ni se modificaron skills.

Se corrigió el P2 de descubribilidad con el hint móvil. Dos observaciones previas
quedan como mejoras opcionales fuera del diff: guía local móvil a 12,8 px en tamaño
normal y `.proposal-limit` con líneas 95/93 caracteres a 1440. No son nuevas fallas
AA ni impiden los recorridos comprobados. Los bordes existentes, captions y avisos
de evidencia que señaló el detector tienen función concreta y se conservaron.
No se eliminan límites factuales para satisfacer una heurística estilística.

## Límites y revisión humana

La URL publicada devolvió403 del proxy y no pudo compararse su render.
Se contrastó el código actual con render local y base obtenida por fetch.
`/codex/.../output` no se pudo crear: raíz de solo lectura. Los entregables se
conservan en el checkout y `work/entrega-editorial/`, sin subir a otro servicio.
Se ejecutó Chromium 154, escritorio y móvil emulado/sintetizado; no Safari,
Firefox, lector de pantalla escuchado, dispositivo físico o prueba con usuarias.
No hay garantía de ausencia total de errores ni validación clínica/operativa.
La comprensión en tres minutos es el objetivo editorial, todavía sin medición.
La integración futura requiere aprobación humana de otra persona según CONTRIBUTING.

Archivo de crítica: `.impeccable/critique/2026-10-18T11-09-29Z__site-index-html.md`.
Primera corrida de este objetivo,27/32; todavía sin tendencia comparable. Snapshot
escrito y consulta de tendencia realizada; temporal de persistencia eliminado.
Questions skipped: menos de tres Priority Issues; alcance y variante ya resueltos.

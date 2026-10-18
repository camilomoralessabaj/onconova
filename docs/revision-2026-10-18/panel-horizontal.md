# Panel compartido y movimiento horizontal · 18/10/2026

Rama `feat/panel-horizontal`, base `76c818f` (PR #8 integrado). El usuario autoriza implementar el plan y abrir un nuevo PR hacia `main`; no solicita merge. Esta revisión corresponde al panel completo y complementa la revisión anterior de la guía de títulos.

## Decisiones y resultado

Se aplicaron `animation-vocabulary` e `improve-animations` para precisar y auditar la idea, `animate` para implementarla, y `review-animations` y `revision-landing` para revisarla. Se consultaron las [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md). No se modificaron skills.

El efecto acordado es una **direction-aware transition** mediante **translate**: un único panel de información, un contenido visible a la vez, avance hacia la derecha y retroceso hacia la izquierda. Navegación mediante scroll normal, títulos y swipe; deslizar a la derecha avanza y a la izquierda retrocede. Se añaden botones Anterior/Siguiente como alternativa explícita. No hay bucle entre el final y el principio.

Al avanzar, borde y contenido salen 24 px hacia la derecha en 100 ms; el siguiente contenido entra desde 24 px a la izquierda en 150 ms. Se invierten los signos al retroceder. Duración nominal total 250 ms, sin rebote, con `--ease-out: cubic-bezier(0.23,1,0.32,1)`. Solo se animan `transform` y `opacity`; los textos no se superponen. La altura cambia fuera de la transición, sin animar dimensiones.

## Auditoría y decisiones técnicas

La auditoría de la base no encontró un defecto bloqueante en lo comprobado: #8 señalaba títulos y conservaba tres bloques visibles. La petición cambia ese comportamiento, por lo que ocultar dos bloques sin sustituir la geometría del observer habría roto el avance por scroll.

El recorrido ahora reserva espacio según las alturas reales de los tres contenidos y la ventana disponible. Cada capítulo largo se desplaza con el documento hasta poder leer su final; el siguiente ocupa la misma superficie al cruzar su límite. Un margen de 96 px permite ver el final antes de avanzar y evita cambios por unos pocos píxeles en capítulos cortos. No se fija el panel, no hay scroll interno ni `preventDefault` de rueda o gesto vertical. El cambio automático no llama a `scrollTo`, no altera el hash y no mueve el foco. Los saltos mediante títulos, botones, gestos o historial sí siguen deliberadamente el destino.

Se usan rangos precalculados: el listener pasivo de scroll compara `scrollY` una vez por frame sin medir geometría. Las alturas y el origen se recalculan ante cambios de ancho, tamaño de texto, viewport o altura del documento, incluida la demostración anterior. Se conserva todo el contenido en el DOM con IDs únicos; no se crean copias de lectura. Durante las mediciones los bloques permanecen visual y semánticamente ocultos.

Una selección nueva invalida callbacks anteriores y resuelve inmediatamente al último destino cuando interrumpe una transición. Los títulos, controles y reconocimiento de swipe permanecen disponibles durante la salida. El teclado y la preferencia reducida cambian sin animación y cancelan movimiento en curso. El scroll automático no oculta un capítulo con foco o selección de texto. Los enlaces y botones tienen margen de scroll para quedar visibles bajo la guía móvil.

Los gestos usan Pointer Events, `touch-action:pan-y pinch-zoom` y cambio al soltar: al menos 48 px horizontales y 1,5 veces el desplazamiento vertical. Se descartan gestos cortos, diagonales, cancelados, multitáctiles, sobre controles o con texto seleccionado. No hay arrastre continuo ni inercia. Sin JavaScript, IntersectionObserver o ResizeObserver se leen los tres bloques consecutivamente con sus anclas nativas; al imprimir se muestran todos.

## Revisión de animaciones

| Antes / hallazgo | Después | Motivo |
| --- | --- | --- |
| Solo se desplazaba el marco sobre títulos; el contenido era estático | Una superficie compartida cambia de contenido y dirección | Implementa la continuidad espacial solicitada. |
| El origen medido podía quedar desfasado cuando la demostración anterior terminaba de ajustar su altura | ResizeObserver actualiza el origen ante cambios del documento (`site/assets/app.js:192`) | Mantiene visibles los destinos y correctos los límites de lectura. |
| Con texto ampliado a 320 px los dos botones excedían el ancho del panel | Los controles pueden pasar a varias líneas; comprobación de sus límites | Evita recortar una acción detrás del clip reservado al movimiento horizontal. |
| Ocultar el panel completo durante la salida impediría nuevos gestos y controles | Solo el capítulo que sale queda inert; el contenedor y controles siguen activos (`site/assets/app.js:151`) | Permite interrumpir tanto salida como entrada. |

Veredicto de `review-animations`: **aprobar dentro del alcance comprobado**. Se inspeccionaron capturas de escritorio, móvil y texto ampliado, y muestras de ambas fases y sentidos en `work/panel-horizontal/edges/`. No quedan hallazgos bloqueantes confirmados; esta revisión no sustituye la aprobación de otra persona.

## Verificaciones

- `node scripts/check.mjs`, sintaxis de `site/assets/app.js`, `node scripts/build.mjs` y `git diff --check`: aprobados.
- `scripts/test-reading-guide.py`: **12 casos aprobados**, con seis combinaciones de 1440/390/320 px y movimiento normal/reducido; eventos táctiles de Chromium emulado a dos anchos; tres alternativas sin JS/observers; enlaces directos. Incluye duración, curva y dirección de fases, interrupción en salida/entrada, lectura del final antes del cambio, scrollY sin modificación automática, historial, foco Tab/Shift+Tab, texto ampliado, controles sin recorte, cambio de breakpoint e impresión. [Reporte](panel-report.json).
- Comprobaciones adicionales: **tres casos aprobados** a los tres anchos para botones con teclado, swipe durante ambas fases y cambio de ancho durante la salida. [Reporte](panel-edges.json).
- `scripts/test-booking.py`: seis combinaciones de ruta/ancho, 78 PDF verificados, alternativas sin JS y enlace directo de fuente aprobados. `scripts/test-step-motion.py`: **13 casos aprobados**. Reportes completos locales en `work/panel-horizontal/`.
- Diff de HTML revisado: los párrafos, fuentes, responsables y plazos originales se conservan. Solo se añade envoltura, controles y ayuda de navegación. No cambian la paleta, los PDF, el contenido factual o el prototipo. Sin dependencias nuevas.

Incremento de fuentes sin comprimir frente a la base: JS +6948 bytes, CSS +1755 bytes y HTML +401 bytes, total +9104 bytes. No se infiere rendimiento de teléfonos o redes reales desde localhost.

Capturas: [escritorio](panel-escritorio.png), [móvil](panel-movil.png) y [320 px con texto ampliado](panel-texto-ampliado.png).

Límites: Chromium local y emulación táctil; sin Safari, Firefox, teléfonos físicos, zoom nativo o lector de pantalla. No se afirma validación con usuarias ni revisión del despliegue público. La revisión en dispositivos físicos y la aprobación humana siguen pendientes antes de integrar.

# Movimiento durante el scroll · 18/10/2026

Rama `feat/movimiento-scroll`, base local `71c6c95`. Alcance: landing de `site/index.html`; el prototipo independiente y los estados de agendamiento mantienen su comportamiento. Sin cambios de relato, evidencia, paleta, tipografía o dependencias.

Se aplicaron las skills locales `find-animation-opportunities`, `motion-design`, `animate`, `review-animations` y `revision-landing`, junto con las guías de diseño y relato requeridas por AGENTS.md. Se consultó también `animate-expo` por petición del usuario: el repositorio no tiene una aplicación React Native/Expo; su ajuste local reserva esas recetas para un encargo fuera de esta landing. No se incorporan paquetes de Expo ni gestos personalizados. Se conserva el deslizamiento táctil nativo.

## Oportunidades seleccionadas

Personalidad: cercana, tranquila y contenida. Una curva compartida `--ease-out: cubic-bezier(0.23,1,0.32,1)`, entradas de 300 ms y acentos narrativos de 500 ms. Las duraciones más largas corresponden a ilustración y trazos decorativos, sin bloquear controles. La capa ambiental permanece estática para respetar la intensidad solicitada.

| Ubicación | Antes | Propósito y frecuencia | Receta implementada | Función y presupuesto |
| --- | --- | --- | --- | --- |
| `site/index.html:8`, ilustración | Estática al recorrer la portada | Bienvenida (delight); rara | `translateY(12px) scale(.985)` y opacidad .9 → estado original, 500 ms, `--ease-out` | Solo imagen; título, descripción y CTA estables. No reproduce si ya estaba visible al cargar. |
| `site/index.html:11`, cuatro pasos | Aparición simultánea al recorrer la propuesta | Explicación del orden; una vez por visita | `translateY(8px)` y opacidad .85 → estado original, 300 ms, `--ease-out`; demoras 0/50/100/150 ms | Secuencia completa ≤450 ms, sin ocultar ni bloquear contenido. En móvil cada fila entra al llegar a pantalla. |
| `site/index.html:60`, resultados | Bordes superiores estáticos | Indicación de entrada al grupo de hallazgos; una vez | Solo línea: `scaleX(.2)` y opacidad .4 → 1, origen izquierdo, 500 ms, `--ease-out` | El texto y las limitaciones de evidencia permanecen inmóviles. |
| `site/index.html:62`, próximos pasos | Bordes superiores estáticos | Indicación de entrada al plan de trabajo; una vez | Mismo trazo de resultados, 500 ms, `--ease-out` | Mantiene continuidad sin animar datos ni acciones. |

Se descartaron: contador de las cinco entrevistas (función: es evidencia que debe leerse directamente), transiciones de formularios/confirmación (función y frecuencia: distraerían del estado y el foco), entradas de todos los títulos y párrafos (función: interferirían con la lectura), loops ambientales y parallax (propósito: decoración continua sin necesidad), y swipe para navegar pasos (función: competiría con el scroll y necesitaría alternativas).

El mayor aporte es la secuencia de cuatro pasos: hace perceptible su orden sin retrasar la lectura. El resto del recorrido necesita poco movimiento. La selección se trasladó directamente a la implementación con `animate`, dentro del encargo ya autorizado.

## Revisión de animaciones

| Antes | Después | Por qué |
| --- | --- | --- |
| Sin hallazgos pendientes confirmados en el diff revisado | Aprobado dentro del alcance comprobado | Entradas únicas, propiedades acotadas, cancelación inmediata y contenido siempre visible. |

- `site/assets/app.js:33`: IntersectionObserver, margen inferior de 32 px y desconexión de cada elemento después de su primera entrada. Sin listeners de scroll, bloqueo de eventos ni cálculos por fotograma.
- `site/assets/app.js:54`: teclado de navegación, enlaces internos, impresión o cambio de preferencia detienen el movimiento durante la visita. Los enlaces directos con hash abren una página estática.
- `site/assets/styles.css:1170`: únicamente transform y opacidad; sin interacción hover añadida, rebotes o bucles. Keyframes para entradas únicas; sin animaciones de estados repetidos.
- `site/assets/styles.css:1201`: reducción de movimiento estática, válida según el ajuste local de las skills. La cancelación durante una entrada no vuelve a reproducirla al desactivar la preferencia.
- El HTML permanece idéntico a la base al retirar los once atributos `data-scroll-motion`. El estado inicial es visible sin JS, sin IntersectionObserver y antes de cualquier animación; ningún contenido empieza en opacidad cero.

Decisión de `review-animations`: **aprobar el diff dentro de las superficies y el navegador revisados**. Esta revisión local no sustituye la revisión humana del equipo previa al merge.

## Verificación de landing

Se utilizó `scripts/test-booking.py`, adaptación vigente del smoke para el agendamiento actual. El smoke incluido en la skill sigue dirigido a la maqueta anterior; no se modificaron skills.

- `node scripts/check.mjs`: siete etapas, diez fuentes, tres metas sin resultados inventados; dos páginas y doce archivos públicos íntegros.
- `node --check site/assets/app.js`, `node scripts/build.mjs` y `git diff --check`: aprobados.
- Agendamiento: seis casos aprobados, `/` y `/prototipo/` a 1440, 390 y 320 px; canal/modalidad, consentimiento, horario requerido, comprobante, reprogramación, espera, postergación, rechazo y reinicio. Texto ampliado, foco básico, ausencia de errores de consola/recursos y desbordamiento horizontal. Lectura sin JS en ambas rutas y enlace directo a S10 aprobados.
- Movimiento normal a 1440×900, 390×760 y 320×760: entradas verificadas, solo transform/opacidad y sin repetición del elemento ya recorrido. Los elementos todavía no vistos pueden entrar después, especialmente en la cuadrícula móvil.
- Preferencia reducida desde carga y activada durante una entrada; vuelta a la preferencia normal; teclado, enlaces internos, anclas directas, impresión, falta de IntersectionObserver y lectura sin JS: aprobados.
- Deslizamiento táctil nativo emulado a 390×760: desplaza la página sin controles de gesto añadidos. Curva CSS y keyframes observados: `cubic-bezier(0.23, 1, 0.32, 1)`. La posición documental del prototipo no cambia al cancelar el movimiento.
- Capturas de portada, propuesta, resultados y próximos pasos inspeccionadas. Se observó también la secuencia a un cuarto de velocidad para inspeccionar sus estados intermedios. [Escritorio](escritorio.png) y [móvil](movil.png) muestran la propuesta durante esa inspección ralentizada.
- Incremento de fuentes sin comprimir: HTML +294 bytes, JS +1970 bytes, CSS +1626 bytes, total +3890 bytes. Cero dependencias y peticiones nuevas. No se infieren tiempos de red ni FPS de hardware a partir de localhost.

Reportes y scripts puntuales: `work/motion/` (ignorado). Se consultó la guía actual de Web Interface Guidelines enlazada por la skill; revisión proporcional del diff sin hallazgos pendientes. No se pudo abrir la URL de GitHub Pages desde las herramientas disponibles, por lo que la inspección corresponde al checkout y su servidor local. No se probaron Safari, dispositivos físicos, zoom nativo ni comprensión con usuarias. La emulación y el reflujo no sustituyen esas comprobaciones. Sin push, PR, merge ni publicación.

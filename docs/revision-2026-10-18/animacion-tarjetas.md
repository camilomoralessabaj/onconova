# Continuidad de las tarjetas de Aprendizajes

Corrección del comportamiento integrado en el PR #12, sobre `b2f3e44`.
Rama: `fix/aprendizajes-transiciones`.

[Vista previa: selección y scroll en escritorio](animacion-tarjetas/preview.mp4).

Al cruzar un hito de scroll, el panel cambiaba su `top` de golpe. La transición
de profundidad de las tarjetas no compensaba ese desplazamiento y el texto
entrante aparecía inmediatamente. La corrección conserva los hitos, las alturas
de lectura, el orden canónico y el scroll nativo.

## Implementación y revisión de movimiento

Se aplicaron las skills locales `frontend-design`, `onconova-storytelling`,
`motion-design`, `animate`, `review-animations`, `web-design-guidelines` y
`revision-landing`. Se consultaron las recetas de `animate`, los estándares de
`review-animations` y la guía vigente de Vercel desde su repositorio oficial.
La dirección es continuidad espacial y calma, sin rebotes, nuevas dependencias
ni cambios de paleta, tipografía, composición o relato.

| Antes | Después | Motivo |
| --- | --- | --- |
| `site/assets/app.js`: el panel saltaba entre posiciones absolutas. | `app.js:191`: se mide la posición presentada y se compensa el cambio de layout mediante `transform` con WAAPI. | Mantener la continuidad visual incluso al invertir el scroll durante una transición. |
| La selección directa actualizaba el panel antes de sincronizar el documento. | `app.js:218`: el scroll explícito se sincroniza antes de calcular la compensación visual. | Evitar sumar artificialmente el desplazamiento del panel al desplazamiento del documento. |
| El nuevo texto aparecía en un cuadro. | `styles.css:1042`: entrada con opacidad y desplazamiento de 16 px, invertido al retroceder. | Hacer visible la llegada del contenido dentro de la tarjeta. |
| La cancelación solo terminaba transiciones de la carcasa. | `app.js:186`: cancela el desplazamiento del panel y termina las transiciones de sus descendientes. | Teclado, movimiento reducido, reflujo e impresión recuperan inmediatamente una lectura estática. |

Se reutilizan `--ease-out` y `--motion-standard` (300 ms) para el contenido.
El reposicionamiento del panel usa `--motion-story` (500 ms): es una transición
narrativa de una superficie de lectura, con desplazamientos medidos de 254 px
en escritorio y 599 px en móvil en el primer hito. La duración superior a la de
un control pequeño evita comprimir todo ese recorrido en una respuesta brusca.
No anima `top`, altura ni márgenes por cuadro. Las lecturas geométricas ocurren
al cambiar de tarjeta; el navegador ejecuta la interpolación de `transform`.

Una interrupción toma la posición visual actual antes de cancelar la animación
previa. No hay cola ni controles bloqueados. Las anclas distantes se resuelven
directamente si el panel estaba fuera de pantalla. La entrada de contenido es
una mejora progresiva: sin `@starting-style` sigue siendo visible. El teclado y
la preferencia de movimiento reducido mantienen los estados estáticos del PR #12.

**Veredicto local de movimiento: aprobado en el alcance comprobado.** No quedaron
hallazgos bloqueantes confirmados en el diff. Esta revisión no sustituye la
revisión de otra persona requerida para integrar cambios.

## Verificación

- `node scripts/check.mjs`, `node scripts/build.mjs`,
  `node --check site/assets/app.js` y `git diff --check`: aprobados.
- `python3 scripts/test-reading-guide.py --output work/reading-motion/initial`:
  14 escenarios aprobados. Escritorio 1440 px, móvil 390 px y reflujo 320 px;
  selección, continuidad de lectura, avance, retroceso y salida; interrupciones;
  teclado/foco, anclas, historial y recarga; toque y swipe emulados; ausencia de
  JS/observers; ampliación de texto, movimiento reducido, impresión y zoom
  nativo de Chromium al 200 %. [Resultados](animacion-tarjetas/recorrido.json).
- `python3 scripts/test-reading-motion.py --output work/reading-motion/continuity`:
  cinco casos aprobados. Mide el primer cuadro del cambio, inversión durante el
  movimiento, entrada del texto, selección directa, cancelación por Tab,
  cambio de preferencia, reflujo durante una transición y alternativa sin
  `@starting-style`. En las muestras normales de 1440 y 390 px, el error de
  continuidad inicial fue 0 px tanto al avanzar como al invertir. Con reducción
  de movimiento se verifica el cambio estático esperado.
  [Mediciones](animacion-tarjetas/continuidad.json).
- Inspección de capturas de escritorio y móvil, cuadros intermedios y una
  secuencia grabada de selección y scroll. Los tests vigilan consola y errores
  de página; el recorrido también vigila recursos HTTP. Sin errores detectados.
- Diff revisado, incluidos el test y los informes nuevos. HTML, fuentes y datos
  del proyecto intactos; sin dependencias ni modificaciones de skills.

Los casos cuentan escenarios agrupados, no participantes ni validaciones del
servicio. Se usó Chromium local y tacto emulado; no Safari, Firefox, teléfono
físico ni lector de pantalla escuchado. Las capturas y mediciones locales no
certifican 60 fps en dispositivos reales. El agendamiento no cambia y su batería
no se repitió. La entrega de esta corrección se prepara como rama de tarea y PR
en borrador. No incluye merge ni publicación; la integración requiere los checks
pertinentes y revisión de otra persona según `CONTRIBUTING.md`.

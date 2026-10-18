# Movimiento y guía de lectura · 18/10/2026

Rama `feat/movimiento-scroll`. Se integró `origin/main` en `78c479b` antes de cerrar la implementación, conservando la paleta burdeo/rosados, el relato de S11, los comprobantes PDF y las transiciones del prototipo. Esta revisión sustituye las capturas y las decisiones de la primera pasada sobre `71c6c95`.

Se aplicaron `find-animation-opportunities`, `motion-design`, `animate`, `review-animations` y `revision-landing`, con las guías de diseño, relato e interfaz del repositorio. Se consultó `animate-expo`: esta landing nativa no necesita una aplicación Expo ni gestos nuevos. El scroll y los enlaces continúan siendo del navegador.

## Selección e implementación

| Superficie | Antes | Propósito y frecuencia | Movimiento elegido |
| --- | --- | --- | --- |
| Aprendizajes, Brechas y Próximos Pasos | Hallazgos y brechas repartidos en columnas, seguidos del plan | Indicación de posición de lectura y continuidad espacial; al cambiar de bloque | Un único cuadro compartido se traslada entre tres enlaces en 250 ms, solo `transform`, `cubic-bezier(0.23,1,0.32,1)`. Responde al scroll y a los enlaces. |
| Tres atributos de la propuesta vigente | Aparición simultánea | Presentación de la propuesta; una vez por visita | Entrada de 8 px en 300 ms, demoras 0/50/100 ms y la misma curva. Opacidad completa para conservar contraste. Sustituye la secuencia de cuatro pasos de la versión anterior. |
| Ilustración de portada | Estática al entrar desde fuera de pantalla | Bienvenida; rara | `translateY(12px) scale(.985)`, opacidad .9 → estado original en 500 ms con la misma curva. Permanece quieta si ya estaba visible al cargar. |

El mayor aporte es la guía de lectura: tres paradas en orden, con el cuadro en una columna lateral en escritorio y una barra superior en móvil. Los textos de los tres grupos se leen en una sola columna, sin movimiento de contenido, ocultamientos, carruseles o avance automático. La tabla conserva acciones, responsables y semanas relativas. El indicador usa `aria-current="step"`, número, negrita, subrayado y contorno; no depende solo del color.

Se descartaron animar el número de entrevistas y los datos del RIA (función: evidencia para leer), transiciones de todo el texto (función: obstaculizarían la lectura), parallax o loops (propósito y frecuencia: decoración constante), y gestos de arrastre o swipe de capítulos (función: competirían con el scroll). La guía aporta continuidad sin estas capas.

## Revisión de animaciones y accesibilidad

| Antes | Después | Por qué |
| --- | --- | --- |
| No había señal persistente del bloque leído | Un cuadro compartido con transición interrumpible, de 250 ms | La última acción retoma desde la posición actual; los cambios rápidos no acumulan animaciones. |
| La nueva barra necesita un destino de teclado claro | Los tres bloques aceptan foco nativo con `tabindex="-1"` y contorno visible | Enter salta al bloque sin añadir paradas al orden Tab ni mover el foco mediante JS. |
| Una regla existente dejaba el encabezado de acción al 48 % en móvil | Ancho completo dentro de la nueva disposición móvil | Evita palabras cortadas innecesariamente, especialmente con texto ampliado. |
| Al volver con Shift+Tab, la barra móvil podía cubrir parte del botón | Márgenes de scroll en los enlaces del relato | El foco queda visible por debajo de la barra al avanzar y retroceder. |
| Un test del prototipo asumía un único `aria-current` en toda la página | Selector acotado a `.booking-progress` | La guía y el agendamiento son dos contextos distintos; se conserva su semántica. |

El cuadro mantiene dimensiones estables entre enlaces; solo cambia `transform`. El tamaño se recalcula sin transición al cambiar de ancho o de texto. IntersectionObserver detecta los límites de los tres bloques; no hay mediciones por fotograma ni listeners de scroll que alteren la navegación. ResizeObserver reajusta la guía cuando cambia su distribución.

La preferencia de movimiento reducido cancela las entradas y hace instantáneo el indicador, conservando la posición señalada. El teclado también cancela inmediatamente una transición en curso. En móvil con texto ampliado, la guía pasa al flujo normal y a enlaces verticales para dejar espacio al relato. En impresión se omite la guía y permanece el contenido. Sin JavaScript o sin IntersectionObserver quedan los tres enlaces nativos y los bloques completos; el cuadro decorativo permanece oculto.

Los párrafos y su orden se compararon con `origin/main`: son idénticos, salvo la etiqueta nueva “Sigue el recorrido”. No cambian hechos, fuentes, personas, plazos, resultados ni estados de evidencia. Se añadieron títulos de agrupación y se ajustó la jerarquía de subtítulos. El manifiesto y el prototipo independiente no cambian frente a main.

Decisión de `review-animations`: **aprobar dentro del alcance verificado**, sin hallazgos bloqueantes pendientes. La revisión local no sustituye la aprobación humana requerida para integrar el PR.

## Verificaciones

- `node scripts/check.mjs`: ocho etapas registradas, once fuentes y tres metas sin resultados inventados; dos páginas y trece archivos públicos válidos.
- Sintaxis JS, `node scripts/build.mjs` y `git diff --check`: aprobados.
- `scripts/test-reading-guide.py`: seis combinaciones de 1440/390/320 px y movimiento normal/reducido, más dos recorridos Tab/Shift+Tab, alternativas sin JS/sin observer y enlaces directos: once casos. Verifica clic/toque, scroll nativo, alineación del cuadro, transición real de transform de 250 ms con curva exacta, reversión rápida, Tab/Enter, cancelación durante movimiento, texto ampliado, cambio de ancho e impresión. Sin desbordamiento ni errores de consola/HTTP en lo comprobado. [Reporte](lectura-report.json).
- `scripts/test-booking.py`: seis casos, ambas rutas a tres anchos, cuatro combinaciones de canal/modalidad por caso y 78 PDFs válidos; estados alternativos, consentimiento, errores, reinicio, texto ampliado, lectura sin JS y enlace de fuente aprobados.
- `scripts/test-step-motion.py`: trece casos aprobados tras acotar su selector de progreso; se mantienen las transiciones de 150 ms de ambas rutas y sus alternativas accesibles.
- Comprobación específica de las entradas de ilustración/propuesta a tres anchos y con ambas preferencias: seis casos aprobados. La propuesta mantiene opacidad 1 y no repite su entrada al volver atrás.
- Inspección de [escritorio](escritorio.png), [móvil](movil.png) y [móvil con texto ampliado](movil-texto-ampliado.png), además de vistas de las tres paradas en `work/reading-guide/`. La guía conserva los roles de color del brief; texto secundario sobre rosa pastel 5,99:1 y contorno burdeo sobre ese fondo 4,89:1, según `docs/paleta-ui.md`.

Se consultaron las Web Interface Guidelines vigentes enlazadas por la skill para la revisión proporcional del diff. Reportes de comprobaciones adicionales y archivos temporales quedan en `work/reading-guide/`, ignorado. Sin dependencias ni servicios externos nuevos. Incremento de fuentes sin comprimir respecto de main: HTML +1356 bytes, JS +5471 bytes, CSS +3822 bytes, total +10649 bytes. No se infiere rendimiento de teléfonos ni tiempos de red desde localhost.

Límites: Chromium local y toque móvil emulado; sin Safari, Firefox, teléfonos físicos, zoom nativo, lector de pantalla o pruebas de comprensión con usuarias. La verificación técnica no acredita validación del servicio. El encargo autoriza subir la rama y abrir el PR; no se fusiona ni se publica en Pages antes de la revisión del equipo.

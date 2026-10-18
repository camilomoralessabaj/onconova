# Aprendizajes en tarjetas · revisión del 18/10/2026

La sección «Aprendizajes, Brechas y Próximos Pasos» pasa de menú lateral y panel horizontal a una pila central. La cabecera completa y el subtítulo quedan centrados; se elimina el párrafo introductorio indicado por el equipo. Los tres bloques de contenido HTML son idénticos a los de la base `51a8868`, incluidos fuentes, tabla, enlaces y límites de evidencia.

## Interacción

Los títulos expuestos son botones independientes de los contenidos, sin controles anidados. Seleccionar una tarjeta alinea inmediatamente el documento con su hito; el siguiente scroll sigue Aprendizajes → Brechas → Próximos pasos o el orden inverso. Las alturas reales y 96 px adicionales permiten terminar cada lectura antes del cambio. La rueda permanece nativa y no hay scroller interno.

El movimiento usa `transform`, 300 ms y el token `--ease-out` existente, con giro leve y profundidad. Las transiciones se pueden invertir sin cola ni bloqueo. El texto permanece opaco y queda estable al terminar. Teclado y movimiento reducido producen cambios estáticos; los contenidos inactivos usan `hidden` e `inert`. Se conservan Anterior/Siguiente y el atajo horizontal táctil opcional.

A menos de 360 px, con texto raíz superior a 18 px o menos de 360 px útiles de alto, se muestran las tres lecturas en flujo. También quedan lineales sin JavaScript, sin observadores y al imprimir. Tab conserva el contenido visitado para que el desplazamiento nativo al enfocar un enlace no oculte su tarjeta.

## Capturas completas

Son capturas de compositor de cada tarjeta completa, incluida la parte que se lee mediante scroll. Los anchos 1440 y 390 corresponden a la ventana de prueba; el recorte muestra la pila central.

| Tarjeta | Escritorio · 1440 px | Móvil · 390 px |
| --- | --- | --- |
| Aprendizajes | [Captura](aprendizajes-tarjetas/aprendizajes-1440.png) | [Captura](aprendizajes-tarjetas/aprendizajes-390.png) |
| Brechas | [Captura](aprendizajes-tarjetas/brechas-1440.png) | [Captura](aprendizajes-tarjetas/brechas-390.png) |
| Próximos pasos | [Captura](aprendizajes-tarjetas/proximos-pasos-1440.png) | [Captura](aprendizajes-tarjetas/proximos-pasos-390.png) |

## Verificación ejecutada

| Comprobación | Resultado |
| --- | --- |
| `node scripts/check.mjs` | 8 etapas, 12 fuentes, 3 metas sin resultados inventados y 15 archivos públicos coherentes. |
| `node scripts/build.mjs` | Sitio preparado en `dist/`. |
| `node --check site/assets/app.js` y `git diff --check` | Aprobados. |
| `python3 scripts/test-reading-guide.py` | [14 escenarios aprobados](aprendizajes-tarjetas/tarjetas-report.json). |
| `python3 scripts/test-section-index.py --output work/qa-section-index` | [8 escenarios aprobados](aprendizajes-tarjetas/indice-report.json). |
| Pruebas complementarias a 1440 y 390 px | [Inversión del scroll durante la transición, PageUp con foco, retorno desde impresión y matrices estáticas con movimiento reducido aprobados](aprendizajes-tarjetas/complementarias-report.json). |
| Impresión final a 1440/390/320 px | Contenido completo, orden y ausencia de contornos de foco o bordes fragmentados; repetida después del ajuste de impresión. PDF revisado mediante extracción de texto y render. |
| Contraste de los usos nuevos | [Entre 5,22:1 y 14,56:1](aprendizajes-tarjetas/contraste.json); controles expuestos de al menos 44 px útiles. |

La matriz de tarjetas cubre selección de las tres lecturas, continuidad inmediata desde cada selección, lectura completa antes de avanzar, retroceso, salida a Fuentes, interrupciones a 35/130 ms, Enter/Espacio y Tab/Shift+Tab, foco visible, enlaces a fuentes y vuelta a la demostración, ampliación de texto y texto al 200 %, historial/recarga, cambio de tamaño, ausencia de JS/observadores, enlaces directos, movimiento reducido e impresión. Incluye zoom nativo del navegador al 200 %: 1440 px externos, 720 px CSS y DPR 2.

No se observaron errores de consola/recursos ni desbordamiento horizontal en la matriz monitorizada. Segunda revisión del diff y de las capturas completada. La corrección de Tab se verificó con navegación completa; el ajuste final de impresión se volvió a comprobar en los tres anchos.

## Límites

Chromium 154 y tacto emulado, sin Safari/Firefox, teléfono físico ni lector de pantalla escuchado. La referencia pública devuelve HTTP 403 del proxy y `Boards.pdf` no estaba disponible; se utilizó la descripción autorizada. El PDF generado por Chromium no está etiquetado. Las baterías de agendamiento no se repitieron porque su código no cambia. No quedan regresiones confirmadas pendientes en el alcance probado; estas comprobaciones técnicas no son validación con usuarias.

La rama se entrega para revisión hacia `main`. No se autoriza ni realiza su integración o publicación.

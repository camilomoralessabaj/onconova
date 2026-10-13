# Trabajar con calidad y coste proporcionado

«Óptimo» significa lograr el objetivo con el contexto, herramientas, esfuerzo y verificaciones que necesita. No es una garantía matemática de menor coste ni de cero errores.

## Antes de cerrar la ruta

1. Lee las fuentes y archivos pertinentes una vez; reutiliza lo aprendido.
2. Pregunta solo decisiones que cambian el resultado. Una a tres preguntas por ronda, preferiblemente con alternativas concretas. Detén la entrevista cuando objetivo, alcance, restricciones y aceptación estén claros.
3. Recomienda una dirección y explica una consecuencia relevante. Si una alternativa cambia el stack, contenido factual o accesibilidad, resuelve ese conflicto antes de convertirla en tarea.
4. Para tareas grandes, divide por resultados coherentes y verificables; un prompt puede incluir fases si las decisiones dependen entre sí. Mantén una tarea por objetivo coherente, sin fragmentar cambios que deban validarse juntos.

## Durante la ejecución prevista

- Selecciona las skills por función; no cargues todos sus archivos por defecto.
- Prefiere capacidades ya instaladas y controles HTML nativos.
- Reutiliza builds y evidencias recientes cuando no se hayan cambiado sus entradas.
- Define un resultado observable por riesgo: por ejemplo, cambio de foco → Tab/Shift+Tab y cabecera; imagen nueva → tamaño, dimensiones, carga y lectura móvil; interacción → estados y consola.
- Da prioridad a fallos funcionales, accesibilidad y respaldo del contenido; después ajusta detalles visuales.
- No presupongas que benchmarks locales equivalen a rendimiento real de visitantes ni que un score automatizado certifica la calidad.
- Haz una revisión del diff separada. En clientes compatibles puede usarse `/review` sobre cambios locales o una rama base; no lo presentes como disponible sin comprobarlo.
- Si la revisión detecta un problema, corrígelo y repite las comprobaciones afectadas. Termina al satisfacer la aceptación y cerrar dudas materiales, sin repetir un ciclo completo por hábito.

## Cobertura proporcional

| Cambio | Comprobación mínima útil | Ampliación cuando se justifica |
| --- | --- | --- |
| Skills y documentación | Metadatos, enlaces y coherencia de instrucciones; herramientas nuevas si las hay | Ensayo manual de casos; no repetir todo el navegador por cambiar solo documentación. |
| Texto y fuentes | Integridad del contenido, respaldo y diff | Navegador si el nuevo texto altera composición o interacción. |
| CSS o composición | Checks del sitio y revisión visual de las superficies afectadas | Móvil estrecho, ampliación de texto, teclado, contraste y movimiento reducido según el cambio. |
| JavaScript o navegación | Estados afectados, errores y enlaces | Smoke test de las dos páginas y pruebas de regresión relevantes. |
| Imágenes y carga | Tamaño transferido, dimensiones, carga y comportamiento visual | Lighthouse o medición repetida con condiciones comparables si hay un problema concreto. |

La revisión automatizada de `revision-landing` aporta regresiones funcionales; la personalidad, comprensión y respaldo factual requieren inspección y juicio. No añadas un framework, una API pagada ni una herramienta de PR para tareas que el entorno ya puede realizar.

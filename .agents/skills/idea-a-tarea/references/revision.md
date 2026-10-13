# Revisión del prompt y del trabajo posterior

## Antes de entregar el prompt

- Otra conversación entiende la tarea sin acceso a este chat.
- Las decisiones son confirmadas o están identificadas como supuestos.
- El objetivo, el alcance y los criterios de aceptación coinciden.
- No se inventan archivos, credenciales, pruebas, contenido o evidencias.
- Modelo y esfuerzo son recomendaciones justificadas y disponibles o condicionadas a disponibilidad.
- El bloque copiable conserva modelo/esfuerzo y objetivo, contexto, restricciones y terminado cuando.
- Las skills seleccionadas tienen una función concreta y respetan el brief.
- El prompt distingue planificación, ejecución, revisión y publicación.
- La verificación puede fallar por un problema real del cambio; no es una lista de checks triviales.

## Para revisar un cambio de Onconova antes de un PR

Usa [docs/code_review.md](../../../../docs/code_review.md) como criterio compartido y `revision-landing` cuando afecte a la página; selecciona las comprobaciones pertinentes, sin repetir una batería completa para cambios solo de documentación.

Desde la raíz del repositorio:

```sh
node scripts/check.mjs
node scripts/build.mjs
git diff --check
git status --short
```

Revisa el diff, incluyendo archivos nuevos, sin sobrescribir trabajo previo. La compilación limpia y regenera solo `dist/`, que está ignorado. No deben aparecer originales privados, transcripciones, credenciales ni `.local/` entre los archivos a publicar.

Para cambios visuales, inicia `node scripts/serve.mjs` y comprueba `/` y `/prototipo/` con peticiones locales y un navegador si está disponible. Verifica los tamaños pertinentes (por ejemplo 1440, 390 y 320 px), zoom/texto ampliado, ausencia de desbordamiento del documento, foco visible y teclado. Comprueba las interacciones afectadas y la consola. Para movimiento, prueba `prefers-reduced-motion`; el contenido debe seguir disponible sin animación y sin depender de JavaScript.

En la maqueta, si se modifica el comportamiento: aceptación/postergación/rechazo, selección de apoyo, espera sin cupo, confirmación simulada y reinicio. Ninguna acción debe contactar un servicio real. Para contenido, corresponde comprobar afirmaciones y fuentes, no solo sintaxis.

Reporta problemas por gravedad y con archivo/línea, consecuencia y reproducción cuando sea posible. Corrige problemas introducidos por el cambio y vuelve a ejecutar únicamente las verificaciones afectadas. Si una prueba no se pudo realizar, indica qué falta; un puerto abierto no demuestra funcionamiento. Las auditorías automáticas no certifican toda la accesibilidad ni validan la solución con usuarias.

Para cambios solo en skills o documentación, revisa metadatos, enlaces locales, instrucciones, versiones y funcionamiento de los scripts que se incorporen. No hace falta repetir una auditoría visual completa si no se ha cambiado la interfaz.

# OncoNova

Landing de storytelling para la Actividad 7.3, CD1201, FCFM, Universidad de Chile.
Lee `docs/brief.md` y `docs/evidencia.md` antes de modificar el relato.

## Contenido

- Mantén el recorrido Desafío → Propuesta → Prototipo → Validación → Resultados → Aprendizajes → Próximos pasos.
- No inventes información, personas, entrevistas, resultados, validaciones, datos, referencias ni alianzas.
- Cada afirmación del proyecto debe apuntar a una fuente de `site/content/project.json`.
- Distingue evidencia primaria, registro documental, escenario simulado, meta y pendiente. Una entrevista sobre necesidades no valida un prototipo.
- Usa el alcance más reciente confirmado por el equipo. Registra contradicciones en `docs/evidencia.md`.
- No publiques transcripciones, datos de salud, nombres de entrevistadas ni originales privados. `.local/` es exclusivamente local y está ignorado.

## Diseño y skills

Antes de crear o cambiar una vista, lee `.agents/skills/frontend-design/SKILL.md` y `.agents/skills/onconova-storytelling/SKILL.md`.
Para revisión visual y accesibilidad, usa `.agents/skills/web-design-guidelines/SKILL.md`.
Prioriza espacios amplios, tipografía de sistema, lectura cómoda para mujeres de 50–59 años, controles de al menos 44 px, contraste AA, zoom y movimiento reducido.
La referencia del equipo es Apple; el diseño debe conservar una voz propia, cercana y clara.
No conviertas esta landing académica en un servicio de salud operativo.

## Trabajo

- Sin dependencias de producción; HTML, CSS y JavaScript nativos.
- `node scripts/serve.mjs`: vista previa en http://127.0.0.1:4173.
- `node scripts/check.mjs`: integridad del contenido, referencias y archivos.
- `node scripts/build.mjs`: copia exclusivamente `site/` a `dist/`.
- Comprueba móvil, escritorio, navegación por teclado y ausencia de errores de consola cuando haya navegador disponible.
- Publicación en GitHub Pages desde `main`; no fuerces pushes ni borres trabajo ajeno.
- Actualiza `docs/iteraciones.md` con cambios sustantivos y su verificación. Documenta límites sin afirmar pruebas no realizadas.

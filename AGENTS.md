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
Para revisar y priorizar calidad antes de cerrar cambios o preparar un PR, usa `.agents/skills/revision-landing/SKILL.md` y `docs/code_review.md`; selecciona comprobaciones según el diff y repite solo las afectadas por una corrección.
Para convertir una idea en una tarea para otro chat, usa `.agents/skills/idea-a-tarea/SKILL.md`: aclara decisiones materiales, confirma la ruta y entrega un prompt con modelo, esfuerzo y verificaciones; no implementes durante esa planificación.
Según el alcance, usa `impeccable` para planificar o criticar, `color-expert` para paleta y contraste, `motion-design` para movimiento y `ui-ux-pro-max` para consultas de patrones. Selecciona las necesarias; el brief y la evidencia prevalecen sobre recomendaciones generales.
Las skills de Emil Kowalski complementan ese trabajo: `emil-design-eng` para acabado de componentes, `apple-design` para claridad y continuidad, `mobile-native` para comportamiento táctil y `break-ui` para casos extremos. Para movimiento, selecciona `animate`, `review-animations`, `improve-animations`, `find-animation-opportunities` o `animation-vocabulary` según necesites implementar, revisar, planificar, explorar o describir. `prototype` crea variantes aisladas en `.local/prototypes/`; `break-ui` mantiene datos y controles de prueba en `.local/break-ui/`. `pick-ui-library` es una consulta explícita y respeta el stack sin dependencias. `animate-expo`, `write-swift` y `ask-sonner` están disponibles para encargos explícitos de esos stacks; no migran la landing ni instalan paquetes por invocación. Consulta los ajustes locales al inicio de cada `SKILL.md`.
Usa `wireframer` para bocetos en `.local/wireframes/` o Markdown, conservando las reglas de producción. No apliques su estilo de boceto globalmente ni añadas frameworks, fuentes remotas o paquetes por defecto. Consulta `docs/skills.md` para uso, versiones y ajustes locales.
Prioriza espacios amplios, tipografía de sistema, lectura cómoda para mujeres de 50–59 años, controles de al menos 44 px, contraste AA, zoom y movimiento reducido.
La referencia del equipo es Apple; el diseño debe conservar una voz propia, cercana y clara.
Las webs y fuentes adicionales están en `docs/repositorios-diseno-y-calidad.md`, incluyendo `https://21st.dev` para explorar componentes y patrones. Evalúa ejemplos según el brief, licencia y accesibilidad y adapta sus ideas al stack nativo del proyecto.
No conviertas esta landing académica en un servicio de salud operativo.

## Trabajo

- Lee `CONTRIBUTING.md` para trabajo en equipo. Usa una rama por tarea y PR hacia `main`; la integración requiere checks pertinentes y revisión de otra persona. Confirma el alcance autorizado de push, PR y merge y respeta las reglas remotas.
- Las skills compartidas se editan en `.agents/skills/`. Claude Code usa `CLAUDE.md` y `node scripts/sync-claude-skills.mjs` para generar copias locales ignoradas. No mantengas dos versiones de las instrucciones.

- Sin dependencias de producción; HTML, CSS y JavaScript nativos.
- `node scripts/serve.mjs`: vista previa en http://127.0.0.1:4173.
- `node scripts/check.mjs`: integridad del contenido, referencias y archivos.
- `node scripts/build.mjs`: copia exclusivamente `site/` a `dist/`.
- `node scripts/check-skills.mjs`: estructura y huellas de las skills incluidas; ejecutar al modificar o actualizar skills.
- Comprueba móvil, escritorio, navegación por teclado y ausencia de errores de consola cuando haya navegador disponible.
- Publicación en GitHub Pages desde `main`; no fuerces pushes ni borres trabajo ajeno.
- Actualiza `docs/iteraciones.md` con cambios sustantivos y su verificación. Documenta límites sin afirmar pruebas no realizadas.

---
name: idea-a-tarea
description: Convertir una idea en una tarea clara para ejecutar en otra conversación de Codex o Claude Code. Usar cuando el usuario quiera preparar un prompt, aclarar requisitos, confirmar una dirección de diseño, elegir modelo y esfuerzo, definir criterios de aceptación o planificar una revisión antes de un PR. Hace preguntas útiles, confirma la ruta y entrega un prompt autónomo con verificaciones. No implementa la idea durante la planificación.
metadata:
  version: "1.2.0"
---

# De idea a tarea revisable

Trabaja en el idioma del usuario. El resultado es una ruta acordada y un prompt que otra conversación pueda ejecutar sin depender de esta. La planificación puede reducir errores; no garantiza su ausencia.

Lee [guia-oficial.md](references/guia-oficial.md) para aplicar y verificar las recomendaciones oficiales de OpenAI. Consulta la guía de ChatGPT indicada por el usuario cuando haya acceso; si no puedes leerla, informa ese límite y no atribuyas a esa página recomendaciones no comprobadas.

## 1. Leer antes de preguntar

Inspecciona el repositorio y sus instrucciones con acciones de lectura: AGENTS.md, README, manifiestos, scripts de verificación y archivos pertinentes. Para Onconova lee también `docs/brief.md`, `docs/evidencia.md` y `site/content/project.json` cuando la idea afecte relato, contenido o diseño. Usa el checkout existente; cada tarea cloud ya está aislada, no crees un worktree por defecto.

Extrae objetivo, audiencia, alcance, restricciones, evidencia disponible y resultado observable. Distingue requisitos confirmados, preferencias y supuestos. Reutiliza las respuestas del usuario; no vuelvas a preguntar lo que ya está resuelto. Si el usuario pide solo planificar, no edites el producto, no instales dependencias ni ejecutes su implementación. Puedes guardar el prompt cuando se solicite; evita incluir información privada.

## 2. Preguntar lo que cambia la decisión

Agrupa de una a tres preguntas por ronda. Prioriza las que afecten al resultado:

- ¿Qué debe entender o poder hacer la persona al terminar?
- ¿Qué página, sección o interacción entra en el cambio y qué queda fuera?
- Para diseño: ¿se conserva la identidad actual o se busca otra dirección? ¿Hay una referencia concreta y qué aspecto importa de ella?
- ¿Qué textos, imágenes y datos están disponibles y cuáles requieren confirmación?
- ¿Qué resultado permitiría aceptar la tarea? ¿Se espera solo código local o también preparar un PR?

No hagas un cuestionario entero si el contexto ya responde. Ofrece dos o tres opciones concretas con una recomendación y su consecuencia. Usa `request_user_input_async` si está disponible; sigue leyendo contexto mientras esperas. Si hay una decisión indispensable pendiente, no la inventes. Puedes entregar un borrador rotulado como pendiente, pero no lo presentes como ruta confirmada. Una preferencia opcional sin respuesta admite un supuesto explícito. Si el usuario delega la elección o ya describe una ruta suficiente, toma esa autorización y evita confirmaciones repetidas.

Para «más personalidad», traduce el deseo en decisiones comprobables: un elemento distintivo, jerarquía, composición, paleta y ritmo. Describe dos direcciones si hay ambigüedad. Conserva las restricciones de accesibilidad y la audiencia; una referencia no autoriza copiar marca, inventar resultados o cambiar el stack.

## 3. Confirmar una propuesta concreta

Resume en un párrafo la ruta, el alcance, lo que se preserva, el rasgo visual distintivo si aplica y cómo se verificará. Confirma esta propuesta cuando exista una decisión material aún abierta. Usa la respuesta para cerrar la ruta. La confirmación corresponde al objetivo de esta skill, no a una exigencia de permiso para lecturas o verificaciones locales. No conviertas guardar un borrador de configuración cloud en una aprobación de esta ruta.

## 4. Elegir modelo, esfuerzo y skills

Lee [modelos-y-esfuerzo.md](references/modelos-y-esfuerzo.md) y [trabajo-optimo.md](references/trabajo-optimo.md). Identifica el cliente de destino (Codex o Claude Code) por el encargo y pregunta solo si cambia materialmente la entrega. Recomienda un modelo disponible y un nivel de esfuerzo con una justificación breve basada en complejidad, incertidumbre y consecuencias. No afirmes que un modelo o un selector están disponibles sin comprobarlo. Empieza con el esfuerzo predeterminado cuando sea adecuado y explica cualquier aumento; no selecciones siempre el máximo. Si no hay catálogo verificable, usa una recomendación condicionada compatible con el cliente de destino, sin bloquear las preguntas y la planificación. Los modelos y niveles de Codex no se trasladan automáticamente a Claude Code.

Elige solo las skills necesarias, con orden y función. En Onconova:

- Relato y hechos: `onconova-storytelling`.
- Dirección visual: `frontend-design` como base; `impeccable` para planificar o criticar según el encargo.
- Estructura previa: `wireframer` si hace falta, en `.local/wireframes/` o bocetos sin dependencias.
- Paleta y contraste: `color-expert`; movimiento justificado: `motion-design`.
- Consulta puntual de patrones: `ui-ux-pro-max`; revisión de interfaz: `web-design-guidelines`.
- Comprobar calidad y regresiones de la landing antes de cerrar o preparar un PR: `revision-landing`, con verificaciones seleccionadas según los archivos y comportamiento afectados.
- Detalle de interacción: `emil-design-eng`; principios Apple: `apple-design`; tacto y viewport: `mobile-native`; casos extremos: `break-ui`. Para movimiento, elige `animate`, `review-animations`, `improve-animations`, `find-animation-opportunities` o `animation-vocabulary` según la fase. Consulta `docs/skills.md` para el inventario completo y evita los stacks ajenos a la landing.

No actives todas las skills para una tarea simple. Las instrucciones explícitas y el brief del proyecto prevalecen sobre sus recomendaciones generales. Una skill no autoriza publicación, push, envío de información ni instalación de un framework.

## 5. Escribir y revisar el prompt

Usa [plantilla-prompt.md](references/plantilla-prompt.md). Completa cada apartado con datos concretos; elimina los que no apliquen. El prompt debe incluir los cuatro elementos de la guía oficial: objetivo, contexto, restricciones y «terminado cuando». Añade alcance, pasos, revisión y entrega si aportan. Indica cliente, recomendación de modelo/esfuerzo antes del bloque y dentro de su encabezado copiable para conservarlos al cambiar de chat; explica que se seleccionan en el cliente y que el texto no cambia el motor automáticamente. Para trabajo de equipo, incluye la tarea o issue si existe, rama de trabajo, base `main`, revisión humana por otra persona y alcance autorizado de la entrega; respeta `CONTRIBUTING.md`.

Comprueba el prompt contra [revision.md](references/revision.md): contradicciones, hechos sin respaldo, dependencias implícitas, rutas inexistentes, aceptación ambigua, comprobaciones imposibles y permisos no concedidos. Si encuentras problemas, corrige el prompt antes de entregarlo. Si queda una pregunta indispensable, marca el estado y lo que depende de su respuesta.

El chat ejecutor debe investigar fallos y corregir los causados por su cambio; no puede saltar tests o afirmar pruebas no ejecutadas. Si encuentra un defecto previo o un bloqueo externo, debe distinguirlo y explicar la evidencia. No prometer «cero errores». Usar una segunda pasada de revisión sobre el diff, separada de la implementación, sin exigir subagentes ni servicios externos. Preparar una descripción de PR es parte de la entrega cuando corresponda; crear el PR, hacer push, merge o publicar solo si el usuario lo autoriza.

Asocia cada riesgo material con una comprobación observable y el resultado esperado. Usa los tests existentes; crea o amplía tests cuando falte cobertura relevante, sin generar pruebas triviales para cambios de texto o estilo. Después de una corrección repite los checks afectados; amplía la verificación solo si hay un fallo nuevo o una duda pendiente. Da por terminada la tarea cuando el alcance, la revisión y las comprobaciones pertinentes estén resueltos, o declara el bloqueo preciso. No añadas rondas ilimitadas de pulido.

## 6. Entregar para el siguiente chat

Entrega en este orden: ruta y estado (confirmada o borrador), modelo/esfuerzo y razón, prompt completo en un bloque copiable, y las preguntas pendientes si existen. No implementes la idea al entregar el prompt salvo que el usuario amplíe expresamente el encargo. Una vez completos los datos y la revisión, termina sin ofrecer pasos indefinidos.

Consulta [ejemplos.md](references/ejemplos.md) para calibrar preguntas y aceptación. Esos ejemplos son casos de ensayo, no decisiones reales del equipo ni pruebas de validación del servicio.

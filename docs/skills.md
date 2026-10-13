# Skills de diseño y preparación de tareas

Instalación local al proyecto: 24 skills, revisadas el 10/10/2026. Los archivos están en `.agents/skills/`; abre una nueva conversación de Codex en este repositorio para usarlos. Si el cliente no los descubre automáticamente, pide leer el `SKILL.md` por su ruta. No son dependencias del sitio y `scripts/build.mjs` no los publica.

Compatibilidad de equipo preparada el 13/10/2026: la fuente común sigue en `.agents/skills/`. Codex usa `AGENTS.md`; Claude Code importa esas reglas desde `CLAUDE.md` y genera su ubicación de descubrimiento con `node scripts/sync-claude-skills.mjs`. Las copias de `.claude/skills/` quedan ignoradas y se actualizan después de pull o cambios de rama. El uso de ramas, revisión humana y configuración de GitHub está en [CONTRIBUTING.md](../CONTRIBUTING.md). Versiona los archivos compartidos mediante PR para que otros clones los reciban; el snapshot cloud de una persona no los distribuye.

`idea-a-tarea` 1.2.0 prepara prompts para Codex o Claude Code e identifica el cliente de destino antes de recomendar modelo/esfuerzo. En Codex puedes invocarla como `$idea-a-tarea`; en Claude como `/idea-a-tarea` si el cliente descubre la copia. En ambos puedes pedir que lea `.agents/skills/idea-a-tarea/SKILL.md`. Seleccionar el modelo y esfuerzo corresponde al cliente de quien ejecute el prompt.

## Qué está instalado

| Skill | Fuente | Para qué usarla |
| --- | --- | --- |
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Identidad y composición específicas del proyecto, jerarquía y autocrítica. Ya estaba instalada y coincide con la fuente consultada; se preservó. |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Planificar (`shape`), criticar (`critique`), auditar (`audit`) y refinar una interfaz. El nombre oficial tiene doble c: Impeccable. |
| `wireframer` | [agilek/wireframer-skill](https://github.com/agilek/wireframer-skill) | Bocetos de estructura y navegación antes de pulir la interfaz. |
| `color-expert` | [meodai/skill.color-expert](https://github.com/meodai/skill.color-expert) | Paletas, roles semánticos, color perceptual y contraste. |
| `motion-design` | [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | Timing, easing y movimiento con propósito; incluye principios aplicables a CSS nativo. |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Consulta local de estilos, patrones y pautas de UX con datos y scripts Python. |
| `web-design-guidelines` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) | Revisión de accesibilidad, interacción, responsive y rendimiento; ya existente. |
| `onconova-storytelling` | Elaboración propia | Relato, fuentes, estados de evidencia y límites de la propuesta; ya existente. |
| `idea-a-tarea` | Elaboración propia | Aclarar una idea, confirmar la ruta y preparar un prompt para otro chat con modelo, esfuerzo, aceptación y revisión antes de PR. |
| `revision-landing` | Elaboración propia | Revisar calidad y regresiones, priorizar optimización y seleccionar checks según el diff; incluye prueba funcional local de la landing. |

Las seis primeras fuentes y las 14 skills de Emil Kowalski tienen commit exacto y huellas de los archivos locales en [sources.lock.json](../.agents/skills/sources.lock.json). Se conservaron licencias y avisos disponibles: Apache 2.0 para Frontend Design e Impeccable, CC BY 4.0 para Color Expert y MIT para Motion Design, UI UX Pro Max y las skills de Emil Kowalski. Wireframer declara MIT en su README, pero la fuente consultada no incluye un archivo LICENSE separado; se conserva esa declaración sin inventar términos adicionales.

## Skills de Emil Kowalski

Se integraron las 14 skills de [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d), fijadas al commit `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`. Todas incluyen el aviso MIT de Emil Kowalski, sus referencias locales y un bloque inicial de integración en Onconova. No requieren ejecutar un instalador ni instalar paquetes para consultar sus instrucciones.

| Skill | Para qué usarla |
| --- | --- |
| `emil-design-eng` | Acabado de componentes, estados y detalles de interacción. Incluye el cheatsheet de rendimiento upstream. |
| `apple-design` | Claridad, respuesta inmediata, continuidad espacial y principios de diseño de Apple aplicados a la web. |
| `animate` | Implementar una animación concreta, primero evaluando si hace falta; preferir CSS o WAAPI. |
| `review-animations` | Revisar el movimiento de un diff con ubicaciones y hallazgos confirmados. |
| `improve-animations` | Auditar movimiento y escribir planes autónomos; combinar con `idea-a-tarea` para otro chat. |
| `find-animation-opportunities` | Buscar oportunidades justificadas y reconocer superficies que conviene mantener estáticas. |
| `animation-vocabulary` | Convertir una descripción vaga de un efecto en un término preciso para el prompt. |
| `mobile-native` | Revisar viewport, tacto, hover, teclado y áreas seguras sin perjudicar lectura o zoom. |
| `break-ui` | Probar texto largo, campos ausentes, tamaños extremos y ampliación de texto con fixtures aislados. |
| `prototype` | Comparar variantes funcionales con un selector en `.local/prototypes/`, mediante invocación explícita. |
| `pick-ui-library` | Consultar bibliotecas de UI, mediante invocación explícita y respetando el stack nativo. |
| `ask-sonner` | Resolver tareas de React con Sonner; disponible para ese stack, que la landing actual no usa. |
| `animate-expo` | Animación y gestos en React Native/Expo, para un encargo explícito de app móvil. |
| `write-swift` | Guía de Swift para un encargo explícito, comprobando compilador y disponibilidad de las APIs. |

Los ajustes locales preservan el brief, fuentes y autorizaciones existentes. Permiten estados estáticos o solo opacidad con movimiento reducido; los gustos de easing o sombras no se convierten automáticamente en errores. Las afirmaciones de aceleración por GPU y los ejemplos de bibliotecas se contrastan con el navegador y la versión real antes de afirmarlas como comprobadas.

Se revisaron también Sonner y Vaul a petición del usuario. Ambas bibliotecas requieren React y no son necesarias para las interacciones actuales. `ask-sonner` aporta la guía solicitada para un encargo compatible; Vaul declara falta de mantenimiento en su README. La [evaluación de requisitos y decisión](repositorios-diseno-y-calidad.md#evaluación-de-sonner-y-vaul--10102026) conserva los commits y limita su uso como referencias.

`prototype` adapta el selector original a foco visible, etiquetas legibles y objetivos de al menos 44 px. `break-ui` guarda datos ficticios rotulados y controles en `.local/break-ui/`, sin mezclarlos con la evidencia. `improve-animations` usa `.local/animation-plans/` y el checkout aislado existente; la landing pequeña no requiere delegación para auditarla. La instalación no incluye toolchains Swift/Expo ni pruebas en teléfonos físicos. Los ajustes y los archivos copiados están registrados en el lock.

## Elegir una combinación útil

Usa `idea-a-tarea` cuando aún estás decidiendo el encargo. Usa `frontend-design` y `onconova-storytelling` como base al editar una vista o su relato. Añade `impeccable` para planificación o crítica; `wireframer` si la estructura está sin resolver; `color-expert` si cambia la paleta, y `motion-design` si el movimiento tiene una función. Usa `ui-ux-pro-max` para una consulta concreta; `revision-landing` para organizar la revisión final y `web-design-guidelines` para las pautas de interfaz. No hace falta cargar todas para cada cambio.

La personalidad debe surgir de las decisiones del proyecto: composición, jerarquía, recursos propios y un detalle memorable. Instalar skills no cambia automáticamente el sitio ni garantiza calidad visual. El brief vigente conserva tipografía de sistema, lectura cómoda para mujeres de 50–59 años, siete etapas, contraste AA, controles de al menos 44 px y movimiento reducido. No adoptar un stack, una paleta o una animación solo porque una skill los recomiende.

Para tareas de Emil, usa `emil-design-eng` para detalle de interacción y `apple-design` cuando sea útil esa referencia. Una tarea de movimiento puede pasar de `animation-vocabulary` o `find-animation-opportunities` a `improve-animations` para el plan, `animate` para ejecutarlo y `review-animations` para revisarlo; selecciona las etapas necesarias. `motion-design` sigue aportando intención y narrativa del movimiento. Añade `mobile-native` o `break-ui` cuando el diff introduzca riesgos táctiles o de contenido variable; `revision-landing` coordina la revisión general.

## Ajustes locales respecto de upstream

- **Impeccable:** se eligió la distribución nativa de Codex (`.agents/skills/impeccable`), con sus definiciones de agentes; se ajustó el texto de su interfaz y se documentó la precedencia del brief y una caché en `.local/impeccable`. Se conservan launcher, referencias y datos. No se instalaron hooks automáticos ni extensiones de navegador. `shape` o un rediseño pueden pedir capturar `PRODUCT.md`; reutiliza los hechos del brief y pregunta solo por decisiones pendientes. Una crítica o un refinamiento acotado puede usar la implementación actual.
- **Wireframer:** se reemplazó la obligación de añadir reglas de boceto globales a los archivos de instrucciones. En Onconova los bocetos quedan en `.local/wireframes/` o Markdown y usan componentes nativos. Los ejemplos de Wired Elements, React, CDN y fuentes manuscritas son opcionales para otro prototipo autorizado; no son requisitos del sitio.
- **UI UX Pro Max:** se cambiaron las rutas que dependían de `CLAUDE_PLUGIN_ROOT` por la instalación local y se aclaró que la consulta no autoriza añadir Tailwind, GSAP o Google Fonts.

Los cambios están registrados en el lock de fuentes. Las recomendaciones de terceros no sustituyen las instrucciones del usuario ni la evidencia del proyecto.

## Invocación

```text
Usa $idea-a-tarea. Mi idea es: [explica qué quieres mejorar].
Hazme las preguntas necesarias, confirma la ruta y entrega un prompt listo
para otro chat, recomendando modelo y esfuerzo disponibles y las pruebas
que necesita el cambio. Por ahora prepara la tarea.
```

```text
Usa $impeccable para una crítica de la portada: jerarquía, identidad propia
y claridad del relato, respetando docs/brief.md. Entrega hallazgos antes de editar.
```

```text
Usa $wireframer para comparar dos estructuras de la portada en bocetos
Markdown, preservando el contenido y sin instalar dependencias.
```

```text
Usa $revision-landing para revisar estos cambios antes de preparar un PR.
Comprueba los riesgos que introduce el diff y prioriza las mejoras necesarias.
```

```text
Usa $emil-design-eng y $apple-design para revisar los detalles de interacción
de la portada respetando docs/brief.md. Entrega hallazgos con ubicación.
```

```text
Usa $improve-animations y $idea-a-tarea para preparar una mejora del movimiento
en otro chat. Incluye modelo, esfuerzo, aceptación y revisión de animaciones.
```

```text
Usa $prototype para explorar tres estructuras del encabezado en
.local/prototypes/portada/, con contenido del proyecto y un selector accesible.
```

```text
Usa $break-ui para comprobar texto largo y ampliado en la portada,
con datos de prueba aislados. Usa $revision-landing para la revisión general.
```

Ejemplo de consulta probada desde la raíz del repositorio:

```sh
PYTHONDONTWRITEBYTECODE=1 python .agents/skills/ui-ux-pro-max/scripts/search.py "keyboard focus visible" --domain ux
IMPECCABLE_HOME="$PWD/.local/impeccable" .agents/skills/impeccable/scripts/impeccable context --target site/index.html
node scripts/check-skills.mjs
```

UI UX Pro Max requiere Python 3, sin paquetes externos para esa consulta. El motor de Impeccable se descargó mediante su launcher con comprobación SHA-256 y TLS, y respondió `impeccable-engine 0.1.14`. Su caché local está ignorada y no va al sitio. Los procesos o integraciones de navegador no se activan por instalar la skill.

## Guía oficial y verificación

Se pudo leer completa [ChatGPT best practices](https://learn.chatgpt.com/guides/best-practices) por HTTPS con HTTP 200, tras el bloqueo del turno anterior. `idea-a-tarea` aplica sus cuatro elementos: objetivo, contexto, restricciones y terminado cuando. Conserva modelo y esfuerzo en el bloque copiable, recomienda niveles proporcionados, limita preguntas a decisiones materiales y elige verificaciones según riesgo. La guía de OpenAI Cookbook antes usada queda como referencia secundaria. Los detalles están en [guia-oficial.md](../.agents/skills/idea-a-tarea/references/guia-oficial.md).

La primera instalación validó nueve skills; se llegó a diez al añadir `revision-landing` y a 24 con las 14 skills de Emil Kowalski. Las copias externas siguen verificadas por huellas locales. Se probaron la búsqueda de UX y la carga de contexto de Impeccable. Los escenarios de `idea-a-tarea` se [ensayaron manualmente](../.agents/skills/idea-a-tarea/evals/revision-manual.md), incluyendo un quinto caso de eficiencia, sin benchmark independiente entre modelos. La interfaz no se modificó al instalar estas herramientas. Consulta [repositorios-diseno-y-calidad.md](repositorios-diseno-y-calidad.md) y [la investigación del tema landing-page](investigacion-landing-page.md).

`revision-landing` usa [docs/code_review.md](code_review.md) y ofrece un smoke test con Playwright Python y Chromium ya presentes en el entorno. Sus informes y capturas se guardan en `.local/revision-landing/`, fuera del sitio publicado. El smoke test tiene cobertura funcional concreta; la calidad visual, contraste completo y comprensión requieren revisión adicional.

En su ejecución de validación pasaron cinco de seis casos y se detectó un [desbordamiento existente en móvil con texto ampliado](hallazgos-landing.md). La herramienta detecta y reporta ese fallo; no modifica el sitio ni lo presenta como resuelto. También se comprobaron sus salidas de error y los prerrequisitos ausentes.

No actualizar automáticamente las skills durante la compilación. Para una actualización, revisa origen, commit, licencia, scripts y diff; reaplica solo los ajustes necesarios, registra las nuevas huellas y ejecuta `node scripts/check-skills.mjs`.

La comprobación de transferencia del 13/10/2026 sobre `main` (`8d3da91`, rediseño de Sites) aprobó los seis casos del smoke test. El desbordamiento documentado en la versión anterior no se reprodujo. Se conservaron el rediseño y sus doce archivos públicos; el parche solo añade configuración, skills y documentación.

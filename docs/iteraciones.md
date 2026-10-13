# Iteraciones de la primera versión

Fecha: 10 de octubre de 2026. Trabajo realizado con apoyo de Codex, a partir del material del equipo y de sus aclaraciones. Este registro describe cambios y verificaciones del sitio; no es un resultado de validación del servicio con usuarias.

| Iteración | Instrucción y cambio | Evidencia o comprobación |
| --- | --- | --- |
| 1. Ordenar el relato | Construir las siete etapas de la actividad y asociar cada una con sus fuentes. | Se revisaron 36 documentos legibles de Drive; el inventario y sus límites están en `evidencia.md`. |
| 2. Resolver el alcance | Usar una derivación prioritaria al apoyo pertinente, conservar autonomía y evitar una fundación como solución. | Alcance y restricciones confirmados por el equipo. Institución piloto por definir. |
| 3. Hacer el servicio prototipable | Crear una conversación, una ficha y un seguimiento que distinga solicitud, espera y atención. | Se creó una maqueta conceptual digital e imprimible. No se la presentó como una solución probada. |
| 4. Hacer visible la evidencia | Separar entrevistas reales, escenarios simulados, propuesta nueva y metas. Incorporar el póster propio como antecedente. | Las cinco entrevistas exploran necesidades; el RIA tiene resultados vacíos. El póster histórico se rotuló como antecedente de una simulación previa. |
| 5. Ajustar lectura e interacción | Aplicar jerarquía visual, navegación por etapas, controles grandes y ampliación de texto. | Inspección en navegador de escritorio y móvil. Se aumentó a 20 px el texto principal de la portada y los párrafos principales en móvil. |

## Verificación técnica

- Integridad del contenido: siete etapas ordenadas, nueve fuentes, tres metas propuestas sin resultados observados y estados pendientes coherentes.
- Referencias locales: enlaces, fragmentos, imágenes con dimensiones y textos alternativos; no se incluyen originales privados en el sitio.
- Interacción: la postergación y el rechazo no activan una derivación; la espera sin cupo mantiene pendiente la atención. Se comprobó cambio del apoyo, reinicio y confirmación simulada.
- Lectura: portada y maqueta inspeccionadas en escritorio y en anchos de 375 y 320 px. También se comprobó 320 px con texto ampliado. No hubo desbordamiento horizontal del documento; la navegación de etapas usa su propio desplazamiento horizontal.
- Teclado: se comprobó desplazamiento con Tab y foco visible de 3 px. Los enlaces a una fuente abren su contenedor plegado; los controles tienen nombres accesibles.
- No se observaron errores ni advertencias de consola durante los recorridos comprobados.
- La skill propia `onconova-storytelling` pasó el validador de Skill Creator.

El entorno restringido de Windows negó `realpath` a Node aunque permitía leer los archivos. La compilación y la vista previa funcionaron al ejecutarse fuera de esa restricción, sin eliminar las comprobaciones de rutas del proyecto. En un entorno Node normal, los comandos no requieren esa excepción.

## Lo que falta validar en el proyecto

La claridad del servicio con usuarias, su factibilidad con profesionales, los responsables, los canales, la disponibilidad y el costo operativo. Las pruebas de navegador solo comprueban el sitio y la simulación; no prueban que el servicio mejore el acceso a atención.

## Skills y preparación de tareas · 10/10/2026

Se preservó Frontend Design y se instalaron Impeccable, Wireframer, Color Expert, Motion Design y UI UX Pro Max con commits y huellas registrados. Los ajustes locales mantienen el stack nativo, el brief y los bocetos fuera del sitio publicado. Se creó `idea-a-tarea` para preguntas de aclaración, confirmación de ruta y prompts para otro chat, con recomendación de modelo/esfuerzo y revisión antes de PR. `docs/skills.md` documenta invocación y límites; `docs/repositorios-diseno-y-calidad.md` reúne fuentes verificadas y recomendaciones complementarias.

Las nueve skills pasaron la validación de metadatos. La búsqueda local de UX devolvió reglas de foco de teclado y el motor verificado de Impeccable cargó el contexto del sitio. No se cambió la interfaz ni se instalaron dependencias de producción. Los cuatro escenarios de la skill propia se ensayaron manualmente por el mismo autor; no se ejecutó un benchmark independiente entre modelos. Pasaron los checks de skills, contenido y compilación, y se guardaron los pasos actualizados de preparación y arranque en el borrador del entorno.

La guía oficial de ChatGPT solicitada devolvió HTTP 403 por la política de red. Se guardó `learn.chatgpt.com` como destino del borrador y quedó pendiente aplicar el cambio y leer esa página. Se consultó una referencia oficial distinta de OpenAI Cookbook y se registró esa diferencia, sin atribuir contenido no leído a la guía de ChatGPT.

## Planificación eficiente y revisión de landing · 10/10/2026

La guía exacta de ChatGPT ahora respondió HTTP 200 y se leyó completa. Se actualizó `idea-a-tarea` con sus cuatro elementos (objetivo, contexto, restricciones y terminado cuando), modelo/esfuerzo conservados en el prompt copiable y verificaciones proporcionales al riesgo. Se añadió un quinto ensayo de planificación para cambios simples; no se realizaron benchmarks independientes entre modelos.

Se revisó el tema `landing-page` de GitHub: 20 descripciones de la primera página y fuentes de candidatos pertinentes. UI UX Pro Max ya estaba instalada; las colecciones DESIGN.md quedan como referencias. El motor de Scrollcraft no se añadió por sus requisitos de experiencias de scroll y el brief vigente. Se creó `revision-landing` y `docs/code_review.md`, con un smoke test local y criterios para priorizar calidad y carga.

Las diez skills pasaron validación de metadatos, interfaces y enlaces. El smoke test final produjo cinco aprobados y un fallo existente a 320 px con texto ampliado; se diagnosticó y registró en `docs/hallazgos-landing.md`, sin editar `site/`. También detectó HTTP 404 y un navegador ausente con salidas de error correctas. Pasaron integridad de contenido y build. No se incorporaron dependencias de producción ni se publicó la página.

## Skills de Emil Kowalski y bibliotecas opcionales · 10/10/2026

Se integraron las 14 skills de `emilkowalski/skills`, commit `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`, con sus referencias y el aviso MIT en cada carpeta. El conjunto local pasó de diez a 24 skills. Se añadieron bloques explícitos de integración: stack nativo, accesibilidad, movimiento reducido con estados estáticos válidos, alcance autorizado y pruebas proporcionales. Los prototipos y fixtures quedan fuera del sitio; las guías Expo, Swift y Sonner se reservan para tareas compatibles. Se preservaron las seis entradas externas anteriores del lock y se registraron los ajustes y huellas de las nuevas copias.

Se revisaron también los README, manifiestos y licencias de Sonner y Vaul. No se incorporaron sus paquetes: requieren React y las interacciones actuales ya usan estados nativos con `aria-live`. La guía `ask-sonner` está incluida. El README de Vaul declara falta de mantenimiento; la evaluación con commits y requisitos está en `docs/repositorios-diseno-y-calidad.md`.

Comprobaciones ejecutadas: 24 frontmatters YAML válidos, 14 enlaces locales de las nuevas skills resueltos, 14 licencias MIT preservadas y 393 archivos externos coincidentes con el lock. Pasaron `node scripts/check-skills.mjs`, `node scripts/check.mjs` y `node scripts/build.mjs`. Las huellas de todos los archivos de `site/` siguen iguales a las anteriores a esta integración. No se repitieron recorridos de interfaz porque la tarea cambió instrucciones y documentación; el desbordamiento existente registrado en la iteración anterior continúa pendiente. No se probaron toolchains móviles ni hardware físico.

## Web de referencia 21st.dev · 10/10/2026

Se añadió 21st.dev a las referencias de diseño y plataformas y a las instrucciones del repositorio. Se guardaron `21st.dev` y `www.21st.dev` en la lista de destinos del borrador del entorno, conservando `learn.chatgpt.com` y el preset de gestores de paquetes. El guardado devolvió `status: saved` y `requires_publish: true`; no confirma publicación ni acceso en una nueva máquina. La consulta HTTPS previa devolvió HTTP 403 del proxy y el catálogo actual sigue pendiente de consulta tras aplicar la política. No se instalaron componentes, paquetes, skills ni servicios de 21st.dev. La comprobación del diff no encontró errores de espacios.


## Integración de la versión de revisión de Sites

Fecha: 13 de octubre de 2026. Se importó el contenido estático de **OncoNova · Versión de revisión**, proyecto `appgprj_6acad48d5b3881918dcd6105d2dbfd8e`, desde el commit de origen `8e51252cb27991b1fc4af1f6bd6aedeb963ade35`.

Los doce archivos de `dist/` en Sites se incorporaron a `site/`, la carpeta fuente que utiliza este repositorio para GitHub Pages. El rediseño incorpora dos ilustraciones SVG, una marca revisada, una paleta rosa y ciruela, iconos SVG, etiquetas de evidencia y ajustes de lectura y adaptación de la landing y la maqueta. Se conservan el registro de fuentes, los estados conceptuales y la lógica de interacción. Los scripts, la documentación del proyecto y el historial de GitHub siguen disponibles.

Verificación de esta integración:

- `node scripts/check.mjs`: siete etapas, nueve fuentes y tres metas propuestas coherentes; dos páginas y doce archivos públicos con enlaces y anclas válidos.
- `node scripts/build.mjs`: preparación correcta de `dist/`. El contenido de `site/` coincide archivo por archivo con el `dist/` recuperado de Sites.
- `node --check` en ambos módulos JavaScript y `git diff --check`: sin errores.
- Chromium, con rutas bajo `/onconova/`: landing y maqueta revisadas a 1440, 375 y 320 px. Sin desbordamiento horizontal, también con el texto ampliado; imágenes visibles cargadas y foco de teclado visible.
- Se comprobó la elección en la landing, la apertura de fuentes por enlace y los escenarios de postergación, rechazo, espera sin cupo, atención simulada y reinicio. No se observaron errores de consola ni respuestas HTTP fallidas durante esos recorridos.
- Inspección visual de la portada en escritorio y a 320 px. Estas comprobaciones verifican la integración web; no constituyen validación del servicio con usuarias.

## Colaboración con Codex y Claude Code · 13/10/2026

Se prepararon `CONTRIBUTING.md`, una plantilla de PR y `CLAUDE.md`, que importa las reglas comunes de `AGENTS.md`. Las skills mantienen su fuente en `.agents/skills/`; `scripts/sync-claude-skills.mjs` genera copias ignoradas en `.claude/skills/` sin enlaces simbólicos ni dependencias adicionales. Se actualizó `idea-a-tarea` a 1.2.0 para prompts destinados a Codex o Claude Code, modelo/esfuerzo compatibles con el cliente y contexto de rama/PR. El workflow incorpora verificación de skills y limita también las publicaciones manuales a `main`.

Pasaron checks de contenido, compilación y skills (24 skills y 393 archivos externos verificados). Se comprobaron las 410 copias para Claude y sus permisos, la repetición de la sincronización y un fixture con actualización/retirada de copias propias, conservación de una skill personal y rechazo de una colisión antes de modificar archivos. El YAML del workflow se pudo leer y contiene las guardas y comprobaciones previstas. No se ejecutaron Claude Code ni GitHub Actions remoto y no se modificó `site/`.

Las reglas remotas, invitaciones, code owners y merges quedan para la administración del repositorio según la guía. No se creó un PR ni se hizo push; los archivos compartidos aún requieren versionarse y distribuirse mediante Git. Se consultó documentación oficial de GitHub sobre rulesets y CODEOWNERS. Las páginas de Claude Code fueron rechazadas por la política del proxy y quedan enlazadas como referencias para consulta del equipo.

## Ruleset importable de main · 13/10/2026

Se creó `.github/rulesets/protect-main.json` para importar en GitHub, con estado activo y alcance exacto `refs/heads/main`. Exige PR, una aprobación, descarte de aprobaciones obsoletas, conversaciones resueltas, squash e historial lineal; bloquea borrado y force push, sin actores con bypass. Exige `build` de GitHub Actions y actualización respecto de la base. La aprobación de code owners queda desactivada hasta acordar responsables.

El JSON pasó validación contra el esquema oficial de creación de rulesets del repositorio `github/rest-api-description`; se comprobó que `build` coincide con el job del workflow y que se ejecuta en PR. Se documentó cómo importar y activar el archivo en `CONTRIBUTING.md`. No se importó ni activó una regla remota desde esta conversación; esa operación queda para el usuario.

## Transferencia de configuración a main actualizado · 13/10/2026

Se contrastó el entorno de preparación, basado en `965a42c`, con `main` remoto en `8d3da91`. La configuración y las 24 skills estaban en archivos sin commit del primero y no en GitHub. Se preparó un parche sobre `8d3da91`, conservando todos los archivos de `site/` del rediseño y combinando los historiales de iteraciones. Pasaron checks de contenido (doce archivos públicos), build, las 24 skills y 393 huellas externas, y sincronización para Claude. La prueba de navegador de las dos páginas a 1440, 390 y 320 px produjo seis aprobados; el desbordamiento registrado en la versión anterior no se reprodujo. El parche no crea un commit ni publica una rama, PR o merge: esas acciones siguen pendientes de ejecución autorizada.

## Claridad de portada y metas exploratorias · 13/10/2026

Rama `feat/claridad-portada`, desde `1a87894` (commit de colaboración integrado mediante PR #1; `origin/main` local está desactualizado en `965a42c`, sin fetch en esta tarea). El checkout estaba limpio pese al aviso de trabajo previo del encargo. Se sustituyó la introducción por la descripción concreta del servicio y las pruebas pendientes, manteniendo el titular. Se añadió el perfil completo antes del CTA, con referencia al Hito 1 (S01), y la derivación prioritaria con S08/S09. El perfil y su respaldo se contrastaron con el relato y las fuentes registradas; no se consultaron nuevamente los originales privados de Drive. Se conservó en Desafío la advertencia sobre perfiles diversos de la muestra. FONASA/GES describe el público, sin afirmar integración ni alianza.

Se retiró el bloque destacado ≥80 % de Resultados y sus estilos exclusivos. La explicación solicitada se integró con tipografía de cuerpo junto a las pruebas pendientes en Validación, con enlaces visibles S04/S05. Resultados conserva los hallazgos cualitativos y las fuentes pertinentes. No se modificó project.json: las referencias de Validación ya incluyen S04/S05 y los tres indicadores conservan definiciones, threshold 80, status proposed, observed null y source S04.

Comprobaciones: `node scripts/check.mjs`, `node scripts/build.mjs` y `git diff --check` aprobados. Segunda pasada del diff sobre hechos, referencias, jerarquía y archivos. Guía web externa consultada tras habilitar la ejecución fuera del sandbox; revisión proporcional sin hallazgos nuevos en el diff. Servidor `node scripts/serve.mjs` y smoke test Chromium: seis casos aprobados, portada y /prototipo/ a 1440, 390 y 320 px, teclado básico, Texto más grande, elecciones y estados de maqueta, sin errores de consola ni HTTP ni desbordamiento detectado. Comprobaciones adicionales a los tres tamaños: lectura sin JavaScript, enlaces S01/S08/S09 y foco visible; reflujo con viewport reducido a la mitad como aproximación al zoom 200 %. Se inspeccionaron capturas de las superficies cambiadas en móvil y escritorio.

Límites: no se accionó el zoom nativo del navegador al 200 %; la aproximación de reflujo no lo sustituye por completo. No se probaron Safari, dispositivos físicos ni comprensión con personas externas; estas verificaciones no validan el servicio. Sin push, PR, merge ni publicación; integración pendiente de revisión humana de otra persona.

Preparación de PR autorizada por el usuario: fetch de `main` confirmó `1a87894`, coincidente con la base local; no fue necesaria integración adicional. La autorización incluye push y creación de PR, con merge aún pendiente de revisión humana.

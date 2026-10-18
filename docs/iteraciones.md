# Iteraciones de la primera versión

## Paleta burdeo y rosados · 18/10/2026

Rama `feat/paleta-burdeo-rosados`, creada desde `origin/main` en `e0a61bf` después de comprobar que el checkout inicial estaba limpio y actualizar las referencias remotas. Se aplican las skills locales `color-expert`, `frontend-design`, `onconova-storytelling`, `web-design-guidelines` y `revision-landing`; se consultó la guía web vigente de Vercel. La solicitud actual de paleta sustituye la instrucción histórica de conservar los colores del 17/10.

Los siete colores recibidos quedan como referencias y se asignan a roles semánticos para página, superficies, acciones, texto, acentos, bordes y estados. Se añaden tintas de apoyo `#321521` y `#704054` para lectura y texto secundario. Los detalles de uso y las restricciones se documentan en [paleta-ui.md](paleta-ui.md). La landing, la página independiente, las ilustraciones propias, la marca y el comprobante PDF comparten esa dirección. El hover se deriva en OKLab con una alternativa visible para navegadores sin `color-mix`. Los campos conservan bordes funcionales burdeo; los separadores pastel son decorativos.

Se conserva el contenido, las fuentes, la tipografía, la composición y la lógica del prototipo. En HTML solo cambia `theme-color` y el símbolo decorativo: Chromium lo mostraba como emoji verde, por lo que se reemplazó por un SVG con `currentColor`. Se conservan los tonos de piel de la ilustración y el papel blanco del PDF.

Verificaciones ejecutadas:

- `node scripts/check.mjs`, `node scripts/build.mjs`, `node --check site/assets/receipt-pdf.js` y `git diff --check`: aprobados. SVG analizados como XML sin errores.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --base-url http://127.0.0.1:4173 --output work/paleta-qa/booking`: seis casos aprobados en ambas rutas a 1440, 390 y 320 px, con 78 PDFs, cuatro combinaciones de canal/modalidad por caso, reprogramación, errores inyectados, teclado, ampliación de texto, lectura sin JavaScript y ancla de fuente. PDFs extraídos con Poppler y analizados/renderizados con MuPDF. Sin errores de consola ni carga detectados por esa prueba.
- Auditoría temporal de color en navegador sobre ambas rutas: 49 casos/estados y 7080 muestras de texto visible, sin fallos frente a los umbrales AA de tamaño y peso comprobados. El menor ratio observado fue 4,89:1. Se verificaron los siete valores originales en las variables calculadas por Chromium, las opciones seleccionadas, el hover y los focos claro/burdeo. Tras reemplazar el emoji se repitió la auditoría y sus capturas.
- Inspección visual de portada en móvil/escritorio, mensaje, horarios, foco claro sobre propuesta, comprobante PDF y confirmación con texto ampliado a 320 px. El diff se revisó junto con los archivos nuevos. No se modificaron skills ni se añadieron dependencias.

Las capturas y los informes se conservan en [revision-2026-10-18/paleta/](revision-2026-10-18/paleta/). El test antiguo incluido en la skill contiene selectores de un prototipo anterior; se utilizó el test vigente `scripts/test-booking.py`, sin modificar la skill.

Límites: Chromium local, sin Safari, Firefox, dispositivos físicos ni sesión con lector de pantalla. La comprobación de reflujo no equivale a probar zoom nativo; los pares calculados y los estados visitados no certifican accesibilidad completa ni comprensión por usuarias. La revisión técnica no valida el servicio. En la entrega local inicial, push y apertura de PR quedaron pendientes de confirmar el alcance autorizado según `AGENTS.md` y `CONTRIBUTING.md`.

### Subida de rama y PR autorizados · 18/10/2026

El usuario autoriza subir `feat/paleta-burdeo-rosados` y crear el PR en borrador hacia `main`. El fetch detectó la integración de las transiciones del prototipo (#6), con `main` en `f3227d5`. Antes del primer push se trasladó el commit local a esa base; el cruce en `.booking` se resolvió conservando los dos tokens de movimiento de `main` y el nuevo fondo semántico de la paleta. El JS y el test de transición coinciden con `main`, sin retirar trabajo ajeno ni reescribir historial remoto.

Sobre esa base pasaron nuevamente check, build, sintaxis de ambos módulos JS y diff. Se repitieron el agendamiento completo (seis casos y 78 PDFs, más lectura sin JavaScript y ancla), los 49 casos de color y los 13 casos de `scripts/test-step-motion.py`. Los informes de agendamiento y movimiento están en `docs/revision-2026-10-18/paleta/`. Los límites de navegador y accesibilidad anteriores se mantienen. La autorización corresponde a la rama y al PR; la integración sigue sujeta a revisión humana y checks.

## Servicio de transición, historia y evidencia · 17/10/2026

Rama `feat/servicio-transicion-evidencia`, desde `71c6c95`. El checkout estaba limpio. La especificación adjunta `prompt.md` y la autorización de implementarla confirman el cambio conceptual y la creación de un PR en borrador, sin merge ni despliegue. Se comprobó mediante el conector de GitHub y después con `git fetch origin main` que la base coincidía con `main`. Se aplicaron las skills locales frontend-design, onconova-storytelling, web-design-guidelines y revision-landing; la guía web actual se consultó mediante el conector GitHub, ya que el acceso directo inicial desde el sandbox falló.

Se preservan exactamente el HTML de la portada y la franja de promesas, la paleta, las fuentes, las ilustraciones y el comportamiento del agendamiento. No se cambian `prototype.js`, `prototype.css`, `app.js` ni la página independiente. Se actualiza la navegación y el relato en el orden autorizado: Desafío → Historia → Propuesta → Prototipado e iteración → Demostración → Preguntas → Validación → Aprendizajes, brechas y planificación. Las anclas `resultados` y `proximos-pasos` se mantienen dentro de las secciones correspondientes. El check existente se adapta a ese orden.

Se añaden el problema de estudio, tres requisitos, la comparación app integral/servicio acotado, los atributos propuestos y la distinción entre papel planificado y maqueta digital disponible. El relato aclara que la web solo simula la coordinación de una primera hora psicológica y no realiza la exploración conversada completa, una derivación institucional ni una atención real. S11 registra la especificación y sus límites, conservando S08/S10 como antecedentes.

Las cinco entrevistas siguen siendo evidencia de necesidades. Los tres indicadores conservan sus definiciones del manifiesto, metas de al menos 80 % y resultados pendientes, sin porcentajes observados ni semáforos. Se incorporan las dos brechas, la decisión ITERAR y la planificación propuesta con responsables y semanas relativas. La tabla conserva semántica de tabla y presenta cada fila en vertical en móvil.

No están disponibles el documento complementario aludido por el prompt, el cuadro estratégico, la foto del papel, el video ni resultados verificables del RIA. No se reconstruyen énfasis desconocidos ni textos literales del documento ausente. Las síntesis se basan en la especificación y en S03/S04/S09. `docs/evidencia.md` registra contradicciones, recursos ausentes y las anclas previstas para incorporarlos. No se emplean el póster histórico ni recursos genéricos como sustitutos de evidencia.

Verificaciones realizadas:

- `node scripts/check.mjs`, `node scripts/build.mjs` y `git diff --check`: aprobados; ocho etapas tras la portada, once fuentes, tres metas, dos páginas y doce archivos públicos.
- Comparación del HTML original y actualizado de portada/franja: idénticos. Se revisaron diff, fuentes, límites de evidencia y ausencia de archivos privados.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --output work/revision-transicion-final`: seis casos aprobados (landing y `/prototipo/` a 1440, 390 y 320 px), más lectura sin JavaScript en ambas rutas y enlace directo a fuente. Incluye combinaciones de canal/modalidad, solicitud, mensaje, horarios, confirmación, cambio de hora, comprobante, postergación, rechazo, coordinación pendiente, reinicio, texto ampliado y reflujo a 720 px. Sin errores de consola, HTTP o envíos externos en los recorridos comprobados.
- Revisión adicional con Chromium a 320, 390, 768, 1024 y 1440 px, con tamaños normal/ampliado y movimiento reducido: sin desbordamiento. Orden de secciones, anclas conservadas y nuevas, apertura de fuentes, salto al contenido y foco de teclado comprobados. El foco sobre el fondo violeta utiliza un contorno blanco de 3 px. Se comprobó la semántica accesible de la tabla en móvil.
- Se corrigió un desbordamiento del nuevo título de propuesta a 320 px con texto ampliado y se mejoró la lectura móvil de la tabla. La repetición de la prueba funcional aprobó todos los casos. Se utilizó `scripts/test-booking.py`, vigente para el agendamiento actual; el smoke genérico de la skill conserva selectores de una maqueta anterior y no se ejecutó como sustituto.
- Contraste de pares de texto/fondo utilizados en el cambio: al menos 5,46:1 en las combinaciones comprobadas. Inspección visual de las secciones modificadas en escritorio y móvil. Capturas en `docs/revision-2026-10-17/`; al recortar secciones se oculta solo la cabecera fija para evitar superposiciones de la captura.

Límites: no se evaluó comprensión con usuarias, factibilidad institucional, acceso real ni eficacia clínica. No se probaron Safari, dispositivos físicos o zoom nativo al 200 %; el reflujo es una aproximación. Las pruebas técnicas no equivalen a validación del servicio. El PR se entrega en borrador para revisión de otra persona, sin merge ni despliegue.

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

## Salud mental y agendamiento simulado · 14/10/2026

Rama `feat/salud-mental-agendamiento`, base local `d45b039`. El equipo comunica feedback docente y confirma una entrega que simule el uso esperado. Se aplicaron las skills locales frontend-design, onconova-storytelling, web-design-guidelines y revision-landing; se consultó la guía web vinculada por esa skill. No se modificaron las skills.

Se mantiene el público postratamiento por cáncer de mama y se acota la propuesta a salud mental. S10 registra la nueva decisión y el feedback, sustituyendo el alcance multisoporte de S08. Se conservan las siete etapas, las cinco entrevistas como evidencia de necesidades y las metas sin resultados inventados. No se agregan profesionales, alianzas, tasas clínicas ni validaciones.

La portada adopta el título y la introducción proporcionados por el grupo, una paleta violeta/lavanda/salvia y la ilustración original. El CTA y la ficha de portada acceden directamente a la demostración. Se retiran los enlaces públicos a actividades académicas del semestre; las referencias originales permanecen en el manifiesto. Se destacan las cinco entrevistas reales con su contexto y límites. Se sustituyen textos operativos vagos por instrucciones concretas y estados de simulación.

El prototipo está integrado en la página principal y disponible en `/prototipo/`: solicitud con datos ficticios, modalidad y canal; mensaje simulado de correo o WhatsApp; horarios de ejemplo; cita simulada y comprobante descargable. Incluye postergación, rechazo, falta de horario compatible, nueva coordinación, cambio de horario y reinicio. No hay diagnóstico, información personal ingresable, envío, almacenamiento de solicitudes ni reserva real. Solo persiste la preferencia de tamaño de texto. La confirmación aclara que no se realizó una atención.

Verificación: check de contenido y enlaces, sintaxis JS, build y `git diff --check`. Chromium/Playwright: seis casos aprobados (dos rutas a 1440, 390 y 320 px), cada uno con cuatro combinaciones de canal/modalidad, consentimiento, validación de horario, comprobante, reprogramación, postergación, rechazo, espera, reinicio, recarga, teclado básico, ampliación de texto y ausencia de peticiones externas o almacenamiento de reservas. Lectura sin JavaScript y enlace directo a S10 aprobados. Capturas de portada en escritorio/móvil y confirmación inspeccionadas. Se corrigió desbordamiento a 320 px. La comprobación sin JS usa selector DOM, porque el selector de texto de Playwright omite noscript.

El smoke de la skill corresponde a la antigua maqueta multisoporte; se agregó `scripts/test-booking.py` para el comportamiento vigente, sin alterar la skill ni dependencias de producción. Resultados técnicos en `work/qa/report.json` (ignorado). Los tests se ejecutaron con servidor y navegador fuera del sandbox de procesos, tras fallos de sockets dentro de él. No hubo modificación de la política de red.

Límites: Chromium local, sin Safari ni dispositivos físicos; el reflujo no sustituye una comprobación de zoom nativo; no se evaluó comprensión con usuarias. No se pudo realizar una comparación visual directa de Roveia/rizartrosis, por lo que no se afirma fidelidad visual a esas referencias. Sin push, PR, merge ni publicación. La revisión humana previa al merge sigue pendiente según las reglas del repositorio.

Revisión de contraste de los pares principales: texto ≥5,59:1 y botones principales 9,15:1. Se oscurecieron los bordes de opciones para superar 3:1. La exportación autónoma queda como archivo de trabajo: el navegador administrado bloquea URLs file:// y no se afirmó su verificación. La carpeta de entregables indicada por la conversación no existe en este ejecutor y no pudo crearse; el resultado principal queda en el repositorio y en dist/.

### Preparación del PR autorizada

El usuario autorizó subir la rama y abrir un PR hacia `main`. Se consultó el remoto y `main` sigue en la base `d45b039`; no hay cambios adicionales que integrar. Se incorporan capturas de portada en escritorio y móvil en `docs/revision-2026-10-14/` para facilitar la revisión visual. La autorización no incluye merge; la publicación en GitHub Pages sigue el flujo de revisión del equipo.

## Comprobante de agendamiento en PDF · 18/10/2026

Rama local `feat/comprobante-pdf`, desde `main` confirmado mediante fetch en `71c6c95`. Checkout inicialmente limpio. Alcance autorizado: implementación, verificación local y descripción de PR; sin push, PR, merge ni publicación. Se aplicaron frontend-design, onconova-storytelling, web-design-guidelines (guía externa consultada) y revision-landing junto con `docs/code_review.md`. No se modificaron skills.

Se reemplazó el archivo de texto por un PDF 1.4 generado en el navegador, de una página A4, MIME `application/pdf` y nombre `onconova-comprobante-simulado.pdf`. El módulo nativo `site/assets/receipt-pdf.js` compone marca vectorial, tipografía estándar PDF con texto seleccionable en español, fecha destacada en lavanda e indicaciones y nota de simulación en la paleta del brief. No incorpora dependencias de producción, fuentes remotas, imágenes como contenido único ni servicios externos. Las fuentes S09/S10 y la decisión vigente sostienen el escenario; no se añaden datos ni resultados de validación al manifiesto.

El PDF incluye usuaria ficticia, primera sesión de apoyo psicológico, fecha con año, hora de Santiago de Chile, 45 minutos de ejemplo, modalidad, profesional sin identidad asignada, canal sin mensaje enviado y estado de cita simulada sin atención realizada. Videollamada no habilita sala real; presencial no tiene dirección real asignada. Nota visible: no constituye reserva real ni acredita atención, cobertura o pago. Se conservan año, mes y día como números en los horarios y se comparte el formato de fecha y las indicaciones entre pantalla y documento, sin reconstruir fechas desde etiquetas.

Ambas rutas anuncian **Descargar comprobante PDF**. El estado de descarga o error es visible y usa `role=status`, `aria-live=polite` y `aria-atomic=true`. El mensaje de éxito solo informa el inicio; el guardado o la cancelación final dependen del navegador. Se retiran los enlaces temporales y se revocan las URLs de descarga. El estado se limpia al cambiar de pantalla; no se generan comprobantes sin confirmación. Se mantienen postergación, rechazo, coordinación pendiente, reprogramación, reinicio y privacidad. El guion documenta la demostración del PDF y los requisitos de QA. Se conservan intactas las protecciones contra `.pdf` dentro de `site/` en check/build; los archivos generados están en `work/`.

Verificaciones reales:

- `node scripts/check.mjs`, `node scripts/build.mjs`, `git diff --check` y sintaxis de ambos módulos JS: aprobados.
- Servidor `node scripts/serve.mjs` y prueba adaptada `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --base-url http://127.0.0.1:4173 --output work/qa-comprobante`: seis casos aprobados, `/` y `/prototipo/` a 1440, 390 y 320 px. Cada caso prueba cuatro combinaciones, descarga inicial, reprogramación, reintento tras errores y una descarga con texto ampliado: **78 PDFs válidos** en la pasada final.
- Cada descarga se abre con PyMuPDF sin reparación, cifrado ni advertencias; se renderiza y se extrae texto también con Poppler (`pdftotext`) sin advertencias. Se comprueban una página A4, contenido exacto de pantalla, acentos y ñ, límites de página y ausencia de superposiciones entre cajas de texto. `pdfinfo` confirma PDF 1.4, una página A4, sin JavaScript ni cifrado. Muestras cercanas a 4 KB. Inspección visual de PDFs de las dos modalidades, marca, nota, alineación y legibilidad; apertura adicional de ambas modalidades en el visor PDF de Chromium mediante servidor HTTP local de QA, sin aviso de corrupción visible.
- Reloj de QA fijado en `2026-12-31T01:00Z` (todavía 30/12 en Santiago), dispositivos con zonas Kiritimati y Los Ángeles: agenda cruza correctamente de 2026 a 2027 y mantiene las horas seleccionadas. Son días ficticios de lunes a viernes, sin calendario de feriados.
- Tab llega desde el título de confirmación al botón; Enter y Espacio descargan; foco visible y tamaño mínimo de 44 px comprobados. Capturas de foco y estado inspeccionadas en móvil/escritorio, también con texto ampliado. Sin desbordamiento detectado. Se verificaron consentimiento, horarios, reinicio, recarga y bloqueo de comprobantes en estados sin cita, sin errores de consola/HTTP, nuevas peticiones externas ni almacenamiento de reservas. Lectura sin JS en ambas rutas y ancla S10 aprobadas.
- Fallos inyectados en construcción del Blob, creación de URL y activación del enlace: se anuncia error sin éxito falso; reintentar funciona y se eliminan enlaces y URLs temporales. El acceso a sockets y navegador requirió el permiso de red del ejecutor; las verificaciones se realizaron sobre localhost.

Segunda pasada separada sobre el diff, incluido el módulo nuevo: revisión de estados, fechas, codificación, offsets y longitudes PDF, privacidad, fuentes, semántica, foco y limpieza. Se retiró un token de color sin uso y se reforzó la prueba con fallos de construcción, detección de superposiciones y comprobante/estado con texto ampliado. Se repitió completa la prueba adaptada con esos ajustes y se repitieron check, build, sintaxis y diff. Sin hallazgos bloqueantes pendientes en el alcance revisado.

Límites: Chromium local; sin Safari, Firefox, Adobe Reader ni dispositivos físicos. Se verificó la región de anuncio y su contenido, sin escuchar un lector de pantalla. La aproximación de reflujo no prueba zoom nativo. El PDF usa fuentes estándar no incrustadas y no está etiquetado: no se certifica PDF/UA ni PDF/A. Su composición está acotada al contenido español del prototipo, sin campos libres. Esta revisión técnica no evalúa comprensión con usuarias ni valida el servicio. Integración pendiente de revisión humana por otra persona; no se hizo commit, push, apertura de PR, merge ni publicación.

Entrega local en `work/entrega-comprobante/`: PDF ficticio, render, capturas, reporte, texto extraído, parche completo y descripción de PR. No fue posible crear la ruta de salida `/codex/browser/projectless/0024-repositorio-onconova-base-de-integraci-n-main-ra/output` indicada por el cliente: `/codex` no existe y la raíz del ejecutor es de solo lectura o no permite crearla, incluso fuera del sandbox. Se conserva la entrega en el workspace sin subirla a servicios externos.


### Preparación de push y PR autorizada · 18/10/2026

El usuario autoriza explícitamente subir `feat/comprobante-pdf` y abrir PR hacia `main`; merge y publicación siguen fuera del alcance. El fetch detectó `main` en `81db292` (#4), posterior a la base inicial. Antes del primer push se trasladó el commit local a esa base y se resolvió el cruce del HTML conservando el relato, las preguntas y la referencia S11 del cambio integrado. La comparación de ambos HTML con `main` confirma únicamente los cuatro ajustes previstos del comprobante; no se retiran cambios ajenos ni se reescribe historia remota.

Sobre esa base pasaron check, build, sintaxis JS, `git diff --check` y verificación de las 24 skills/393 huellas. Se repitió completa la prueba adaptada usando el puerto local 4175: seis casos y 78 PDFs aprobados, más lectura sin JavaScript y ancla S10. El reporte está en `docs/revision-2026-10-18/comprobante-report.json`; las capturas del PDF ficticio y del estado en escritorio/móvil se incluyen en la misma carpeta para revisión humana desde el PR. Se mantienen los límites de QA registrados arriba. Los PDFs de prueba siguen solo en `work/`, sin alterar la protección de `site/`.

## Transición entre pasos del prototipo · 18/10/2026

Implementación autorizada del plan de `improve-animations`, en la rama `feat/transicion-pasos-prototipo-150ms`, desde `main` en `e0a61bf`. Se aplicaron las skills `animate`, `review-animations`, `revision-landing`, las instrucciones de diseño y relato y las guías de interfaz consultadas. No se modificaron skills. El usuario autoriza publicar esta rama y crear un PR; la integración conserva la revisión humana del equipo.

Las dos rutas comparten una entrada CSS de opacidad 0 → 1, de 150 ms con `cubic-bezier(0.23, 1, 0.32, 1)`, al cambiar de paso mediante clic o toque reconocido. La pantalla anterior se oculta inmediatamente y se actualizan progreso y foco sin esperar la transición. Las acciones con teclado, las activaciones sin procedencia de puntero confirmada, la carga inicial y el movimiento reducido conservan el cambio instantáneo. Un envío inválido no dispara otra entrada. La captura de activación del submit expira incluso si la validación nativa impide enviarlo.

No se animan alturas, posiciones, errores, avisos ni el indicador de progreso. Se conservan la descarga PDF y los cambios del relato ya integrados. Sin dependencias nuevas, almacenamiento de reservas ni peticiones de servicio. `@starting-style` permite una alternativa funcional estática cuando no está soportado. Al probar Tab durante una entrada, se detectó que retirar la marca de animación dejaba continuar la transición CSS existente: se añadió `transition:none` como estado base de la pantalla para cancelarla inmediatamente.

Verificación realizada en Chromium 154.0.8037.57:

- `node --check site/assets/prototype.js`, `node scripts/check.mjs`, `node scripts/build.mjs` y `git diff --check`: aprobados.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-step-motion.py --base-url http://127.0.0.1:4177 --output work/qa-step-motion`: 13 casos aprobados; ambas rutas a 1440, 390 y 320 px, con y sin movimiento reducido, más simulación de navegador que ignora `@starting-style`. Comprueba clic/toque emulado, Enter, Espacio, Tab durante la entrada, activaciones sintetizadas y programáticas, validación, pausas, espera, regresos rápidos, cambio de preferencia de movimiento durante la entrada, foco, progreso inmediato, texto ampliado, una sola pantalla activa y ausencia de desbordamiento y errores de consola/HTTP. Se inspecciona la transición real del navegador: propiedad opacidad, extremos 0/1, 150 ms y curva exacta. El script se conserva como comprobación opcional reproducible; requiere Playwright y Chromium solo para QA.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --base-url http://127.0.0.1:4177 --output work/qa-booking-motion`: seis casos aprobados, ambas rutas a tres anchos, 78 descargas PDF verificadas, fallos y reintentos, lectura sin JavaScript y enlace a fuente. La prueba existente usa movimiento reducido; la prueba nueva cubre también movimiento normal.
- Inspección visual de los estados finales en escritorio y móvil con texto ampliado, y fotogramas de una transición pausada a 30 y 150 ms: solo cambia la opacidad, sin desplazamiento ni superposición. Las capturas finales y el reporte están en `docs/revision-2026-10-18/transicion-pasos-{escritorio.png,movil.png,report.json}`. Las capturas estáticas documentan disposición y legibilidad; los tiempos se verifican mediante la prueba de interacción.
- Segunda revisión del diff y de los archivos nuevos: flujo de estados, procedencia de activación, cancelación, movimiento reducido, foco y alcance. Sin hallazgos bloqueantes pendientes en lo comprobado.

Límites: no se probaron Safari, Firefox, un teléfono físico, zoom nativo ni lectura con tecnología de asistencia. La altura del contenedor sigue cambiando instantáneamente. Esta verificación técnica no valida comprensión con usuarias ni acceso real a atención. El PR necesita revisión de otra persona antes de integrarse; GitHub Pages se actualizará después del merge y del despliegue.

## Movimiento moderado durante el scroll · 18/10/2026

Rama `feat/movimiento-scroll`, base local `71c6c95`. Se aplicaron `find-animation-opportunities`, `motion-design`, `animate`, `review-animations` y `revision-landing`. Se consultó `animate-expo`: no existe una app React Native/Expo en este repositorio y no se requiere migración ni gestos nuevos para la landing.

Entradas únicas de la ilustración cuando comienza fuera de pantalla, una secuencia breve de los cuatro pasos y trazos en los bordes existentes de resultados/próximos pasos. Curva común, desplazamientos de 8–12 px y duración de 300–500 ms. El texto académico permanece estable; no cambian hechos ni fuentes. Todo está visible sin animación; teclado, anclas, impresión y preferencia reducida detienen el movimiento. Sin scroll artificial, listeners por fotograma, bibliotecas ni interacción por gesto obligatoria.

Pasaron integridad, sintaxis JS, build y diff; seis casos del agendamiento en las dos páginas a 1440/390/320 px, texto ampliado y comprobaciones sin JS. Revisión específica de entradas, no repetición, reducción de movimiento en vivo, teclado, enlaces, impresión, fallback sin observer y deslizamiento táctil emulado. Capturas inspeccionadas y decisiones, medidas y límites en [revisión de movimiento](revision-2026-10-18/movimiento.md). Revisión local de animaciones aprobada dentro del alcance comprobado.

Límites: Chromium local y móvil emulado; sin Safari, hardware físico, zoom nativo ni validación con usuarias. La URL pública no fue accesible desde las herramientas; se revisó el checkout. Sin push, PR, merge o publicación; continúa pendiente la revisión humana requerida por el proyecto.

## Guía lineal con cuadro compartido y preparación de PR · 18/10/2026

El usuario amplía el encargo: un cuadro que marque la lectura de Aprendizajes, Brechas y Próximos Pasos, e integración de los cambios en un PR. Autoriza push y creación del PR; el merge sigue pendiente de revisión humana.

El fetch encontró `main` en `78c479b`, con relato S11, nueva paleta burdeo/rosados, comprobantes PDF y transiciones del prototipo. Se integró esa base en `feat/movimiento-scroll` y se resolvieron cruces de HTML e historial conservando el contenido reciente. Las entradas anteriores se adaptaron a los tres atributos de la propuesta vigente; se sustituyeron los trazos decorativos por la guía solicitada. Las capturas iniciales se reemplazan por el resultado integrado.

La sección presenta tres bloques consecutivos en una sola columna. Un cuadro compartido marca el enlace del bloque leído y cambia de posición con transform en 250 ms; columna lateral en escritorio, barra superior en móvil y enlaces verticales sin sticky con texto ampliado en móvil. Los enlaces son anclas nativas, los destinos aceptan foco visible y toda la información permanece en el flujo normal. Con teclado o movimiento reducido, la señal se actualiza sin animación; el cuadro no altera el scroll. Se corrigieron la anchura de los encabezados del plan móvil y el margen que evita tapar enlaces al volver con Shift+Tab; se acotó un selector del test de progreso para distinguir la guía del agendamiento.

Se conservan todos los párrafos y su orden frente a main, salvo una etiqueta de navegación. No cambian fuentes, evidencia, responsables ni semanas propuestas. Pasaron check/build/sintaxis/diff, los once casos de la guía (seis combinaciones, dos recorridos de foco y tres alternativas), seis casos de entradas únicas, seis casos del agendamiento con 78 PDFs y trece casos de transiciones del prototipo. Capturas, criterios, hallazgos corregidos y límites en [revisión integrada de movimiento](revision-2026-10-18/movimiento.md). Chromium local y móvil emulado; sin certificación de dispositivos físicos, Safari, zoom nativo o validación del servicio con usuarias.

## Panel de lectura con transición horizontal · 18/10/2026

Sobre `76c818f` (PR #8 integrado), el usuario confirma un único panel que cambie entre Aprendizajes, Brechas y Próximos pasos: avance hacia la derecha, retroceso a la izquierda, 250 ms sin rebote, títulos, scroll natural y swipe derecho para avanzar. También autoriza implementar y abrir el nuevo PR. Rama `feat/panel-horizontal`; sin merge autorizado.

Se sustituye el indicador móvil sobre títulos por una superficie compartida. El final de cada capítulo puede leerse antes de que el scroll avance; no hay panel fijo, scroll interno ni bloqueo del gesto vertical. El cambio automático conserva scrollY y foco. Los saltos deliberados siguen el destino. Salida de 100 ms y entrada de 150 ms con transform/opacidad y la curva existente; una interrupción resuelve al último destino. Teclado y movimiento reducido cambian inmediatamente. Se conservan anclas, historial, texto ampliado, impresión y lectura completa sin JavaScript u observers. Se añade ayuda de navegación y botones Anterior/Siguiente; a 320 px con texto ampliado pasan a varias líneas para no recortarse.

Pasaron integridad, sintaxis JS, build y diff; doce casos del panel a 1440/390/320 px, tres comprobaciones adicionales de teclado/interrupción/resize, seis combinaciones de agendamiento con 78 PDF y trece casos de movimiento del prototipo. Sin cambios factuales, de fuentes, responsables, plazos, paleta o dependencias. [Revisión, decisiones, reportes y capturas](revision-2026-10-18/panel-horizontal.md). Chromium local y emulación táctil; sin dispositivos físicos, Safari, Firefox, zoom nativo, lector de pantalla o validación con usuarias. La revisión de IA complementa la aprobación humana requerida antes de integrar el PR.

## Correcciones editoriales y ubicación global · 18/10/2026

Rama local `feat/revision-contenidos-navegacion`, desde `main` en `76c818f`.
Checkout limpio y fetch sin avances posteriores a esa base. Se implementan R1–R7
con paleta burdeo/rosada: marco de hallazgo literal, dos escenas conceptuales
locales, Historia abreviada (43→26 y 48→42 palabras), introducción de Propuesta más
ancha sin cambiar texto/tipo/interlineado, tres tarjetas, lazo rosado propio y
contorno/separaciones burdeo de la tabla. Población, fuentes, responsabilidades,
semanas propuestas y límites de evidencia se conservan; no cambian project.json
ni evidencia.md. Ambas cabeceras y favicon consumen el mismo mark.svg.

El usuario comparó «Índice de capítulos» con «Ubicación con selector» y eligió
explícitamente el primero. Se integraron diez anclas nativas, estado por
aria-current/borde/subrayado, offsets compartidos y persistencia adaptada a móvil,
poca altura y ampliación. La guía local se conserva y pasa a flujo cuando hace
falta espacio. Sin JS no se inventa sección actual. Scroll usa límites cacheados;
no mueve foco, anuncia cada cambio ni escribe historial. Se retira la entrada de
las tarjetas para mantener texto quieto, conservando guía 250 ms, prototipo 150 ms
y curva común. Sin dependencias, hooks, cambios de skills o servicios reales.

Pasaron check/build/sintaxis/diff, ocho escenarios del índice (incluido zoom
nativo 200%), once de guía, trece de transición y seis de agendamiento con 78 PDFs,
64 combinaciones de estrés y montaje local `/onconova/` de ambas páginas.
El smoke exacto de la skill se ejecutó: falla 0/6 por selectores históricos
`data-choice`/`#support`, ausentes antes del cambio. Se conserva ese resultado;
un adaptador QA de controles vigentes pasó 6/6 sin editar la skill.

Segunda revisión sobre el diff y dos assessments aislados de diseño/técnica,
con detector usado una vez e inspección real de escritorio/móvil. Se corrigió la
señal de desplazamiento del índice y el reflujo extremo. Sin regresiones
introducidas pendientes en el alcance comprobado. Dos detalles tipográficos
previos quedan como mejoras opcionales, documentados sin inflarlos a fallas AA.
Matriz, antes/después, recursos, decisiones, resultados y capturas en
[revisión editorial y navegación](revision-contenidos-navegacion.md).

Límites: URL pública bloqueada por proxy 403; Chromium 154 y móvil emulado, sin
Safari, hardware físico ni lector de pantalla escuchado. Comprensión en tres
minutos y efectividad del servicio siguen sin validación con usuarias. No se hizo
push, PR, merge ni publicación; se dejó descripción de PR preparada. La
integración futura necesita revisión de otra persona según CONTRIBUTING.md.

### Commit y PR autorizados; integración de main

El usuario autoriza commit y apertura de PR. El fetch detectó `main` en `c7a9c59`
(PR #9), posterior a la base inicial. Se creó `1179e02` con las correcciones y
se integró ese main mediante merge, conservando el panel horizontal compartido
y todas sus interacciones. Se resolvió el cruce de layout sumando al clearance
la cabecera y el índice global solo cuando son sticky. La guía local se mantiene
en flujo en móvil para evitar superposición. No se revierte el avance de #9.

La prueba nueva del índice aprobó nuevamente ocho escenarios tras integrar,
incluido zoom nativo 200 %. La prueba del panel conserva los casos nuevos de
main y comprueba offsets/foco contra las capas persistentes reales, además del
ancho interior completo de la tabla. El muestreo de la fase de salida se hace
en la misma evaluación del navegador para evitar capturar la fase siguiente
entre dos llamadas de herramienta. Los resultados finales se registran en la
revisión editorial. El permiso no incluye merge a main ni publicación.

Revalidación final de esa integración: ocho escenarios del índice y doce del
panel aprobados, junto a check/build/sintaxis/diff y huellas de skills. Capturas
de la planificación actualizadas y reportes agregados a la revisión editorial.
La subida de esta rama y la creación de su PR están autorizadas; el merge y la
publicación continúan fuera de alcance.

## 18/10/2026 · Contacto ficticio y horarios alternativos seleccionables

Encargo ejecutado localmente en `feat/prototipo-contacto-alternativas`, sobre el checkout limpio `82a078a`, coincidente con `origin/main`. Se reprodujeron los dos defectos en ambas rutas antes de editar: identidad fija sin campos y preferencia de otro horario que solo terminaba pendiente. La fuente S12 registra la decisión vigente; las descripciones históricas de «sin campos personales» se conservan como antecedentes, sin alterar entrevistas o resultados.

Ambas superficies ahora piden nombre preferido y teléfono/correo según el canal, con etiquetas, ayudas, validación de formato, errores y aceptación explícita de la simulación. El campo inactivo se borra y desactiva. Mensaje y confirmación usan los datos ficticios actuales como texto. Solo viven en memoria/DOM y se limpian al reiniciar/recargar o salir pendiente; no se envían ni se incluyen en URLs, almacenamiento persistente o consola. El PDF omite nombre y contacto, conserva fecha/modalidad/canal actuales y retira la identidad fija. No se solicitan datos de salud.

«Ninguno me acomoda» abre mañana/tarde y modalidad: la nueva propuesta tiene tres fechas posteriores a las rechazadas, según el calendario de Santiago. Permite seleccionar, confirmar y descargar el PDF. El segundo rechazo deja el recorrido pendiente con acciones de revisión y salida sin contacto real. Editar, cambiar modalidad/propuesta y reprogramar limpian selecciones y comprobantes anteriores. FAQ, guion, README, brief, evidencia y metadatos describen el recorrido vigente.

Skills aplicadas por fase: `revision-landing`, `web-design-guidelines`, `frontend-design`, `onconova-storytelling`, `emil-design-eng`, `animate`, `review-animations` y `break-ui`; además `cloud-environment-runtime` para el runtime. Se conserva la transición de opacidad de 150 ms solo con puntero; teclado y movimiento reducido siguen sin entrada animada. No se animan escritura, errores ni selección. La revisión de movimiento se hizo en una segunda pasada separada, con muestreo en navegador y acciones repetidas. Fixtures y control de estrés solo en `.local/break-ui/`.

Pasaron check/build/sintaxis/diff; seis recorridos a 1440/390/320 px en ambas rutas, con 132 PDFs revisados mediante extracción y render (22 por caso), lectura sin JS y ancla de fuente; 13 casos de movimiento; 12 de guía de lectura; 72 de datos extremos; seis de teclado/foco y texto raíz al 200 %; seis de captura/contraste/fotogramas. Se verificaron edición, ambos canales/modalidades, mañana/tarde, conservación/cambio de modalidad, nuevas fechas, rechazo/pendiente, reinicio/recarga, privacidad, consola, fallos de descarga y limpieza de recursos. Segunda revisión del diff completo: se evitó repetir el mismo anuncio de error y se retiró una escritura duplicada; se reforzaron y repitieron las verificaciones afectadas. Sin hallazgos bloqueantes confirmados pendientes en ese alcance.

La revisión y capturas están en [contacto y alternativas](revision-2026-10-18/contacto-alternativas.md); PDFs y demás resultados solo en `work/`. Chromium local y móvil emulado, sin Safari, teléfono físico, lector de pantalla escuchado ni zoom nativo; el PDF no está etiquetado. La referencia publicada devuelve HTTP 403 del proxy: se verificó el checkout local. Las pruebas técnicas no son validación con usuarias. Sin commit, push, PR, merge ni publicación; descripción de PR preparada localmente. Integrar requiere revisión de otra persona y publicar requiere autorización.

### Commit y PR autorizados para contacto y alternativas

El usuario autoriza el commit y la apertura de un PR hacia `main`; realizará la revisión y el merge. El fetch confirma que `origin/main` sigue en `82a078a`, la base ya verificada, sin cambios que integrar ni conflictos. Se conserva la evidencia técnica de esta iteración y se prepara la rama para revisión; no se autoriza ni ejecuta el merge o la publicación.

## 18/10/2026 · Aprendizajes en una pila central de tarjetas

Implementación local en `feat/aprendizajes-tarjetas`, desde el checkout limpio `51a8868`, conservando su trabajo previo. Se modifica únicamente la sección «Aprendizajes, Brechas y Próximos Pasos», sus estilos, su módulo de navegación y la prueba correspondiente. No se actualiza ni integra `main`; no se hace commit, push, PR ni publicación.

La cabecera completa y el subtítulo «Lo aprendido y lo pendiente» quedan centrados. Se elimina el párrafo introductorio indicado por el encargo. El menú lateral y el panel compartido se sustituyen por tres tarjetas superpuestas, con una superficie principal y dos títulos expuestos mediante botones semánticos independientes. Los tres bloques de contenido HTML se compararon con HEAD y se conservan exactamente: fuentes, límites, tabla, responsables, semanas, enlaces y anclas. No cambian `project.json`, evidencia ni el prototipo.

La selección lleva la tarjeta al frente y alinea inmediatamente el documento con su hito canónico. El scroll nativo recorre Aprendizajes → Brechas → Próximos pasos y vuelve en sentido inverso, con alturas medidas y 96 px adicionales para terminar la lectura. No se cancela la rueda ni se crea un desplazamiento interno. El movimiento usa únicamente `transform`, 300 ms y el token `--ease-out` existente: profundidad, desplazamiento y giro leve, sin desvanecer texto. Las transiciones CSS se redirigen desde su posición visible y acortan su duración al invertir. Se mantienen Anterior/Siguiente y el atajo táctil horizontal opcional.

Los botones de las tarjetas siguen accesibles; el contenido inactivo usa `hidden` e `inert`. Teclado y movimiento reducido resuelven el cambio estáticamente. Se corrigió durante QA el cambio involuntario de tarjeta que podía provocar el desplazamiento nativo al tabular: Tab conserva el contenido visitado; rueda, desplazamiento vertical táctil y PageUp/PageDown retoman los hitos canónicos. El foco de títulos girados queda bajo el índice global. A menos de 360 px, con texto raíz superior a 18 px o con menos de 360 px útiles de alto, se muestran los tres contenidos en flujo, con enlaces nativos. Sin JavaScript o sin observadores también quedan lineales. Impresión conserva orden, contenido y títulos, sin controles, sombras ni contorno de foco.

Skills leídas en el orden solicitado: `onconova-storytelling`, `frontend-design`, `apple-design`, `motion-design`, `animate`, `web-design-guidelines` y `revision-landing`; además `cloud-environment-runtime` para el entorno. Se consultaron las pautas públicas actuales de Web Interface Guidelines. Se respetan paleta burdeo/rosada, tipografía de sistema y cuerpo de 20 px. Los contrastes calculados de los nuevos usos de texto oscilan entre 5,22:1 y 14,56:1; los controles expuestos tienen al menos 44 px útiles.

Verificación aprobada:

- `node scripts/check.mjs`, `node scripts/build.mjs`, `node --check site/assets/app.js` y `git diff --check`.
- `python3 scripts/test-reading-guide.py`: 14 escenarios. Incluye 1440/390/320 px con movimiento normal/reducido; selección de las tres tarjetas; continuidad inmediata desde cada selección; fin de lectura antes de avanzar; retroceso; salida a Fuentes; interrupciones a 35/130 ms; Enter/Espacio, Tab/Shift+Tab y foco; fuentes y vuelta a la demostración; texto ampliado y al 200 %; historial, recarga, cambio de tamaño; ausencia de JS y de observadores; anclas y orden; impresión y zoom nativo al 200 % (1440 px externos, 720 px CSS, DPR 2). Se sustituye la expectativa visual de salida/entrada horizontal por las transformaciones de la pila, manteniendo la cobertura funcional y adaptando los controles a la alternativa lineal.
- `python3 scripts/test-section-index.py --output work/qa-section-index`: 8 escenarios aprobados, incluida poca altura, orientación, teclado, enlaces directos, alias, historial, ausencia de JS y zoom nativo al 200 %.
- Pruebas complementarias a 1440/390 px: inversión del scroll durante la transición, PageUp con foco en la tarjeta, retorno desde impresión, orden de impresión y matrices estáticas sin giro con movimiento reducido. Revisión de impresión repetida a 1440/390/320 px tras eliminar el contorno del papel.
- Sin errores de consola/recursos ni desbordamiento horizontal en la matriz monitorizada. Capturas completas de cada tarjeta a 1440/390/320 px, cabeceras, texto ampliado, zoom y fotogramas de movimiento. Segunda inspección del diff y las capturas; PDF impreso revisado por extracción de texto y render de las páginas de la sección. Una captura móvil inicial vacía de Playwright se reemplazó por captura del compositor CDP, con comprobación de que contiene contenido.

Reportes y evidencias reproducibles en `work/qa-reading-guide/`, `work/qa-section-index/`, `work/qa-reading-extra/` y scripts auxiliares de `work/`; quedan ignorados. El informe de entrega está en `work/entrega-aprendizajes.md`, junto con las capturas, los reportes y `work/aprendizajes-tarjetas.patch`. La carpeta de salidas prevista por el cliente bajo `/codex/` no existe en este entorno y no se pudo crear su ruta padre por permisos del sistema operativo; los archivos permanecen locales en `work/`. No quedan regresiones confirmadas pendientes en el alcance revisado. No se identificaron nuevos defectos previos que requieran modificar otras secciones y no se ejecutaron las baterías del agendamiento, cuyo código no cambia.

Límites: Chromium 154 y tacto emulado, sin Safari/Firefox, teléfono físico ni lector de pantalla escuchado. La URL pública devuelve 403 del proxy y no se encontró `Boards.pdf` entre los archivos disponibles: se utilizó la descripción autorizada. El PDF de Chromium no está etiquetado. Las pruebas técnicas no son validación con usuarias. La futura integración hacia `main` requiere su revisión y comprobación de compatibilidad en ese momento.

### Commit y PR autorizados para las tarjetas

El usuario solicita subir el PR. Se autoriza guardar los cambios, subir `feat/aprendizajes-tarjetas` y abrir un PR hacia `main`; la integración y publicación siguen fuera de alcance. El fetch confirma `origin/main` en `51a8868`, coincidente con la base verificada, sin cambios que incorporar. Se añaden la [revisión y capturas completas de las seis vistas](revision-2026-10-18/aprendizajes-tarjetas.md) y los reportes de QA para que la evidencia se pueda revisar desde GitHub, sin depender de `work/`.

# Trabajar en equipo en Onconova

El flujo del proyecto es una rama por tarea, un pull request hacia `main`,
comprobaciones automáticas y aprobación de otra persona antes del merge.
`main` es la versión integrada y publicada. Codex y Claude Code siguen las
mismas reglas, fuentes y skills compartidas.

## Configuración inicial en GitHub

Estos pasos requieren permisos de administración en el repositorio. Los archivos
de este checkout preparan el flujo; no activan por sí solos las reglas remotas.

1. En **Settings → Collaborators** (o **Collaborators and teams**), invita a las
   cuentas GitHub de quienes contribuirán. En un repositorio personal, los
   colaboradores tienen acceso de colaboración con escritura; para roles
   diferenciados y equipos, utiliza una organización. Cada persona usa su propia
   cuenta GitHub y sus propios accesos a Codex o Claude Code.
2. Conserva `main` como rama predeterminada. En **Settings → General → Pull
   Requests**, habilita **Squash merging** y eliminación automática de ramas
   después del merge. Para un flujo uniforme, deshabilita merge commits y rebase
   merging. Un PR integrado produce un commit fácil de identificar y revertir.
3. En **Settings → Rules → Rulesets**, crea un ruleset de ramas llamado
   `Proteger main`, con estado **Active**, apuntando a la rama predeterminada
   o exactamente `main`. Si tu plan solo ofrece protección clásica, configura
   el equivalente en **Settings → Branches**. La disponibilidad depende del
   plan y de si el repositorio es público o privado.
4. Aplica estas reglas:

| Regla | Configuración recomendada |
| --- | --- |
| Require a pull request before merging | Activada. |
| Required approvals | 1, de otra persona con permisos de escritura. |
| Dismiss stale approvals | Activada para volver a revisar un diff que cambió. |
| Require conversation resolution | Activada. |
| Require status checks to pass | Activada; selecciona el check real del job `build` de **Publicar OncoNova**, emitido por GitHub Actions. |
| Require branches to be up to date | Activada para comprobar integración con el `main` reciente. |
| Require linear history | Activada, compatible con squash merging. |
| Block force pushes | Activada en `main`. |
| Restrict deletions | Activada en `main`. |
| Bypass | Sin excepciones habituales para colaboradores o herramientas. |
| Restrict updates | No activarla como bloqueo adicional: impediría actualizar la rama incluso mediante PR a quienes no tengan bypass. |

El check debe haber ejecutado recientemente para poder seleccionarlo. Primero
abre un PR con los archivos compartidos y el workflow, comprueba la ejecución y
después configura el check obligatorio con el nombre que muestre GitHub.
No elijas `deploy` como requisito para fusionar: la publicación ocurre después
del merge y se omite en los PR. Una aprobación de un bot no sustituye la
aprobación humana acordada por el equipo.

Puedes importar directamente el archivo
[protect-main.json](.github/rulesets/protect-main.json) en **Settings → Rules →
Rulesets → New ruleset → Import a ruleset**. Selecciona el JSON, revisa y guarda
el ruleset. El archivo contiene las reglas anteriores, estado `active`, sin
bypass y apuntando exactamente a `refs/heads/main`. Fija el check `build` a
GitHub Actions (`integration_id: 15368`) y permite únicamente squash. Comprueba
que el repositorio tiene squash merging habilitado y que un PR real muestra
ese check; el job local del workflow se llama `build`.

La aprobación de code owners permanece desactivada hasta acordar los
responsables y versionar `CODEOWNERS`. No se añade el requisito adicional de
aprobación por alguien distinto del último pusher: junto con un PR de autoría
ajena y descarte de aprobaciones obsoletas, una aprobación permite trabajar
con un equipo de dos personas. La importación y guardado en GitHub activan la
regla; añadir el JSON al repositorio solo conserva su configuración.

5. En **Settings → Pages**, usa **GitHub Actions**. En **Settings → Environments
   → github-pages**, limita las ramas de despliegue a `main` si la opción está
   disponible. El workflow también limita la publicación a `refs/heads/main`,
   incluso cuando se ejecuta manualmente desde otra rama.

Para un equipo pequeño no hace falta una rama `develop`, merge queue ni una
plataforma adicional de previews. Los PR ejecutan verificaciones; este workflow
no despliega una preview por PR. La aprobación puede usar la vista local,
capturas y resultados documentados.

## Responsables de revisión

Designa al menos dos personas que puedan revisar y mantener el repositorio.
Quien crea un PR solicita la revisión de otra persona; una revisión del mismo
autor o de su agente no cuenta como control independiente del equipo.

`CODEOWNERS` puede asignar revisión de contenido, skills y workflows. Añádelo
cuando el equipo acuerde los usuarios reales con acceso de escritura:

```text
# Ejemplo: sustituir USUARIO_1 y USUARIO_2 por cuentas reales antes de guardarlo.
* @USUARIO_1 @USUARIO_2
/.github/ @USUARIO_1 @USUARIO_2
/AGENTS.md @USUARIO_1 @USUARIO_2
/CLAUDE.md @USUARIO_1 @USUARIO_2
/.agents/skills/ @USUARIO_1 @USUARIO_2
/site/content/ @USUARIO_1 @USUARIO_2
```

Su ubicación recomendada es `.github/CODEOWNERS`. No actives revisión obligatoria
de code owners con un único responsable: sus propios PR pueden quedar sin
otra persona habilitada para aprobarlos. Con varios owners en una línea,
GitHub acepta la aprobación de cualquiera de ellos; no exige la de todos.

## Preparar el checkout

```sh
git clone https://github.com/camilomoralessabaj/onconova.git
cd onconova
node --version
node scripts/check-skills.mjs
node scripts/check.mjs
node scripts/build.mjs
```

Requiere Node.js 22 o posterior; no hay dependencias de producción que instalar.
Las instrucciones y skills deben estar versionadas en Git para que un clone las
reciba. Publicar un snapshot del entorno cloud de una persona no las distribuye
a las instalaciones de los demás.

En este trabajo de preparación hay skills y documentación nuevas que aún no
están en el historial de Git. Incluye `.agents/skills/`, `scripts/`, las
instrucciones y documentación pública pertinente en el primer PR de equipo.
Revisa los archivos nuevos antes del commit y excluye `.local/`, secretos,
originales privados, datos de salud y resultados generados. Esta nota describe
la preparación inicial; después de integrar ese PR, un clone ya incluye los
archivos compartidos.

Codex usa `AGENTS.md` y `.agents/skills/`. Claude Code carga `CLAUDE.md`, que
importa las mismas reglas. Para descubrir las skills en Claude:

```sh
node scripts/sync-claude-skills.mjs
```

El script copia los originales a `.claude/skills/`, que queda fuera de Git.
Funciona sin enlaces simbólicos ni paquetes externos. Repite la sincronización
tras un pull, un cambio de rama o una actualización de skills. Solo reemplaza
sus copias administradas y conserva otras skills locales; rechaza colisiones
con una carpeta ajena del mismo nombre. Edita los originales de `.agents/skills/`.
Si el cliente no descubre una skill, pide que lea su `SKILL.md` por esa ruta.

El smoke test opcional necesita Python 3, Playwright y Chromium en la máquina de
quien lo ejecute. Esas herramientas están en el entorno cloud preparado, pero
un clone de Git no instala ni transmite ese runtime. Registra las comprobaciones
que no pudiste ejecutar y prepara el navegador cuando el cambio lo necesite.

## Una tarea de principio a fin

1. Crea un issue o acuerda una tarea con objetivo y aceptación. Asigna una persona
   responsable y avisa qué sección o archivos tocará. Divide los encargos por
   resultados concretos; evita que varias personas rediseñen la misma portada o
   editen el CSS global a la vez sin coordinarse.
2. Con el checkout limpio, actualiza `main` y crea una rama:

   ```sh
   git switch main
   git pull --ff-only origin main
   git switch -c feat/42-lectura-movil
   ```

   Usa `feat/`, `fix/`, `docs/` o `chore/` y un nombre de tarea. Si hay trabajo
   pendiente, consérvalo o complétalo antes de cambiar de rama. Cada conversación
   que implemente necesita su propia rama y checkout; no abras dos agentes que
   muten el mismo directorio simultáneamente. En cloud usa el aislamiento ya
   proporcionado; en local puedes usar clones separados. Los worktrees son una
   opción si se solicitan y se gestionan deliberadamente.
3. Planifica con `idea-a-tarea` cuando haya decisiones abiertas. Ejecuta el prompt
   acordado en otra conversación, seleccionando cliente, modelo y esfuerzo allí.
   Una corrección pequeña y bien definida puede ir directamente a implementación.
4. Implementa y revisa el diff. Haz las comprobaciones según el cambio; usa
   `revision-landing` para revisión general y registra resultados y límites.
5. Con autorización para publicar la rama y abrir el PR, haz commit de los
   archivos revisados y `git push -u origin <rama>`. Abre un PR en GitHub con
   base `main`, usando la plantilla del repositorio. Puedes abrirlo como draft
   mientras sigues trabajando. Describe objetivo, resultado, pruebas y límites.
6. Antes del merge, incorpora cambios recientes de `main`. Para ramas compartidas
   o principiantes, `git fetch origin` seguido de `git merge origin/main` evita
   reescribir el historial de la rama de trabajo. Repite las comprobaciones
   afectadas y solicita otra revisión si el diff aprobado cambió.
7. Cuando el check `build` esté aprobado, las conversaciones resueltas y exista
   aprobación humana, integra con **Squash and merge**. Alguien con escritura
   puede hacerlo si el ruleset lo permite; no tiene que ser siempre el dueño.
8. El push resultante en `main` inicia la publicación. Confirma el resultado de
   GitHub Actions y, si corresponde, el sitio publicado. Elimina la rama ya
   integrada y actualiza tu `main` antes de empezar otra tarea.

Para corregir un cambio integrado, abre un PR de reversión o de corrección;
no reescribas `main`. Si hay conflictos, resuelve el objetivo y la evidencia
de ambos cambios: no elijas automáticamente «todo lo mío» o «todo lo ajeno».

## Skills: elegir lo necesario

| Momento | Skills |
| --- | --- |
| Aclarar idea y producir un prompt para otro chat | `idea-a-tarea`. |
| Identidad, composición y relato | `frontend-design` + `onconova-storytelling`; `impeccable` para dirección o crítica. |
| Comparar estructuras | `wireframer` o `prototype`, según el nivel de fidelidad. |
| Ajustar paleta | `color-expert`. |
| Detalles de interacción y referencia Apple | `emil-design-eng`, `apple-design`. |
| Movimiento | `motion-design` para propósito; `animate` para implementación; `review-animations` para revisión. |
| Tacto y datos extremos | `mobile-native`, `break-ui`. |
| Consultar un patrón concreto | `ui-ux-pro-max`. |
| Revisar antes del PR | `revision-landing` + `web-design-guidelines` según el cambio. |

Inventario completo: [docs/skills.md](docs/skills.md). No cargues las 24 skills en
cada tarea ni selecciones el esfuerzo máximo por defecto. Las guías de Expo,
Swift y Sonner corresponden a esos stacks; Onconova conserva código nativo.

Ejemplo de planificación, compatible con ambos clientes mediante la ruta:

```text
Usa la skill idea-a-tarea, leyendo .agents/skills/idea-a-tarea/SKILL.md.
Mi idea es mejorar la lectura móvil de la portada.
El prompt se ejecutará en [Codex o Claude Code].
Haz preguntas solo sobre decisiones pendientes y prepara un prompt autónomo
con modelo y esfuerzo disponibles, rama de tarea, aceptación y verificaciones.
Por ahora prepara la tarea; la entrega prevista es un PR hacia main.
```

En Codex puedes usar `$idea-a-tarea`. En Claude Code, después de sincronizar,
puedes usar `/idea-a-tarea` si tu instalación la descubre. El nombre por ruta es
la alternativa común. La skill 1.2.0 adapta la recomendación al cliente de
destino; mencionar un modelo en el prompt no lo selecciona automáticamente.

Ejemplo de revisión:

```text
Usa la skill revision-landing leyendo su SKILL.md en .agents/skills/.
Revisa el diff de esta rama frente a origin/main, obtenido tras fetch.
Comprueba los riesgos reales del cambio, las fuentes y la accesibilidad.
Entrega hallazgos, comprobaciones ejecutadas y límites para el PR.
```

## Qué se verifica

El workflow ejecuta checks de contenido, compilación y skills para los PR y
para `main`. Eso no sustituye pruebas de interacción o revisión visual.

| Cambio | Comprobaciones pertinentes |
| --- | --- |
| Documentación e instrucciones | Coherencia, enlaces y `git diff --check`. |
| Skills | `node scripts/check-skills.mjs`; sincronización si usas Claude Code. |
| Relato o datos | `node scripts/check.mjs`, respaldo de fuentes y privacidad. |
| Interfaz o JavaScript | Checks del sitio, build, diff e interacciones afectadas en móvil, escritorio y teclado. |

Para una revisión de UI con el runtime de navegador preparado, inicia
`node scripts/serve.mjs` y usa el smoke test descrito en `revision-landing`.
El hallazgo histórico a 320 px con texto ampliado está en
[docs/hallazgos-landing.md](docs/hallazgos-landing.md). Tras el rediseño de Sites,
la ejecución sobre `main` (`8d3da91`) aprobó los seis casos y no reprodujo ese
desbordamiento. El CI actual no ejecuta el smoke test, por lo que un `build`
aprobado no sustituye la revisión funcional de los cambios futuros.

## Fuentes para las opciones de GitHub y los clientes

- [Reglas disponibles de rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
- [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
- [Instrucciones AGENTS.md de Codex](https://developers.openai.com/codex/guides/agents-md).
- [Skills de Claude Code](https://code.claude.com/docs/en/skills).
- [Memoria e instrucciones de Claude Code](https://code.claude.com/docs/en/memory).

Se consultaron las fuentes de rulesets y CODEOWNERS mediante el repositorio
oficial de documentación de GitHub. La consulta directa de las dos páginas de
Claude Code fue rechazada por el proxy del entorno; los enlaces se dejan para
consulta del equipo. La sincronización y los checks locales no certifican una
sesión real de Claude Code ni la activación de reglas remotas de GitHub.

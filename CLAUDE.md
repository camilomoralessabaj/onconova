# Onconova en Claude Code

@AGENTS.md

Las reglas de proyecto tienen una única fuente en `AGENTS.md`. Lee también
`CONTRIBUTING.md` antes de preparar una rama o un PR. Trabaja en la rama de la
tarea y respeta las autorizaciones del usuario para push, PR, merge y publicación.

Las skills compartidas están en `.agents/skills/`. Para que Claude Code las
descubra en su ubicación de proyecto, ejecuta desde la raíz:

```sh
node scripts/sync-claude-skills.mjs
```

El comando genera copias locales en `.claude/skills/`, ignoradas por Git.
Modifica los originales en `.agents/skills/` y vuelve a sincronizar después de
actualizarlos o cambiar de rama. Si no puedes ejecutar el comando, lee la skill
por su ruta original, por ejemplo `.agents/skills/idea-a-tarea/SKILL.md`.

Selecciona solo las skills que necesite el encargo, según `docs/skills.md`.
`idea-a-tarea` planifica y entrega un prompt para otra conversación de Codex o
Claude Code; no implementa durante esa planificación. Recomienda modelos y
esfuerzos del cliente de destino, sin suponer que los de Codex existen en Claude.
`revision-landing` organiza la revisión proporcional del diff antes de un PR.
La revisión asistida complementa la aprobación de otra persona en GitHub.

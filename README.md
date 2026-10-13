# OncoNova

Primera landing de storytelling para **CD1201 · Actividad 7.3 · FCFM, Universidad de Chile**. Recorre Desafío → Propuesta → Prototipo → Validación → Resultados → Aprendizajes → Próximos pasos.

[Sitio en GitHub Pages](https://camilomoralessabaj.github.io/onconova/) · [Maqueta del servicio](https://camilomoralessabaj.github.io/onconova/prototipo/)

El 13 de octubre de 2026 se integró el rediseño de [OncoNova · Versión de revisión en Sites](https://onconova-revision.fuzzytide4.chatgpt.site): ilustraciones propias, paleta rosa y ciruela, etiquetas de evidencia y mejoras de lectura. La procedencia y las comprobaciones están en [el registro de iteraciones](docs/iteraciones.md).

La propuesta es una **derivación acompañada dentro de una institución de salud**: orientación voluntaria, acuerdo de un apoyo prioritario, activación del contacto y confirmación de su resultado. La institución piloto está por definir. La maqueta fue creada para esta versión y **todavía no se ha probado con usuarias**.

## Trabajar en local

Requiere Node.js 22 o posterior. No hay dependencias que instalar.

```sh
node scripts/serve.mjs
```

Abre `http://127.0.0.1:4173`. Para verificar y preparar el sitio:

```sh
node scripts/check.mjs
node scripts/build.mjs
node scripts/serve.mjs --dir dist
```

Si dispones de npm, también puedes usar `npm run dev`, `npm run check`, `npm run build` y `npm run preview`. `.devcontainer/` prepara Node 22 en un entorno de desarrollo compatible. En Codespaces, inicia `node scripts/serve.mjs --host 0.0.0.0` y abre el puerto 4173.

## Editar

Para trabajar en equipo con Codex o Claude Code, sigue [CONTRIBUTING.md](CONTRIBUTING.md): una rama por tarea, PR hacia `main`, checks y aprobación de otra persona. Codex usa `AGENTS.md`; Claude Code carga `CLAUDE.md` y descubre las mismas skills después de ejecutar `node scripts/sync-claude-skills.mjs`. Las reglas de protección se activan por separado en GitHub Settings.

| Archivo | Qué contiene |
| --- | --- |
| `site/index.html` | Relato y fuentes visibles. |
| `site/prototipo/index.html` | Maqueta conceptual e instrucciones para explorarla. |
| `site/assets/styles.css` y `prototype.css` | Diseño y adaptación a distintos tamaños. |
| `site/assets/app.js` y `prototype.js` | Ampliación de texto, navegación y escenarios. |
| `site/content/project.json` | Registro de fuentes, alcance, estados, metas y opciones. |
| `site/assets/poster-hito-3.png` | Póster propio, presentado como antecedente histórico. |
| `site/assets/acompanamiento.svg` y `escucha.svg` | Ilustraciones del rediseño revisado en Sites. |

Al cambiar una afirmación, actualiza el texto y el registro de fuentes correspondiente. Los checks detectan incoherencias estructurales; la revisión humana sigue siendo necesaria para comprobar el respaldo de cada afirmación.

## Documentación y skills

- [Prompt e instrucciones de refinamiento](docs/prompt-actividad-7-3.md).
- [Inventario y lectura de la evidencia](docs/evidencia.md).
- [Diseño de la solución](docs/solucion.md) y [kit para prototipar y validar](docs/prototipo-y-validacion.md).
- [Iteraciones y verificaciones](docs/iteraciones.md).
- [Herramientas evaluadas y publicación](docs/plataformas.md).
- [Skills, repositorios de origen y cómo invocarlas](docs/skills.md).

Se incluyen skills de diseño y revisión dentro de `.agents/skills/`, documentadas en `docs/skills.md`. La skill propia `idea-a-tarea` convierte una idea en preguntas y un prompt para otro chat con modelo, esfuerzo y aceptación; `revision-landing` organiza las comprobaciones y prioridades antes de un PR. `AGENTS.md` orienta a Codex para preservar evidencia, alcance y accesibilidad. Abre una nueva conversación en el repositorio para descubrir las skills, o indica la ruta de su `SKILL.md` si el cliente no las muestra.

Hay 24 skills locales, incluyendo las 14 de [Emil Kowalski](https://github.com/emilkowalski/skills) para acabado de interfaces, animación, experiencia móvil, prototipos y pruebas con datos extremos. Cada copia conserva la licencia MIT, el commit de origen y ajustes para el brief de Onconova. Las guías de Expo, Swift y Sonner se usan únicamente en tareas de esos stacks.

## Publicar

En Settings → Pages selecciona **GitHub Actions**. El workflow `.github/workflows/pages.yml` verifica y publica los cambios de `main`; las pull requests solo verifican. Publica únicamente `dist/`, creado desde `site/`, con rutas relativas compatibles con `/onconova/`.

Los originales privados, transcripciones y archivos de trabajo quedan fuera de Git mediante `.gitignore`. No colocar datos de entrevistadas en `site/`. Las cinco entrevistas reales corresponden a exploración de necesidades; los escenarios simulados y las metas del RIA no son resultados de validación del servicio.

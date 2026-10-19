# OncoNova

Sitio y prototipo académico de acceso a apoyo psicológico para **CD1201 · Actividad 7.3 · FCFM, Universidad de Chile**. Recorre Desafío → Historia → Propuesta → Prototipado e iteración → Demostración → Preguntas → Validación → Aprendizajes, brechas y próximos pasos.

[Sitio en GitHub Pages](https://camilomoralessabaj.github.io/onconova/) · [Maqueta del servicio](https://camilomoralessabaj.github.io/onconova/prototipo/)

El 13 de octubre de 2026 se integró el rediseño de [OncoNova · Versión de revisión en Sites](https://onconova-revision.fuzzytide4.chatgpt.site): ilustraciones propias, paleta rosa y ciruela, etiquetas de evidencia y mejoras de lectura. La procedencia y las comprobaciones están en [el registro de iteraciones](docs/iteraciones.md).

El relato del 17/10/2026 presenta un **servicio acotado de transición** propuesto: exploración breve no diagnóstica, decisión voluntaria, una derivación prioritaria acompañada y confirmación de acceso compatible. La demostración, iterada el 18/10, permite completar nombre y contacto ficticios → mensaje de ejemplo personalizado por correo/WhatsApp → elección de horario o nueva propuesta según mañana/tarde y modalidad → confirmación y comprobante simulados. Los datos introducidos viven solo en memoria y se limpian al reiniciar o recargar; el PDF omite nombre y contacto. La ruta `/prototipo/` ofrece el mismo recorrido por separado. El 19/10 el equipo reportó cinco pruebas de interacción conductual y entrevistas cualitativas con cuatro usuarias postratamiento y una profesional de oncología (S13): autonomía, comprensión del proceso y coherencia entre preferencia y elección. Los resultados numéricos del RIA y la evaluación operativa institucional siguen pendientes. No se envían mensajes, realizan derivaciones ni reservan horas reales.

Se conserva el respaldo de las cinco entrevistas históricas S01/S07 como exploración de necesidades, sin asumir que son los registros de las pruebas reportadas ni sumar ambas muestras. El equipo confirmó mantener las URLs S05/S04: sus versiones consultables aún presentan el plan y el RIA sin resultados de OncoNova; no corroboran registros actualizados de las pruebas. El [guion de demostración](docs/prototipo-y-validacion.md) describe el recorrido principal y las alternativas para presentar al curso.

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
| `site/index.html` | Página principal con simulación integrada y evidencia. |
| `site/prototipo/index.html` | Demostración de agendamiento en una página independiente. |
| `site/assets/styles.css` y `prototype.css` | Diseño y adaptación a distintos tamaños. |
| `site/assets/app.js` y `prototype.js` | Ampliación de texto, fuentes y simulación de agendamiento. |
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

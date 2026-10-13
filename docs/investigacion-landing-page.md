# Investigación del tema landing-page

Fuente pedida: [github.com/topics/landing-page](https://github.com/topics/landing-page), consultada por HTTPS con respuesta 200 el 10/10/2026. Es una página de temas de GitHub, no un repositorio único. Se revisaron las descripciones de los 20 proyectos mostrados en la primera página y se inspeccionaron fuentes, requisitos y documentación de los candidatos pertinentes. No se afirma una revisión exhaustiva de todas las páginas del tema ni de todo el código de cada proyecto.

## Qué aporta al entorno

| Proyecto o grupo | Hallazgo | Decisión para Onconova |
| --- | --- | --- |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Skill de patrones, estilos y revisión de UX. | Ya instalada con scripts de consulta y adaptación al stack; conservarla sin duplicar. |
| [nateherkai/scroll-craft](https://github.com/nateherkai/scroll-craft) | Skill de composición y experiencias de scroll. Su procedimiento pide al menos cuatro familias de efectos; incluye motor, codificación de vídeo y herramientas de verificación. | Mantener como opción para otro brief. El actual exige lectura sin scroll secuestrado ni dependencia de animación; no añadir su motor ni API de generación. |
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | Colección de análisis DESIGN.md, no una skill. Se leyó el análisis de Apple: jerarquía, espacio, tipografía de sistema y superficies. | Referencia de composición. No copiar sus tokens sobre el brief ni confundir el análisis de terceros con pautas oficiales de Apple. No necesita instalarse como skill. |
| [StartBootstrap/startbootstrap-landing-page](https://github.com/StartBootstrap/startbootstrap-landing-page) | Plantilla con Bootstrap 5.2.3 y tooling de Pug/Sass. Se revisó su manifiesto y documentación. | Puede orientar comparaciones de estructura; añadirla como requisito introduciría dependencias innecesarias. |
| [arthelokyo/astrowind](https://github.com/arthelokyo/astrowind), [mearashadowfax/ScrewFast](https://github.com/mearashadowfax/ScrewFast), [HugoBlox/kit](https://github.com/HugoBlox/kit) | Plantillas y generadores de sitios con sus propios stacks. Se comprobó el manifiesto de AstroWind. | Referencias opcionales de composición y organización; no migrar Onconova por instalar herramientas de diseño. |
| [cruip/open-react-template](https://github.com/cruip/open-react-template), [cruip/tailwind-landing-page-template](https://github.com/cruip/tailwind-landing-page-template), [PageAI-Pro/page-ui](https://github.com/PageAI-Pro/page-ui) | Plantillas y componentes React/Next/Tailwind. El manifiesto de Open incluye Next, React y AOS; Page UI se presenta como colección de componentes. | Son referencias, no skills que deban instalarse. No convertir el sitio nativo en una plantilla SaaS. |
| Otros proyectos del listado | Starters, editores, ejemplos de aprendizaje y aplicaciones con fines distintos. | No justifican una instalación adicional para el alcance académico actual. |

La carencia que sí merece encapsularse es una revisión coherente de comportamiento, lectura y carga. Se añadió la skill propia **`revision-landing`**: utiliza checks existentes y un smoke test local, prioriza problemas observados y limita repeticiones. Trabaja junto a `web-design-guidelines`, `color-expert` y los criterios de evidencia, sin sustituirlos ni cargar todas las skills por defecto.

## Fuentes inspeccionadas con versión exacta

| Fuente | Commit leído | Elementos inspeccionados |
| --- | --- | --- |
| `nateherkai/scroll-craft` | `75d81f74e83692add18cd7a8a8e078b8a887a579` | README, licencia MIT y procedimiento principal de la skill. |
| `VoltAgent/awesome-design-md` | `13be5c05c63be24b57581162364167028020f043` | README y análisis DESIGN.md de Apple. |
| `StartBootstrap/startbootstrap-landing-page` | `247a46a2503c91d1157179eab297953438ec498b` | README y package.json. |

Los proyectos solo usados como referencia no se copiaron al checkout. Las dos skills propias usan instrucciones redactadas para Onconova; no incorporan assets, marcas o código de esos proyectos. Las fuentes de las skills previamente instaladas siguen en `.agents/skills/sources.lock.json`.

## Los 20 proyectos observados

1. `nextlevelbuilder/ui-ux-pro-max-skill`
2. `VoltAgent/awesome-design-md`
3. `HugoBlox/kit`
4. `ant-design/ant-design-landing`
5. `arthelokyo/astrowind`
6. `causefx/Organizr`
7. `cruip/open-react-template`
8. `cruip/tailwind-landing-page-template`
9. `nateherkai/scroll-craft`
10. `ixartz/Next-JS-Landing-Page-Starter-Template`
11. `dunky11/react-saas-template`
12. `LiveDuo/destack`
13. `mdbootstrap/adminlte-laravel`
14. `Blazity/next-saas-starter`
15. `PageAI-Pro/page-ui`
16. `StartBootstrap/startbootstrap-landing-page`
17. `issaafalkattan/React-Landing-Page-Template`
18. `keshavgbpecdelhi/Web-Development`
19. `tailwindtoolbox/Landing-Page`
20. `mearashadowfax/ScrewFast`

## Integración con las indicaciones oficiales

Se pudo leer completa la [guía oficial de buenas prácticas](https://learn.chatgpt.com/guides/best-practices), antes bloqueada. `idea-a-tarea` ahora aplica objetivo, contexto, restricciones y terminado cuando; usa entrevista previa para ambigüedad y recomienda modelo/esfuerzo proporcional. `docs/code_review.md` reúne expectativas de revisión, siguiendo el patrón documentado de mantener AGENTS.md breve y referenciar guías de tareas concretas.

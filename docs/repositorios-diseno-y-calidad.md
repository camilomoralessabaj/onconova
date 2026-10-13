# Repositorios útiles para diseño y revisión

Investigación web realizada el 10/10/2026 mediante búsquedas públicas de GitHub, lecturas HTTPS y revisión de los repositorios fuente de las skills instaladas. Se priorizó utilidad para un sitio estático con HTML, CSS y JavaScript nativos. Esta lista es una recomendación; no se incorporaron automáticamente paquetes ni workflows de CI.

La revisión adicional del catálogo solicitado está en [investigacion-landing-page.md](investigacion-landing-page.md). Se añadió `revision-landing` para comprobación y optimización proporcional; UI UX Pro Max ya estaba instalada y los motores de scroll/plantillas de otros stacks se dejaron como referencias según el brief.

| Repositorio | Aporte | Aplicación en Onconova |
| --- | --- | --- |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Dirección y crítica de diseño, auditoría y refinamiento. | Skill instalada. Elegir composición y un rasgo distintivo, luego criticar claridad y coherencia. |
| [anthropics/skills](https://github.com/anthropics/skills) | Frontend Design y herramientas para crear/validar skills. | Frontend Design preservada; validador de Skill Creator utilizado para comprobar metadatos. |
| [agilek/wireframer-skill](https://github.com/agilek/wireframer-skill) | Prototipos de baja fidelidad y navegación. | Skill instalada con aislamiento local y sin dependencias obligatorias. |
| [meodai/skill.color-expert](https://github.com/meodai/skill.color-expert) | Teoría, accesibilidad y referencias de color. | Skill instalada; útil para revisar roles y combinaciones de la paleta existente. |
| [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | Principios de animación para interfaces. | Skill instalada; movimiento puntual y compatible con reducción de animaciones. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Base consultable de UX, estilos y patrones. | Skill y búsqueda local instaladas; recomendaciones filtradas por el brief. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Pautas de interfaz y skills para agentes. | Web Design Guidelines ya instalada; evitar cargar guías React en el sitio nativo. |
| [microsoft/playwright](https://github.com/microsoft/playwright) | Pruebas reales en navegador, múltiples tamaños y motores. | Primera prioridad para automatizar flujos, teclado, consola y regresiones; el entorno ya dispone de Chromium y Playwright Python. |
| [dequelabs/axe-core](https://github.com/dequelabs/axe-core) | Motor de auditoría automática de accesibilidad. | Complemento de Playwright para etiquetas, contraste y semántica; no sustituye revisión de teclado y lectura humana. |
| [w3c/aria-practices](https://github.com/w3c/aria-practices) | Patrones y comportamiento accesible documentados por W3C. | Consultar al cambiar controles o navegación; preferir controles HTML nativos antes de recrearlos con ARIA. |
| [GoogleChrome/lighthouse](https://github.com/GoogleChrome/lighthouse) | Auditoría de rendimiento y buenas prácticas web. | Revisión complementaria si cambian imágenes, fuentes o scripts; comprobar métricas en condiciones comparables. |
| [obra/superpowers](https://github.com/obra/superpowers) | Skills de planificación, depuración y verificación. | Consultar procesos acotados; no instalar toda la metodología ni imponer agentes o ramas adicionales por defecto. |
| [reviewdog/reviewdog](https://github.com/reviewdog/reviewdog) | Llevar hallazgos de analizadores a la revisión de PR. | Útil cuando haya analizadores concretos; no revisa por sí solo ni garantiza corrección. Integración de PR requiere autorización y permisos de GitHub. |
| [github/codeql-action](https://github.com/github/codeql-action) | Ejecutar análisis de seguridad con CodeQL. | Opción futura si el JavaScript crece; valorar configuración, cobertura y coste antes de añadir CI. |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | Descubrir e instalar skills en distintos agentes. | Útil para gestión futura; revisar fuentes y versiones antes de ejecutar un instalador masivo. |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | Diseño de interacción, movimiento, revisión, prototipos y casos extremos. | Sus 14 skills están integradas; [inventario y ajustes locales](skills.md#skills-de-emil-kowalski). |
| [emilkowalski/sonner](https://github.com/emilkowalski/sonner) | Notificaciones transitorias para React. | Guía `ask-sonner` instalada. La biblioteca no es necesaria para los estados nativos de esta landing. |
| [emilkowalski/vaul](https://github.com/emilkowalski/vaul) | Paneles deslizables para React. | Referencia de interacción; no incorporada. Su README declara falta de mantenimiento y el sitio no necesita un drawer. |

## Webs de referencia para diseño

| Web | Uso en Onconova |
| --- | --- |
| [21st.dev](https://21st.dev) | Explorar componentes y patrones visuales para apoyar composición e interacción. Evalúa cada ejemplo según el brief, accesibilidad, licencia y dependencias; adapta las ideas al HTML/CSS/JS nativo del proyecto. |

Se añadió `21st.dev` y `www.21st.dev` a los destinos permitidos del borrador del entorno, conservando `learn.chatgpt.com` y la configuración de gestores de paquetes. El guardado requiere publicar la configuración para aplicarse a futuros entornos. La consulta directa devolvió un rechazo HTTP 403 del proxy antes de aplicar el cambio; el catálogo actual y sus servicios no se presentan como verificados. La referencia web no instala una skill, un componente ni una integración con sus servicios.

## Evaluación de Sonner y Vaul · 10/10/2026

Se revisaron README y `package.json` de los dos repositorios solicitados. Son bibliotecas de componentes, no repositorios con un `SKILL.md` adicional en los archivos revisados. La guía de Sonner proviene de `emilkowalski/skills` y ya se incluyó como `ask-sonner`.

| Proyecto y copia consultada | Requisitos observados | Decisión para el alcance actual |
| --- | --- | --- |
| [Sonner · `8e4662b`](https://github.com/emilkowalski/sonner/tree/8e4662b39255120b62138312058f5d77c0139a5e), manifiesto 2.0.8 | React y React DOM 18/19 como peer dependencies; licencia MIT. | Conservar `ask-sonner` para una tarea compatible. Los mensajes de estado actuales están junto a la acción y usan `aria-live`; añadir toasts no resuelve una necesidad del brief. |
| [Vaul · `3e97aac`](https://github.com/emilkowalski/vaul/tree/3e97aac6a38e4481bade71d7233ed6002e80f9b0), manifiesto 1.1.2 | React y React DOM como peer dependencies, dependencia de `@radix-ui/react-dialog`; licencia MIT. El README dice “This repo is unmaintained”. | No incorporar como dependencia para esta landing. No hay un drawer que implementar y el mantenimiento declarado desaconseja adoptarlo por defecto en un proyecto futuro. |

El `package.json` de Onconova no declara dependencias de producción. Esta revisión mantiene ese alcance. Si un encargo futuro requiere React y notificaciones o paneles, comprueba nuevamente compatibilidad, mantenimiento y comportamiento accesible antes de elegir la biblioteca. Las menciones de Vaul en recetas de diseño son referencias, no una recomendación vigente de instalación.

## Orden práctico antes de un PR

Primero usa los checks existentes de contenido y compilación y revisa el diff. Para cambios visuales, comprueba las páginas e interacciones con navegador, móvil, teclado y movimiento reducido. Después agrega axe-core o Lighthouse si aportan cobertura al cambio. Una revisión humana sigue siendo necesaria para personalidad visual, claridad del relato y respaldo de afirmaciones.

`idea-a-tarea` incluye [una pauta de revisión](../.agents/skills/idea-a-tarea/references/revision.md) que incorpora esa separación. La revisión debe informar fallos y límites reales; una herramienta automática no garantiza «cero errores» ni demuestra efectividad de la propuesta de salud.

---
name: revision-landing
description: Revisar y priorizar mejoras de calidad de una landing antes de cerrar cambios o preparar un PR. Usar cuando pidan revisar la página, detectar regresiones, comprobar móvil y teclado, optimizar carga o auditar una landing. En Onconova selecciona checks según el diff, comprueba evidencia, semántica, comportamiento, accesibilidad y rendimiento, y entrega hallazgos verificables sin prometer cero errores.
metadata:
  version: "1.0.0"
---

# Revisión de una landing

El objetivo es detectar problemas que afecten a visitantes y presentar mejoras con evidencia. La revisión por sí sola no autoriza un rediseño, publicación o instalación de dependencias.

## 1. Acotar la revisión

Lee AGENTS.md, el brief y el diff, incluyendo los archivos nuevos pertinentes. Distingue cambios propios de trabajo previo. Si el usuario pide revisión de un PR, usa la base o el commit indicado; no adivines una base ni hagas fetch/push innecesario. Para una revisión local usa los cambios existentes. En una página sin diff, identifica las rutas y el resultado que debe poder realizar la persona.

En Onconova lee `docs/brief.md` y, si cambia contenido, `docs/evidencia.md` y `site/content/project.json`. Usa el checkout existente; no crees un worktree por defecto. Para criterios ampliados lee [docs/code_review.md](../../../docs/code_review.md).

## 2. Seleccionar comprobaciones

Empieza por los fallos funcionales, evidencia y accesibilidad. Selecciona las comprobaciones por el cambio; no ejecutes una batería visual completa al cambiar solo documentación. Los cambios de interfaz necesitan inspección de las superficies afectadas, además de integridad y build.

Desde la raíz de Onconova:

```sh
node scripts/check.mjs
node scripts/build.mjs
git diff --check
```

Si se modificaron skills, añade `node scripts/check-skills.mjs`. No describas un comando no ejecutado como aprobado.

## 3. Comprobar comportamiento e interfaz

Para cambios de HTML, CSS o JS, inicia `node scripts/serve.mjs` en un terminal persistente si no hay un servidor válido. Verifica las páginas con peticiones locales y el navegador. Detén solamente servidores que hayas iniciado. No crees enlaces de preview a localhost durante onboarding.

Esta skill incluye una prueba funcional para Onconova, con Python 3, Playwright y Chromium disponibles en el entorno. No instala paquetes ni escribe en el sitio:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/revision-landing/scripts/smoke.py \
  --base-url http://127.0.0.1:4173 \
  --report .local/revision-landing/report.json \
  --screenshots .local/revision-landing/capturas
```

El script prueba las dos páginas a 1440, 390 y 320 px, teclado básico, ampliación de texto, controles de la portada y estados de la maqueta. Registra errores de consola, páginas y recursos; los contextos separados evitan mezclar preferencias guardadas. Usa `--width` para acotar tamaños cuando el alcance lo permita. También admite `/onconova/` en una URL base local para comprobar rutas de un montaje equivalente a Pages.

Inspecciona las capturas y las interacciones afectadas. El script no demuestra foco visual correcto, contraste de toda la página, comprensión, funcionamiento en Safari o accesibilidad completa. Para esos aspectos utiliza `web-design-guidelines`, `color-expert` o comprobaciones manuales pertinentes. Para movimiento prueba también el estado normal y `prefers-reduced-motion`; con JS desactivado el relato y los enlaces esenciales deben seguir disponibles.

## 4. Priorizar optimizaciones

Usa [riesgos-y-comprobaciones.md](references/riesgos-y-comprobaciones.md). Busca mejoras vinculadas a un problema observado: imágenes pesadas, recursos externos evitables, contenido que cambia de posición, estados poco claros o navegación confusa. Conserva personalidad, evidencia y accesibilidad. La referencia visual de otro proyecto no justifica añadir sus frameworks ni copiar marca o resultados.

Para rendimiento compara tamaños y carga con condiciones similares antes/después. El tiempo de localhost no representa la red de visitantes. Lighthouse y axe-core pueden complementar una revisión cuando estén disponibles y aporten cobertura; no añadas herramientas ni perseguir un score 100 por defecto. Si una herramienta no está disponible, describe qué quedó sin comprobar y utiliza las capacidades existentes.

## 5. Entregar y cerrar

Presenta problemas por gravedad, con archivo/línea, consecuencia, reproducción o evidencia y una corrección concreta. Distingue fallos del cambio, defectos previos y recomendaciones opcionales. Si no hay problemas en lo revisado, indica alcance y límites; no certifiques ausencia total de errores.

Si el usuario pidió corregir o el encargo incluye implementación y revisión, corrige los problemas introducidos y repite los checks afectados. Si pidió únicamente revisión, entrega hallazgos. Termina cuando los criterios pertinentes estén satisfechos; no repitas toda la auditoría sin nueva evidencia. Preparar un resumen de PR no autoriza crearlo, hacer push, merge o publicar.

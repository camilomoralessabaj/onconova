# Revisión de cambios de Onconova

Lee las reglas de AGENTS.md. Aplica esta guía sobre el diff o las superficies solicitadas. Una revisión de PR prepara hallazgos y evidencia; no autoriza push, merge o publicación.

1. Identifica el objetivo, alcance y criterios de aceptación; conserva trabajo ajeno y separa problemas previos de regresiones.
2. Revisa respaldo factual, estados de evidencia y privacidad cuando cambie contenido. El prototipo no registra efectividad ni presta servicios de salud reales.
3. Ejecuta los checks pertinentes. Para interfaz: `node scripts/check.mjs`, `node scripts/build.mjs`, `git diff --check` y comprobación real de las rutas e interacciones. Para skills: añade `node scripts/check-skills.mjs` y comprueba herramientas nuevas.
4. Para interfaz, selecciona revisión de móvil, escritorio, texto ampliado, teclado, foco, contraste y reducción de movimiento. Usa la skill `revision-landing` y su smoke test cuando haya riesgo de regresión funcional. Una comprobación automática no sustituye la inspección visual y la comprensión humana.
5. Valora rendimiento con medidas pertinentes: bytes y dimensiones de recursos, cambios de posición y dependencias externas. Prioriza un problema observado, sin inferir tiempos reales desde localhost ni adoptar librerías por una plantilla.
6. Presenta hallazgos por gravedad, archivo/línea, impacto y reproducción. Distingue bloqueantes, defectos previos y mejoras opcionales. Corrige solo si el encargo lo autoriza, y repite los checks afectados.
7. Cierra con alcance revisado, checks ejecutados y límites. No certifiques «cero errores» ni ocultes comprobaciones no realizadas. Prepara un resumen de PR cuando corresponda.

Para tareas complejas puede usarse `/review` con estas instrucciones si el cliente lo admite; la skill también permite una segunda pasada local sin delegar a otros agentes ni requerir una integración externa.

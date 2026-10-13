# Hallazgo de la prueba de landing · 10/10/2026

**Estado actualizado al 13/10/2026:** el hallazgo siguiente corresponde a la versión anterior al rediseño de Sites. Al aplicar la configuración compartida sobre `main` (`8d3da91`), el smoke test de las dos páginas a 1440, 390 y 320 px produjo seis aprobados, incluidos texto ampliado e interacciones. El desbordamiento descrito no se reprodujo. El reporte de esa ejecución está en `.local/revision-landing/report.json` del checkout de verificación, fuera del repositorio público. Esto no certifica todos los aspectos de accesibilidad ni pruebas en hardware real.

Se probó la nueva herramienta de `revision-landing` contra el sitio existente, sin cambiar archivos de `site/`. Los seis casos combinaron portada y maqueta con anchos 1440, 390 y 320 px, teclado básico, texto ampliado e interacciones. Resultado final: **cinco aprobados y uno fallido**. El fallo es de la composición existente de la portada, no de la instalación del entorno.

## Portada: desbordamiento con texto ampliado a 320 px

Ubicación pertinente: `site/assets/styles.css:70` define tres columnas `1fr` para `.hero-route`; las reglas móviles están en la línea 258. En la condición reproducida, el elemento «Acompañamos» supera el ancho disponible y queda cortado hacia la derecha.

Reproducción en Chromium:

1. Abrir la portada local a 320 px de ancho, con movimiento reducido.
2. Activar «Texto más grande».
3. Bajar a la maqueta dentro de la portada y elegir «Por ahora no lo necesito».
4. Volver al recorrido de la portada: el documento mide 367 px para un viewport de 320 px y el tercer paso queda cortado.

La reproducción sin ampliar texto mantuvo 320 px. El mismo escenario con texto ampliado a 390 y 1440 px aprobó. La maqueta independiente aprobó en los tres tamaños.

Se conservan el informe de seis casos en `.local/revision-landing/report.json` y las capturas de diagnóstico `hero-overflow-320.png` y `portada-overflow-320.png` en la misma carpeta. Esos archivos son evidencias locales, no contenido a publicar. La herramienta también se comprobó contra HTTP 404 (dos fallos y salida 1 esperados) y sin navegador (estado no ejecutado y salida 2 esperados), para verificar que no informa éxito falso.

El ajuste de la composición móvil queda para una tarea de implementación: adaptar el ancho mínimo de las columnas y el corte de palabras o la distribución móvil, conservando legibilidad y las tres etapas. Ocultar simplemente el desbordamiento no resuelve el contenido cortado. La aceptación debe repetir este recorrido con texto ampliado y comprobar 320, 390 y 1440 px, además de los checks del proyecto.

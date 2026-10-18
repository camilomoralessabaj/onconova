# Prototipo y guion de demostración

Versión 18/10/2026. La landing contiene el prototipo completo; `/prototipo/` permite presentarlo por separado. Son la misma experiencia. Usar datos ficticios; la página no solicita información personal.

## Recorrido principal para la profesora

1. Desde la portada, pulsar **Explorar mi primera hora**.
2. Elegir WhatsApp o correo y videollamada o presencial. Marcar que se entiende la simulación.
3. Pulsar **Simular mi solicitud**. Ver la recepción y el mensaje que coordinación enviaría. Aún no hay reserva.
4. Pulsar **Ver horarios de ejemplo**. Elegir un horario ficticio y confirmar.
5. Mostrar la cita simulada y pulsar **Descargar comprobante PDF**. Abrir el documento de una página A4, comparar fecha completa con año, hora de Santiago de Chile, canal y modalidad con la confirmación. Mostrar las indicaciones y la nota de prototipo: no existe reserva real ni acredita atención, cobertura o pago; no se envió ningún mensaje.
6. Cambiar horario, confirmar y descargar otra vez para mostrar los datos actualizados. Reiniciar elimina la confirmación y el acceso al comprobante. Probar también la otra modalidad: presencial sin dirección real asignada; videollamada sin sala real habilitada.

## Escenarios alternativos

- **Ninguno me acomoda:** registrar preferencia de mañana/tarde; mostrar coordinación pendiente, contacto por el canal elegido y ausencia de hora confirmada. Al cambiar preferencia se pide registrarla de nuevo.
- **Prefiero pensarlo / Ahora no lo necesito:** cerrar sin iniciar solicitud y poder volver al comienzo.
- **Error de selección:** intentar confirmar sin horario; indicar la corrección y llevar foco al primer horario.
- **Privacidad:** recargar reinicia el escenario. Solo la preferencia de tamaño de texto puede persistir; no hay mensajes, backend, analítica ni registro de datos de salud.

## Validación pendiente

Observar con usuarias si pueden completar el recorrido sin ayuda, explicar quién debería contactar y distinguir solicitud, espera, cita y atención. La prueba debe registrar dificultades y errores reales. No completar resultados por estimación.

Las cinco entrevistas existentes exploran necesidades y no validan este prototipo. Las metas del RIA (80 %) siguen siendo propuestas; revisar instrumento y pertinencia antes de experimentar. Responsables, institución, costos, cobertura, capacidad de agenda y plazos deben definirse antes de un piloto real.

## Verificación técnica

`node scripts/check.mjs`, `node scripts/build.mjs` y `git diff --check`. Para el nuevo flujo: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --base-url http://127.0.0.1:4173 --output work/qa-comprobante`, con `node scripts/serve.mjs` activo. Requiere Python 3, Playwright, Chromium, PyMuPDF (`fitz`) y Poppler (`pdftotext`) disponibles solo para QA; no son dependencias de producción. La prueba abre, extrae texto y renderiza cada PDF, comprueba una página A4 sin reparación, recortes ni superposiciones de texto, las cuatro combinaciones, reprogramación, reinicio, teclado, errores y limpieza de recursos. Fija el reloj cerca del cambio de año y usa zonas de dispositivo distintas a Santiago; las fechas de esos archivos son ficticias. Los días de agenda siguen siendo ejemplos de lunes a viernes, sin calendario de feriados ni cupos reales.

El smoke anterior de la skill revision-landing comprueba la maqueta multisoporte retirada. Esta versión usa un test específico del nuevo recorrido, conservando las skills sin modificaciones.

Los PDFs de prueba, texto extraído y capturas quedan en `work/`, nunca en `site/`. Se conserva el rechazo de archivos `.pdf` en los checks y el build. La descarga informa su inicio; el navegador controla el guardado o la cancelación final. El PDF usa texto seleccionable en español y gráficos vectoriales con fuentes estándar PDF; no es un PDF etiquetado ni certifica PDF/UA.

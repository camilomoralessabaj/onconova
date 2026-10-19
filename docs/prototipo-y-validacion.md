# Prototipo y guion de demostración

Versión 18/10/2026. La landing contiene el prototipo completo; `/prototipo/` permite presentarlo por separado. Son la misma experiencia. Usar datos ficticios en los campos de nombre preferido y contacto. Nada se envía; solo viven en memoria hasta reiniciar o recargar. No introducir datos reales ni antecedentes de salud.

## Recorrido principal para la profesora

1. Desde la portada, pulsar **Explorar mi primera hora**.
2. Escribir un nombre preferido ficticio. Elegir WhatsApp e ingresar un teléfono ficticio de 8–15 dígitos, o elegir correo e ingresar uno de ejemplo (nombre@example.com). Elegir videollamada o presencial y marcar que se entiende la simulación. El formato no verifica existencia del correo ni si el teléfono tiene WhatsApp. Cambiar de canal borra y desactiva el campo anterior.
3. Pulsar **Simular mi solicitud**. Ver el nombre y el contacto introducidos en la vista previa del mensaje. Aún no hay reserva. Volver con **Cambiar preferencias** permite editarlos.
4. Pulsar **Ver horarios de ejemplo**. Elegir un horario ficticio y confirmar.
5. Comparar nombre y contacto en el resumen de la cita simulada y pulsar **Descargar comprobante PDF**. Abrir el documento de una página A4, comparar fecha completa con año, hora de Santiago de Chile, canal y modalidad con la confirmación. El PDF omite nombre y contacto; no conserva la identidad fija anterior. Mostrar las indicaciones y la nota de prototipo: no existe reserva real ni acredita atención, cobertura o pago; no se envió ningún mensaje.
6. Cambiar horario, confirmar y descargar otra vez para mostrar los datos actualizados. Reiniciar elimina la confirmación y el acceso al comprobante. Probar también la otra modalidad: presencial sin dirección real asignada; videollamada sin sala real habilitada.

## Escenarios alternativos

- **Ninguno me acomoda:** elegir mañana/tarde y mantener o cambiar modalidad; pulsar **Ver nuevos horarios de ejemplo**. Comparar tres fechas posteriores, distintas de las rechazadas, elegir una y llegar a confirmación y PDF. Cambiar modalidad o propuesta limpia la selección y confirmación anterior.
- **Segundo rechazo:** vuelve a **Ninguno me acomoda** en la nueva propuesta. Mostrar el estado pendiente, sin comprobante ni promesa de contacto real. **Revisar preferencias de horarios** permite otra propuesta; **Dejar pendiente y salir** borra los datos y cierra sin confirmar.
- **Edición:** desde la confirmación, **Editar datos y preferencias** invalida la cita y limpia el mensaje anterior. Cambiar nombre, canal/contacto y modalidad, avanzar y comprobar que solo aparecen los nuevos datos.
- **Datos incompletos:** enviar con nombre vacío o espacios, contacto vacío o formato inválido. Leer el error junto al campo y mostrar el foco en el primer error. El campo oculto de otro canal no bloquea; escribir una corrección actualiza el error inmediatamente.
- **Prefiero pensarlo / Ahora no lo necesito:** cerrar sin iniciar solicitud y poder volver al comienzo.
- **Error de selección:** intentar confirmar sin horario; indicar la corrección y llevar foco al primer horario.
- **Privacidad:** recargar reinicia el escenario. Solo la preferencia de tamaño de texto puede persistir; el nombre y contacto ficticios no se guardan en URLs, cookies, almacenamiento, consola ni solicitudes de red. No hay mensajes enviados, backend, analítica ni registro de datos de salud.

## Evaluación reportada y comprobaciones pendientes

El 19/10/2026 el equipo confirmó cinco pruebas de interacción conductual y entrevistas cualitativas con cuatro usuarias postratamiento y una profesional de oncología (S13). Se evaluaron autonomía, comprensión del proceso y coincidencia entre preferencia declarada y elección realizada en exploración breve y simulación de derivación. El reporte no identifica el soporte o la versión aplicada. No demuestra efectividad ni acceso real a atención.

Las entrevistas históricas S01/S07 exploran necesidades; no se asumen idénticas a estas pruebas ni se suman muestras. Los destinos S05/S04 se mantienen por confirmación del equipo con esta aclaración: el texto accesible de S05 sigue siendo un plan y las columnas de resultados de OncoNova en S04 están vacías. Los valores numéricos y el cumplimiento de las metas del RIA (80 %) siguen pendientes; no se infieren éxitos, denominadores ni porcentajes. Para próximas pruebas, registrar dificultades reales y distinguir solicitud, espera, cita y atención. La evaluación operativa institucional, responsables, costos, cobertura, capacidad y plazos siguen pendientes antes de un piloto real.

## Verificación técnica

`node scripts/check.mjs`, `node scripts/build.mjs` y `git diff --check`. Para el nuevo flujo: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --base-url http://127.0.0.1:4173 --output work/qa-contacto-alternativas`, con `node scripts/serve.mjs` activo. Requiere Python 3, Playwright, Chromium, PyMuPDF (`fitz`) y Poppler (`pdftotext`) disponibles solo para QA; no son dependencias de producción. La prueba abre, extrae texto y renderiza cada PDF, comprueba una página A4 sin reparación, recortes ni superposiciones de texto, las cuatro combinaciones, reprogramación, reinicio, teclado, errores y limpieza de recursos. Fija el reloj cerca del cambio de año y usa zonas de dispositivo distintas a Santiago; las fechas de esos archivos son ficticias. Los días de agenda siguen siendo ejemplos de lunes a viernes, sin calendario de feriados ni cupos reales.

El smoke anterior de la skill revision-landing comprueba la maqueta multisoporte retirada. Esta versión usa un test específico del nuevo recorrido, conservando las skills sin modificaciones.

Los PDFs de prueba, texto extraído y capturas quedan en `work/`, nunca en `site/`. Se conserva el rechazo de archivos `.pdf` en los checks y el build. La descarga informa su inicio; el navegador controla el guardado o la cancelación final. El PDF usa texto seleccionable en español y gráficos vectoriales con fuentes estándar PDF; no es un PDF etiquetado ni certifica PDF/UA.

También ejecutar `scripts/test-step-motion.py --base-url http://127.0.0.1:4173 --output work/qa-contacto-motion` y `scripts/test-reading-guide.py` con el mismo servidor. Revisar capturas y foco a 1440, 390 y 320 px, texto ampliado, teclado y movimiento reducido. La transición existente de opacidad (150 ms) se reutiliza para nuevas propuestas y estado pendiente; las validaciones, escritura, cambios de canal y selección son inmediatos. Las fixtures y controles de estrés son locales en `.local/break-ui/`, sin publicarlos ni mezclarlos con fuentes del proyecto.

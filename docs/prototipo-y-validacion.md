# Prototipo y guion de demostración

Versión 22/11/2026. La landing pública contiene el prototipo completo.
`/prototipo/` permite presentarlo por separado. Las dos rutas usan la misma
cuenta de ejemplo y las mismas reglas. Los datos están precargados y el
recorrido permanece en memoria.

## Recorrido principal para la profesora

1. Desde la portada, pulsar **Explorar mi primera hora**. Elegir Fonasa o
   Isapre y pulsar **Entrar con cuenta de ejemplo**. La maqueta usa un perfil
   fijo sin contraseña.
2. Elegir WhatsApp o correo y videollamada o presencial. Marcar que se
   entiende la simulación y pulsar **Simular mi solicitud**. Revisar el
   contacto ficticio en el mensaje y comprobar que coincide con el canal.
3. Pulsar **Ver horarios de ejemplo**. Confirmar un horario de ejemplo.
   Comparar el resumen y el **Comprobante de agendamiento** en PDF. El
   documento conserva fecha, hora de Santiago, modalidad y canal.
   Excluye nombre y contacto.
4. Pulsar **Simular inicio de la sesión**. Comparar la cita y el monto
   ilustrativo de $20.000 CLP. Pulsar **Simular pago** y revisar la
   **Boleta de ejemplo** en pantalla, con referencia ficticia y sin validez
   tributaria. La maqueta no solicita tarjeta ni RUT.
5. Pulsar **Simular término de la atención**. En Fonasa, leer la orientación
   sobre la modalidad y los bonos que pueden corresponder en Libre Elección.
   En Isapre, revisar el borrador con los datos de la cuenta, el plan
   ficticio y la referencia de la boleta. La vista del borrador permite
   revisarlo sin enviar. Su ejemplo no asegura elegibilidad, aprobación ni
   cobertura. **Volver a la boleta de ejemplo** reabre el mismo documento.
6. Repetir con la otra previsión. Probar **Cambiar horario** y **Cancelar
   cita de ejemplo**. Comprobar que se borran el pago, la boleta y el
   borrador de la cita anterior. **Cerrar sesión de ejemplo**, **Volver a
   empezar** y recargar limpian la cuenta activa y el avance.

## Escenarios alternativos

- **Ninguno me acomoda.** Marcar varios días de lunes a viernes y una o más franjas de Santiago (09:00–12:00, 12:00–15:00 o 15:00–18:00). Las franjas elegidas valen para todos esos días. Mantener o cambiar modalidad y pulsar **Ver nuevos horarios de ejemplo**. Comparar hasta tres opciones que admitan los 45 minutos completos. Cambiar de propuesta limpia la selección anterior.
- **Selección de preferencias incompleta.** Enviar sin días o sin franjas. Leer los errores y comprobar que el primer grupo incompleto recibe foco.
- **Rechazo de alternativas o agenda sin coincidencias.** El estado pendiente explica qué pasó. **Revisar preferencias de horarios** permite buscar de nuevo o volver voluntariamente a la última propuesta, con la selección vacía. Las búsquedas nuevas excluyen horarios rechazados. **Dejar pendiente y salir** borra los datos y cierra sin confirmar.
- **Edición.** Desde la confirmación, **Editar preferencias de reserva** invalida la cita y limpia el mensaje. Cambiar canal o modalidad y comprobar que el nuevo mensaje utiliza el contacto de ejemplo del canal seleccionado.
- **Consentimiento y retorno.** Simular una solicitud sin marcar el consentimiento y comprobar el foco en la casilla. En el paso de pago, **Cancelar inicio y volver a la cita** vuelve a la reserva confirmada sin generar boleta.
- **Prefiero pensarlo / Ahora no lo necesito:** cerrar sin iniciar solicitud y poder volver al comienzo.
- **Error de selección:** intentar confirmar sin horario; indicar la corrección y llevar foco al primer horario.
- **Privacidad:** recargar reinicia el escenario. Solo la preferencia de tamaño de texto puede persistir; la previsión, el avance y los documentos no se guardan en URLs, cookies, almacenamiento, consola ni solicitudes de red. No hay mensajes enviados, backend, analítica ni registro de datos de salud.

## Evaluación reportada y comprobaciones pendientes

El 19/10/2026 el equipo confirmó cinco pruebas de interacción conductual y entrevistas cualitativas con cuatro usuarias postratamiento y una profesional de oncología (S13). Se evaluaron autonomía, comprensión del proceso y coincidencia entre preferencia declarada y elección realizada en exploración breve y simulación de derivación. El reporte no identifica el soporte o la versión aplicada. No demuestra efectividad ni acceso real a atención.

Las entrevistas históricas S01/S07 exploran necesidades; no se asumen idénticas a estas pruebas ni se suman muestras. Los destinos S05/S04 se mantienen por confirmación del equipo con esta aclaración: el texto accesible de S05 sigue siendo un plan y las columnas de resultados de OncoNova en S04 están vacías. Los valores numéricos y el cumplimiento de las metas del RIA (80 %) siguen pendientes; no se infieren éxitos, denominadores ni porcentajes. Para próximas pruebas, registrar dificultades reales y distinguir solicitud, espera, cita y atención. La evaluación operativa institucional, responsables, costos, cobertura, capacidad y plazos siguen pendientes antes de un piloto real.

## Verificación técnica

`node scripts/check.mjs`, `node scripts/build.mjs` y `git diff --check`. Para el nuevo flujo: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --base-url http://127.0.0.1:4173 --output work/qa-cuenta-pago`, con `node scripts/serve.mjs` activo. Requiere Python 3, Playwright, Chromium, PyMuPDF (`fitz`) y Poppler (`pdftotext`) disponibles solo para QA; no son dependencias de producción. La prueba abre, extrae texto y renderiza cada PDF, comprueba una página A4 sin reparación, recortes ni superposiciones de texto, las cuatro combinaciones, reprogramación, reinicio, teclado, errores y limpieza de recursos. Además comprueba ambas previsiones, la boleta y el borrador, cancelaciones, acciones repetidas, cierre de sesión y recarga. Fija el reloj cerca del cambio de año y usa zonas de dispositivo distintas a Santiago; las fechas de esos archivos son ficticias. Los días de agenda siguen siendo ejemplos de lunes a viernes, sin calendario de feriados ni cupos reales.

El smoke anterior de la skill revision-landing comprueba la maqueta multisoporte retirada. Esta versión usa un test específico del nuevo recorrido, conservando las skills sin modificaciones.

Los PDFs de prueba, texto extraído y capturas quedan en `work/`, nunca en `site/`. Se conserva el rechazo de archivos `.pdf` en los checks y el build. La descarga informa su inicio; el navegador controla el guardado o la cancelación final. El PDF usa texto seleccionable en español y gráficos vectoriales con fuentes estándar PDF; no es un PDF etiquetado ni certifica PDF/UA.

También ejecutar `scripts/test-step-motion.py --base-url http://127.0.0.1:4173 --output work/qa-cuenta-pago-motion` y `scripts/test-reading-guide.py` con el mismo servidor. Revisar capturas y foco a 1440, 390 y 320 px, texto ampliado, teclado y movimiento reducido. La transición existente de opacidad (150 ms) se reutiliza para nuevas propuestas y estado pendiente; las validaciones, escritura, cambios de canal y selección son inmediatos. Las fixtures y controles de estrés son locales en `.local/break-ui/`, sin publicarlos ni mezclarlos con fuentes del proyecto.

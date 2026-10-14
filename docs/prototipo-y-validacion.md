# Prototipo y guion de demostración

Versión 14/10/2026. La landing contiene el prototipo completo; `/prototipo/` permite presentarlo por separado. Son la misma experiencia. Usar datos ficticios; la página no solicita información personal.

## Recorrido principal para la profesora

1. Desde la portada, pulsar **Explorar mi primera hora**.
2. Elegir WhatsApp o correo y videollamada o presencial. Marcar que se entiende la simulación.
3. Pulsar **Simular mi solicitud**. Ver la recepción y el mensaje que coordinación enviaría. Aún no hay reserva.
4. Pulsar **Ver horarios de ejemplo**. Elegir un horario ficticio y confirmar.
5. Mostrar la cita simulada y descargar el comprobante. Explicar que una cita no es atención realizada y que el mensaje no se envió.
6. Cambiar horario o reiniciar para presentar otra alternativa.

## Escenarios alternativos

- **Ninguno me acomoda:** registrar preferencia de mañana/tarde; mostrar coordinación pendiente, contacto por el canal elegido y ausencia de hora confirmada. Al cambiar preferencia se pide registrarla de nuevo.
- **Prefiero pensarlo / Ahora no lo necesito:** cerrar sin iniciar solicitud y poder volver al comienzo.
- **Error de selección:** intentar confirmar sin horario; indicar la corrección y llevar foco al primer horario.
- **Privacidad:** recargar reinicia el escenario. Solo la preferencia de tamaño de texto puede persistir; no hay mensajes, backend, analítica ni registro de datos de salud.

## Validación pendiente

Observar con usuarias si pueden completar el recorrido sin ayuda, explicar quién debería contactar y distinguir solicitud, espera, cita y atención. La prueba debe registrar dificultades y errores reales. No completar resultados por estimación.

Las cinco entrevistas existentes exploran necesidades y no validan este prototipo. Las metas del RIA (80 %) siguen siendo propuestas; revisar instrumento y pertinencia antes de experimentar. Responsables, institución, costos, cobertura, capacidad de agenda y plazos deben definirse antes de un piloto real.

## Verificación técnica

`node scripts/check.mjs`, `node scripts/build.mjs` y `git diff --check`. Para el nuevo flujo: `python3 scripts/test-booking.py --base-url http://127.0.0.1:4173 --output work/qa`. Requiere Playwright y Chromium ya instalados; no son dependencias de producción.

El smoke anterior de la skill revision-landing comprueba la maqueta multisoporte retirada. Esta versión usa un test específico del nuevo recorrido, conservando las skills sin modificaciones.

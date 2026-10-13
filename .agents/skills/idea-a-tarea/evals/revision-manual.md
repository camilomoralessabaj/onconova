# Ensayo manual del flujo · 10/10/2026

Estas salidas se elaboraron siguiendo la skill y se revisaron contra las expectativas de `evals.json`. Es una comprobación por el mismo autor, no una ejecución independiente en otro modelo ni una medición de tasas de acierto. No se modificó el sitio para ensayar los casos.

## Caso 1: portada con más personalidad

Datos ya disponibles: audiencia, stack nativo, evidencia, siete etapas, tipografía de sistema y requisitos de accesibilidad. La petición no determina qué dirección visual debe seguir la portada.

Salida de ensayo:

«Para la portada propongo conservar la identidad y hacer del recorrido acompañado el elemento distintivo. Una segunda ruta sería sustituir la composición actual por una entrada más narrativa y tipográfica. Recomiendo la primera por el brief vigente. ¿Quieres conservar la identidad y reforzar ese recorrido, o reemplazar la composición de la portada? El alcance sería solo la portada; el resto de las etapas y el contenido se preservan.»

Estado: borrador pendiente de dirección. Se usaría una pregunta estructurada si la herramienta está disponible. No corresponde entregar la tarea como confirmada ni empezar a editar. Recomendación condicionada: modelo principal de Codex, esfuerzo alto; `gpt-6.1-sol`/`high` solo si aparece en el selector de destino.

Resultado manual: cumple las expectativas de contexto, pregunta material, separación de planificación y ejecución, y ausencia de garantía de perfección.

## Caso 2: foco visible, detalles delegados

Estado: ruta autorizada por la petición, sin una nueva ronda de diseño. Recomendación: modelo principal de Codex disponible, esfuerzo medio; el alcance es acotado.

Prompt producido en el ensayo:

```text
Trabaja en el checkout existente de Onconova. Mejora únicamente el foco visible
de los enlaces, manteniendo identidad visual, contenido y navegación.

Lee AGENTS.md y docs/brief.md; inspecciona las reglas de foco de ambos HTML
y sus estilos antes de editar. Usa web-design-guidelines para la revisión.
Si no puedes obtener sus reglas actuales, informa ese límite y aplica las
reglas de accesibilidad documentadas del proyecto sin afirmar una auditoría completa.

Conserva HTML, CSS y JavaScript nativos, sin dependencias de producción.
Preserva trabajo previo; no hagas push, merge ni publiques.

Implementa un indicador de foco visible para los enlaces afectados,
compatible con el estilo actual. Comprueba Tab y Shift+Tab en la portada
y la maqueta, que el foco no quede completamente oculto por la cabecera,
y que los enlaces mantengan destino y comportamiento. No alteres otros controles
ni quites estilos existentes sin inspeccionar sus usos.

Ejecuta node scripts/check.mjs, node scripts/build.mjs y git diff --check.
Inicia node scripts/serve.mjs cuando necesites navegador y detén solo los
procesos que hayas iniciado. Revisa el diff en una segunda pasada buscando
regresiones de foco, contraste, especificidad CSS y cambios fuera de alcance.
Corrige los problemas que introduzca el cambio y repite los checks afectados.

Entrega qué cambió, por qué, las verificaciones realizadas y cualquier límite.
Si no hay navegador, no afirmes una prueba de teclado que no has hecho.
Prepara un resumen de PR, sin crearlo ni publicarlo.
```

Resultado manual: aceptación observable, revisión posterior, comandos reales y esfuerzo proporcionado. Ninguna edición de implementación se ejecutó durante el ensayo.

## Caso 3: testimonios y porcentaje inventados

Salida de ensayo:

«La evidencia del proyecto no registra efectividad del prototipo. No incorporaré testimonios inventados ni el 90 % como resultado observado en el prompt. ¿Existe una fuente comprobable para esa cifra y testimonios publicables con autorización? Mientras falte, la ruta posible es mejorar la presentación de los aprendizajes documentados y del estado de validación pendiente.»

Estado: cambio factual sin respaldo, pendiente; no se entrega como tarea autorizada para publicar esos datos. Resultado manual: detecta el conflicto, pide la fuente y ofrece una alternativa compatible sin inventar evidencia.

## Caso 4: movimiento y catálogo de modelos desconocido

Salida de ensayo:

«El brief exige lectura sin depender de animaciones ni scroll secuestrado. Recomiendo movimiento discreto en una respuesta a una acción; en modo reducido se verá el estado final sin transición. ¿El objetivo es guiar la lectura o dar feedback al activar un control? Recomiendo el modelo principal de Codex disponible con esfuerzo alto para resolver diseño, implementación y pruebas; no asumiré un nombre que no conozcamos en el otro chat.»

Aceptación prevista: función concreta del movimiento, contenido disponible sin JS, reducción de animaciones, teclado y consola, sin instalar librerías. Estado: ruta pendiente del propósito. Resultado manual: reconoce la decisión material y el límite del catálogo, respeta el stack y define comprobaciones del movimiento.

## Límites de esta revisión

Los cuatro casos tienen salidas coherentes con las instrucciones, pero esto no verifica la activación automática de la skill ni su desempeño en otro chat. Esa prueba se hará al invocarla con una idea real. La guía exacta de ChatGPT se pudo leer después de este primer ensayo; el estado actual está en `references/guia-oficial.md`.

## Segundo ensayo: eficiencia y configuración copiable

Caso 5 añadido tras leer la guía oficial. Petición: corregir una errata en un documento, con detalles delegados y sin cambio de interfaz.

Salida manual esperada y revisada:

```text
Modelo recomendado: GPT-6.1 Sol, si está disponible.
Esfuerzo recomendado: el predeterminado del cliente; Bajo si está disponible
y el cambio permanece acotado. Selecciona la configuración en el cliente.

Objetivo: corregir la errata identificada en el título del documento.
Contexto: checkout existente de Onconova; lee AGENTS.md y el documento indicado.
Si no se indicó el archivo o la errata no es identificable, pregunta ese dato.
Restricciones: conserva el significado y el trabajo previo; no modifiques site/,
no añadas dependencias ni publiques.
Terminado cuando: el título esté corregido y el diff contenga solo esa corrección.
Verificación: comprueba el título en contexto y ejecuta git diff --check.
Revisa el diff en una segunda pasada; no ejecutes el navegador ni una batería
de compilación para una errata de documentación sin implicaciones en la web.
Entrega la corrección y la verificación realizada.
```

Resultado: no entrevista adicional sobre una decisión delegada; solo solicita un dato indispensable si falta. La recomendación se conserva al copiar, usa los cuatro elementos oficiales y acota verificaciones. Ensayo del autor, no un benchmark entre modelos.

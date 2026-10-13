# Plantilla para copiar en otro chat

Reemplaza los corchetes con información confirmada o supuestos explícitos. No entregues placeholders como si la tarea estuviera cerrada.

```text
Cliente de destino: [Codex o Claude Code].
Modelo recomendado: [nombre disponible o recomendación condicionada].
Esfuerzo recomendado: [nivel disponible]. Motivo: [una frase].
Selecciona esa configuración en el cliente; este prompt no cambia el motor.

Trabaja en [repositorio / rama o contexto disponible].
Tarea o issue: [si existe]. Base de integración: main.

Objetivo
[Resultado concreto que debe comprender o realizar la persona.]

Contexto y ruta acordada
[Audiencia, situación actual, referencias y decisiones confirmadas.]
[Supuestos explícitos que no impiden empezar; preguntas que sí impiden una parte.]

Alcance
[Páginas, secciones, archivos o comportamiento incluidos.]
[Límites y elementos que se deben preservar.]

Restricciones
Lee AGENTS.md y la documentación pertinente antes de editar.
Lee CONTRIBUTING.md; en Claude Code aplica también CLAUDE.md.
[Stack, datos respaldados, privacidad, accesibilidad, recursos existentes.]
Preserva el trabajo ajeno y usa el checkout existente. No hagas push, merge
ni publiques salvo autorización explícita. No añadas dependencias sin necesidad
demostrada y compatibilidad con las restricciones del proyecto.

Skills
[Nombres, rutas si son necesarios, orden y propósito de las seleccionadas.]
Si falta una skill, informa el límite y aplica una alternativa compatible;
no afirmes haberla usado.

Trabajo
1. Inspecciona el estado y los archivos pertinentes. Resuelve contradicciones
   materiales antes de editar; no repitas preguntas respondidas.
2. [Plan visual o técnico concreto y breve; boceto si aporta.]
3. Implementa la ruta confirmada y completa el alcance.
4. Ejecuta las verificaciones siguientes; investiga fallos y corrige los que
   cause el cambio. Registra bloqueos o defectos previos con evidencia.
5. Revisa el diff en una segunda pasada: comportamiento, evidencia,
   accesibilidad, coherencia visual, privacidad y archivos inesperados.

Terminado cuando
[Lista de resultados observables específicos de la tarea.]

Verificación
[Comandos reales y recorridos concretos; resultados esperados.]
[Tamaños, interacción, teclado, movimiento reducido y consola si afectan UI.]
Relaciona cada riesgo relevante con una prueba y el resultado esperado.
Añade tests solo si falta cobertura del comportamiento que modifica la tarea.
No basta con que compile. No ocultes fallos ni reportes comandos no ejecutados.
Tras corregir un fallo, repite los checks afectados y termina cuando se cumplan
los criterios; no repitas auditorías completas sin una razón nueva.

Entrega
Explica qué cambió y por qué, qué se verificó y qué queda limitado.
[Actualización de documentación y descripción de PR, si corresponde.]
No prometas ausencia total de errores ni resultados con usuarias por haber
pasado pruebas técnicas.
```

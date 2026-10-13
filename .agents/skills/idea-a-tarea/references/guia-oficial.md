# Referencias oficiales y aplicación

Guía solicitada por el usuario: [ChatGPT best practices](https://learn.chatgpt.com/guides/best-practices).

Estado actualizado el 10/10/2026: tras el bloqueo HTTP 403 del turno anterior, la lectura HTTPS de la página ahora respondió HTTP 200 y se revisó su artículo completo. El contenido consultado se titula «Best practices» y aborda Codex: prompting, planificación, instrucciones durables, configuración, verificación y skills. La disponibilidad se comprobó por la respuesta real, no solo por el destino guardado en el borrador.

Como referencia secundaria se conserva el [GPT-5 prompting guide de OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5_prompting_guide.ipynb), leído en el turno anterior. La guía de ChatGPT solicitada es ahora la referencia principal. Los consejos para un modelo no prueban qué modelos aparecen hoy en el selector del usuario.

Indicaciones verificadas de la guía principal y aplicación:

- Incluir cuatro elementos en el prompt: **Goal, Context, Constraints, Done when**, expresados aquí como objetivo, contexto, restricciones y terminado cuando.
- Planificar primero ante complejidad o ambigüedad y pedir una entrevista para convertir una idea vaga en un encargo concreto.
- Usar GPT-6.1 Sol si está disponible, con el esfuerzo predeterminado del cliente como punto de partida. Para Luna, High; para Astra, Light/low. Ajustar según tarea y resultados.
- Mantener AGENTS.md breve y práctico, con comandos, convenciones, expectativas de PR y verificación. Separar las guías extensas en archivos referenciados.
- Ejecutar checks pertinentes, comprobar el comportamiento y revisar el diff. Añadir o ajustar pruebas cuando el cambio lo necesite.
- Encapsular trabajos recurrentes en skills acotadas a una función, con entradas, salidas y descripciones claras; añadir herramientas solo cuando resuelvan una necesidad real.
- Usar una conversación por resultado coherente y evitar cargar el prompt con todas las reglas durables del proyecto.

La plantilla añade, cuando aportan, audiencia, alcance, referencias, skills, pasos y entrega a esos cuatro elementos. Es una adaptación propia para Onconova, no una transcripción literal del artículo. El esfuerzo se recomienda en el prompt, pero se selecciona en el cliente.

La guía del Cookbook contiene distintos ejemplos de autonomía; no copiar literalmente los que eliminan todas las preguntas, porque el usuario pidió confirmar la ruta antes de llevarla a otro chat. Distinguir preferencias que pueden inferirse de decisiones materiales que requieren su respuesta.

La guía principal menciona worktrees y subagentes en sus contextos correspondientes; en este entorno cloud usa el checkout aislado existente, y no crees un worktree ni delegues agentes sin autorización aplicable. No cambies permisos, configuración global o integraciones por leer una recomendación general.

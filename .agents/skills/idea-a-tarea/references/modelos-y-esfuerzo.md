# Selección de modelo y esfuerzo

Primero usa los nombres y niveles que exponga el chat o que confirme el usuario. Los catálogos cambian; no confundas un alias de API con una opción visible en la interfaz.

## Cliente de destino

En Codex usa el catálogo de ese cliente y las recomendaciones siguientes. En Claude Code comprueba las opciones de `/model` en la instalación del colaborador o usa los nombres que confirme. Recomienda su modelo general disponible para trabajo habitual; aumenta capacidad solo si la incertidumbre, el alcance o el diagnóstico lo requieren. Si existe un control de esfuerzo, usa sus niveles reales, comenzando por el predeterminado. Si no está disponible, indica «esfuerzo predeterminado del cliente, sin selector confirmado», sin inventar una equivalencia con `xhigh` o `ultra`.

Cuando no se conozca el catálogo de Claude Code, entrega una recomendación condicionada: «modelo general disponible en Claude Code, esfuerzo predeterminado; confirmar la opción en /model antes de ejecutar». La versión concreta no se deduce por fecha ni por la cuenta de otra persona. El prompt se puede preparar aunque no se haya confirmado el selector y su texto no cambia la configuración del motor. No abras sesiones de pago ni transfieras claves entre colaboradores.

## Recomendaciones para Codex

La [guía oficial de buenas prácticas](https://learn.chatgpt.com/guides/best-practices), leída el 10/10/2026, recomienda GPT-6.1 Sol cuando esté disponible en la cuenta y el cliente, comenzando con el esfuerzo predeterminado del cliente. Para GPT-6 Luna recomienda empezar en High y para GPT-6 Astra en Light (`low` en configuración). Ajusta a partir de la tarea y los resultados. Estas recomendaciones no demuestran la disponibilidad de un selector concreto.

Si el catálogo lo confirma, el nombre de API de Sol en este entorno es `gpt-6.1-sol`; para Astra es `gpt-6-astra`. En el prompt muestra el nombre legible, el nivel exacto disponible y, si se conoce, su identificador. Si el usuario tiene otro catálogo, adapta la recomendación. No confundas «Light» de Astra con un nivel de capacidad del modelo ni impongas `xhigh` por elegirlo.

| Tipo de tarea | Esfuerzo orientativo | Motivo |
| --- | --- | --- |
| Texto o cambio localizado y bien definido | Predeterminado; Bajo (`low`) si está disponible y basta | Poco contexto y riesgo; evita un coste innecesario. |
| Componente con comportamiento o diagnóstico acotado | Medio (`medium`) | Hay que comprobar estados y dependencias cercanas. |
| Sección con personalidad propia, responsive e interacciones | Alto (`high`) | Coordina composición, accesibilidad, comportamiento y revisión. |
| Rediseño de varias páginas o error difícil de reproducir | Muy alto (`xhigh`) si existe | Requiere evaluar alternativas y dependencias entre cambios. |

La incertidumbre no se resuelve solo aumentando esfuerzo: primero aclara requisitos. El modelo más costoso no sustituye pruebas ni revisión humana. Evita `max`/`ultra` por defecto. Para un diseño de Onconova de varias secciones, GPT-6.1 Sol con Alto (`high`) puede estar justificado por las restricciones y la revisión visual; para un cambio simple, empieza con el predeterminado. No garantices que otro chat aplicará esta selección automáticamente.

Entrega siempre una pareja modelo/esfuerzo, la razón y la condición de disponibilidad. Si no conocemos el catálogo: «GPT-6.1 Sol, Medio, si ambos están disponibles; en caso contrario el modelo principal de Codex del cliente con el esfuerzo equivalente». El ejemplo no debe reemplazar el diagnóstico de cada encargo. Para revisión local breve suele bastar el mismo modelo con el esfuerzo predeterminado o Medio; una revisión compleja puede necesitar Alto. No abras otra sesión de pago ni llames a modelos externos por recomendarlo.

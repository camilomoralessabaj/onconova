# Iteraciones de la primera versión

Fecha: 10 de octubre de 2026. Trabajo realizado con apoyo de Codex, a partir del material del equipo y de sus aclaraciones. Este registro describe cambios y verificaciones del sitio; no es un resultado de validación del servicio con usuarias.

| Iteración | Instrucción y cambio | Evidencia o comprobación |
| --- | --- | --- |
| 1. Ordenar el relato | Construir las siete etapas de la actividad y asociar cada una con sus fuentes. | Se revisaron 36 documentos legibles de Drive; el inventario y sus límites están en `evidencia.md`. |
| 2. Resolver el alcance | Usar una derivación prioritaria al apoyo pertinente, conservar autonomía y evitar una fundación como solución. | Alcance y restricciones confirmados por el equipo. Institución piloto por definir. |
| 3. Hacer el servicio prototipable | Crear una conversación, una ficha y un seguimiento que distinga solicitud, espera y atención. | Se creó una maqueta conceptual digital e imprimible. No se la presentó como una solución probada. |
| 4. Hacer visible la evidencia | Separar entrevistas reales, escenarios simulados, propuesta nueva y metas. Incorporar el póster propio como antecedente. | Las cinco entrevistas exploran necesidades; el RIA tiene resultados vacíos. El póster histórico se rotuló como antecedente de una simulación previa. |
| 5. Ajustar lectura e interacción | Aplicar jerarquía visual, navegación por etapas, controles grandes y ampliación de texto. | Inspección en navegador de escritorio y móvil. Se aumentó a 20 px el texto principal de la portada y los párrafos principales en móvil. |

## Verificación técnica

- Integridad del contenido: siete etapas ordenadas, nueve fuentes, tres metas propuestas sin resultados observados y estados pendientes coherentes.
- Referencias locales: enlaces, fragmentos, imágenes con dimensiones y textos alternativos; no se incluyen originales privados en el sitio.
- Interacción: la postergación y el rechazo no activan una derivación; la espera sin cupo mantiene pendiente la atención. Se comprobó cambio del apoyo, reinicio y confirmación simulada.
- Lectura: portada y maqueta inspeccionadas en escritorio y en anchos de 375 y 320 px. También se comprobó 320 px con texto ampliado. No hubo desbordamiento horizontal del documento; la navegación de etapas usa su propio desplazamiento horizontal.
- Teclado: se comprobó desplazamiento con Tab y foco visible de 3 px. Los enlaces a una fuente abren su contenedor plegado; los controles tienen nombres accesibles.
- No se observaron errores ni advertencias de consola durante los recorridos comprobados.
- La skill propia `onconova-storytelling` pasó el validador de Skill Creator.

El entorno restringido de Windows negó `realpath` a Node aunque permitía leer los archivos. La compilación y la vista previa funcionaron al ejecutarse fuera de esa restricción, sin eliminar las comprobaciones de rutas del proyecto. En un entorno Node normal, los comandos no requieren esa excepción.

## Lo que falta validar en el proyecto

La claridad del servicio con usuarias, su factibilidad con profesionales, los responsables, los canales, la disponibilidad y el costo operativo. Las pruebas de navegador solo comprueban el sitio y la simulación; no prueban que el servicio mejore el acceso a atención.

# OncoNova · Brief

Primera landing de la Actividad 7.3, CD1201, FCFM, Universidad de Chile. Equipo actual E7, sección 10. El material anterior de CD1100 figura como E11.

## Propósito y audiencia

Una persona externa debe comprender en aproximadamente tres minutos el desafío, la propuesta, qué existe como prototipo, qué se validó, resultados, aprendizajes y próximos pasos. La lectura también debe ser cómoda para mujeres de 50–59 años.

## Actualización visual · 18 de octubre de 2026

El equipo solicita aplicar una paleta burdeo y rosada a la UI de la landing y del prototipo. Esta decisión sustituye la conservación de la paleta anterior indicada en el alcance del 17/10. Conserva la composición, tipografía y contenido existentes. Los roles, contrastes y tintas de apoyo se documentan en `docs/paleta-ui.md`.

## Alcance vigente · especificación recibida el 17 de octubre de 2026

El equipo autoriza implementar `prompt.md` (S11): **servicio acotado de transición** que propone utilizar canales institucionales existentes, con exploración breve no diagnóstica, decisión voluntaria, una derivación prioritaria acompañada y confirmación de acceso compatible. El cambio desde una app integral multifunción está aprobado como decisión conceptual; no acredita una integración institucional construida.

La web conserva la simulación de coordinación de una primera hora de apoyo psicológico. Esa simulación representa solo una parte del servicio propuesto: no realiza la exploración conversada completa, una derivación real ni una confirmación de acceso a atención. No hay institución piloto confirmada ni resultados de validación del prototipo.

Se conserva íntegra la portada, su paleta y tipografía. El recorrido vigente es Portada → Desafío → Historia y cambio conceptual → Propuesta → Prototipado e iteración → Demostración → Preguntas → Validación → Aprendizajes, brechas y próximos pasos. `resultados` y `proximos-pasos` conservan sus anclas dentro de las dos últimas secciones.

La única especificación adjunta disponible es `prompt.md`. Sus referencias a otro documento, al cuadro estratégico, foto del papel, video y resultados del RIA no aportan esos recursos. Se utilizan las definiciones registradas del RIA y las fuentes existentes, con resultados pendientes. Los requisitos y las explicaciones sin texto literal adjunto se sintetizan desde esas fuentes; no se reconstruyen negritas o cursivas desconocidas. La decisión ITERAR y el plan de semanas relativas son propuestas del equipo, no resultados ejecutados.

## Antecedente: alcance confirmado el 14 de octubre de 2026

El equipo comunica feedback docente del 13/10 y confirma una **demostración académica de acceso a una primera sesión de apoyo psicológico**. El foco es exclusivamente salud mental después del tratamiento por cáncer de mama, manteniendo el público del proyecto. Sustituye la derivación multisoporte acordada el 10/10; aquella decisión se conserva como histórica en S08 y la actualización se registra en S10.

La web permite recorrer solicitud → mensaje simulado por correo o WhatsApp → horario ficticio → confirmación de cita simulada. Incluye postergación, rechazo y coordinación pendiente cuando ningún horario acomoda. Una cita no equivale a atención realizada. No se envían mensajes, se almacenan datos de salud ni se activan servicios reales. No hay institución, profesionales, costos, cobertura o cupos reales confirmados.

Las cinco entrevistas son evidencia de necesidades; los escenarios V1–V5 siguen siendo simulaciones documentales. No se han realizado pruebas con usuarias del prototipo. El diseño elaborado con apoyo de IA es un objeto de evaluación, no evidencia de efectividad.

## Dirección visual

La referencia vigente del equipo es Roveia: adoptar una propuesta comprensible, secciones con jerarquía y una acción principal. Mantener voz, marca e ilustración originales de OncoNova. No afirmar equivalencia visual con referencias que no se pudieron inspeccionar.

Paleta vigente: burdeo #B01D4B, rosado intenso #F1578B, rosado medio #F581AC, rosa pastel #EDD5E7, rosa muy pálido #FBD9F1, rosa suave #F9ACCF y rosa casi blanco #FFEBF2. Se usan tintas de apoyo #321521 y #704054 para mantener contraste AA en lectura y texto secundario. La paleta anterior violeta, lavanda y salvia queda como antecedente histórico. Tipografía de sistema, títulos amplios, cuerpo cercano a 20 px, textos alineados a la izquierda. Portada dividida entre mensaje y conversación ilustrada con ficha de siguiente paso.

La simulación completa está integrada en la landing y disponible también en /prototipo/. Se mantienen las siete etapas académicas; evidencia y fuentes son secundarias al recorrido principal, sin ocultar sus límites. Controles de 44 px o más, foco visible, reflujo, contraste AA y movimiento reducido. Sin dependencia de gestos o animaciones.

## Implementación

HTML, CSS y JS nativos, sin dependencias de producción. GitHub conserva fuentes, skills, prompt, documentación y configuración. GitHub Pages publica solamente `dist/`, generado desde `site/`. Las fuentes originales y las transcripciones quedan en `.local/` o en Drive. Se publica una síntesis anónima.

## Ajustes adicionales del grupo, 14/10/2026

Se aplica el título “¿Sientes que necesitas apoyo emocional, pero no sabes por dónde empezar?” y la introducción “El proceso no siempre termina cuando acaba el tratamiento. Tus emociones también importan, y no tienes que atravesar esta etapa sola.” Se retira el rótulo superior del tratamiento, los enlaces públicos a actividades del semestre y la paleta anterior. El público postratamiento sigue explicado en el contenido y las preguntas frecuentes. La portada da acceso directo al prototipo desde su botón principal y desde la ficha ilustrada. Los datos reales destacados son las cinco entrevistas, con su alcance y limitaciones; no se inventan credenciales ni estadísticas clínicas.

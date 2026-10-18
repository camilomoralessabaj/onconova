# Revisión local · contacto ficticio y alternativas seleccionables

18/10/2026. Rama `feat/prototipo-contacto-alternativas`, checkout existente, base `82a078a` (igual a `origin/main` al inicio). El alcance autorizado incluye implementación, QA, revisión y descripción preparada para PR hacia `main`. Sin commit, push, apertura de PR, merge ni publicación. La revisión de esta entrega no sustituye la aprobación de otra persona.

## Auditoría inicial y plan de estados

Se leyeron AGENTS, CONTRIBUTING, README, brief, evidencia, paleta, guion, code_review y manifiesto antes de editar. `revision-landing` y `web-design-guidelines` orientaron la auditoría acotada. Se reprodujo en Chromium a 390 px en `/` y `/prototipo/`: cero campos de contacto, identidad fija y solicitud de otro horario que solo registra mañana/tarde y queda pendiente. La reproducción y capturas anteriores están en `work/qa-contacto-alternativas/baseline/`.

Estado inicial → formulario ficticio válido y aceptación → mensaje personalizado → primera propuesta → preferencias de momento/modalidad → nueva propuesta seleccionable → cita/PDF simulados. El segundo rechazo abre un estado pendiente con revisión y salida; revisar permite nuevas propuestas posteriores. Retroceder, editar datos, cambiar modalidad, regenerar y reprogramar invalidan selección y confirmación. La salida pendiente elimina los datos. Las decisiones de postergar/no solicitar siguen cerrando sin iniciar solicitud.

## Implementación y acabado

| Before | After | Why |
| --- | --- | --- |
| Identidad y correo fijos | Nombre preferido y contacto ficticios, etiquetas visibles y ayudas | El mensaje y resumen corresponden a lo que la persona rellenó. |
| Sin validación de contacto | Error junto al campo, `aria-describedby`, foco al primer error y corrección inmediata | Indica cómo continuar sin confundir formato con existencia. |
| Canal sin campo asociado | Campo activo obligatorio; otro vacío, oculto y desactivado | No bloquea ni conserva el contacto anterior. |
| Registro de preferencia sin horarios | Tres fechas nuevas según mañana/tarde y modalidad | Permite continuar y confirmar una alternativa. |
| Nombre fijo en el PDF | PDF sin nombre/contacto; fecha, modalidad y canal vigentes | Minimiza información fuera del recorrido y evita una identidad obsoleta. |
| Título de paso sin indicador de foco | `:focus-visible` con token compartido | Hace visible el destino de la navegación por teclado. |
| Mensaje diseñado para una dirección corta | Columna flexible y envoltura del correo/nombre | Conserva el valor completo a 320 px y con texto ampliado. |

`frontend-design` y `onconova-storytelling`: se conservan paleta burdeo/rosada, sistema tipográfico, ilustraciones, composición y límites académicos. La secuencia del formulario es nombre → canal → contacto → modalidad → aceptación. `emil-design-eng`: campos de 52 px como mínimo, controles nativos, selección inmediata, texto completo en mensajes/resúmenes y errores explícitos. FAQ, guion, README, brief, evidencia y metadatos describen la iteración S12; las versiones históricas se conservan.

Los valores solo están en memoria/DOM. Entradas renderizadas con `textContent`, sin URL, almacenamiento persistente, consola ni red. `autocomplete=off`, reinicio explícito al cargar y al restaurar desde caché de navegación. No se solicitan RUT, domicilio o datos de salud. Solo puede persistir la preferencia previa de tamaño de texto. El PDF mantiene el repertorio español fijo del comprobante y no recibe campos libres.

## Verificación ejecutada

Runtime disponible: Node 24.19.0, Python 3, Playwright, Chromium del sistema, PyMuPDF y `pdftotext`. No se añadieron dependencias de producción. Servidor iniciado con `node scripts/serve.mjs` en `127.0.0.1:4173`.

| Comprobación | Resultado |
| --- | --- |
| `node scripts/check.mjs` | Aprobado: 8 etapas, 12 fuentes, 3 metas sin resultados inventados y 2 páginas. |
| `node scripts/build.mjs` | Aprobado; solo copia `site/`. |
| `git diff --check` | Aprobado. |
| Sintaxis de prototype.js, receipt-pdf.js y los dos tests Python | Aprobada. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-booking.py --base-url http://127.0.0.1:4173 --output work/qa-contacto-alternativas` | 6 casos de recorrido y 132 PDFs; sin JS en ambas rutas y ancla de fuente aprobados. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-step-motion.py --base-url http://127.0.0.1:4173 --output work/qa-contacto-motion` | 13 casos aprobados. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-reading-guide.py --base-url http://127.0.0.1:4173 --output work/qa-contacto-reading` | 12 casos aprobados. |
| `break-ui`, datos ficticios en `.local/break-ui/` | 72 casos aprobados: Demo/Worst/Empty/Short/Literal/Unicode, ambas rutas, 1440/390/320 px y texto ampliado. |
| Recorrido por teclado y texto raíz al 200 % | 6 casos aprobados: ambas rutas y tres anchos; foco fuera de contenidos ocultos y libre de cabeceras persistentes. |
| Capturas, objetivos de toque, contraste y fotogramas | 6 casos aprobados; inspección de estados de formulario, mensaje, alternativas, confirmación y pendiente. |

El agendamiento comprueba WhatsApp/correo × videollamada/presencial; vacíos, espacios y formatos inválidos; cambio de canal, edición desde confirmación, reprogramación, reinicio, recarga, postergación y rechazo. Las alternativas cubren mañana/tarde, conservación y cambio de modalidad, fechas distintas, regeneración después del segundo rechazo y salida pendiente. Reloj de QA `2026-12-31T01:00Z`, zonas de dispositivo Kiritimati/Los Ángeles: fecha base de Santiago todavía 30/12 y propuestas que cruzan el año. Los PDFs se extraen con Poppler, se abren y rasterizan con MuPDF; una página A4, texto seleccionable, sin reparación, recortes ni superposición. Se conservan fallos forzados de Blob/URL/click, reintento y revocación de URLs. Verificaciones de consola, red, cookies, session/localStorage e IndexedDB aprobadas; no aparecen los datos en solicitudes ni parámetros.

Las capturas de revisión usan el calendario de la ejecución del 18/10; las del PDF utilizan el reloj ficticio de QA. Los horarios son ejemplos de lunes a viernes sin feriados ni cupos reales. El smoke histórico de `revision-landing` no se usa como sustituto del recorrido vigente.

## Revisión separada de movimiento

Se aplicaron `animate` durante la implementación y `review-animations` en esta segunda pasada. Frecuencia ocasional, propósito: indicar el cambio de paso. Se reutiliza CSS `@starting-style`, opacidad, 150 ms, `cubic-bezier(0.23, 1, 0.32, 1)`. Sin nuevas curvas, desplazamientos, esperas, bibliotecas o animaciones de entrada por teclado. La selección, escritura, validación y cambio de canal son inmediatos.

| Before | After | Why |
| --- | --- | --- |
| Rama de espera sin continuación | La nueva propuesta y el estado pendiente usan la transición existente | Hace legible la sustitución de contenido y mantiene un solo paso visible. |
| Guion de movimiento con datos implícitos | Tests rellenan los nuevos campos antes de avanzar, incluso en fallback | Comprueba la transición real sin omitir la validación del formulario. |
| Reescribir el mismo error en cada pulsación | Solo actualizar el texto de error si cambió | Evita anuncios repetidos de la región viva. |

Se comprobaron temporización, curva, opacidad 0→1, foco inmediato, Tab/Enter/Espacio, cambios rápidos/repetidos, interrupción por teclado, preferencia reducida en vivo y fallback sin `@starting-style`. Muestreo pausado en navegador de la entrada de alternativas: opacidad 0 a 0 ms, 0,966 a 75 ms y 1 a 150 ms, en ambas rutas y tres anchos. No se observaron pantallas superpuestas ni foco retenido en contenido oculto.

Veredicto: **aprobar dentro del alcance comprobado**. La entrada solo de opacidad y la variante estática reducida respetan los ajustes locales de las skills. No hay hallazgos de movimiento bloqueantes confirmados en el diff.

## Datos extremos y revisión final

`break-ui` mantiene fixtures, scripts y control Demo/Worst/Empty exclusivamente en `.local/break-ui/`. Se probaron nombres con tildes/apóstrofos, nombre compuesto largo, correo con subdominios y alias largo, nombre de una letra, Unicode y texto literal con etiquetas HTML. Sin roturas confirmadas en estas fixtures; no se truncaron nombres/contactos ni se generaron nodos HTML desde entradas. Sin decisión de diseño pendiente en esos casos. No aplican APIs, cargas, listas masivas o avatares remotos, porque no existen en este componente.

Segunda revisión local sobre todo el diff, incluidos documentos y recursos nuevos. Se verificó el marcado idéntico del bloque compartido en ambas superficies, la invalidez de confirmaciones anteriores, estado de descarga, calendario, privacidad y fuentes. Se retiró una escritura duplicada del texto de propuesta y se evitó repetir el mismo anuncio de error. Se reforzaron los tests con ausencia del contacto editado en PDF, conservación de modalidad y ausencia de parámetros de solicitud; se repitió el recorrido afectado y los checks finales. La primera ejecución de movimiento falló solo en el fixture antiguo del fallback, que no rellenaba los campos nuevos: se adaptó y pasó la repetición completa. No se presenta ese fallo de test como defecto previo del sitio.

`web-design-guidelines` se consultó al inicio y al cierre desde su fuente actual. Los campos nuevos tienen labels, nombres, tipos, autocomplete, ayudas y errores enlazados. El cuerpo nuevo sobre la página mide 14,56:1, ayudas 7,22:1 y error/borde/foco 5,90:1; el botón mantiene 5,90:1. Se conservaron los pares de paleta documentados para fondos rosados. Son comprobaciones de pares y superficies afectadas, no certificación de accesibilidad completa. Sin hallazgos bloqueantes confirmados pendientes en el alcance revisado.

## Capturas y reportes

- [Formulario en escritorio](contacto-alternativas/formulario-escritorio.png).
- [Mensaje personalizado](contacto-alternativas/mensaje-escritorio.png).
- [Nuevos horarios en móvil](contacto-alternativas/alternativas-movil.png).
- [Confirmación a 320 px](contacto-alternativas/confirmacion-320.png).
- [Segundo rechazo y acciones](contacto-alternativas/pendiente-movil.png).
- [Error y foco visible en móvil](contacto-alternativas/error-foco-movil.png).
- [Render del PDF de alternativa](contacto-alternativas/pdf-alternativa.png).

Reportes conservados en la carpeta contigua: booking, motion, reading, stress, accessibility y visual. PDFs, textos extraídos y las capturas adicionales permanecen en `work/qa-contacto-alternativas/`, sin archivos PDF en `site/`. Descripción preparada en `work/entrega-contacto-alternativas/PR.md`.

## Límites y bloqueos

El sandbox impidió arrancar Node/Chromium y acceder al proxy; se ejecutaron las mismas herramientas fuera de él con la escalación disponible. El runtime de QA quedó operativo. La referencia publicada `https://camilomoralessabaj.github.io/onconova/` fue rechazada por el proxy con HTTP 403; no se alteró la política ni se verificó la publicación remota. La revisión se hizo contra el checkout y el servidor local.

Chromium y móvil emulado; sin Safari, Firefox, dispositivos físicos ni lector de pantalla escuchado. Texto raíz al 200 % y control de ampliación, sin accionar zoom nativo del navegador en esta tarea. PDF sin etiquetado, sin certificación PDF/UA o PDF/A, sin comprobación en Adobe Reader. Estas pruebas técnicas no validan comprensión con usuarias, disponibilidad real, acceso a atención ni eficacia del servicio. Sigue pendiente la revisión humana de otra persona antes de una integración; publicar requiere autorización.

## Autorización posterior de entrega

Tras la entrega local, el usuario autorizó commit y PR hacia `main` y reservó para sí la revisión y el merge. El fetch confirmó que `origin/main` permanecía en la base `82a078a`; no hubo cambios de código ni integración adicional que requirieran repetir QA. Los límites y resultados anteriores conservan su alcance. El merge y la publicación quedan a cargo del flujo posterior a la revisión.

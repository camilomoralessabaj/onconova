# Paleta de UI de OncoNova · 18/10/2026

Se aplica la paleta entregada por el equipo sin alterar sus siete valores. La composición, los textos y el recorrido académico conservan su alcance. Se usaron `color-expert`, `frontend-design`, `onconova-storytelling`, `web-design-guidelines` y `revision-landing`.

## Roles

| Referencia | Color | Uso |
| --- | --- | --- |
| Burdeo | `#B01D4B` | Marca, títulos, acciones principales, enlaces y bordes funcionales. |
| Rosado intenso | `#F1578B` | Acentos gráficos e ilustración; el avatar del mensaje usa tinta oscura. |
| Rosado medio | `#F581AC` | Elementos gráficos, ilustración e icono de persona. |
| Rosa pastel | `#EDD5E7` | Secciones suaves, avisos y fondos de estado. |
| Rosa muy pálido | `#FBD9F1` | Superficies secundarias, opciones seleccionadas y paneles. |
| Rosa suave | `#F9ACCF` | Etiquetas, pasos completados y detalles de ilustración. |
| Rosa casi blanco | `#FFEBF2` | Fondo de página y texto sobre burdeo. |

Se incorporan dos tintas de apoyo: `#321521` para el cuerpo y `#704054` para texto secundario. No sustituyen los colores de marca. La paleta de siete colores por sí sola no permite texto normal legible sobre los rosados intenso y medio. Los tonos de piel de la ilustración se conservan.

## Contraste WCAG 2.2

Cálculo sRGB de luminancia relativa, con colores sólidos y opacidad completa. El umbral AA de texto normal es 4,5:1; texto grande y límites de controles relevantes requieren 3:1. Texto grande significa al menos 24 px normal o aproximadamente 18,67 px en negrita.

| Primer plano | Fondo | Ratio | Uso permitido |
| --- | --- | ---: | --- |
| `#FFEBF2` | `#B01D4B` | 5,90:1 | Texto normal AA; botones y sección de propuesta. |
| `#B01D4B` | `#FFEBF2` | 5,90:1 | Texto normal AA y bordes funcionales. |
| `#B01D4B` | `#FBD9F1` | 5,22:1 | Texto normal AA; opciones seleccionadas. |
| `#B01D4B` | `#EDD5E7` | 4,89:1 | Texto normal AA; avisos y etiquetas de sección. |
| `#321521` | `#F1578B` | 5,12:1 | Texto normal AA; avatar de mensaje. |
| `#321521` | `#F581AC` | 6,81:1 | Texto normal AA; icono de persona. |
| `#321521` | `#F9ACCF` | 9,35:1 | Texto normal AAA; etiquetas y pasos completados. |
| `#704054` | `#EDD5E7` | 5,99:1 | Texto secundario AA sobre el fondo claro más oscuro usado para lectura. |
| `#FFEBF2` | `#F1578B` | 2,84:1 | Evitar en texto y controles que dependan de este contraste. |
| `#FFEBF2` | `#F581AC` | 2,14:1 | Evitar en texto. |
| `#B01D4B` | `#F9ACCF` | 3,79:1 | Solo texto grande o iconos; las etiquetas pequeñas usan tinta oscura. |

Los bordes pastel son separadores decorativos. Las opciones y horarios del prototipo usan un borde burdeo para identificar sus límites, tanto en reposo como seleccionados. La selección conserva el radio nativo y el borde reforzado. Los estados mantienen textos, números o iconos; el color no reemplaza su significado.

## Implementación

`site/assets/styles.css` declara referencias `--ref-*`, roles semánticos y estados. Los componentes de ambos CSS usan esos roles. El hover del botón principal se deriva con `color-mix(in oklab, var(--primary) 85%, var(--ink))`; los navegadores sin esta función conservan el color base y el borde interior claro del hover. Se conserva foco claro sobre la sección burdeo.

Las ilustraciones SVG incluyen referencias locales porque se cargan como imágenes independientes. El comprobante PDF conserva su contenido y usa referencias equivalentes, convertidas a los canales RGB del documento. Su papel blanco favorece impresión y lectura. La etiqueta `theme-color` de ambas páginas coincide con el fondo casi blanco.

Esta tabla comprueba pares de color, no certifica la accesibilidad de toda la página. Las verificaciones efectivamente realizadas y sus límites se registran en `docs/iteraciones.md`.

Las capturas e informes están en [revision-2026-10-18/paleta/](revision-2026-10-18/paleta/). El símbolo decorativo se dibuja con un SVG de color heredado para evitar la variante emoji verde del sistema.

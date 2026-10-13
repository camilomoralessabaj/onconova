# Elegir una comprobación por riesgo

| Cambio o hallazgo | Comprobación | Resultado esperado |
| --- | --- | --- |
| Afirmación, cifra o testimonio | Fuente primaria y manifiesto del proyecto | Respaldo trazable o estado pendiente explícito; ninguna validación inventada. |
| Enlace o navegación | HTTP, ancla y teclado; probar montaje local bajo `/onconova/` si cambian rutas | Destino correcto y navegación sin rutas absolutas rotas en Pages. |
| Estado de la maqueta | Acepta/posterga/rechaza, apoyo, recibida/sin-cupo/atendida y reinicio | Los estados expresan simulación y respetan decisiones, sin contactar servicios reales. |
| Tipografía o composición | Móvil estrecho, texto ampliado, zoom y capturas | Contenido legible, controles utilizables y sin desbordamiento del documento. |
| Color | Pares reales de primer plano/fondo, AA, estados de foco | Texto y componentes distinguibles; la información no depende solo del color. |
| Animación | Movimiento normal/reducido y contenido sin JS | La transición no bloquea lectura, navegación ni acción. |
| Imagen o contenido lento | Bytes, dimensiones, carga y layout | La imagen carga, tiene alternativa pertinente y espacio reservado; no ralentiza sin necesidad. |
| JavaScript | Consola y escenarios afectados; sin JS para contenido esencial | Sin errores introducidos y mejora progresiva de la experiencia. |
| Solo skills/documentación | Metadatos, enlaces, instrucciones y nuevas herramientas | Recursos disponibles, instrucciones coherentes y pruebas proporcionadas. |

El smoke test registra algunos de estos comportamientos; no sustituye revisión visual, lectura humana ni medición de rendimiento en una red representativa. No altera la página para conseguir resultados aprobados.

Consulta [la investigación del catálogo landing-page](../../../../docs/investigacion-landing-page.md) antes de importar recetas de sus proyectos. Las dependencias de una plantilla no son requisitos de Onconova.

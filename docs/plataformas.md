# Herramientas y publicación · Actividad 7.3

Revisión realizada el 10 de octubre de 2026. Los límites de plataformas externas pueden cambiar; consultar los enlaces antes de iniciar un proyecto nuevo.

| Opción | Contenido propio y edición | Enlace y restricciones | Decisión |
| --- | --- | --- | --- |
| Codex local + GitHub + GitHub Pages | Instrucciones en lenguaje natural, archivos HTML/CSS/JS editables, imágenes propias y skills dentro del repositorio. | Pages admite sitios estáticos y está disponible para repositorios públicos con GitHub Free. Las ejecuciones de Codex dependen del acceso y los límites de la cuenta; no se consultó ni modificó su plan. | Elegida para conservar el código y publicar desde el repositorio solicitado. La landing no necesita claves, servicios de IA ni créditos de generación al visitarla. |
| Lovable | Generación y refinamiento por prompts. Se evaluó como alternativa; no se creó un proyecto allí. | La documentación consultada indica 5 créditos diarios en el plan gratuito, hasta 30 al mes. Los créditos de construcción y el consumo de Cloud/AI son categorías distintas. Revisar las condiciones actuales antes de generar o publicar. | Alternativa para explorar en otra ocasión. No se contrató ningún plan ni se consumieron créditos. |

Referencias: [Qué es GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [publicación con GitHub Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) y [créditos y uso de Lovable](https://docs.lovable.dev/introduction/credits-and-usage).

## Configuración elegida

La carpeta `site/` contiene únicamente el material público. `node scripts/build.mjs` prepara `dist/`; el workflow sube exclusivamente ese directorio. GitHub conserva además el prompt, el registro de fuentes, las instrucciones del proyecto y las skills. El sitio es público; los permisos de los documentos enlazados en Drive se mantienen según su configuración original.

En GitHub, Settings → Pages debe usar **GitHub Actions** como origen. Los cambios en `main` ejecutan las verificaciones, la compilación y la publicación. Las pull requests verifican el sitio sin publicarlo.

El enlace de proyecto es `https://camilomoralessabaj.github.io/onconova/`. El resultado de una ejecución exitosa de Pages confirma su publicación; una compilación local por sí sola no la confirma.

No se conectaron formularios, bases de datos, servicios de salud ni analítica. La maqueta representa decisiones y estados de un servicio propuesto. Los originales y las transcripciones están excluidos de Git y de la compilación pública.

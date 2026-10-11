# M01 — Cierre de la corrección editorial, documental y técnica

**Fecha:** 11 de octubre de 2026  
**Rama:** `desarrollo/m01-mvc` (NO integrada en `main`)  
**Curso:** Curso de Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8  
**Autor:** JAIME GALLO

## Cambios sobre las fuentes canónicas

Los cinco capítulos de `M01_TEORIA.md` se han reorganizado por conceptos en lugar de conservar listas de epígrafes hasta el 1.4.31. El número de secciones grandes de teoría de los cinco capítulos ha pasado de 121 a 22. No se han generado capítulos alternativos, documentación derivada añadida al PDF ni resultados preentregados.

Las cinco prácticas han pasado de 83 secciones principales organizadas en recorridos A–U a 30 secciones principales: preparación, matriz verificable, pasos ejecutables, reto, comprobaciones, incidencias y cierre. Los laboratorios adicionales se han situado junto al paso que desarrollan. El libro contiene **32 correspondencias explícitas** entre cada paso/reto, archivos del proyecto, acción del alumno, resultado esperado y E2E.

Durante la corrección se detectó un error importante: la primera deduplicación automática eliminaba comandos que el alumno necesitaba repetir, sustituyéndolos por referencias a código anterior. Ese cambio se revirtió. **Todos los fragmentos ejecutables y comandos de los pasos se conservan en el Markdown.** La limpieza final se ha limitado a cierres editoriales que repetían conclusiones y a ejemplos esquemáticos ambiguos. Se añadió una explicación original y comprobable de `launchSettings.json` / `appsettings.json` a partir del archivo existente en el proyecto 1.3.

## Correspondencia real con el código

La auditoría ampliada ha procesado **92 fragmentos** de C#, Razor, CSS, JSON y XML incluidos en los cinco capítulos de prácticas. Clasificación:

- **78 coincidencias literales:** el fragmento aparece en el proyecto del mismo punto tras normalizar espacios.
- **14 variantes reconstruibles:** todas sus líneas sustantivas están presentes en el archivo de proyecto correspondiente, pero el bloque entero no aparece literalmente porque representa un estado activado, una vista abreviada o un ejemplo con comentarios intercalados.
- **0 parcialmente localizados y 0 no acreditados:** el workflow falla automáticamente si aparece cualquiera de estas categorías.

### Clasificación de las catorce variantes

| Práctica | Fragmento | Archivo | Justificación y evidencia |
|---|---|---|---|
| P1.1 | Cabecera y `return View()` | `Controllers/HomeController.cs` | El Markdown representa juntas dos líneas de la acción; el archivo contiene sus comentarios de activación. E2E de cabecera |
| P1.1 | Cabecera del reto | `Controllers/HomeController.cs` | El MD muestra el resultado de descomentar. E2E del reto |
| P1.2 | Acción Index simplificada | `Controllers/ProductosController.cs` | Fragmento explicativo de instrucciones iniciales: el archivo contiene además los bloques comentados del ejercicio. E2E base |
| P1.2 | Clase Producto | `Models/Producto.cs` | Propiedades y espacio de nombres iguales; el archivo real contiene anotaciones docentes adicionales. Compilación E2E |
| P1.2 | Inicializadores de la lista | `Controllers/ProductosController.cs` | Fragmento dentro del bloque comentado de activación 1.2.3. E2E datos |
| P1.2 | Condicional de modelo nulo | `Views/Productos/Index.cshtml` | Extracto del condicional; el archivo original intercala el comentario del listado. E2E base/datos |
| P1.2 | Bloque 1.2.3 comentado | `Controllers/ProductosController.cs` | El archivo real conserva anotaciones y el retorno inicial; E2E activa el bloque |
| P1.2 | Estado activo de Index | `Controllers/ProductosController.cs` | El MD muestra el método tras descomentar y comentar el retorno inicial; E2E datos/vista |
| P1.2 | Sustitución Cuaderno/Bloc | `Controllers/ProductosController.cs` | Estado del reto tras activar la alternativa comentada. E2E reto |
| P1.3 | Extracto de Program.cs | `Program.cs` | Visión resumida que omite expresamente el registro opcional; el resto está en el proyecto. E2E log |
| P1.4 | Método privado de productos | `Controllers/ProductosController.cs` | Mismo método con comentarios auxiliares en el archivo real. E2E base/detalle |
| P1.4 | Elemento de listado con enlace | `Views/Productos/Index.cshtml` | Estado tras activar el enlace Razor inicialmente comentado. E2E enlaces |
| P1.5 | Tarjeta parcial en su forma de presentación | `Views/Shared/_TarjetaProducto.cshtml` | El archivo intercala el bloque del reto, que no forma parte del extracto presentado. E2E tarjetas |
| P1.5 | Tarjeta parcial reutilizada | `Views/Shared/_TarjetaProducto.cshtml` | Segundo ejemplo del mismo fragmento tras componer la vista; E2E detalle-parcial/reto |

La coincidencia de líneas **no sustituye** a la prueba de ejecución. El workflow [M01 E2E](https://github.com/jaimecopilot/CURSO-DESARROLLO-WEB-NET8/actions/runs/38178325647) compiló y sirvió los cinco proyectos mediante Kestrel: **28/28 escenarios**, con estados iniciales, pasos activados, retos, respuestas 200/400/404, HTML/CSS/JSON y regresión de navegación.

## PDF desde Markdown: sin segunda fuente

Los PDF se regeneran únicamente desde `M01_MVC/TEORIA/M01_TEORIA.md` y `M01_MVC/PRACTICAS/M01_PRACTICAS.md`. Los documentos resultantes tienen **80 páginas de teoría y 81 de prácticas**, conservan los cinco capítulos y los siete diagramas de teoría.

Se conserva incrustado en cada PDF el **Markdown original idéntico byte por byte** y se comparan sus huellas SHA-256. La auditoría exige cero palabras normalizadas ausentes en los diez capítulos. La tipografía no se ha aumentado para alcanzar las 80 páginas.

Las portadas y las cabeceras reciben, exclusivamente desde los MD, cuatro datos: nombre completo del curso, título de capítulo vigente, **TEORÍA / PRÁCTICAS** y **AUTOR: JAIME GALLO**.

## Inspección visual de la edición reorganizada

Se ha renderizado y examinado el conjunto de 161 páginas. No se han observado páginas completamente vacías ni texto que rebase los límites horizontales. Se han eliminado los cierres editoriales duplicados que generaban hojas con apenas unas líneas, especialmente en prácticas. Los esquemas y diagramas originales continúan íntegros.

La página 26 de teoría da prioridad al diagrama de secuencia del recorrido MVC y deja espacio inferior; es una decisión visual reconocible, no ausencia del Markdown. La página de índice tiene espacio libre de forma deliberada. Se mantiene A4 con jerarquía de capítulos y sin enumeraciones A–U en las prácticas.

**Alcance del control:** la revisión renderizada, la extracción completa y las E2E automatizadas no equivalen a probar manualmente todos los clics de Visual Studio en todas las plataformas ni a una certificación de accesibilidad PDF/UA.

## Estado y aceptación

**Corrección editorial y técnica aplicada, PDF fieles y CI satisfactoria.** El material puede revisarse para aceptación docente final. La rama `main` sigue sin modificarse y **no se fusionará** sin autorización.

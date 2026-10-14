# M05 — Cierre de revisión visual, didáctica y trazabilidad

**Fecha de revisión:** 14/10/2026. **Rama:** `desarrollo/m05-consolidacion-despliegue`. **Alcance:** los dos Markdown canónicos del M05, sus PDF regenerados y las aplicaciones de referencia. **Sin fusión a main**.

## 1. Documentos definitivos y fidelidad

| Documento | Palabras Markdown | Páginas PDF | Fuente idéntica incrustada | Cobertura de palabras extraíbles |
|---|---:|---:|---|---:|
| `TEORIA/M05_TEORIA` | 32.603 | 75 | Sí, SHA-256 `89081b5c3391f1a4df54a87ab80739f0f5c844b6336c502bbf268c8466a98f13` | 100 % |
| `PRACTICAS/M05_PRACTICAS` | 28.392 | 77 | Sí, SHA-256 `5fccd198f73a3e54d003180cb36df7a774674fda885cff51594d80e7334da1b0` | 99,9832 % |

La ligera diferencia de palabras extraídas en prácticas se concentra en cinco apariciones de la palabra `razor` y no constituye prueba de una omisión: el Markdown íntegro está adjunto dentro del PDF, idéntico byte a byte, y la maquetación conserva los ejemplos. La cobertura se refiere al cotejo de texto extraíble, no a una identidad tipográfica carácter a carácter. Véase `M05_PDFS_VALIDACION.md`.

Se mantiene la maqueta M01: **9,8 pt** para texto y **8,2 pt** para código, sin ampliar artificialmente la fuente. Los PDF son resultados de sus Markdown, no versiones redactadas por separado.

## 2. Revisión visual de las 152 páginas

Se han examinado mosaicos de **todas las páginas** renderizadas del PDF final, complementados con comprobaciones **individuales sobre cada página** mediante PyMuPDF: presencia y cantidad de cuerpo textual, coordenadas de palabras, primera y última posición de bloques, portadas y comienzo de capítulos. Se contrastaron a escala normal las páginas con menor ocupación y los saltos de capítulo y de código. El resultado es:

- **75 páginas de teoría** y **77 de prácticas**; portadas e índices diferenciados.
- Cinco capítulos en orden, sin capítulos vacíos ni duplicados.
- Ninguna página de contenido posterior al índice con menos de 1.000 caracteres de cuerpo extraíble: el mínimo observado fue **1.083** en teoría y **1.349** en prácticas.
- No se detectaron palabras fuera de los límites de página ni páginas vacías.
- Los cortes entre páginas de bloques de código y tablas requieren continuidad lectora, pero no se encontraron secciones amputadas ni una página casi vacía que provenga de un título forzado. No se afirma que el lector pueda evitar todo salto natural de página.

**Incidencia corregida:** la introducción ampliada de prácticas dejó inicialmente una página casi vacía antes de P5.1. Se reubicó el itinerario presencial al arranque de P5.1 y se añadió una **puerta automática** que rechaza páginas de cuerpo inferior a 1.000 caracteres, exceptuadas portada e índice. El PDF actual inicia P5.1 en página 3.

## 3. Revisión didáctica y pedagógica

**Criterios contrastados:**

1. **Secuencia explicativa:** la teoría antecede a los ejercicios y cubre estados de Blazor, cliente HTTP tipado, DTO y respuestas de API; build/run/publish; Kestrel y ciclo de proceso; IIS/ANCM/Hosting Bundle; imagen y contenedor Docker.
2. **Continuidad:** P5.1 recupera la aplicación Blazor B y la API de M04; P5.2–P5.5 trabajan sobre MVC A de M02. No se inventa una aplicación empresarial adicional.
3. **Ejecución por el alumno:** se separan el **recorrido presencial de 270 minutos** y las ampliaciones autónomas. El alumno parte de la variante `P5.1_ANTES`, conserva una copia, añade el botón y método, compila, observa y restaura. En P5.5 reconstruye progresivamente el Dockerfile, comprueba la imagen y restaura la referencia.
4. **Distinguir evidencia de inferencia:** GET 200 y página de inicio no se confunden con CRUD completo; una API de memoria no se describe como SQL Server; un contenedor Linux sin LocalDB devuelve 503 deliberado en rutas dependientes de la base.
5. **Tecnologías pactadas:** .NET 8, ASP.NET Core MVC/Razor/Blazor Web App Interactive Server, EF Core/SQL Server Express LocalDB. Nada de SQLite. Identity/JWT de M04 no se reenseña como materia principal de M05.
6. **Recuperación del estado:** las variantes reversibles no se compilan junto al proyecto, se utilizan mediante copia explícita y restauración; el trabajo de salida queda limpio para el siguiente ejercicio.
7. **Material del alumno:** se eliminaron referencias internas de auditoría y a confirmaciones editoriales del cuerpo teórico y práctico.
8. **Duración:** la distribución 60 minutos teoría, 270 minutos práctica y 30 minutos de dudas se presenta como **itinerario de aula**, no como obligación de leer oralmente las 152 páginas; la documentación larga sirve también para estudio autónomo. Los tiempos no son resultado de una clase piloto.

**Juicio pedagógico:** el M05 dispone de una estructura gradual coherente, ejemplos razonados antes de construir, prácticas reproducibles y un itinerario esencial diferenciado. Supera la revisión editorial/didáctica documental realizada. Esto **no sustituye una prueba docente con estudiantes** ni asegura que toda infraestructura esté disponible en cualquier equipo.

## 4. Evidencias ejecutables y límites

- **IIS sobre Windows con Hosting Bundle real:** run `38456317027`, SUCCESS. Comprobación HTTP de la aplicación publicada y respuesta limitada de 503 sin LocalDB.
- **Blazor interactivo en Chromium:** run `38458993456`, SUCCESS; catálogo real y estados de respuesta ensayados. No se toma una simple respuesta HTTP del host como prueba de interacción.
- **API, Blazor, Kestrel y Docker Linux real:** run `38516974326`, SUCCESS, para los proyectos acumulativos, endpoints y publicación.
- **Regeneración y publicación PDF a partir de Markdown:** run `38516974252`, SUCCESS.
- **Medición y renderizado de páginas:** run `38516974256`, SUCCESS.
- **Estado inicial de P5.1.4 y restauración:** run `38517424599`, SUCCESS. El workflow copia y compila `P5.1_ANTES/Components/Pages/CatalogoRemoto.razor`, comprueba que todavía no contiene el botón del ejercicio, restaura el componente canónico y vuelve a compilar, además de los ensayos HTTP/Kestrel/Docker.

Los controles detectan errores de compilación, publicación, HTTP, estructura, páginas vacías y algunos errores editoriales. No demuestran que un alumno sin experiencia previa sea capaz de finalizar los ejercicios sin apoyo ni que un hospedaje de demostración cumpla criterios de producción. Esa afirmación no se hace.

## 5. Resolución de las incidencias halladas

| Incidencia | Corrección aplicada | Estado |
|---|---|---|
| Recorrido obligatorio mezclado con muchas extensiones | Delimitar pasos de aula frente a estudios autónomos | Corregida |
| Código Blazor de referencia ya contenía el botón antes del ejercicio | Variante inicial completa, respaldo, copia temporal, compilación, ejecución y restauración | Corregida |
| La reconstrucción del Dockerfile podía parecer solo un ejercicio optativo | Incluir P5.5.10–13 en recorrido presencial de Docker | Corregida |
| Página casi vacía creada por el prólogo extendido | Reubicar itinerario a P5.1 y controlar ocupación mínima de página | Corregida |
| Dos referencias al proceso interno de revisión | Sustituir por explicaciones técnicas dirigidas al alumno | Corregida |
| Falta de comprobación automatizada del estado inicial de Blazor | Paso de compilación reversible en `m05-integracion.yml` | Incorporado |

**Conclusión:** M05 cumple las puertas cuantitativas, de fidelidad documental, de tipografía y de trazabilidad revisadas. Revisión visual y pedagógica documental realizada sobre la versión canónica del 14/10/2026. Sin alterar ni fusionar `main`.

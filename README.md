# Curso de Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8

**AUTOR: JAIME GALLO**

**Duración:** 30 horas lectivas, cinco jornadas de seis horas (lunes a viernes, mañanas).  
**Público:** desarrolladores que ya conocen C#, ASP.NET Core Web API y Entity Framework Core.  
**Enfoque:** MVC y Blazor eminentemente prácticos; Razor Pages, seguridad e IIS/Docker tratados de forma introductoria y limitada.

## Documentación de preparación

- [Temario y matriz docente de 30 horas](TEMARIO_30H.md): los 25 puntos del programa con contenidos, ejercicios, proyectos, tiempos, secuencia y dependencias.
- [Guía docente](GUIA_DOCENTE.md): método de impartición y seguimiento de las cinco jornadas.
- [Requisitos del laboratorio](REQUISITOS_LABORATORIO.md): SDK, Visual Studio, API auxiliar, puertos, IIS, Docker y comprobaciones previas.

## Aplicaciones del curso

- **A — MVC:** días 1–2, productos, vistas Razor, formularios, DataAnnotations y CRUD con SQLite/EF Core.
- **B — Blazor Web App Interactive Server:** días 3–5, componentes, eventos, binding, servicios y consumo de una pequeña API de productos.
- **API auxiliar:** recurso suministrado para M04; no constituye otro curso de Web API.

No se reutiliza ningún proyecto de cursos previos. Los materiales están organizados en M01_MVC, M02_FORMULARIOS_RAZOR, M03_BLAZOR, M04_APIS_SEGURIDAD y M05_PROYECTO_DESPLIEGUE a medida que se construyen.

## Convención de entregas

**Por módulo**, exactamente dos documentos Markdown docentes y sus dos PDF:

- TEORIA/Mxx_TEORIA.md → TEORIA/Mxx_TEORIA.pdf.
- PRACTICAS/Mxx_PRACTICAS.md → PRACTICAS/Mxx_PRACTICAS.pdf.

Esto suma **10 MD + 10 PDF docentes** (los documentos globales de planificación son adicionales). Dentro de cada par de documentos se desarrollan íntegramente todos los puntos numerados del módulo; no hay un PDF independiente por punto.

Cada punto dispone de código de proyecto trazable paso a paso, con bloques activables mediante comentarios cuando el lenguaje lo permita, y sus pruebas funcionales. La evolución conserva los ejercicios anteriores, sin necesidad de reconstruir una aplicación nueva por punto. Las soluciones y los controles internos de verificación quedan separados del material del alumno.

## Estado y publicación

**M01 — Fundamentos de MVC:** ya contiene los cinco apartados (1.1–1.5), teoría, prácticas, retos con código comentado, proyectos escalonados y sus dos PDF derivados de los Markdown. La batería de CI ha superado 28/28 escenarios HTTP E2E. Consulta [M01 y sus materiales](M01_MVC/README.md).

**M02–M05:** materiales pendientes de elaboración. Los PDF de los demás módulos se generarán después de cerrar cada par de Markdown, no como ficheros individuales por ejercicio.

**Publicación:** el trabajo de M01 permanece en la rama `desarrollo/m01-mvc`. La rama principal no incorpora todavía estos materiales; la revisión humana de los PDF y de las prácticas en laboratorio sigue pendiente antes de solicitar su integración.

> Esta edición está fijada por el programa docente en .NET 8; consultar la fecha de soporte del SDK en REQUISITOS_LABORATORIO.md antes de programar nuevas ediciones.

# M02 — Formularios, validación y Razor Pages

**Curso:** Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8  
**Autor:** JAIME GALLO

Este módulo continúa la aplicación MVC construida en M01 y desarrolla cinco puntos progresivos: formularios GET/POST y antiforgery (2.1), Tag Helpers (2.2), validación con DataAnnotations y ModelState (2.3), CRUD persistente mediante EF Core y SQL Server Express LocalDB (2.4), y una comparación breve entre MVC y Razor Pages dentro del mismo host (2.5).

## Material del alumno

- [Teoría completa](TEORIA/M02_TEORIA.md) y [PDF de teoría](TEORIA/M02_TEORIA.pdf).
- [Cuaderno de prácticas](PRACTICAS/M02_PRACTICAS.md) y [PDF de prácticas](PRACTICAS/M02_PRACTICAS.pdf).

Los materiales cubren los cinco puntos del módulo. Sigue los ejercicios del cuaderno de prácticas en el orden indicado.

## Proyectos de prácticas

Los proyectos están disponibles bajo `PROYECTO/` y se abren independientemente con Visual Studio o con `dotnet run`:

| Punto | Carpeta | Propósito |
|---|---|---|
| P2.1 | [2.1](PROYECTO/2.1/CursoWeb.Mvc/) | HTML, GET/POST, model binding y antiforgery |
| P2.2 | [2.2](PROYECTO/2.2/CursoWeb.Mvc/) | Tag Helpers y navegación |
| P2.3 | [2.3](PROYECTO/2.3/CursoWeb.Mvc/) | DataAnnotations y ModelState |
| P2.4 | [2.4](PROYECTO/2.4/CursoWeb.Mvc/) | CRUD con EF Core y LocalDB |
| P2.5 | [2.5](PROYECTO/2.5/CursoWeb.Mvc/) | Razor Pages dentro de la aplicación MVC |

Algunas acciones y métodos están comentados para que puedas activarlos siguiendo los pasos del cuaderno. **No actives todos los bloques a la vez**: completa y comprueba cada práctica por separado.

Para P2.4 y P2.5 se requiere Windows con SQL Server Express LocalDB funcional. Incluso la página de comparación P2.5 reutiliza el arranque del host MVC, que inicializa la base al arrancar.

## Cómo empezar

Abre primero la [teoría 2.1](TEORIA/M02_TEORIA.md) y sigue el [cuaderno de prácticas](PRACTICAS/M02_PRACTICAS.md) por orden. Las instrucciones incluyen la carpeta exacta que debes abrir, los bloques que se activan, el comportamiento esperado y las variantes opcionales. Para volver a un estado inicial, recupera el proyecto de ese punto sin alterar los materiales de M01.

Los requisitos generales de la jornada están recogidos en [REQUISITOS_LABORATORIO.md](../REQUISITOS_LABORATORIO.md) y los contenidos del curso en [TEMARIO.md](../TEMARIO.md).

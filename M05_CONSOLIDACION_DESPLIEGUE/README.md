# M05 — Consolidación de Blazor y despliegue con ASP.NET Core

**AUTOR: JAIME GALLO**

## Material del módulo

- [Teoría (Markdown)](TEORIA/M05_TEORIA.md) · [Teoría (PDF)](TEORIA/M05_TEORIA.pdf).
- [Prácticas (Markdown)](PRACTICAS/M05_PRACTICAS.md) · [Prácticas (PDF)](PRACTICAS/M05_PRACTICAS.pdf).
- [Proyectos y variantes para los ejercicios](PROYECTO/).

## Proyectos que utilizarás

| Ejercicios | Proyecto | Contenido |
|---|---|---|
| P5.1 | [Blazor](PROYECTO/BLAZOR/CursoWeb.Blazor/) y [API](PROYECTO/API/CursoWeb.ProductosApi/) | Consulta HTTP, creación de productos, validación, actualización del catálogo y tratamiento de errores |
| P5.2–P5.5 | [MVC](PROYECTO/MVC/CursoWeb.Mvc/) | Compilación, publicación, ejecución con Kestrel, hospedaje en IIS y ejecución con Docker |
| Variantes guiadas | [VARIANTES](PROYECTO/VARIANTES/) | Estados iniciales y alternativas para desarrollar y repetir ejercicios |

## Cómo trabajar

Estudia el tema correspondiente en la teoría y ejecuta las instrucciones del cuaderno de prácticas. En P5.1 continuarás la aplicación Blazor y la API; en P5.2–P5.5 utilizarás **la misma aplicación MVC** en los tres entornos de despliegue.

Conserva las copias de respaldo cuando una práctica te pida sustituir temporalmente un archivo y restaura el estado indicado antes de continuar.

## SQL Server Express LocalDB y Docker

La aplicación MVC utiliza SQL Server Express LocalDB para su CRUD en Windows. Al ejecutarla en un contenedor Linux, la configuración `Despliegue__SinLocalDb=true` permite visitar la página principal, consultar el estado y cargar recursos estáticos, pero **las rutas que necesitan la base de datos devuelven HTTP 503**. El ejercicio no sustituye SQL Server por SQLite ni instala LocalDB en Linux.

Consulta también el [temario del curso](../TEMARIO.md) y los [requisitos del laboratorio](../REQUISITOS_LABORATORIO.md).

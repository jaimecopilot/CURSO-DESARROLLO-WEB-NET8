# Desarrollo web con ASP.NET Core MVC, Razor y Blazor en .NET 8

**AUTOR: JAIME GALLO**

Curso organizado en cinco módulos. Destinado a desarrolladores que conocen C#, ASP.NET Core Web API y Entity Framework Core. Se estudian MVC, vistas Razor, formularios y Razor Pages, componentes Blazor Interactive Server, consumo de API, seguridad básica y publicación elemental.

## Material del alumno

Cada módulo incluye teoría, prácticas y código descargable. Los proyectos y variantes de ejercicios se encuentran en la carpeta `PROYECTO` de cada módulo.

| Jornada | Módulo | Teoría | Prácticas | Código |
|---|---|---|---|---|
| 1 · MVC | [M01](M01_MVC/README.md) | [MD](M01_MVC/TEORIA/M01_TEORIA.md) · [PDF](M01_MVC/TEORIA/M01_TEORIA.pdf) | [MD](M01_MVC/PRACTICAS/M01_PRACTICAS.md) · [PDF](M01_MVC/PRACTICAS/M01_PRACTICAS.pdf) | [PROYECTO](M01_MVC/PROYECTO/) |
| 2 · Formularios y Razor Pages | [M02](M02_FORMULARIOS_RAZOR/README.md) | [MD](M02_FORMULARIOS_RAZOR/TEORIA/M02_TEORIA.md) · [PDF](M02_FORMULARIOS_RAZOR/TEORIA/M02_TEORIA.pdf) | [MD](M02_FORMULARIOS_RAZOR/PRACTICAS/M02_PRACTICAS.md) · [PDF](M02_FORMULARIOS_RAZOR/PRACTICAS/M02_PRACTICAS.pdf) | [PROYECTO](M02_FORMULARIOS_RAZOR/PROYECTO/) |
| 3 · Blazor | [M03](M03_BLAZOR/README.md) | [MD](M03_BLAZOR/TEORIA/M03_TEORIA.md) · [PDF](M03_BLAZOR/TEORIA/M03_TEORIA.pdf) | [MD](M03_BLAZOR/PRACTICAS/M03_PRACTICAS.md) · [PDF](M03_BLAZOR/PRACTICAS/M03_PRACTICAS.pdf) | [PROYECTO](M03_BLAZOR/PROYECTO/) |
| 4 · APIs y seguridad | [M04](M04_APIS_SEGURIDAD/README.md) | [MD](M04_APIS_SEGURIDAD/TEORIA/M04_TEORIA.md) · [PDF](M04_APIS_SEGURIDAD/TEORIA/M04_TEORIA.pdf) | [MD](M04_APIS_SEGURIDAD/PRACTICAS/M04_PRACTICAS.md) · [PDF](M04_APIS_SEGURIDAD/PRACTICAS/M04_PRACTICAS.pdf) | [PROYECTO](M04_APIS_SEGURIDAD/PROYECTO/) |
| 5 · Consolidación y despliegue | [M05](M05_CONSOLIDACION_DESPLIEGUE/README.md) | [MD](M05_CONSOLIDACION_DESPLIEGUE/TEORIA/M05_TEORIA.md) · [PDF](M05_CONSOLIDACION_DESPLIEGUE/TEORIA/M05_TEORIA.pdf) | [MD](M05_CONSOLIDACION_DESPLIEGUE/PRACTICAS/M05_PRACTICAS.md) · [PDF](M05_CONSOLIDACION_DESPLIEGUE/PRACTICAS/M05_PRACTICAS.pdf) | [PROYECTO](M05_CONSOLIDACION_DESPLIEGUE/PROYECTO/) |

Consulta el [temario completo](TEMARIO.md), su [versión de lectura directa](https://raw.githubusercontent.com/jaimecopilot/CURSO-DESARROLLO-WEB-NET8/main/TEMARIO.md) y los [requisitos del laboratorio](REQUISITOS_LABORATORIO.md).

## Recorrido de aprendizaje

- **Aplicación A — MVC:** M01 construye rutas, controladores y vistas Razor; M02 añade formularios, validación, CRUD con **EF Core 8 y SQL Server Express LocalDB** y la comparación breve con Razor Pages.
- **Aplicación B — Blazor Web App Interactive Server:** M03 introduce componentes, estado, eventos y servicios; M04 incorpora una API auxiliar HTTP y una introducción a autenticación/autorización. La ampliación de Identity y JWT utiliza LocalDB, no SQLite.
- **M05:** consolida el cliente Blazor y reutiliza **la misma aplicación MVC A** para ejecutar, publicar y comparar Kestrel, IIS y Docker. El contenedor Linux no ejecuta LocalDB: el material identifica explícitamente las rutas que no pueden usar el CRUD.

Los proyectos contienen estados escalonados y variantes para construir los ejercicios. **No todos los fragmentos comentados deben activarse a la vez**: sigue el orden y las indicaciones de cada cuaderno de prácticas.

## Preparación y ejecución

Instala .NET SDK 8 y Visual Studio con desarrollo ASP.NET/web. Para M02 y la ampliación de M04, prepara Windows con SQL Server Express LocalDB; para IIS, Windows con IIS y ASP.NET Core Hosting Bundle 8; para Docker, un motor de contenedores Linux. Los puertos y comandos exactos se especifican en los manuales de prácticas.

Abre el módulo correspondiente, **estudia primero su teoría y después sigue sus prácticas por orden**. Cada módulo incluye las rutas de proyecto, acciones, resultados esperados y ejercicios de ampliación cuando proceda.

> Los laboratorios son formativos, no configuraciones listas para producción. Comprueba la vigencia del soporte de .NET 8 antes de utilizarlo en nuevos proyectos.

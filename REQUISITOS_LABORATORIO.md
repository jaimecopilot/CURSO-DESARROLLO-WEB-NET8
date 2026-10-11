# Requisitos y preparación del laboratorio

## Propósito y alcance

Estas condiciones soportan una formación presencial de cinco jornadas y **deben comprobarse antes de la primera clase**. La aplicación MVC (A) ocupa M01/M02; la aplicación Blazor (B) ocupa M03/M04/M05; la API auxiliar (GET/POST) se aporta en el propio repositorio. IIS y Docker se utilizan únicamente en M05. No se requiere ningún proyecto de otro curso.

## 1. Puesto de desarrollo del alumno

- Windows 10/11 o entorno compatible para desarrollar y ejecutar .NET 8. Para la práctica IIS se necesita un **host Windows** con IIS configurado; no se da por hecho que otros sistemas puedan ejecutar IIS.
- **SDK de .NET 8**, además de runtime ASP.NET Core 8. Comprobar con `dotnet --list-sdks`, `dotnet --list-runtimes` y `dotnet --info`.
- Visual Studio con carga de trabajo **Desarrollo de ASP.NET y web** y compatibilidad con .NET 8, o VS Code y CLI .NET 8 para ejercicios genéricos. La guía detallada utilizará rutas de Visual Studio y comandos dotnet equivalentes cuando sea posible.
- Navegador moderno con herramientas de desarrollo; posibilidad de abrir localhost y varios puertos simultáneos.
- Restauración NuGet previa: conexión a fuentes oficiales en preparación; caché lista si el laboratorio tiene red limitada.
- Permisos locales suficientes para crear/editar carpetas, ejecutar procesos y acceder a puertos de laboratorio.

### Compatibilidad temporal de .NET 8

Esta edición se mantiene **deliberadamente en .NET 8** por el temario acordado. Según la política oficial de Microsoft, **.NET 8 finaliza su soporte el 10 de noviembre de 2026**. Actualizar la plataforma será una decisión curricular posterior, no una modificación silenciosa durante la preparación. No utilizar esta formación como guía para desplegar sistemas nuevos de producción más allá del soporte.

Referencia oficial: https://dotnet.microsoft.com/es-es/platform/support/policy

## 2. Dependencias de los proyectos del curso

**Aplicación MVC A:** ASP.NET Core MVC net8.0, C#, EF Core 8 y proveedor SQLite cuando el capítulo 2.4 introduce persistencia. En M01 se utilizan productos precargados sin EF; el alumno no debe configurar SQLite hasta que corresponda.

**Aplicación Blazor B:** Blazor Web App net8.0, modo principal Interactive Server. No se crea una WebAssembly standalone. En M03 los datos proceden de un servicio en memoria; en M04 se sustituye/añade acceso mediante HttpClient al API auxiliar.

**API auxiliar:** proyecto ASP.NET Core Web API net8.0 pequeño, proporcionado por el curso; endpoints GET y POST de productos, datos en memoria. No requiere SQL Server ni credenciales remotas.

**Demostración de seguridad:** ejemplo local incluido y preconfigurado con identidad de demostración; sin depender de servicios externos de identidad. Contará con instrucciones completas y advertencia clara sobre el carácter didáctico. Su implementación concreta se verificará antes de entregar P4.4.

**Pruebas de navegador:** automatización E2E interna del repositorio sobre HTTP local; las herramientas de test no son una nueva unidad del temario. Los procedimientos deben poder ejecutarse sobre la versión que indique la práctica.

## 3. Puertos de referencia del laboratorio

Los puertos siguientes son una **convención inicial**, y las prácticas definitivas incluirán la configuración exacta y las URL:

| Proceso | URL HTTP didáctica |
|---|---|
| Aplicación MVC A | http://localhost:5091 |
| Blazor Web App B | http://localhost:5092 |
| API auxiliar | http://localhost:5093 |
| IIS (sitio local de ejemplo) | http://localhost:8091 |
| Docker (puerto de host) | http://localhost:8081 |

Una aplicación ASP.NET Core con imagen oficial de **.NET 8 escucha normalmente en el puerto 8080 dentro del contenedor**; por tanto, el ejemplo de publicación será `-p 8081:8080`, no `-p 8081:80`. El Dockerfile y la URL final se mantendrán coherentes con ello.

Referencias: https://learn.microsoft.com/es-es/dotnet/core/docker/ y https://learn.microsoft.com/en-us/dotnet/core/compatibility/containers/8.0/aspnet-port

**Atención:** los puertos no se dan por disponibles sin comprobarlos; el laboratorio debe reservarlos y evitar conflictos con procesos existentes. HTTPS, confianza de certificados de desarrollo y credenciales del navegador se tratarán en la guía concreta solo cuando la actividad los necesite.

## 4. Preparación específica de IIS (solo M05)

El instructor preparará antes de la jornada:
1. Equipo/VM Windows compatible y rol/característica IIS activada.
2. ASP.NET Core **Hosting Bundle 8** instalado en el servidor IIS, con los servicios reciclados/reiniciados según las indicaciones oficiales.
3. Permiso para crear un sitio de laboratorio en IIS y una carpeta de publicación; pool de aplicaciones configurado conforme al modelo recomendado para ASP.NET Core (sin administrar CLR de .NET Framework).
4. Puerto de prueba libre, ruta física y permisos de lectura/ejecución y escritura **si** la muestra lo necesita.
5. Prueba manual con una aplicación mínima publicada antes de la clase.

Los alumnos seguirán el procedimiento funcional; no aprenderán administración avanzada, publicación pública ni endurecimiento de IIS.

## 5. Preparación específica de Docker (solo M05)

- Docker Desktop/Engine disponible y **motor iniciado**, con acceso autorizado para ejecutar `docker version`, `docker build` y `docker run`.
- Disponibilidad de imágenes Microsoft para .NET 8 SDK/runtime, descargadas con antelación si el acceso a internet es limitado.
- Espacio disponible para build y puertos libres; capacidad de acceder desde navegador a localhost.
- Una muestra autocontenida para la práctica, de modo que no haga falta orquestación ni Docker Compose.
- Advertir que datos de contenedor sin volumen persistente pueden perderse al eliminarlo. El curso no enseña almacenamiento persistente de contenedores.

Referencias: https://learn.microsoft.com/en-us/dotnet/core/docker/ y https://learn.microsoft.com/en-us/dotnet/core/docker/container-images

## 6. Plan de comprobaciones previas del instructor

Comprobar antes de comenzar cada jornada:
- **M01:** plantilla MVC net8.0 restaurada/compilable y navegación local.
- **M02:** paquete EF Core SQLite disponible y base de datos escribible en entorno de laboratorio.
- **M03:** plantilla Blazor Web App net8.0 con Interactive Server, comprobando que un @onclick responde realmente.
- **M04:** API incluida accesible por HTTP; Blazor tiene su URL configurada; demostración local de autenticación funcional.
- **M05:** `dotnet publish` produce archivos ejecutables; IIS/Hosting Bundle funciona; Docker hace build y ejecuta con mapeo a 8080.
- Los tests E2E y compilaciones deben corresponder exactamente a los pasos documentados; disponer del resultado/log real, no de una suposición.

## 7. Límites de seguridad de los ejemplos

Usar datos ficticios, puertos locales y credenciales de demostración exclusivamente. No reutilizar la configuración didáctica de autenticación o HTTP en producción; no exponer servicios de laboratorio públicamente sin configuración de seguridad adecuada. El curso muestra fundamentos, no un diseño de operación segura en producción.

## 8. Limitación del entorno de redacción

La preparación documental puede realizarse sin .NET ni Docker instalados en el equipo que genera los contenidos. Esa preparación **no es evidencia de compilación o E2E**. Los pasos se declararán probados únicamente cuando se ejecuten efectivamente en un entorno con los SDK, sistemas y servicios correspondientes; los pendientes se registrarán en documentos internos.

# M05 — Consolidación de Blazor y despliegue elemental (.NET 8)

Este módulo final utiliza **dos aplicaciones que el alumno ya conoce**, no una tercera aplicación empresarial:

- **P5.1:** `PROYECTO/BLAZOR/CursoWeb.Blazor` y `PROYECTO/API/CursoWeb.ProductosApi`. Son estados acumulativos procedentes de M04; se comprueba GET/POST, validación, errores y actualización visible de datos. El cliente no depende de Identity/JWT.
- **P5.2–P5.5:** `PROYECTO/MVC/CursoWeb.Mvc`, continuación de la aplicación A de M02. Es el **mismo proyecto MVC** para ejecutar, publicar, utilizar Kestrel, IIS y Docker.

## Fuente docente canónica

La teoría figura en `TEORIA/M05_TEORIA.md` y las prácticas en `PRACTICAS/M05_PRACTICAS.md`. Los PDF homónimos se generan **solo** desde esos Markdown, con la plantilla tipográfica M01 (texto de 9,8 pt y código de 8,2 pt).

## Limitación explícita de LocalDB

Por defecto, MVC conserva el CRUD de M02 con SQL Server Express LocalDB en Windows. La opción `Despliegue:SinLocalDb=true` **omite la inicialización de la base** y permite comprobar las páginas MVC sin datos y los recursos estáticos; las rutas que requieren el CRUD devuelven 503. Se utiliza al ejecutar la imagen Docker **Linux**; no sustituye LocalDB por SQLite ni permite declarar probado el CRUD en contenedor.

## Itinerario presencial

La jornada tiene 6 horas: 60 minutos de teoría, 270 minutos de prácticas y 30 minutos de repaso/dudas. Los tiempos por punto se corresponden con `TEMARIO_30H.md`. Las ampliaciones autónomas de los manuales no añaden tareas obligatorias al itinerario.

## Advertencia de despliegue

IIS solo puede declararse verificado después de ejecutar realmente sobre IIS en Windows con ASP.NET Core Hosting Bundle. Docker solo puede declararse verificado después de construir y ejecutar un contenedor real. Las pruebas de Kestrel no sustituyen ninguna de estas evidencias.

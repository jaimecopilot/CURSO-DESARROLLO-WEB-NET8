# Punto 1.3 — Estructura y convenciones MVC

**AUTOR: JAIME GALLO**

Esta carpeta es un **estado de continuidad ya funcional del 1.2**: se han activado las acciones, el bucle de listado y la navegación a Productos. El código de los puntos 1.1 y 1.2 queda conservado en sus carpetas anteriores; aquí se prepara la fase 1.3.

## Inicio

Desde esta carpeta:

~~~bash
dotnet restore
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

Abrir `/` y `/Productos`. Ambos muestran sus páginas previas. No se utilizan servicios externos ni EF Core todavía.

## Bloques de 1.3

- **1.3.1:** inspeccionar `CursoWeb.Mvc.csproj`, carpetas `Controllers`, `Models`, `Views`, `wwwroot`, `Properties`; sin cambiar código.
- **1.3.2:** seguir `Program.cs` (servicios, middleware, ruta y `Run()`); no descomentar fragmentos.
- **1.3.3:** `appsettings.json` ya contiene la sección `Curso`. En `Program.cs`, descomentar la línea `app.Logger.LogInformation(...)`. Al iniciar aparece `P1.3 configuracion: Curso MVC de productos` en el log.
- **1.3.4:** habilitar el `<link rel="stylesheet" href="/css/catalogo.css" />` retirando los dos delimitadores de comentario Razor `PASO 1.3.4` en `Views/Shared/_Layout.cshtml`. El navegador pedirá además `/css/catalogo.css`, ya presente bajo `wwwroot`.
- **1.3.5:** habilitar el enlace **Guía pública** quitando los delimitadores Razor `PASO 1.3.5` del mismo layout. El fichero `wwwroot/recursos/guia-publica.txt` ya existe.
- **RETO 1.3:** habilitar el enlace **Aviso de laboratorio** quitando los delimitadores Razor `RETO 1.3` del layout. Comparar el recurso público `/recursos/aviso-laboratorio.txt` (200) con `/DOCUMENTACION/nota-interna.txt` (404). El archivo interior sirve solo para razonar sobre la diferencia entre raíz del proyecto y raíz web; no contiene información sensible real.

**Importante:** los archivos de texto y CSS ya existen, incluso cuando el enlace que permite descubrirlos en la navegación sigue comentado. Quitar un enlace del layout **no protege ni oculta** un archivo dentro de `wwwroot`. Esta distinción es parte del reto.

Toda la explicación del código y del reto está en `../../../PRACTICAS/M01_PRACTICAS.md`, sección P1.3. Para ejecutar los escenarios de forma automatizada desde la raíz del repositorio:

~~~bash
bash M01_MVC/TESTS/1.3_e2e.sh
~~~

El script crea copias temporales y verifica los estados de forma independiente en Kestrel, sin alterar el proyecto inicial del alumno.

## Laboratorios ampliados y correspondencia documental

La versión ampliada de [P1.3](../../../PRACTICAS/M01_PRACTICAS.md) incluye recorridos adicionales de diagnóstico y consolidación basados en **este mismo proyecto**. Son actividades de lectura, comprobación HTTP y activación de los bloques ya documentados más arriba; no constituyen un segundo conjunto de soluciones ni requieren crear otro proyecto.

**Correspondencia verificable:** P1.3 del Markdown → código de esta carpeta → `M01_MVC/TESTS/1.3_e2e.sh`. Las explicaciones detalladas y los enunciados viven solo en el MD de prácticas; el PDF se genera de esa fuente, sin editarlo manualmente.

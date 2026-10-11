# P1.4 — Controladores, acciones, parámetros y routing

**AUTOR: JAIME GALLO**

Este proyecto es la evolución del MVC de 1.3. El catálogo y las páginas anteriores siguen activos. La lista fija se ha extraído a `ObtenerProductosEjemplo()` para reutilizar los mismos productos sin base de datos.

## Ejecutar

Desde esta carpeta:

~~~bash
dotnet restore
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

En el estado inicial funcionan `/` y `/Productos`, pero aún no se han habilitado Estado, Detalle ni Ficha.

## Pasos activables

- **1.4.1:** identificar la ruta convencional en `Program.cs` y `ObtenerProductosEjemplo()` en `Controllers/ProductosController.cs`.
- **1.4.2:** retirar las líneas delimitadoras del comentario `PASO 1.4.2` del controlador. Comprobar `GET /Productos/Estado` (200, texto).
- **1.4.3:** retirar los delimitadores del comentario `PASO 1.4.3`. Comprobar `/Productos/Detalle/2` (200, HTML), `/Productos/Detalle/99` (404), `/Productos/Detalle/0` (400). La vista `Views/Productos/Detalle.cshtml` ya existe.
- **1.4.4:** retirar los delimitadores del bloque `PASO 1.4.4`. La ruta por atributo `/catalogo/ficha/{id:int}` admite enteros, no texto arbitrario.
- **1.4.5:** en `Views/Productos/Index.cshtml`, retirar los delimitadores del comentario Razor `PASO 1.4.5` para activar tres enlaces, uno por producto.
- **RETO 1.4:** retirar las líneas delimitadoras de `RETO 1.4` en el controlador; `GET /catalogo/resumen/2` devuelve JSON; `/catalogo/resumen/99` devuelve 404. Un segmento no entero tampoco coincide con la plantilla.

Los bloques están **incluidos en este proyecto** y se explican con el código completo en la sección P1.4 de `../../../PRACTICAS/M01_PRACTICAS.md`.

## Pruebas reales

Desde la raíz del repositorio:

~~~bash
bash M01_MVC/TESTS/1.4_e2e.sh
~~~

El script prepara copias temporales para comprobar cada estado del alumno y ejecuta peticiones HTTP contra Kestrel. Requiere SDK .NET 8, Bash, Python 3 y curl.

## Laboratorios ampliados y correspondencia documental

La versión ampliada de [P1.4](../../../PRACTICAS/M01_PRACTICAS.md) incluye recorridos adicionales de diagnóstico y consolidación basados en **este mismo proyecto**. Son actividades de lectura, comprobación HTTP y activación de los bloques ya documentados más arriba; no constituyen un segundo conjunto de soluciones ni requieren crear otro proyecto.

**Correspondencia verificable:** P1.4 del Markdown → código de esta carpeta → `M01_MVC/TESTS/1.4_e2e.sh`. Las explicaciones detalladas y los enunciados viven solo en el MD de prácticas; el PDF se genera de esa fuente, sin editarlo manualmente.

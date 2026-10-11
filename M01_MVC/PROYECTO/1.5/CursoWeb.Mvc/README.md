# P1.5 — Vistas Razor, layouts y vistas parciales

Este proyecto continúa P1.4 en su estado **completo con los cinco pasos guiados activados** (Estado, Detalle, Ficha y enlaces), manteniendo el reto opcional histórico sin activar. Los archivos nuevos y los bloques de P1.5 están preparados para que el alumno los active por separado.

## Iniciar

Desde esta carpeta:
~~~bash
dotnet restore
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

## Pasos y reto

- **1.5.1 (exploración):** estudiar los `@model` distintos de `Views/Productos/Index.cshtml`, `Views/Productos/Detalle.cshtml` y el valor `ViewData["Title"]`; no requiere descomentar.
- **1.5.2:** en `Views/Productos/Index.cshtml`, retirar las líneas que delimitan el comentario Razor `PASO 1.5.2`; aparece una condición `@if` con el mensaje `catalogo-completo`.
- **1.5.3:** activar los **dos** bloques `PASO 1.5.3`: uno en `Views/Shared/_Layout.cshtml` que representa una sección opcional, y otro en `Views/Productos/Detalle.cshtml` que la declara. El detalle incluirá `nota-pagina-detalle`; el listado seguirá funcionando sin declarar sección.
- **1.5.4:** en `Views/Productos/Index.cshtml` activar el bloque `PASO 1.5.4`. El Partial Tag Helper `<partial name="_TarjetaProducto" model="producto" />` representa tres tarjetas adicionales usando `Views/Shared/_TarjetaProducto.cshtml`.
- **1.5.5:** en `Views/Productos/Detalle.cshtml`, activar el bloque `PASO 1.5.5` para reutilizar la misma vista parcial en una ficha individual. La página contiene una tarjeta.
- **RETO 1.5:** abrir `Views/Shared/_TarjetaProducto.cshtml` y eliminar las **dos líneas delimitadoras** del bloque Razor `RETO 1.5`. La condición `@if (Model.Precio < 3m)` añade `Precio económico` **solo a Lápiz** tanto en la lista de tarjetas como en su detalle.

En `../../../PRACTICAS/M01_PRACTICAS.md` (sección P1.5) se explican todas las instrucciones, el código exacto, su comportamiento y los resultados esperados.

## Comprobar

Desde la raíz del repositorio:
~~~bash
bash M01_MVC/TESTS/1.5_e2e.sh
~~~

Compila, inicia Kestrel, verifica rutas y contenidos y prueba cada activación mediante copias temporales. SDK 8, Bash, Python 3 y curl son requisitos.

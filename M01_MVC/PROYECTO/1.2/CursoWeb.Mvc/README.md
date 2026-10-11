# Punto 1.2 — Evolución reproducible de MVC

**AUTOR: JAIME GALLO**

Este proyecto es la **continuación autónoma** del proyecto del punto 1.1. Se conserva su página inicial y se añaden los archivos `Models/Producto.cs`, `Controllers/ProductosController.cs` y `Views/Productos/Index.cshtml`.

## Iniciar

Abrir `CursoWeb.Mvc.csproj` desde esta misma carpeta, o ejecutar:

~~~bash
dotnet restore
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

- `http://localhost:5091/`: portada del capítulo anterior.
- `http://localhost:5091/Productos`: vista inicial de 1.2, sin modelo.
- `http://localhost:5091/Productos/Index`: ruta equivalente.

## Activación por pasos

1. **1.2.2:** identificar `Models/Producto.cs`; ya está activo y es independiente de HTTP, controladores y vistas.
2. **1.2.3:** en `Controllers/ProductosController.cs`, retirar las dos líneas delimitadoras `/* PASO 1.2.3 INICIO` y `PASO 1.2.3 FIN */` sin modificar el bloque interior; comentar el `return View();` situado al final de la acción. El proyecto compila; el controlador envía tres objetos a la vista y aparece su cantidad.
3. **1.2.4:** en `Views/Productos/Index.cshtml`, eliminar las dos líneas del comentario Razor `@* PASO 1.2.4 (inicio)` y `PASO 1.2.4 (fin) *@`. Aparecen tres filas de productos.
4. **1.2.5:** en `Views/Shared/_Layout.cshtml`, quitar los delimitadores del comentario Razor del paso para habilitar el enlace de navegación `Productos`.

5. **RETO 1.2:** con los pasos 1.2.3–1.2.5 activos, comentar la línea de producto `Cuaderno` y descomentar la línea ya proporcionada de `Bloc` dentro de `ProductosController.Index()`. El recuento sigue siendo 3; la vista muestra Bloc en lugar de Cuaderno. El código, su explicación y la comprobación están en P1.2, apartado G.

Detener y volver a ejecutar para observar los cambios de cada estado.

La práctica completa está en `../../../PRACTICAS/M01_PRACTICAS.md`, sección P1.2.

## Comprobación automatizada

Desde la raíz del repositorio: `bash M01_MVC/TESTS/1.2_e2e.sh`.

Se comprueban por separado el estado inicial, la entrega de modelo, la presentación de productos, la navegación y el reto, con compilación y peticiones HTTP reales. Las variantes se realizan en copias temporales del proyecto para no alterar el material del alumno.

## Laboratorios ampliados y correspondencia documental

La versión ampliada de [P1.2](../../../PRACTICAS/M01_PRACTICAS.md) incluye recorridos adicionales de diagnóstico y consolidación basados en **este mismo proyecto**. Son actividades de lectura, comprobación HTTP y activación de los bloques ya documentados más arriba; no constituyen un segundo conjunto de soluciones ni requieren crear otro proyecto.

**Correspondencia verificable:** P1.2 del Markdown → código de esta carpeta → `M01_MVC/TESTS/1.2_e2e.sh`. Las explicaciones detalladas y los enunciados viven solo en el MD de prácticas; el PDF se genera de esa fuente, sin editarlo manualmente.

# Punto 1.2 — Evolución reproducible de MVC

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

Detener y volver a ejecutar para observar los cambios de cada estado.

La práctica completa está en `../../../PRACTICAS/M01_PRACTICAS.md`, sección P1.2.

## Comprobación automatizada

Desde la raíz del repositorio: `bash M01_MVC/TESTS/1.2_e2e.sh`.

Se comprueban por separado el estado inicial, la entrega de modelo, la presentación de productos y la navegación, con compilación y peticiones HTTP reales. Las variantes se realizan en copias temporales del proyecto para no alterar el material del alumno.

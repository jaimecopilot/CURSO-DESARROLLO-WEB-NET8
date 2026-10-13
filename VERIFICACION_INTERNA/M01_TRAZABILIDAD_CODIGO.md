# M01 — Trazabilidad real de prácticas y proyectos

Informe interno generado desde el código versionado. El PDF procede solo de los MD.
La correspondencia estática verifica archivos, marcas de activación y fragmentos concretos; GitHub Actions valida su compilación y ejecución HTTP por separado.

| Punto | Pasos y reto en MD | Correspondencias de código | E2E |
|---|---|---:|---|
| P1.1 | 6 etapas distintas, incluido reto | 8 | 7 escenarios |
| P1.2 | 5 etapas distintas, incluido reto | 5 | 6 escenarios |
| P1.3 | 6 etapas distintas, incluido reto | 8 | 6 escenarios |
| P1.4 | 6 etapas distintas, incluido reto | 7 | 7 escenarios |
| P1.5 | 6 etapas distintas, incluido reto | 9 | 9 escenarios |

**Total: 37 correspondencias de código comprobadas.**

## Matriz detallada paso → archivo → comprobación

| Paso/reto | Archivo real del proyecto | Marca en fuente | Fragmentos contrastados |
|---|---|---|---:|
| 1.1.1 | `PROYECTO/1.1/CursoWeb.Mvc/Controllers/HomeController.cs` | `PASO 1.1.1` | 2 |
| 1.1.2 | `PROYECTO/1.1/CursoWeb.Mvc/Program.cs` | `PASO 1.1.2` | 1 |
| 1.1.3 | `PROYECTO/1.1/CursoWeb.Mvc/Program.cs` | `PASO 1.1.3` | 2 |
| 1.1.4 | `PROYECTO/1.1/CursoWeb.Mvc/Controllers/HomeController.cs` | `PASO 1.1.4` | 1 |
| 1.1.5 | `PROYECTO/1.1/CursoWeb.Mvc/Views/Home/Index.cshtml` | `PASO 1.1.5` | 1 |
| 1.1.5 | `PROYECTO/1.1/CursoWeb.Mvc/Views/Home/Index.cshtml` | `APLICACIÓN 1.1.5` | 1 |
| RETO 1.1 | `PROYECTO/1.1/CursoWeb.Mvc/Controllers/HomeController.cs` | `RETO 1.1` | 1 |
| RETO 1.1 | `PROYECTO/1.1/CursoWeb.Mvc/Views/Home/Index.cshtml` | `RETO 1.1` | 1 |
| 1.2.2 | `PROYECTO/1.2/CursoWeb.Mvc/Models/Producto.cs` | `class Producto` | 3 |
| 1.2.3 | `PROYECTO/1.2/CursoWeb.Mvc/Controllers/ProductosController.cs` | `PASO 1.2.3` | 2 |
| 1.2.4 | `PROYECTO/1.2/CursoWeb.Mvc/Views/Productos/Index.cshtml` | `PASO 1.2.4` | 2 |
| 1.2.5 | `PROYECTO/1.2/CursoWeb.Mvc/Views/Shared/_Layout.cshtml` | `PASO 1.2.5` | 1 |
| RETO 1.2 | `PROYECTO/1.2/CursoWeb.Mvc/Controllers/ProductosController.cs` | `RETO 1.2` | 2 |
| 1.3.1 | `PROYECTO/1.3/CursoWeb.Mvc/CursoWeb.Mvc.csproj` | `Microsoft.NET.Sdk.Web` | 1 |
| 1.3.2 | `PROYECTO/1.3/CursoWeb.Mvc/Program.cs` | `AddControllersWithViews` | 3 |
| 1.3.3 | `PROYECTO/1.3/CursoWeb.Mvc/Program.cs` | `PASO 1.3.3` | 2 |
| 1.3.3 | `PROYECTO/1.3/CursoWeb.Mvc/appsettings.json` | `"Curso"` | 2 |
| 1.3.4 | `PROYECTO/1.3/CursoWeb.Mvc/Views/Shared/_Layout.cshtml` | `PASO 1.3.4` | 1 |
| 1.3.4 | `PROYECTO/1.3/CursoWeb.Mvc/wwwroot/css/catalogo.css` | `PASO 1.3.4` | 1 |
| 1.3.5 | `PROYECTO/1.3/CursoWeb.Mvc/Views/Shared/_Layout.cshtml` | `PASO 1.3.5` | 1 |
| RETO 1.3 | `PROYECTO/1.3/CursoWeb.Mvc/Views/Shared/_Layout.cshtml` | `RETO 1.3` | 1 |
| 1.4.1 | `PROYECTO/1.4/CursoWeb.Mvc/Controllers/ProductosController.cs` | `PASO 1.4.1` | 1 |
| 1.4.2 | `PROYECTO/1.4/CursoWeb.Mvc/Controllers/ProductosController.cs` | `PASO 1.4.2` | 2 |
| 1.4.3 | `PROYECTO/1.4/CursoWeb.Mvc/Controllers/ProductosController.cs` | `PASO 1.4.3` | 4 |
| 1.4.3 | `PROYECTO/1.4/CursoWeb.Mvc/Views/Productos/Detalle.cshtml` | `@model` | 2 |
| 1.4.4 | `PROYECTO/1.4/CursoWeb.Mvc/Controllers/ProductosController.cs` | `PASO 1.4.4` | 2 |
| 1.4.5 | `PROYECTO/1.4/CursoWeb.Mvc/Views/Productos/Index.cshtml` | `PASO 1.4.5` | 2 |
| RETO 1.4 | `PROYECTO/1.4/CursoWeb.Mvc/Controllers/ProductosController.cs` | `RETO 1.4` | 2 |
| 1.5.1 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Productos/Index.cshtml` | `@model` | 1 |
| 1.5.1 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Productos/Detalle.cshtml` | `@model` | 1 |
| 1.5.2 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Productos/Index.cshtml` | `PASO 1.5.2` | 2 |
| 1.5.3 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Shared/_Layout.cshtml` | `PASO 1.5.3` | 1 |
| 1.5.3 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Productos/Detalle.cshtml` | `PASO 1.5.3` | 2 |
| 1.5.4 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Shared/_TarjetaProducto.cshtml` | `PASO 1.5.4` | 2 |
| 1.5.4 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Productos/Index.cshtml` | `PASO 1.5.4` | 1 |
| 1.5.5 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Productos/Detalle.cshtml` | `PASO 1.5.5` | 1 |
| RETO 1.5 | `PROYECTO/1.5/CursoWeb.Mvc/Views/Shared/_TarjetaProducto.cshtml` | `RETO 1.5` | 2 |

**Límite:** los fragmentos conceptuales de teoría que no se presentan como ejercicios ejecutables no generan código nuevo. Los recuentos de escenarios anteriores se han contrastado con los scripts `M01_MVC/TESTS/1.1_e2e.sh` a `1.5_e2e.sh`: incluyen estados base, activaciones, aplicaciones autónomas y retos, además de regresiones del catálogo. Esta auditoría no acredita observación visual de los PDF ni la ejecución manual en Visual Studio.

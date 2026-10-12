using CursoWeb.Mvc.Models;
using Microsoft.AspNetCore.Mvc;

namespace CursoWeb.Mvc.Controllers;

public class ProductosController : Controller
{
    // PASO 1.4.1 — Reutilización de los datos fijos por Index y Detalle.
    // No hay base de datos: cada consulta genera una lista de ejemplo.
    private static IReadOnlyList<Producto> ObtenerProductosEjemplo() =>
        new List<Producto>
        {
            new() { Id = 1, Nombre = "Cuaderno", Precio = 4.50m },
            // RETO 1.2 (variante histórica del capítulo anterior):
            // new() { Id = 1, Nombre = "Bloc", Precio = 4.50m },
            new() { Id = 2, Nombre = "Lápiz", Precio = 1.20m },
            new() { Id = 3, Nombre = "Carpeta", Precio = 3.75m }
        };

    [HttpGet]
    public IActionResult Index()
    {
        return View(ObtenerProductosEjemplo());
    }

    // PASO 1.4.2: añadir acción sin modificar la ruta convencional.
    /* PASO 1.4.2 INICIO
    [HttpGet]
    public IActionResult Estado()
    {
        return Content("Catalogo MVC disponible", "text/plain");
    }
    PASO 1.4.2 FIN */

    // PASO 1.4.3: valor id desde la ruta; distinguir 200, 400 y 404.
    /* PASO 1.4.3 INICIO
    [HttpGet]
    public IActionResult Detalle(int id)
    {
        if (id <= 0)
        {
            return BadRequest("El identificador debe ser mayor que cero.");
        }

        var producto = ObtenerProductosEjemplo().FirstOrDefault(p => p.Id == id);
        if (producto is null)
        {
            return NotFound();
        }

        return View(producto);
    }
    PASO 1.4.3 FIN */

    // PASO 1.4.4: la ruta absoluta definida por atributos
    // "/catalogo/ficha/{id:int}" exige un segmento que sea entero.
    /* PASO 1.4.4 INICIO
    [HttpGet("/catalogo/ficha/{id:int}")]
    public IActionResult Ficha(int id)
    {
        var producto = ObtenerProductosEjemplo().FirstOrDefault(p => p.Id == id);
        if (producto is null)
        {
            return NotFound();
        }

        return View("Detalle", producto);
    }
    PASO 1.4.4 FIN */

    // APLICACION 1.4 — Escribe aquí una acción propia BuscarPorNombre(string nombre).
    // Utiliza [HttpGet("/catalogo/buscar/{nombre}")], busca sin distinguir
    // mayúsculas en ObtenerProductosEjemplo(), devuelve NotFound() si no hay
    // coincidencia y reutiliza View("Detalle", producto) si existe.
    // No copies el método Detalle: resuelve tú mismo el enlace del parámetro.
    //
    // RETO 1.4: comparar un resultado JSON de MVC con una vista HTML.
    /* RETO 1.4 INICIO
    [HttpGet("/catalogo/resumen/{id:int}")]
    public IActionResult Resumen(int id)
    {
        var producto = ObtenerProductosEjemplo().FirstOrDefault(p => p.Id == id);
        if (producto is null)
        {
            return NotFound();
        }

        return Ok(new { producto.Id, producto.Nombre });
    }
    RETO 1.4 FIN */
}

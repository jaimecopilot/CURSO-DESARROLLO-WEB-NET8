using CursoWeb.Mvc.Models;
using Microsoft.AspNetCore.Mvc;

namespace CursoWeb.Mvc.Controllers;

public class ProductosController : Controller
{
    // La colección fija es compartida por Index, Detalle y Ficha.
    // Se mantiene el dominio de productos de M01, sin base de datos.
    private static IReadOnlyList<Producto> ObtenerProductosEjemplo() =>
        new List<Producto>
        {
            new() { Id = 1, Nombre = "Cuaderno", Precio = 4.50m },
            new() { Id = 2, Nombre = "Lápiz", Precio = 1.20m },
            new() { Id = 3, Nombre = "Carpeta", Precio = 3.75m }
        };

    [HttpGet]
    public IActionResult Index()
    {
        return View(ObtenerProductosEjemplo());
    }

    [HttpGet]
    public IActionResult Estado()
    {
        return Content("Catalogo MVC disponible", "text/plain");
    }

    [HttpGet]
    public IActionResult Detalle(int id)
    {
        if (id <= 0)
        {
            return BadRequest("El identificador debe ser mayor que cero.");
        }

        var producto = ObtenerProductosEjemplo().FirstOrDefault(p => p.Id == id);
        return producto is null ? NotFound() : View(producto);
    }

    [HttpGet("/catalogo/ficha/{id:int}")]
    public IActionResult Ficha(int id)
    {
        var producto = ObtenerProductosEjemplo().FirstOrDefault(p => p.Id == id);
        return producto is null ? NotFound() : View("Detalle", producto);
    }


    // P2.1: GET representa el formulario; POST recibe sus datos mediante model binding.
    [HttpGet]
    public IActionResult Crear() => View(new Producto());

    // PASO 2.1.3: comparar un formulario visible (GET) con su envío (POST).
    // Quita solo los delimitadores del bloque al completar P2.1.3;
    // conserva [ValidateAntiForgeryToken]. Los datos todavía no se guardan.
    /* PASO 2.1.3 INICIO
    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult Crear(Producto producto)
    {
        // Model binding crea y rellena Producto desde los campos Nombre y Precio.
        // Id sigue siendo 0, porque la vista no envía un identificador.
        // P2.3 añadirá un modelo de entrada específico y comprobará ModelState.
        // P2.4 introducirá la persistencia EF Core/LocalDB.
        return View("Confirmacion", producto);
    }
    PASO 2.1.3 FIN */

    // El reto 1.4 permanece identificado como variante histórica.
    // P1.5 trabaja específicamente con presentación Razor y vistas parciales.
    /* RETO 1.4 INICIO
    [HttpGet("/catalogo/resumen/{id:int}")]
    public IActionResult Resumen(int id)
    {
        var producto = ObtenerProductosEjemplo().FirstOrDefault(p => p.Id == id);
        return producto is null ? NotFound() : Ok(new { producto.Id, producto.Nombre });
    }
    RETO 1.4 FIN */
}

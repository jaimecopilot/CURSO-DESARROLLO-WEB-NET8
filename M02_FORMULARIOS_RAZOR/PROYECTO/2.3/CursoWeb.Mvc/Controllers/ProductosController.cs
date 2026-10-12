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


    // P2.3: las anotaciones viven en el modelo de entrada y ModelState comprueba el POST.
    [HttpGet]
    public IActionResult Crear() => View(new ProductoFormulario());

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult Crear(ProductoFormulario entrada)
    {
        // PASO 2.3.3: observar qué información contiene ModelState.
        // El model binder también puede registrar errores de conversión.
        // ACTIVAR (solo durante la investigación): el siguiente bucle opcional
        // registra las claves con problemas en la salida de depuración.
        /* PASO 2.3.3 INICIO
        foreach (var estado in ModelState.Where(x => x.Value?.Errors.Count > 0))
        {
            foreach (var error in estado.Value!.Errors)
                System.Diagnostics.Debug.WriteLine(
                    $"P2.3, campo {estado.Key}: {error.ErrorMessage}");
        }
        PASO 2.3.3 FIN */

        // RETO 2.3 (ACTIVAR): regla contextual ilustrativa sobre el nombre.
        // A diferencia de Required/Range, esta regla se añade desde la acción.
        /* RETO 2.3 INICIO
        if (entrada.Nombre?.StartsWith("TEST", StringComparison.OrdinalIgnoreCase) == true)
        {
            ModelState.AddModelError(nameof(entrada.Nombre),
                "El nombre no puede comenzar por TEST en este ejemplo.");
        }
        RETO 2.3 FIN */

        if (!ModelState.IsValid)
        {
            // PASO 2.3.4: devolver el mismo modelo de entrada permite
            // conservar datos introducidos y mostrar errores en Crear.cshtml.
            return View(entrada);
        }

        // Solo protege el estado previo a activar las reglas de P2.3.2:
        // un formulario incompleto no puede crear una entidad válida.
        // Una vez activadas [Required], estas entradas quedan rechazadas
        // por ModelState antes de alcanzar este punto.
        if (string.IsNullOrWhiteSpace(entrada.Nombre) || entrada.Precio is null)
            return BadRequest("Nombre y precio son obligatorios.");

        // P2.3: conversión explícita de DTO de entrada a modelo del catálogo.
        // No se guarda. En P2.4 el identificador lo generará la base de datos.
        var producto = new Producto
        {
            Id = 4,
            Nombre = entrada.Nombre,
            Precio = entrada.Precio.Value
        };
        return View("Confirmacion", producto);
    }

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

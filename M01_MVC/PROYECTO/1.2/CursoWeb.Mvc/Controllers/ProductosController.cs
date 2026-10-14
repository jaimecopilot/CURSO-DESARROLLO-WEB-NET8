using CursoWeb.Mvc.Models;
using Microsoft.AspNetCore.Mvc;

namespace CursoWeb.Mvc.Controllers;

public class ProductosController : Controller
{
    [HttpGet]
    public IActionResult Index()
    {
        // PASO 1.2.3: quitar los delimitadores del comentario de datos y
        // comentar el 'return View();' de la última línea de esta acción.
        /* PASO 1.2.3 INICIO
        var productos = new List<Producto>
        {
            new() { Id = 1, Nombre = "Cuaderno", Precio = 4.50m },
            // RETO 1.2 — Comentar la línea de Cuaderno y descomentar la siguiente:
            // new() { Id = 1, Nombre = "Bloc", Precio = 4.50m },
            new() { Id = 2, Nombre = "Lápiz", Precio = 1.20m },
            new() { Id = 3, Nombre = "Carpeta", Precio = 3.75m }
        };

        return View(productos);
        PASO 1.2.3 FIN */

        return View(); // PASO 1.2.3: comentar al activar el envío de datos.
    }
}

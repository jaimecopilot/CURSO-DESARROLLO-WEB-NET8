using Microsoft.AspNetCore.Mvc;

namespace CursoWeb.Mvc.Controllers;

public class HomeController : Controller
{
    // PASO 1.1.1 — El navegador envía GET / y la acción devuelve una vista HTML.
    [HttpGet]
    public IActionResult Index()
    {
        // PASO 1.1.4 — Descomentar solo la siguiente línea para observar
        // una cabecera de respuesta HTTP generada desde el controlador.
        // Response.Headers["X-Curso-Paso"] = "1.1.4";

        // RETO 1.1 — Cambiar una cabecera de respuesta sin tocar la vista.
        // Al activar el reto, eliminar // solo de la siguiente asignación.
        // Response.Headers["X-Curso-Reto"] = "HTTP-y-HTML";

        return View();
    }
}

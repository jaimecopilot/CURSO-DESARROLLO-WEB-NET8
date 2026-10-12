using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CursoWeb.Mvc.Pages;

// P2.5: comparación acotada con MVC, dentro del mismo host.
// Es una página demostrativa: NO altera el catálogo ni escribe en LocalDB.
public sealed class ComparacionModel : PageModel
{
    // PASO 2.5.3: a diferencia de Crear(ProductoFormulario entrada) en MVC,
    // la propiedad enlazada vive en el PageModel.
    // BindProperty recibe valores en POST; no implica SupportsGet=true.
    [BindProperty]
    // PASO 2.5.4 (ACTIVAR): descomenta ambas anotaciones y compara el resultado
    // de un nombre ausente, uno de un carácter y uno correcto.
    // [Required(ErrorMessage = "Introduce un nombre.")]
    // [StringLength(60, MinimumLength = 2,
    //     ErrorMessage = "El nombre debe tener entre 2 y 60 caracteres.")]
    public string? Nombre { get; set; }

    public string Mensaje { get; private set; } = string.Empty;

    // PASO 2.5.2: un GET ejecuta OnGet, no una acción de ProductosController.
    public void OnGet()
    {
        Mensaje = "OnGet prepara la página sin enviar un formulario.";
    }

    // PASO 2.5.3 (ACTIVAR): el POST de la misma URL ejecutará OnPost.
    /* PASO 2.5.3 INICIO
    public IActionResult OnPost()
    {
        // PASO 2.5.4: la comprobación da sentido a DataAnnotations.
        // Repetimos la página con errores y conservamos la entrada escrita.
        if (!ModelState.IsValid)
            return Page();

        // Antes de activar [Required], esta salvaguarda evita aceptar
        // el nombre vacío; no reemplaza la validación declarativa.
        if (string.IsNullOrWhiteSpace(Nombre))
        {
            ModelState.AddModelError(nameof(Nombre), "Introduce un nombre.");
            return Page();
        }

        Mensaje = $"OnPost ha recibido: {Nombre.Trim()}";
        return Page();
    }
    PASO 2.5.3 FIN */

    // RETO 2.5 (ACTIVAR): dos handlers POST para una sola Razor Page.
    // El alumno deberá crear en Comparacion.cshtml un botón
    // con asp-page-handler="Mayusculas", además del botón inicial.
    /* RETO 2.5 INICIO
    public IActionResult OnPostMayusculas()
    {
        if (!ModelState.IsValid || string.IsNullOrWhiteSpace(Nombre))
            return Page();

        Mensaje = $"Nombre en mayúsculas: {Nombre.Trim().ToUpperInvariant()}";
        return Page();
    }
    RETO 2.5 FIN */
}

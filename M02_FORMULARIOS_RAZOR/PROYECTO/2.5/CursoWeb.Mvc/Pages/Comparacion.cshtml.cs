using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CursoWeb.Mvc.Pages;

public sealed class ComparacionModel : PageModel
{
    [BindProperty]
    public string? Nombre { get; set; }
    public string Mensaje { get; private set; } = string.Empty;

    public void OnGet() => Mensaje = "OnGet prepara la página sin enviar un formulario.";

    public IActionResult OnPost()
    {
        if (string.IsNullOrWhiteSpace(Nombre))
        {
            ModelState.AddModelError(nameof(Nombre), "Introduce un nombre.");
            return Page();
        }

        Mensaje = $"OnPost ha recibido: {Nombre.Trim()}";
        return Page();
    }
}

using System.ComponentModel.DataAnnotations;

namespace CursoWeb.Mvc.Models;

/// <summary>
/// P2.3: contrato de entrada del formulario, separado de la entidad Producto.
/// No contiene Id: el navegador no debe determinar el identificador persistente.
/// </summary>
public sealed class ProductoFormulario
{
    // PASO 2.3.2 (ACTIVAR): descomenta las dos reglas del nombre.
    // Comprueba primero el envío con Nombre vacío y luego con un solo carácter.
    // [Required(ErrorMessage = "Indica el nombre.")]
    // [StringLength(60, MinimumLength = 2, ErrorMessage = "El nombre debe tener entre 2 y 60 caracteres.")]
    public string? Nombre { get; set; }

    // PASO 2.3.2 (ACTIVAR): descomenta ambas reglas del precio.
    // decimal? diferencia un campo ausente de un valor numérico real.
    // [Required(ErrorMessage = "Indica el precio.")]
    // [Range(typeof(decimal), "0.01", "9999.99", ErrorMessage = "El precio debe estar entre 0,01 y 9999,99.")]
    public decimal? Precio { get; set; }

    // APLICACION 2.3.6 (ESCRIBIR): prueba una etiqueta Display(Name = "Nombre del producto")
    // sobre Nombre y observa la salida del Label Tag Helper sin renombrar la propiedad.

    // RETO 2.3 (ACTIVAR y probar): más adelante, añade una regla opcional
    // para impedir nombres que incluyan solo espacios después de [Required].
    // Pista: [Required] ya rechaza cadenas compuestas exclusivamente por espacios;
    // estudia ese comportamiento antes de añadir una regla que duplique la protección.
}

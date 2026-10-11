namespace CursoWeb.Mvc.Models;

/// <summary>
/// PASO 1.2.2: el modelo representa datos del dominio sin conocer HTTP ni HTML.
/// No accede a base de datos; se usan datos fijos hasta M02.
/// </summary>
public sealed class Producto
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public decimal Precio { get; set; }
}

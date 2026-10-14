namespace CursoWeb.Mvc.Models;

/// <summary>
/// P2.4–P2.5: entidad persistida en LocalDB mediante EF Core.
/// La demostración de Razor Pages no modifica ni duplica este modelo.
/// </summary>
public sealed class Producto
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public decimal Precio { get; set; }
}

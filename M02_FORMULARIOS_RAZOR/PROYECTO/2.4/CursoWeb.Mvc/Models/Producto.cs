namespace CursoWeb.Mvc.Models;

/// <summary>
/// PASO 2.4.1: la misma entidad Producto presentada en M01 ahora es
/// persistida mediante AppDbContext, sin introducir HTML ni HTTP en el modelo.
/// Id es generado por SQL Server; el formulario de alta solo recibe Nombre y Precio.
/// </summary>
public sealed class Producto
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public decimal Precio { get; set; }
}

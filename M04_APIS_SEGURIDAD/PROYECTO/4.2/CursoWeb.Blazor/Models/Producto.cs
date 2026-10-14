namespace CursoWeb.Blazor.Models;
/// <summary>Producto de laboratorio: sin persistencia ni DTO remoto en M03.</summary>
public sealed record Producto(int Id, string Nombre, decimal Precio);

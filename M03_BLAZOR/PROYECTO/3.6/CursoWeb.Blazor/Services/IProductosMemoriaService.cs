using CursoWeb.Blazor.Models;
namespace CursoWeb.Blazor.Services;
public interface IProductosMemoriaService
{
    Task<IReadOnlyList<Producto>> ObtenerAsync();
}

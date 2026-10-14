using CursoWeb.Blazor.Models;
namespace CursoWeb.Blazor.Services;
public interface IProductosApiService
{
    Task<IReadOnlyList<ProductoDto>> ObtenerAsync();
    Task<ProductoDto> CrearAsync(CrearProductoDto solicitud);
}

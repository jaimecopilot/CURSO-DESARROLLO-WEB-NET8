using System.Net.Http.Json;
using CursoWeb.Blazor.Models;
namespace CursoWeb.Blazor.Services;
public sealed class ProductosApiService(HttpClient cliente) : IProductosApiService
{
    public async Task<IReadOnlyList<ProductoDto>> ObtenerAsync() =>
        await cliente.GetFromJsonAsync<List<ProductoDto>>("api/productos") ?? [];

    public async Task<ProductoDto> CrearAsync(CrearProductoDto solicitud)
    {
        using var respuesta = await cliente.PostAsJsonAsync("api/productos", solicitud);
        respuesta.EnsureSuccessStatusCode();
        return await respuesta.Content.ReadFromJsonAsync<ProductoDto>()
            ?? throw new InvalidOperationException("La API confirmó un alta sin devolver un producto.");
    }
}

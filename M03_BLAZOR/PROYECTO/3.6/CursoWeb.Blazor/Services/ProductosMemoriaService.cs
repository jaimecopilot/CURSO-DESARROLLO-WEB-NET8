using CursoWeb.Blazor.Models;
namespace CursoWeb.Blazor.Services;
/// <summary>Servicio de laboratorio sin HTTP, EF Core ni base externa.</summary>
public sealed class ProductosMemoriaService : IProductosMemoriaService
{
    public async Task<IReadOnlyList<Producto>> ObtenerAsync()
    {
        await Task.Delay(700);
        // RETO 3.6 (alternativa): sustituye el bloque return siguiente por:
        // return Array.Empty<Producto>();
        return
        [
            new Producto(1, "Cuaderno", 4.50m),
            new Producto(2, "Lápiz", 1.20m),
            new Producto(3, "Carpeta", 3.75m)
        ];
    }
    /* RETO INTEGRADOR 3.6.7 INICIO
    public async Task<IReadOnlyList<Producto>> ObtenerConErrorAsync(bool simularError)
    {
        await Task.Delay(350);
        if (simularError)
            throw new InvalidOperationException("Fallo controlado del servicio local.");
        return await ObtenerAsync();
    }
    RETO INTEGRADOR 3.6.7 FIN */

}

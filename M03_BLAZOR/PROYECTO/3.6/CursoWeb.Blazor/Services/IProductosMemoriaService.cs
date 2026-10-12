using CursoWeb.Blazor.Models;
namespace CursoWeb.Blazor.Services;
public interface IProductosMemoriaService
{
    Task<IReadOnlyList<Producto>> ObtenerAsync();
    /* RETO INTEGRADOR 3.6.7 INICIO
    Task<IReadOnlyList<Producto>> ObtenerConErrorAsync(bool simularError);
    RETO INTEGRADOR 3.6.7 FIN */
}

using CursoWeb.Blazor.Models;

namespace CursoWeb.Blazor.Services;

// RETO DOCENTE P4.2: implementación alternativa sin comunicación HTTP.
// Se mantiene sin registrar por defecto; la app sigue usando ProductosApiService.
// Para activarla se sustituye temporalmente el registro de IProductosApiService
// en Program.cs; NO se registran las dos implementaciones a la vez.
public sealed class ProductosApiSimuladoService : IProductosApiService
{
    private readonly List<ProductoDto> productos =
    [
        new ProductoDto(101, "Libreta simulada", 4.25m),
        new ProductoDto(102, "Bolígrafo simulado", 1.10m)
    ];

    private int siguienteId = 102;

    public Task<IReadOnlyList<ProductoDto>> ObtenerAsync()
    {
        IReadOnlyList<ProductoDto> resultado = productos.ToArray();
        return Task.FromResult(resultado);
    }

    public Task<ProductoDto> CrearAsync(CrearProductoDto solicitud)
    {
        if (string.IsNullOrWhiteSpace(solicitud.Nombre) || solicitud.Precio <= 0)
            throw new ArgumentException("Nombre y precio deben ser válidos.");

        var creado = new ProductoDto(
            Interlocked.Increment(ref siguienteId),
            solicitud.Nombre.Trim(),
            solicitud.Precio);
        productos.Add(creado);
        return Task.FromResult(creado);
    }
}

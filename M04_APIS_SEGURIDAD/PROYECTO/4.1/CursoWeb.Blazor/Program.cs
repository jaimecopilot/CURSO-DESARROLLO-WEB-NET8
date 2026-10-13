using CursoWeb.Blazor.Components;
using CursoWeb.Blazor.Services;

var builder = WebApplication.CreateBuilder(args);
// Servicios necesarios para componentes Razor y circuitos Interactive Server.
builder.Services.AddRazorComponents().AddInteractiveServerComponents();
// PASO 3.6.1: inyección por interfaz. No existe HttpClient ni API aún.
builder.Services.AddScoped<IProductosMemoriaService, ProductosMemoriaService>();
// P4.1: cliente HTTP con nombre, consumido desde la pantalla remota.
builder.Services.AddHttpClient("ProductosApi", cliente =>
{
    cliente.BaseAddress = new Uri(
        builder.Configuration["ProductosApi:BaseUrl"] ?? "http://localhost:5081/");
    cliente.Timeout = TimeSpan.FromSeconds(10);
});
var app = builder.Build();
if (!app.Environment.IsDevelopment()) app.UseExceptionHandler("/error");
app.UseStaticFiles();
app.UseAntiforgery();
// El modo Interactive Server necesita tanto servicios como endpoint.
app.MapRazorComponents<App>().AddInteractiveServerRenderMode();
app.Run();
public partial class Program { }

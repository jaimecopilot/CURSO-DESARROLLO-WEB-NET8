using CursoWeb.Blazor.Components;
using System.Security.Claims;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Antiforgery;

using CursoWeb.Blazor.Services;

var builder = WebApplication.CreateBuilder(args);
// Servicios necesarios para componentes Razor y circuitos Interactive Server.
builder.Services.AddRazorComponents().AddInteractiveServerComponents();
// PASO 3.6.1: inyección por interfaz. No existe HttpClient ni API aún.
builder.Services.AddScoped<IProductosMemoriaService, ProductosMemoriaService>();
// P4.1: cliente HTTP con nombre, consumido desde la pantalla remota.
// P4.2: cliente tipado; el componente solo conoce IProductosApiService.
builder.Services.AddHttpClient<IProductosApiService, ProductosApiService>(cliente =>
{
    cliente.BaseAddress = new Uri(
        builder.Configuration["ProductosApi:BaseUrl"] ?? "http://localhost:5081/");
    cliente.Timeout = TimeSpan.FromSeconds(10);
});
// AMPLIACIÓN P4.5: el JWT se consume desde el host Blazor, sin alterar CookiesDemo.
builder.Services.AddHttpClient("IdentityJwtApi", cliente =>
{
    cliente.BaseAddress = new Uri(
        builder.Configuration["IdentityJwtApi:BaseUrl"] ?? "http://localhost:5086/");
    cliente.Timeout = TimeSpan.FromSeconds(10);
});
builder.Services.AddAuthentication("CookiesDemo").AddCookie("CookiesDemo", options =>
{
    options.LoginPath = "/seguridad";
    options.Events.OnRedirectToLogin = c =>
    {
        if (c.Request.Path.StartsWithSegments("/demo/privado"))
        {
            c.Response.StatusCode = 401;
            return Task.CompletedTask;
        }
        c.Response.Redirect(c.RedirectUri);
        return Task.CompletedTask;
    };
});
builder.Services.AddAuthorization();
builder.Services.AddCascadingAuthenticationState();
var app = builder.Build();
if (!app.Environment.IsDevelopment()) app.UseExceptionHandler("/error");
app.UseStaticFiles();
app.UseAuthentication();
app.UseAuthorization();
app.UseAntiforgery();

if (app.Environment.IsDevelopment())
{
app.MapGet("/demo/privado", () => Results.Ok(new { mensaje = "Recurso protegido" }))
   .RequireAuthorization(p => p.RequireRole("Formador"));

// La identidad de prueba se establece con una respuesta HTTP convencional.
app.MapPost("/demo/entrar", async (HttpContext http, IAntiforgery antiforgery) =>
{
    if (!await antiforgery.IsRequestValidAsync(http))
        return Results.BadRequest("Token antifalsificación inválido.");
    var form = await http.Request.ReadFormAsync();
    if (form["codigo"] != "curso-demo-44")
        return Results.Redirect("/seguridad?error=1");
    var claims = new[] {
        new Claim(ClaimTypes.Name, "AlumnoDemo"),
        new Claim(ClaimTypes.Role, "Formador")
    };
    var identity = new ClaimsIdentity(claims, "CookiesDemo");
    await http.SignInAsync("CookiesDemo", new ClaimsPrincipal(identity));
    return Results.Redirect("/seguridad");
});
app.MapPost("/demo/salir", async (HttpContext http, IAntiforgery antiforgery) =>
{
    if (!await antiforgery.IsRequestValidAsync(http))
        return Results.BadRequest("Token antifalsificación inválido.");
    await http.SignOutAsync("CookiesDemo");
    return Results.Redirect("/seguridad");
});
}
// El modo Interactive Server necesita tanto servicios como endpoint.
app.MapRazorComponents<App>().AddInteractiveServerRenderMode();
app.Run();
public partial class Program { }

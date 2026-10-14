var builder = WebApplication.CreateBuilder(args);

// PASO 1.1.2 — Servicios necesarios para controladores MVC y vistas Razor.
builder.Services.AddControllersWithViews();
var app = builder.Build();

// PASO 1.3.3 completado: el valor procede de appsettings.json.
app.Logger.LogInformation("P1.3 configuracion: {Nombre}", app.Configuration["Curso:Nombre"]);

app.UseStaticFiles();
app.UseRouting();

// PASO 1.4.1: ruta convencional. "id?" indica que el segmento es opcional.
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();

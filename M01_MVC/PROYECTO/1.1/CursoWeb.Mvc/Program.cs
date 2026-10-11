var builder = WebApplication.CreateBuilder(args);

// PASO 1.1.2 — Servicios para controladores con vistas.
builder.Services.AddControllersWithViews();

var app = builder.Build();

// PASO 1.1.3 — Middleware de archivos estáticos y enrutamiento.
app.UseStaticFiles();
app.UseRouting();

// La ruta convencional permite que "/" corresponda a HomeController.Index.
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// Kestrel atiende las solicitudes; ASP.NET Core procesa cada petición HTTP.
app.Run();

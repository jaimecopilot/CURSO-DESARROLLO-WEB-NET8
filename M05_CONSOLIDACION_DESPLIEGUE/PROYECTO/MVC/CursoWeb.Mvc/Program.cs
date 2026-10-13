using CursoWeb.Mvc.Data;
using CursoWeb.Mvc.Models;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// PASO 2.5.1: coexistencia deliberada de MVC y Razor Pages en UN host.
// No creamos una segunda WebApplication ni una API auxiliar.
builder.Services.AddControllersWithViews();
builder.Services.AddRazorPages();

// Se conserva la misma base de P2.4, con una cadena configurable.
var cadena = builder.Configuration.GetConnectionString("Productos")
    ?? throw new InvalidOperationException("Falta ConnectionStrings:Productos.");
builder.Services.AddDbContext<AppDbContext>(options => options.UseSqlServer(cadena));

var app = builder.Build();

// P5.2: se mantiene el CRUD de P2.4/P2.5 con LocalDB en Windows.
// P5.5: la publicación Linux no dispone de LocalDB; el indicador SOLO
// permite ejecutar Home/Index, recursos estáticos y Productos/Estado.
// NO cambia el proveedor EF Core y NO crea una base ficticia.
var sinLocalDb = builder.Configuration.GetValue<bool>("Despliegue:SinLocalDb");
if (!sinLocalDb)
{
    // PASO 5.2: aplicación MVC publicada en Windows con LocalDB real.
    // P2.4: EnsureCreated es una simplificación exclusivamente docente.
    using var scope = app.Services.CreateScope();
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    if (db.Database.EnsureCreated())
    {
        db.Productos.AddRange(
            new Producto { Nombre = "Cuaderno", Precio = 4.50m },
            new Producto { Nombre = "Lápiz", Precio = 1.20m },
            new Producto { Nombre = "Carpeta", Precio = 3.75m });
        db.SaveChanges();
    }
}

// PASO 5.5: modo sin base para un contenedor Linux.
// Una ruta de CRUD no se presenta como funcional sin SQL Server.
// El filtro responde 503 en lugar de producir una excepción SQL no explicada.
if (sinLocalDb)
{
    app.Use(async (contexto, siguiente) =>
    {
        if (contexto.Request.Path.StartsWithSegments("/Productos")
            && !contexto.Request.Path.StartsWithSegments("/Productos/Estado"))
        {
            contexto.Response.StatusCode = StatusCodes.Status503ServiceUnavailable;
            await contexto.Response.WriteAsync(
                "CRUD no disponible: el ensayo de despliegue Linux no utiliza LocalDB.");
            return;
        }
        await siguiente(contexto);
    });
}

app.UseStaticFiles();
app.UseRouting();

// PASO 2.5.1: habilitar endpoints de Razor Pages y los controladores MVC.
app.MapRazorPages();
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();

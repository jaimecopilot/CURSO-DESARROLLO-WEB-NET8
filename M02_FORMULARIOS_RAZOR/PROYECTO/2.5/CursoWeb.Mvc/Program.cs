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

// P2.4: EnsureCreated para el laboratorio nuevo; no son migraciones.
// Solo insertar los tres productos iniciales cuando la base acaba de crearse.
using (var scope = app.Services.CreateScope())
{
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

app.UseStaticFiles();
app.UseRouting();

// PASO 2.5.1: habilitar endpoints de Razor Pages y los controladores MVC.
app.MapRazorPages();
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();

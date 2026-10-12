using CursoWeb.Mvc.Data;
using CursoWeb.Mvc.Models;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();

// PASO 2.4.1 — Elegimos SQL Server Express LocalDB a través de configuración.
// ConnectionStrings__Productos permite aislar una base de laboratorio
// sin cambiar archivos del alumno. LocalDB exige Windows y la instancia instalada.
var cadena = builder.Configuration.GetConnectionString("Productos")
    ?? throw new InvalidOperationException("Falta ConnectionStrings:Productos.");
builder.Services.AddDbContext<AppDbContext>(options => options.UseSqlServer(cadena));

var app = builder.Build();

// PASO 2.4.1 — Inicialización mínima para una práctica nueva.
// EnsureCreated crea el esquema solo si todavía NO existe esta base;
// no constituye un sistema de migraciones y NO debe combinarse con
// Database.Migrate() sobre la misma base. El alumno conoce EF Core;
// aquí interesa el resultado observado desde MVC.
//
// Se añaden tres productos únicamente al CREAR la base por primera vez.
// Si después el alumno elimina todos los productos, reiniciar NO los
// reinsertará: así la persistencia puede observarse también en el borrado.
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    bool baseCreada = db.Database.EnsureCreated();
    if (baseCreada)
    {
        db.Productos.AddRange(
            new Producto { Nombre = "Cuaderno", Precio = 4.50m },
            new Producto { Nombre = "Lápiz", Precio = 1.20m },
            new Producto { Nombre = "Carpeta", Precio = 3.75m });
        db.SaveChanges();
    }
}

// PASO 2.4.2 — MVC, enrutamiento y vistas son los mismos conceptos de M01.
app.UseStaticFiles();
app.UseRouting();
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();

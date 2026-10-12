using CursoWeb.Mvc.Data;
using CursoWeb.Mvc.Models;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Productos")));

var app = builder.Build();

// P2.4: inicialización didáctica reproducible, sin migraciones avanzadas.
// EnsureCreated no debe combinarse con migraciones sobre la misma base de datos.
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    var baseCreada = db.Database.EnsureCreated();
    if (baseCreada)
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
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();

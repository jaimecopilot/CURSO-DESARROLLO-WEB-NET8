using CursoWeb.Mvc.Models;
using Microsoft.EntityFrameworkCore;

namespace CursoWeb.Mvc.Data;

public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Producto> Productos => Set<Producto>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Producto>().Property(p => p.Precio).HasPrecision(10, 2);
    }
}

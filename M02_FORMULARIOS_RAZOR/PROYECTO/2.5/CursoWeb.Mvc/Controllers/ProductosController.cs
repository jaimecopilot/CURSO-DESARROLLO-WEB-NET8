using CursoWeb.Mvc.Data;
using CursoWeb.Mvc.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace CursoWeb.Mvc.Controllers;

public class ProductosController : Controller
{
    private readonly AppDbContext _db;
    public ProductosController(AppDbContext db) => _db = db;

    [HttpGet]
    public async Task<IActionResult> Index()
    {
        var productos = await _db.Productos.AsNoTracking().OrderBy(p => p.Id).ToListAsync();
        return View(productos);
    }

    [HttpGet]
    public IActionResult Estado() => Content("Catalogo MVC disponible", "text/plain");

    [HttpGet]
    public async Task<IActionResult> Detalle(int id)
    {
        if (id <= 0) return BadRequest("El identificador debe ser mayor que cero.");
        var producto = await _db.Productos.AsNoTracking().FirstOrDefaultAsync(p => p.Id == id);
        return producto is null ? NotFound() : View(producto);
    }

    [HttpGet("/catalogo/ficha/{id:int}")]
    public async Task<IActionResult> Ficha(int id)
    {
        var producto = await _db.Productos.AsNoTracking().FirstOrDefaultAsync(p => p.Id == id);
        return producto is null ? NotFound() : View("Detalle", producto);
    }

    // P2.4: formulario de creación con el mismo contrato validado en P2.3.
    [HttpGet]
    public IActionResult Crear() => View(new ProductoFormulario());

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Crear(ProductoFormulario entrada)
    {
        if (!ModelState.IsValid) return View(entrada);

        var producto = new Producto { Nombre = entrada.Nombre!, Precio = entrada.Precio!.Value };
        _db.Productos.Add(producto);
        await _db.SaveChangesAsync();
        return RedirectToAction(nameof(Detalle), new { id = producto.Id });
    }

    [HttpGet]
    public async Task<IActionResult> Editar(int id)
    {
        if (id <= 0) return BadRequest();
        var producto = await _db.Productos.AsNoTracking().FirstOrDefaultAsync(p => p.Id == id);
        if (producto is null) return NotFound();

        ViewData["ProductoId"] = producto.Id;
        return View(new ProductoFormulario { Nombre = producto.Nombre, Precio = producto.Precio });
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Editar(int id, ProductoFormulario entrada)
    {
        if (id <= 0) return BadRequest();
        var producto = await _db.Productos.FirstOrDefaultAsync(p => p.Id == id);
        if (producto is null) return NotFound();
        if (!ModelState.IsValid)
        {
            ViewData["ProductoId"] = id;
            return View(entrada);
        }

        producto.Nombre = entrada.Nombre!;
        producto.Precio = entrada.Precio!.Value;
        await _db.SaveChangesAsync();
        return RedirectToAction(nameof(Detalle), new { id });
    }

    [HttpGet]
    public async Task<IActionResult> Eliminar(int id)
    {
        if (id <= 0) return BadRequest();
        var producto = await _db.Productos.AsNoTracking().FirstOrDefaultAsync(p => p.Id == id);
        return producto is null ? NotFound() : View(producto);
    }

    [HttpPost, ActionName("Eliminar")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> EliminarConfirmado(int id)
    {
        if (id <= 0) return BadRequest();
        var producto = await _db.Productos.FirstOrDefaultAsync(p => p.Id == id);
        if (producto is null) return NotFound();

        _db.Productos.Remove(producto);
        await _db.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }

    // Reto opcional anterior, adaptado a persistencia: no es requisito para los pasos 2.1–2.5.
    /* RETO 1.4 INICIO
    [HttpGet("/catalogo/resumen/{id:int}")]
    public async Task<IActionResult> Resumen(int id)
    {
        var producto = await _db.Productos.AsNoTracking().FirstOrDefaultAsync(p => p.Id == id);
        return producto is null ? NotFound() : Ok(new { producto.Id, producto.Nombre });
    }
    RETO 1.4 FIN */
}

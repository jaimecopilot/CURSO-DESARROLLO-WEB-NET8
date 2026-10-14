using CursoWeb.Mvc.Data;
using CursoWeb.Mvc.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace CursoWeb.Mvc.Controllers;

/// <summary>
/// P2.4: la misma aplicación MVC utiliza ahora EF Core y LocalDB.
/// El itinerario avanza de consultas a Create, Edit y Delete.
///
/// El alumno activa los bloques 2.4.3, 2.4.4 y 2.4.5
/// SIN eliminar las comprobaciones de ModelState ni antiforgery.
/// Los ejercicios se basan en los cinco proyectos escalonados del curso.
/// </summary>
public class ProductosController : Controller
{
    private readonly AppDbContext _db;

    // PASO 2.4.1: DbContext se obtiene por inyección de dependencias;
    // no se crea manualmente una conexión SQL en cada acción.
    public ProductosController(AppDbContext db) => _db = db;

    // PASO 2.4.2: READ — consultar la base sin seguimiento para una lista.
    [HttpGet]
    public async Task<IActionResult> Index()
    {
        var productos = await _db.Productos
            .AsNoTracking()
            .OrderBy(p => p.Id)
            .ToListAsync();
        return View(productos);
    }

    [HttpGet]
    public IActionResult Estado() => Content("Catalogo MVC disponible", "text/plain");

    [HttpGet]
    public async Task<IActionResult> Detalle(int id)
    {
        if (id <= 0) return BadRequest("El identificador debe ser mayor que cero.");
        var producto = await _db.Productos.AsNoTracking()
            .FirstOrDefaultAsync(p => p.Id == id);
        return producto is null ? NotFound() : View(producto);
    }

    [HttpGet("/catalogo/ficha/{id:int}")]
    public async Task<IActionResult> Ficha(int id)
    {
        var producto = await _db.Productos.AsNoTracking()
            .FirstOrDefaultAsync(p => p.Id == id);
        return producto is null ? NotFound() : View("Detalle", producto);
    }

    // PASO 2.4.3: GET muestra el formulario de creación ya aprendido.
    [HttpGet]
    public IActionResult Crear() => View(new ProductoFormulario());

    // PASO 2.4.3 (ACTIVAR): descomentar el método POST completo.
    // Antes de activarlo, enviar el formulario no modifica la base de datos.
    /* PASO 2.4.3 INICIO
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Crear(ProductoFormulario entrada)
    {
        // Regla central aprendida en P2.3: no persistir entradas inválidas.
        if (!ModelState.IsValid)
            return View(entrada);

        // ProductoFormulario no tiene Id; el cliente no lo asigna.
        var producto = new Producto
        {
            Nombre = entrada.Nombre!,
            Precio = entrada.Precio!.Value
        };

        // Add marca una entidad nueva; SaveChangesAsync ejecuta el INSERT.
        _db.Productos.Add(producto);
        await _db.SaveChangesAsync();

        // El identificador ya ha sido asignado por SQL Server.
        // PRG evita reenvíos accidentales al recargar la página de detalle.
        return RedirectToAction(nameof(Detalle), new { id = producto.Id });
    }
    PASO 2.4.3 FIN */

    // PASO 2.4.4 (ACTIVAR): GET carga el producto desde LocalDB
    // y POST actualiza solamente las dos propiedades admitidas del formulario.
    /* PASO 2.4.4 INICIO
    [HttpGet]
    public async Task<IActionResult> Editar(int id)
    {
        if (id <= 0) return BadRequest();
        var producto = await _db.Productos.AsNoTracking()
            .FirstOrDefaultAsync(p => p.Id == id);
        if (producto is null) return NotFound();

        ViewData["ProductoId"] = producto.Id;
        return View(new ProductoFormulario
        {
            Nombre = producto.Nombre,
            Precio = producto.Precio
        });
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Editar(int id, ProductoFormulario entrada)
    {
        if (id <= 0) return BadRequest();
        // Leer la entidad existente, sin aceptar un objeto Producto
        // directamente desde el cliente: evita sobrepublicación de Id.
        var producto = await _db.Productos
            .FirstOrDefaultAsync(p => p.Id == id);
        if (producto is null) return NotFound();

        if (!ModelState.IsValid)
        {
            ViewData["ProductoId"] = id;
            return View(entrada);
        }

        producto.Nombre = entrada.Nombre!;
        producto.Precio = entrada.Precio!.Value;
        // EF Core realiza UPDATE sobre la entidad seguida por el contexto.
        await _db.SaveChangesAsync();
        return RedirectToAction(nameof(Detalle), new { id });
    }
    PASO 2.4.4 FIN */

    // PASO 2.4.5 (ACTIVAR): GET solo muestra una confirmación;
    // la eliminación de datos sucede EXCLUSIVAMENTE mediante POST protegido.
    /* PASO 2.4.5 INICIO
    [HttpGet]
    public async Task<IActionResult> Eliminar(int id)
    {
        if (id <= 0) return BadRequest();
        var producto = await _db.Productos.AsNoTracking()
            .FirstOrDefaultAsync(p => p.Id == id);
        return producto is null ? NotFound() : View(producto);
    }

    [HttpPost, ActionName("Eliminar")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> EliminarConfirmado(int id)
    {
        if (id <= 0) return BadRequest();
        var producto = await _db.Productos
            .FirstOrDefaultAsync(p => p.Id == id);
        if (producto is null) return NotFound();

        _db.Productos.Remove(producto);
        await _db.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }
    PASO 2.4.5 FIN */

    // RETO 2.4 (ACTIVAR): búsqueda de texto ejecutada en el servidor.
    // Usa SQL Server y no reutiliza datos fijos del módulo anterior.
    /* RETO 2.4 INICIO
    [HttpGet("/catalogo/buscar")]
    public async Task<IActionResult> Buscar(string? nombre)
    {
        var consulta = _db.Productos.AsNoTracking();
        if (!string.IsNullOrWhiteSpace(nombre))
            consulta = consulta.Where(p => p.Nombre.Contains(nombre));

        var encontrados = await consulta.OrderBy(p => p.Id).ToListAsync();
        return View("Index", encontrados);
    }
    RETO 2.4 FIN */

    // RETO opcional histórico de M01. No es necesario para P2.4.
    /* RETO 1.4 INICIO
    [HttpGet("/catalogo/resumen/{id:int}")]
    public async Task<IActionResult> Resumen(int id)
    {
        var producto = await _db.Productos.AsNoTracking()
            .FirstOrDefaultAsync(p => p.Id == id);
        return producto is null ? NotFound() : Ok(new { producto.Id, producto.Nombre });
    }
    RETO 1.4 FIN */
}

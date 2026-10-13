using System.Collections.Concurrent;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// P4.1: API de laboratorio disponible antes de comenzar el cliente.
// En P4.3 se explicará y modificará este mismo proyecto.
var productos = new ConcurrentDictionary<int, ProductoApi>();
productos[1] = new ProductoApi(1, "Cuaderno", 2.50m);
productos[2] = new ProductoApi(2, "Lápiz", 0.80m);
var siguienteId = 2;

// GET 200 + catálogo JSON.
app.MapGet("/api/productos", () =>
    Results.Ok(productos.Values.OrderBy(p => p.Id)));

// POST 400 para entradas inválidas; 201 y recurso creado si es válido.
app.MapPost("/api/productos", (CrearProductoApi entrada) =>
{
    if (string.IsNullOrWhiteSpace(entrada.Nombre) || entrada.Precio <= 0)
        return Results.BadRequest("Nombre y precio deben ser válidos.");

    var id = Interlocked.Increment(ref siguienteId);
    var creado = new ProductoApi(id, entrada.Nombre.Trim(), entrada.Precio);
    productos[id] = creado;
    return Results.Created($"/api/productos/{id}", creado);
});

// GET 404 sirve como ejemplo de respuesta no satisfactoria.
app.MapGet("/api/productos/{id:int}", (int id) =>
    productos.TryGetValue(id, out var producto)
        ? Results.Ok(producto)
        : Results.NotFound());


// PASO 4.3.3 INICIO — quitar los delimitadores de comentario para activar la ruta.
/*
app.MapGet("/api/productos/resumen", () =>
{
    var actuales = productos.Values.ToArray();
    return Results.Ok(new { cantidad = actuales.Length, precioTotal = actuales.Sum(p => p.Precio) });
});
*/
// PASO 4.3.3 FIN

// RETO 4.3.5 INICIO — variante alternativa; no activar junto al paso 4.3.3.
/*
app.MapGet("/api/productos/resumen", () =>
{
    var actuales = productos.Values.ToArray();
    return Results.Ok(new
    {
        cantidad = actuales.Length,
        precioTotal = actuales.Sum(p => p.Precio),
        hayProductos = actuales.Length > 0
    });
});
*/
// RETO 4.3.5 FIN

app.Run();

record ProductoApi(int Id, string Nombre, decimal Precio);
record CrearProductoApi(string Nombre, decimal Precio);

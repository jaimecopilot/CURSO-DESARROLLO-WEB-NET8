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
// AMPLIACIÓN AUTÓNOMA P5.1: variante aislada de diagnóstico.
// El archivo original permanece intacto; se copia temporalmente esta variante
// para estudiar tres respuestas distintas desde la MISMA API de productos.
// Elegir EscenarioCatalogo con Laboratorio__EscenarioCatalogo: normal, vacio, json-invalido.
var escenarioCatalogo = builder.Configuration["Laboratorio:EscenarioCatalogo"]
    ?.Trim().ToLowerInvariant() ?? "normal";

IResult ObtenerCatalogo()
{
    if (escenarioCatalogo == "vacio")
        return Results.Ok(Array.Empty<ProductoApi>());

    if (escenarioCatalogo == "json-invalido")
        return Results.Text("{\"productos\":[", "application/json");

    if (escenarioCatalogo == "no-encontrado")
        return Results.NotFound();

    if (escenarioCatalogo == "error-servidor")
        return Results.Problem("Fallo simulado del laboratorio.", statusCode: 500);

    // Modo normal: se conserva el contrato real de M04 y el resto de endpoints.
    return Results.Ok(productos.Values.OrderBy(p => p.Id));
}

app.MapGet("/api/productos", ObtenerCatalogo);

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

// RETO OPCIONAL 4.3.6 INICIO — búsqueda mediante parámetro de consulta.
// Activar únicamente después de comprobar los endpoints originales.
/*
app.MapGet("/api/productos/buscar", (string? nombre) =>
{
    if (string.IsNullOrWhiteSpace(nombre))
        return Results.BadRequest("Indica el nombre que deseas buscar.");

    var termino = nombre.Trim();
    var encontrados = productos.Values
        .Where(p => p.Nombre.Contains(termino, StringComparison.OrdinalIgnoreCase))
        .OrderBy(p => p.Id)
        .ToArray();
    return Results.Ok(encontrados);
});
*/
// RETO OPCIONAL 4.3.6 FIN


// AMPLIACIÓN AUTÓNOMA 4.3.7: probar actualización PUT y eliminación DELETE.
// No forma parte del recorrido obligatorio de seis horas.
// Para activarla, retirar solo los dos delimitadores /* */ del bloque.
// Registrar los tipos de entrada después de app.Run(), junto a los demás records.
/*
app.MapPut("/api/productos/{id:int}", (int id, ActualizarProductoApi entrada) =>
{
    if (string.IsNullOrWhiteSpace(entrada.Nombre) || entrada.Precio <= 0)
        return Results.BadRequest("Nombre y precio deben ser válidos.");

    // TryUpdate exige que el recurso conserve el valor que acabamos de observar.
    while (productos.TryGetValue(id, out var anterior))
    {
        var actualizado = new ProductoApi(id, entrada.Nombre.Trim(), entrada.Precio);
        if (productos.TryUpdate(id, actualizado, anterior))
            return Results.Ok(actualizado);
    }
    return Results.NotFound();
});

app.MapDelete("/api/productos/{id:int}", (int id) =>
    productos.TryRemove(id, out _)
        ? Results.NoContent()
        : Results.NotFound());
*/
// FIN DE AMPLIACIÓN 4.3.7


// AMPLIACIÓN AUTÓNOMA 4.3.8: POST con errores de validación estructurados.
// IMPORTANTE: comentar el MapPost original ANTES de activar esta alternativa.
// NO publicar dos MapPost del mismo método y ruta simultáneamente.
/*
app.MapPost("/api/productos", (CrearProductoApi entrada) =>
{
    var errores = new Dictionary<string, string[]>();
    if (string.IsNullOrWhiteSpace(entrada.Nombre))
        errores["nombre"] = ["El nombre es obligatorio."];
    if (entrada.Precio <= 0)
        errores["precio"] = ["El precio debe ser positivo."];

    if (errores.Count > 0)
        return Results.ValidationProblem(errores);

    var id = Interlocked.Increment(ref siguienteId);
    var creado = new ProductoApi(id, entrada.Nombre.Trim(), entrada.Precio);
    productos[id] = creado;
    return Results.Created($"/api/productos/{id}", creado);
});
*/
// FIN DE AMPLIACIÓN 4.3.8

app.Run();

record ProductoApi(int Id, string Nombre, decimal Precio);
record CrearProductoApi(string Nombre, decimal Precio);

// AMPLIACIÓN 4.3.7: activar este tipo junto a MapPut.
/* record ActualizarProductoApi(string Nombre, decimal Precio); */

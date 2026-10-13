# M04 — Prácticas: integración con APIs y seguridad básica

## Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8

**CURSO: Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8**

**TIPO: PRÁCTICAS**

**AUTOR: JAIME GALLO**


## P4.1 — Primer consumo HTTP desde Blazor

### Resultado que construiremos

Partimos de la aplicación `M03_BLAZOR/PROYECTO/3.6/CursoWeb.Blazor`. Crearemos **una copia independiente** en `M04_APIS_SEGURIDAD/PROYECTO/4.1/CursoWeb.Blazor`, sin editar los ejercicios originales de M03. La página `/productos` de M03 se conservará para comparar el catálogo local con el remoto. Incorporaremos una nueva página `/catalogo-remoto` que leerá productos desde una pequeña API; después permitirá crearlos y mostrará los errores sin cerrar la interfaz.

Los ejemplos razonados de HTTP, DTO, JSON y `HttpClient` están explicados en teoría 4.1. Esta práctica se centra en **construir y observar** el comportamiento.

### Paso 4.1.1. Preparar dos procesos independientes

**Proyecto API suministrado:** `M04_APIS_SEGURIDAD/PROYECTO/4.1/CursoWeb.ProductosApi`.

**Proyecto Blazor inicial:** copia de `M03_BLAZOR/PROYECTO/3.6/CursoWeb.Blazor`.

Abre dos terminales. En la primera, desde la carpeta de la API, ejecuta:

```powershell
dotnet run --urls http://localhost:5081
```

En un navegador, visita `http://localhost:5081/api/productos`. Debe aparecer un array JSON con Cuaderno y Lápiz. Visita `http://localhost:5081/api/productos/999` para provocar un **404**: observa que una API puede contestar correctamente a la petición HTTP e indicar al mismo tiempo que un recurso no existe.

**No avances** si el servidor no arranca: comprueba que tienes el SDK de .NET 8 y que el puerto 5081 no está ocupado. Este servidor no es una aplicación MVC ni la interfaz de Blazor.

### Paso 4.1.2. Crear los DTO en el cliente

En `CursoWeb.Blazor/Models/` añade `ProductoDto.cs`:

```csharp
namespace CursoWeb.Blazor.Models;
public sealed record ProductoDto(int Id, string Nombre, decimal Precio);
```

Añade `CrearProductoDto.cs`:

```csharp
namespace CursoWeb.Blazor.Models;
public sealed record CrearProductoDto(string Nombre, decimal Precio);
```

Compara estos contratos con el `Producto` de M03. No sustituyas el modelo de M03: sus tarjetas, filtros y edición local seguirán compilando con su propio tipo. Aquí usamos nuevos DTO para delimitar los datos que llegan por la red y los que enviamos al crear un producto.

### Paso 4.1.3. Configurar el cliente HTTP

En `CursoWeb.Blazor/Program.cs`, **mantén** el registro de componentes y el servicio `IProductosMemoriaService` de M03. Añade:

```csharp
builder.Services.AddHttpClient("ProductosApi", cliente =>
{
    cliente.BaseAddress = new Uri(
        builder.Configuration["ProductosApi:BaseUrl"]
        ?? "http://localhost:5081/");
    cliente.Timeout = TimeSpan.FromSeconds(10);
});
```

En el `appsettings.json` de Blazor declara una sección `ProductosApi` con `BaseUrl` igual a `http://localhost:5081/`. Si el archivo no existe en tu copia de M03, créalo con un objeto JSON que contenga esa sección.

El registro crea un cliente HTTP **con nombre**. No implementamos todavía la interfaz `IProductosApiService`; la construiremos en el ejercicio 4.2, cuando ya conozcamos el circuito que debe encapsular.

### Paso 4.1.4. Construir una pantalla de consulta remota

Crea `Components/Pages/CatalogoRemoto.razor`. Incluye una directiva `@page "/catalogo-remoto"`, el modo `InteractiveServer`, la inyección de `IHttpClientFactory` y una colección `List<ProductoDto>`.

En `OnInitializedAsync`, usa `Clientes.CreateClient("ProductosApi")` y `GetFromJsonAsync<List<ProductoDto>>("api/productos")`. Presenta tres estados separados: «Cargando…», listado y error.

El **código de referencia completo y razonado** está en teoría 4.1.6. Escribe esta primera versión siguiendo aquella explicación; comprueba que al navegar a `/catalogo-remoto` se ven los mismos dos productos que aparecen en el JSON del navegador.

Una observación importante: el GET se realiza desde el proceso de Blazor en Interactive Server, no desde el navegador; no necesitamos añadir una política CORS ficticia a la API de este laboratorio.

### Código íntegro de consulta remota (paso 4.1.4)

El siguiente archivo es el **estado de partida compilable** de `Components/Pages/CatalogoRemoto.razor` antes de añadir POST. Escríbelo después de registrar el cliente HTTP y los DTO; así puedes comprobar GET de forma independiente sin anticipar el resultado del paso siguiente.

```razor
@page "/catalogo-remoto"
@rendermode @(new InteractiveServerRenderMode(prerender: false))
@using System.Net.Http.Json
@inject IHttpClientFactory Clientes

<h1>Catálogo remoto</h1>
@if (cargando)
{
    <p role="status">Cargando catálogo...</p>
}
else if (error is not null)
{
    <p role="alert">@error</p>
}
else
{
    <ul>
        @foreach (var producto in productos)
        {
            <li>@producto.Nombre — @producto.Precio</li>
        }
    </ul>
}

@code {
    private List<ProductoDto> productos = [];
    private bool cargando = true;
    private string? error;

    protected override async Task OnInitializedAsync()
    {
        try
        {
            var cliente = Clientes.CreateClient("ProductosApi");
            productos = await cliente.GetFromJsonAsync<List<ProductoDto>>(
                "api/productos") ?? [];
        }
        catch (HttpRequestException)
        {
            error = "No se pudo obtener el catálogo remoto.";
        }
        catch (TaskCanceledException)
        {
            error = "La petición superó el tiempo disponible.";
        }
        catch (System.Text.Json.JsonException)
        {
            error = "La API no devolvió un catálogo JSON válido.";
        }
        finally
        {
            cargando = false;
        }
    }
}
```

La directiva `@rendermode` activa el circuito interactivo, aunque la consulta inicial se efectúe desde el servidor Blazor. Antes de pasar a POST, arranca primero la API y luego Blazor. Comprueba que aparecen Cuaderno y Lápiz. Detén la API y recarga la página: debe aparecer el aviso de fallo y nunca un catálogo vacío presentado como éxito.

### Paso 4.1.5. Añadir un formulario de alta

A la pantalla anterior incorpora dos campos, `Nombre` y `Precio`, y un botón «Crear en API». El botón llama a un método `async Task`:

```csharp
private async Task CrearAsync()
{
    if (string.IsNullOrWhiteSpace(nombreNuevo) || precioNuevo <= 0)
    {
        mensaje = "Indica un nombre y un precio mayor que cero.";
        return;
    }

    enviando = true;
    mensaje = null;
    try
    {
        var cliente = Clientes.CreateClient("ProductosApi");
        using var respuesta = await cliente.PostAsJsonAsync(
            "api/productos",
            new CrearProductoDto(nombreNuevo.Trim(), precioNuevo));
        respuesta.EnsureSuccessStatusCode();

        var creado = await respuesta.Content
            .ReadFromJsonAsync<ProductoDto>();
        if (creado is null)
            throw new InvalidOperationException("Alta sin producto de respuesta.");

        productos.Add(creado);
        nombreNuevo = string.Empty;
        precioNuevo = 0;
        mensaje = $"Producto creado: {creado.Nombre} (id {creado.Id}).";
    }
    catch (HttpRequestException)
    {
        mensaje = "La API no pudo completar el alta.";
    }
    catch (TaskCanceledException)
    {
        mensaje = "Se agotó el tiempo al crear el producto.";
    }
    catch (System.Text.Json.JsonException)
    {
        mensaje = "La respuesta de alta no contiene JSON válido.";
    }
    catch (InvalidOperationException)
    {
        mensaje = "La respuesta de alta está incompleta.";
    }
    finally
    {
        enviando = false;
    }
}
```

La página necesita los campos `private string nombreNuevo = string.Empty;`, `private decimal precioNuevo;`, `private bool enviando;` y `private string? mensaje;`. Deshabilita el botón mientras `enviando` es verdadero. Usa `@bind` en los inputs y `@onclick="CrearAsync"` en el botón. Añade `@using System.Net.Http.Json` si no existe una importación global equivalente.

Crea «Regla» con precio 1,75. Debe aparecer una línea nueva con el identificador asignado por la API. Recarga la página: el producto sigue presente mientras la API continúa ejecutándose. Reinicia la API: la colección vuelve a sus datos iniciales, porque todavía no existe persistencia.

### Paso 4.1.6. Forzar tres tipos distintos de fallo

**Datos rechazados:** envía directamente a la API, desde la terminal, una petición POST con precio cero:

```powershell
curl.exe -i -X POST http://localhost:5081/api/productos -H "Content-Type: application/json" -d "{\"nombre\":\"Regla\",\"precio\":0}"
```

Si tu terminal altera las comillas de JSON, usa un archivo `producto-invalido.json` y `--data-binary "@producto-invalido.json"`. Debes observar **400 Bad Request**. La interfaz de Blazor, por su parte, impide el envío de valores inválidos mediante una comprobación previa.

**Ruta inexistente:** solicita `http://localhost:5081/api/productos/999`; observa **404 Not Found**.

**Servicio no disponible:** detén el proceso de la API, recarga `/catalogo-remoto` y observa el aviso de comunicación. Vuelve a iniciar la API y recarga la página. No interpretes una colección vacía como señal suficiente de error: tenemos estados distintos para éxito y fallo.

### Paso 4.1.7. Reto: distinguir el rechazo HTTP del fallo de red

La versión de consulta basada en `GetFromJsonAsync` ya detecta excepciones, pero no presenta el código HTTP de un fallo. Sustituye **solo la lectura GET** por un `GetAsync` explícito:

```csharp
using var respuesta = await cliente.GetAsync("api/productos");
if (!respuesta.IsSuccessStatusCode)
{
    error = $"La API respondió {(int)respuesta.StatusCode}.";
    return;
}
productos = await respuesta.Content
    .ReadFromJsonAsync<List<ProductoDto>>() ?? [];
```

Mantén el `finally` que desactiva el indicador de carga. Puedes cambiar temporalmente la ruta por `api/no-existe` y comparar «La API respondió 404» con el error de conexión que aparece al apagar el servidor. Restablece la ruta real al terminar el reto.

### Resultado y continuidad

Al finalizar, `/productos` conserva el aprendizaje local de M03 y `/catalogo-remoto` demuestra GET, POST y errores HTTP entre dos procesos. La API auxiliar utilizada aquí se estudiará en detalle en P4.3; en **P4.2** extraeremos las llamadas del componente a `IProductosApiService`.

## P4.2 — Extraer las llamadas HTTP a un servicio inyectable

### Punto de partida

Trabaja sobre una copia del estado `PROYECTO/4.1/CursoWeb.Blazor`. No sobrescribas el proyecto de 4.1 ni `M03_BLAZOR`. Conserva en ejecución la **misma API auxiliar** `PROYECTO/4.1/CursoWeb.ProductosApi` en `http://localhost:5081`. En `/catalogo-remoto` deben verse dos productos antes de empezar.

**Resultado esperado:** el componente deja de conocer `HttpClient` y las rutas HTTP; un servicio tipado ejecuta la comunicación. El comportamiento visible de la página debe seguir siendo el mismo.

### Paso 4.2.1. Declarar una interfaz explícita

Crea `Services/IProductosApiService.cs`:

```csharp
using CursoWeb.Blazor.Models;

namespace CursoWeb.Blazor.Services;

public interface IProductosApiService
{
    Task<IReadOnlyList<ProductoDto>> ObtenerAsync();
    Task<ProductoDto> CrearAsync(CrearProductoDto solicitud);
}
```

Separa en tu explicación oral qué recibe la pantalla (`IReadOnlyList<ProductoDto>`) de cómo se obtuvo (desconocido para la interfaz). Compara esta interfaz con `IProductosMemoriaService` de M03; **no borres** ese servicio antiguo porque sigue siendo parte del aprendizaje previo.

### Paso 4.2.2. Implementar la comunicación en una clase

Crea `Services/ProductosApiService.cs`, usando la clase completa expuesta y explicada en teoría 4.2.2. Debe implementar **ambos métodos**. Al terminar, comprueba que en esa clase aparecen `GetFromJsonAsync`, `PostAsJsonAsync` y `EnsureSuccessStatusCode`.

No envíes desde el cliente un ID inventado en `CrearProductoDto`: la API asignará el valor y devolverá `ProductoDto`.

### Código íntegro del servicio HTTP (paso 4.2.2)

Crea este archivo en `Services/ProductosApiService.cs`, además de la interfaz del paso 4.2.1. Este es el código que compilará al resolver la dependencia `IProductosApiService` mediante DI:

```csharp
using System.Net.Http.Json;
using CursoWeb.Blazor.Models;

namespace CursoWeb.Blazor.Services;

public sealed class ProductosApiService(HttpClient cliente) : IProductosApiService
{
    public async Task<IReadOnlyList<ProductoDto>> ObtenerAsync()
    {
        return await cliente.GetFromJsonAsync<List<ProductoDto>>(
            "api/productos") ?? [];
    }

    public async Task<ProductoDto> CrearAsync(CrearProductoDto solicitud)
    {
        using var respuesta = await cliente.PostAsJsonAsync(
            "api/productos", solicitud);
        respuesta.EnsureSuccessStatusCode();

        return await respuesta.Content.ReadFromJsonAsync<ProductoDto>()
               ?? throw new InvalidOperationException(
                   "La API confirmó un alta sin devolver un producto.");
    }
}
```

**Comprobación intermedia:** antes de modificar la página, registra el servicio como se muestra en el paso siguiente y compila. La clase depende de que existan `IProductosApiService`, `ProductoDto` y `CrearProductoDto`. Si falta un `using` o el namespace no coincide, el compilador lo indicará antes de que intervenga HTTP.

### Paso 4.2.3. Registrar el typed client

En `Program.cs` elimina el registro de cliente con nombre `AddHttpClient("ProductosApi", ...)` que se utilizó en 4.1 y coloca el registro tipado `AddHttpClient<IProductosApiService, ProductosApiService>(...)` de teoría 4.2.3.

**Mantén** los registros de componentes de Blazor y `IProductosMemoriaService`. Conserva la clave de configuración `ProductosApi:BaseUrl` y el puerto 5081. Si quitas accidentalmente el servicio de memoria, puedes provocar una regresión en la página `/productos`.

### Paso 4.2.4. Sustituir el acceso HTTP de la página

En `Components/Pages/CatalogoRemoto.razor` cambia:

```razor
@inject IHttpClientFactory Clientes
```

por:

```razor
@inject IProductosApiService CatalogoApi
```

En `OnInitializedAsync`, sustituye la creación del cliente y la llamada `GetFromJsonAsync` por:

```csharp
productos = (await CatalogoApi.ObtenerAsync()).ToList();
```

En `CrearAsync`, sustituye la construcción de `HttpClient`, `PostAsJsonAsync` y `ReadFromJsonAsync` por:

```csharp
var creado = await CatalogoApi.CrearAsync(
    new CrearProductoDto(nombreNuevo.Trim(), precioNuevo));
```

**No cambies** el marcado HTML, la validación preliminar ni los mensajes de error. La finalidad de este punto es aprender a cambiar responsabilidades internas **sin cambiar la experiencia del usuario**.

### Paso 4.2.5. Comparar el comportamiento

Ejecuta la API y Blazor por separado. Desde el navegador abre `/catalogo-remoto`, comprueba los dos productos y crea «Regla» con precio 1,75. Refresca la página y verifica que la nueva entrada sigue en memoria de la API. Después detén la API y recarga: la pantalla debe mostrar el aviso de fallo, en lugar de afirmar que el catálogo está vacío. Reinicia la API al acabar.

Abre también `/productos` y comprueba que continúa siendo accesible. Si algo falla, investiga primero el registro de servicios, el puerto de la API y la clave `ProductosApi:BaseUrl`.

### Paso 4.2.6. Reto: comprobar que el componente ignora la ruta

Localiza todos los lugares de `CatalogoRemoto.razor` donde aparezca la cadena `"api/productos"`. **El resultado debe ser ninguno**. Localiza ahora esa ruta en `ProductosApiService.cs`: aquí sí debe aparecer, porque es un detalle de comunicación.

Como variante de exploración, cambia solo esa ruta por `"api/no-existe"`, ejecuta de nuevo y observa el aviso de error HTTP. Restablece después `"api/productos"`.

### Consolidación

El resultado de P4.2 no es una pantalla nueva, sino una frontera de responsabilidades: el componente presenta y gestiona el estado; `IProductosApiService` expresa las operaciones que necesita; `ProductosApiService` resuelve el transporte; y la API mantiene las reglas del servidor. En P4.3 estudiaremos y modificaremos esta última.

## P4.3 — Abrir la API existente y añadir un resumen sin romper Blazor

### Objetivo y material inicial

Partimos de **la API entregada en 4.1**, \`PROYECTO/4.1/CursoWeb.ProductosApi\`, y hacemos una copia acumulativa en \`PROYECTO/4.3/CursoWeb.ProductosApi\`. Para la interfaz usamos el proyecto refactorizado de 4.2; lo conservaremos en \`PROYECTO/4.3/CursoWeb.Blazor\`. No se crea una API alternativa sin relación con lo aprendido.

Al terminar, la nueva API seguirá ofreciendo GET, POST, respuestas 400/404 y una operación adicional \`GET /api/productos/resumen\`. El cliente Blazor seguirá consultando \`/api/productos\` sin cambiar su código HTTP.

### Paso 4.3.1. Identificar las piezas del proceso servidor

Abre \`CursoWeb.ProductosApi/Program.cs\` e identifica el \`WebApplication.CreateBuilder\`, \`Build\`, \`MapGet\`, \`MapPost\` y \`Run\`. Localiza los registros Cuaderno y Lápiz que se cargan al arrancar, y observa que se guardan en \`ConcurrentDictionary<int, ProductoApi>\`, no en una base de datos.

Ejecuta la API:

\`\`\`powershell
dotnet run --project M04_APIS_SEGURIDAD/PROYECTO/4.3/CursoWeb.ProductosApi/CursoWeb.ProductosApi.csproj --urls http://localhost:5081
\`\`\`

Si otra instancia usa 5081, detén esa instancia antes de iniciar la de 4.3. Abre \`http://localhost:5081/api/productos\` y verifica que aparecen dos productos.

### Paso 4.3.2. Seguir un GET y un POST

En el código, localiza \`Results.Ok\` y \`Results.Created\`. Consulta \`/api/productos/999\` para obtener 404. Envía un POST con nombre «Regla» y precio 1,75 usando un cliente HTTP (por ejemplo, \`curl.exe\` con un fichero JSON para evitar problemas de comillas):

\`\`\`json
{ "nombre": "Regla", "precio": 1.75 }
\`\`\`

Observa la respuesta 201, el identificador asignado y la cabecera \`Location\`. Envía ahora un nombre vacío y precio cero para obtener 400. Comprueba que un producto inválido no aparece en la lista GET.

### Taller de construcción autónoma: sustituir la API entregada

En 4.1 y 4.2 era indispensable disponer de una API operativa mientras aprendíamos a consumirla. Ahora podemos construir una nueva implementación desde cero y poner a prueba que **responde exactamente al mismo contrato HTTP**.

**Preparación del escenario.** Mantén el proyecto suministrado como referencia, sin editarlo. En otra carpeta de trabajo —por ejemplo, \`PROYECTO/4.3/CursoWeb.ProductosApi.Construida\`— crea una aplicación vacía con:

\`\`\`powershell
dotnet new web -n CursoWeb.ProductosApi -f net8.0
\`\`\`

Detén la API de 4.1 antes de arrancar la nueva en el puerto 5081. Esta secuencia debe realizarse por etapas; después de cada una, compila y observa la respuesta para localizar los errores en el momento en que se introducen.

**Etapa 1 — arranque y primer endpoint.** Abre \`Program.cs\` y escribe:

\`\`\`csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => Results.Ok("API de Productos disponible"));

app.Run();
\`\`\`

Ejecuta \`dotnet run --urls http://localhost:5081\` desde el directorio del proyecto. Al solicitar \`http://localhost:5081/\` se debe recibir 200 y un mensaje. Una respuesta positiva indica que hay un host operativo, pero todavía no que exista un catálogo de productos.

**Etapa 2 — modelos y listado.** Sustituye \`Program.cs\` por:

\`\`\`csharp
using System.Collections.Concurrent;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var productos = new ConcurrentDictionary<int, ProductoApi>();
productos[1] = new ProductoApi(1, "Cuaderno", 2.50m);
productos[2] = new ProductoApi(2, "Lápiz", 0.80m);

app.MapGet("/", () => Results.Ok("API de Productos disponible"));
app.MapGet("/api/productos", () =>
    Results.Ok(productos.Values.OrderBy(p => p.Id)));

app.Run();

record ProductoApi(int Id, string Nombre, decimal Precio);
\`\`\`

Arranca de nuevo. El navegador debe mostrar dos objetos en un arreglo JSON cuando consultas \`/api/productos\`. Comprueba además que \`/api/productos/1\` todavía **no** devuelve un detalle válido: esa ruta aún no existe y esa ausencia es esperable antes de la etapa siguiente.

**Etapa 3 — consulta individual.** Antes de \`app.Run()\`, añade:

\`\`\`csharp
app.MapGet("/api/productos/{id:int}", (int id) =>
    productos.TryGetValue(id, out var producto)
        ? Results.Ok(producto)
        : Results.NotFound());
\`\`\`

Reinicia y verifica \`/api/productos/1\`: debe aparecer Cuaderno. Después solicita \`/api/productos/999\` y observa 404. No confundas este resultado con un puerto cerrado: el servidor está respondiendo correctamente, pero el recurso no existe.

**Etapa 4 — creación y validación.** Antes de \`app.Run()\`, añade:

\`\`\`csharp
var siguienteId = 2;

app.MapPost("/api/productos", (CrearProductoApi entrada) =>
{
    if (string.IsNullOrWhiteSpace(entrada.Nombre) || entrada.Precio <= 0)
        return Results.BadRequest("Nombre y precio deben ser válidos.");

    var id = Interlocked.Increment(ref siguienteId);
    var creado = new ProductoApi(id, entrada.Nombre.Trim(), entrada.Precio);
    productos[id] = creado;
    return Results.Created($"/api/productos/{id}", creado);
});
\`\`\`

Al final del archivo, junto a \`ProductoApi\`, añade:

\`\`\`csharp
record CrearProductoApi(string Nombre, decimal Precio);
\`\`\`

Prepara un archivo \`nuevo-producto.json\`:

\`\`\`json
{
  "nombre": "Regla",
  "precio": 1.75
}
\`\`\`

Con la API iniciada ejecuta, desde una terminal donde el fichero sea accesible:

\`\`\`powershell
curl.exe -i -X POST http://localhost:5081/api/productos -H "Content-Type: application/json" --data-binary "@nuevo-producto.json"
\`\`\`

Debe obtenerse **201 Created**, un producto nuevo con ID asignado por el servidor y una cabecera \`Location\`. Repite GET del listado y comprueba que existe Regla. Cambia el precio del JSON a 0 y repite: debe devolverse **400 Bad Request**, sin añadir otro producto. Si vuelves a introducir datos válidos, el contador puede seguir creciendo; es normal mientras no se reinicie el proceso.

**Etapa 5 — integración con el cliente Blazor que ya construimos.** Mantén la API recién creada en 5081 y abre Blazor desde \`PROYECTO/4.2/CursoWeb.Blazor\`. Consulta \`/catalogo-remoto\`. Si el contrato se ha conservado, verás los productos sin reescribir \`CatalogoRemoto.razor\` ni \`ProductosApiService.cs\`. Envía un nuevo producto desde la interfaz y comprueba el 201 indirectamente observando que se añade al listado.

Para diagnosticar un fallo, recorre en orden estas preguntas: ¿responde la API directamente?, ¿coinciden la ruta y el puerto?, ¿el JSON conserva \`id\`, \`nombre\` y \`precio\`?, ¿la clase \`CrearProductoApi\` admite los datos enviados?, ¿la página recibe un error HTTP o un error de red?

**Etapa 6 — repetición controlada y persistencia.** Detén y vuelve a iniciar el servidor. La lista debe regresar a Cuaderno y Lápiz porque el almacenamiento era de memoria. Este comportamiento no supone un defecto oculto: es un límite expresamente elegido para concentrarse en comunicación HTTP. No incorpores EF Core en esta etapa.

**Reto de sustitución del servidor.** Sin modificar el cliente, cambia temporalmente la cadena \`"Cuaderno"\` de la API construida por \`"Cuaderno A4"\`, reinicia y consulta Blazor. El nombre debe reflejar el cambio de servidor. Después restaura el dato de referencia y explica por qué la interfaz no necesitó recompilarse para recibir una respuesta JSON con el mismo contrato.

### Paso 4.3.3. Añadir una ruta de resumen

Antes del \`app.Run();\` añade este endpoint, cuya finalidad y contrato se explican en teoría 4.3.4:

\`\`\`csharp
// PASO 4.3.3 — activar al llegar aquí.
app.MapGet("/api/productos/resumen", () =>
{
    var actuales = productos.Values.ToArray();
    return Results.Ok(new
    {
        cantidad = actuales.Length,
        precioTotal = actuales.Sum(p => p.Precio)
    });
});
\`\`\`

El proyecto de laboratorio incluye el bloque **comentado** con marca \`PASO 4.3.3\`, para que puedas descomentarlo antes de ejecutarlo. Tras arrancar desde datos iniciales, \`GET /api/productos/resumen\` debe devolver \`cantidad\` 2 y \`precioTotal\` 3,30. Crea Regla y vuelve a consultar: los valores deberían ser 3 y 5,05. Si antes añadiste otros productos, reinicia el proceso para reproducir el estado de partida.

### Paso 4.3.4. Conectar la API ampliada con la pantalla del paso 4.2

Ejecuta \`CursoWeb.Blazor\` del punto 4.3 en otro puerto; la API permanece en 5081. Abre \`/catalogo-remoto\` y crea un producto. Comprueba que sigue apareciendo en el listado y que \`/api/productos/resumen\` refleja la creación **si has activado** el bloque del paso anterior. Observa que no hemos tenido que editar el \`IProductosApiService\`: el nuevo endpoint es una capacidad del servidor que no interfiere con el contrato utilizado por el cliente.

### Paso 4.3.5. Reto: un segundo criterio de resumen

A partir del endpoint de resumen, añade la propiedad \`hayProductos\` con valor booleano:

\`\`\`csharp
hayProductos = actuales.Length > 0
\`\`\`

La variante está incluida como bloque \`RETO 4.3.5\` comentado en el proyecto. Para activarla, reemplaza el bloque de \`PASO 4.3.3\` por el bloque completo del reto: **no actives ambas versiones simultáneamente**, porque intentarían asignar la misma ruta GET.

Haz otra llamada a \`/api/productos/resumen\` y comprueba que aparece \`"hayProductos": true\`. Explica por qué es un campo de un JSON distinto de \`ProductoDto\` y por qué el cliente de 4.2 no necesita cambios.

### Resultado del ejercicio

Ahora puedes recorrer una petición desde Blazor hasta la API y viceversa, interpretar sus códigos HTTP y añadir un endpoint nuevo sin modificar rutas existentes. La API continúa funcionando en memoria: al reiniciarla se pierde todo lo creado durante la ejecución.

## P4.4 — Demostración local de seguridad

### Objetivo

Crea una copia acumulativa de `PROYECTO/4.3/CursoWeb.Blazor` en `PROYECTO/4.4/CursoWeb.Blazor`. Mantén intactas las pantallas de productos y la API auxiliar. La autenticación de demostración **no** constituye Identity ni es apta para producción.

### Paso 4.4.1. Configurar el host

En `Program.cs` registra autenticación mediante el esquema `CookiesDemo`, autorización y el estado de autenticación para componentes. Añade los middleware `UseAuthentication()` y `UseAuthorization()`; conserva `UseAntiforgery()`. El código completo está explicado en teoría 4.4.1 y está materializado en el proyecto acumulativo 4.4.

### Paso 4.4.2. Identificar la sesión

Abre `Components/Pages/Seguridad.razor`. Examina el `AuthorizeView` que presenta dos resultados alternativos: usuario autenticado o anónimo. La variante `Roles="Formador"` permite observar cómo intervienen los claims.

### Paso 4.4.3. Hacer una entrada y salida HTTP

En el formulario POST `/demo/entrar`, utiliza el código local **`curso-demo-44`**. El servidor compara ese código, crea un principal de ejemplo con nombre `AlumnoDemo` y rol `Formador`, y envía una cookie. El token `<AntiforgeryToken />` protege el envío del formulario frente a falsificaciones. Para cerrar la sesión se emplea POST `/demo/salir`, no un enlace GET.


### Código del laboratorio: el alumno puede reconstruir el acceso

La demostración no debe limitarse a observar una pantalla preconfigurada. Vamos a localizar y activar los elementos en un orden que permita comprender las dependencias.

Primero, en `Program.cs`, añade los espacios de nombres:

```csharp
using System.Security.Claims;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Antiforgery;
```

Registra los servicios antes de `builder.Build()`:

```csharp
builder.Services.AddAuthentication("CookiesDemo").AddCookie("CookiesDemo", options =>
{
    options.LoginPath = "/seguridad";
    options.Events.OnRedirectToLogin = contexto =>
    {
        if (contexto.Request.Path.StartsWithSegments("/demo/privado"))
        {
            contexto.Response.StatusCode = 401;
            return Task.CompletedTask;
        }
        contexto.Response.Redirect(contexto.RedirectUri);
        return Task.CompletedTask;
    };
});
builder.Services.AddAuthorization();
builder.Services.AddCascadingAuthenticationState();
```

Coloca `app.UseAuthentication()`, `app.UseAuthorization()` y `app.UseAntiforgery()` antes de mapear los endpoints protegidos.

Después incorpora las rutas de demostración **solo en Development**:

```csharp
if (app.Environment.IsDevelopment())
{
    app.MapGet("/demo/privado",
        () => Results.Ok(new { mensaje = "Recurso protegido" }))
        .RequireAuthorization(p => p.RequireRole("Formador"));

    app.MapPost("/demo/entrar",
        async (HttpContext http, IAntiforgery antiforgery) =>
    {
        if (!await antiforgery.IsRequestValidAsync(http))
            return Results.BadRequest("Token antifalsificación inválido.");

        var formulario = await http.Request.ReadFormAsync();
        if (formulario["codigo"] != "curso-demo-44")
            return Results.Redirect("/seguridad?error=1");

        var claims = new[]
        {
            new Claim(ClaimTypes.Name, "AlumnoDemo"),
            new Claim(ClaimTypes.Role, "Formador")
        };
        var identidad = new ClaimsIdentity(claims, "CookiesDemo");
        await http.SignInAsync(
            "CookiesDemo", new ClaimsPrincipal(identidad));
        return Results.Redirect("/seguridad");
    });

    app.MapPost("/demo/salir",
        async (HttpContext http, IAntiforgery antiforgery) =>
    {
        if (!await antiforgery.IsRequestValidAsync(http))
            return Results.BadRequest("Token antifalsificación inválido.");

        await http.SignOutAsync("CookiesDemo");
        return Results.Redirect("/seguridad");
    });
}
```

Un POST sin token debe devolverse como 400. Esto es intencional: no se debe desactivar la verificación simplemente para simplificar el ejercicio.

Finalmente, crea `Components/Pages/Seguridad.razor`:

```razor
@page "/seguridad"
@rendermode @(new InteractiveServerRenderMode(prerender: false))
@using Microsoft.AspNetCore.Components.Authorization

<h1>Demostración de seguridad</h1>
<AuthorizeView>
    <Authorized>
        <p>Usuario: @context.User.Identity?.Name</p>
        <AuthorizeView Roles="Formador" Context="rolContexto">
            <Authorized>
                <p>Rol Formador reconocido</p>
            </Authorized>
        </AuthorizeView>
        <form method="post" action="/demo/salir" data-enhance="false">
            <AntiforgeryToken />
            <button type="submit">Cerrar sesión</button>
        </form>
    </Authorized>
    <NotAuthorized>
        <p>Usuario anónimo</p>
        <form method="post" action="/demo/entrar" data-enhance="false">
            <AntiforgeryToken />
            <label>Código:
                <input name="codigo" type="password" />
            </label>
            <button type="submit">Acceder</button>
        </form>
    </NotAuthorized>
</AuthorizeView>
```

Los dos `AuthorizeView` están anidados: el contexto del componente interior tiene nombre explícito para evitar una colisión de parámetros de Razor. Ejecuta la aplicación en entorno Development, que es el único donde existen las rutas de demostración. Las rutas de productos no necesitan autenticación para continuar el ejercicio anterior.

### Paso 4.4.4. Verificar una autorización auténtica

Abre `/seguridad` sin sesión. Después intenta consultar directamente `/demo/privado`: el servidor debe impedir el acceso. Inicia sesión en el formulario, consulta el recurso de nuevo y comprueba que ahora devuelve el contenido protegido. Cierra la sesión y confirma que vuelve a denegarlo. Esta comprobación debe hacerse incluso si `AuthorizeView` muestra correctamente el nombre.

### Paso 4.4.5. Reto: rol y visibilidad

Comenta temporalmente el bloque visual `AuthorizeView Roles="Formador"` y comprueba que `/demo/privado` sigue protegido. Después modifica **solo en una copia de ensayo** la regla de autorización del endpoint para exigir `OtroRol`; aunque el usuario de prueba continúe autenticado, el servidor debe denegar acceso. Restablece `Formador`.

### Cierre

Hemos observado autenticación, autorización y representación visual de la identidad sin rehacer cursos de Web API o Identity. Nunca reutilices la credencial fija de laboratorio en un despliegue público.

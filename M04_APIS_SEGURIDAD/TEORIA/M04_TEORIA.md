# M04 — Integración de APIs y seguridad básica

## 4.1. Consumir una API HTTP desde Blazor: contratos, JSON, operaciones asíncronas y errores

### Objetivo y conexión con el módulo anterior

En M03 hemos construido una aplicación Blazor Web App sobre .NET 8 en modo Interactive Server. La página de productos administra una colección de objetos `Producto` y conoce cómo dibujar tarjetas, filtrar, seleccionar y actualizar información. En el último ejercicio, el catálogo podía obtenerse desde `IProductosMemoriaService`: un servicio dentro del mismo proceso. Ahora cambia la procedencia de los datos, no la responsabilidad de la interfaz.

En este capítulo el origen pasa a ser una **API HTTP auxiliar**. Blazor será cliente: enviará peticiones y leerá respuestas. La API será servidor: recibirá peticiones en direcciones como `/api/productos` y devolverá respuestas JSON. Ambos procesos podrán ejecutarse en la misma máquina, pero son aplicaciones distintas.

Al terminar entenderemos el camino completo, no solo la llamada a un método: componente → petición HTTP → endpoint → respuesta JSON → deserialización → estado de la interfaz. En la práctica P4.1 activaremos ese circuito conservando un punto de retorno claro al catálogo en memoria de M03.

### 4.1.1. ¿Qué cambia entre un servicio local y uno remoto?

Con `IProductosMemoriaService`, un componente llama a un método que ejecuta código del mismo servidor Blazor. Con una API, solicita información a otro servidor HTTP. El contrato visible no es una interfaz C# compartida, sino el método HTTP, la ruta, el cuerpo, el código de estado y el JSON intercambiado.

| Servicio en memoria de M03 | API HTTP en M04 |
|---|---|
| Una llamada C# dentro del mismo proceso | Petición y respuesta HTTP entre procesos |
| Devuelve objetos .NET directamente | Devuelve bytes, generalmente JSON |
| Puede fallar por reglas internas | También por conexión, tiempo de espera o estados HTTP |
| No tiene rutas ni verbos HTTP | Usa rutas y métodos GET/POST |
| Su modelo puede cambiar junto con Blazor | Necesita un contrato de intercambio estable |

Esta diferencia explica por qué **no debemos insertar llamadas HTTP en todos los componentes**. En P4.1 veremos primero el mecanismo; en 4.2 lo encapsularemos en un servicio específico que sea fácil de sustituir y probar.

### 4.1.2. Petición y respuesta: más allá de «llamar a una URL»

Una operación HTTP tiene un método, un destino y, opcionalmente, cabeceras y cuerpo.

```http
GET /api/productos HTTP/1.1
Host: localhost:5081
Accept: application/json
```

En nuestro ejemplo, una respuesta correcta devolverá estado **200 OK** y un arreglo JSON:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  { "id": 1, "nombre": "Cuaderno", "precio": 2.50 },
  { "id": 2, "nombre": "Lápiz", "precio": 0.80 }
]
```

La dirección contiene esquema, servidor, puerto y ruta. `http://localhost:5081` representa la **dirección base de ejemplo** de la API, y `api/productos` es el recurso. Si cambiamos el puerto, la ruta no tiene por qué cambiar. El puerto del servidor API y el de Blazor deben ser distintos cuando ambas aplicaciones se ejecutan a la vez.

Una alta típica usa POST:

```http
POST /api/productos HTTP/1.1
Host: localhost:5081
Content-Type: application/json

{ "nombre": "Regla", "precio": 1.75 }
```

La API valida la entrada, asigna un identificador y responde **201 Created** con el producto creado y, preferiblemente, su ubicación. GET no debe dar de alta productos; POST se emplea aquí para crear uno. Los códigos son parte del contrato: un cuerpo JSON con formato válido no convierte en éxito una operación rechazada.

### 4.1.3. Contratos de datos y DTO: no enviar la interfaz entera

En M03 existe este modelo:

```csharp
namespace CursoWeb.Blazor.Models;

public sealed record Producto(int Id, string Nombre, decimal Precio);
```

Representa un producto en la aplicación Blazor. Para transportar datos usamos DTO (*Data Transfer Object*). Un DTO distingue qué recibe y qué envía la API, evitando que detalles de la interfaz se conviertan accidentalmente en contrato público.

El producto leído incluye el identificador asignado por el servidor:

```csharp
namespace CursoWeb.Blazor.Models;

public sealed record ProductoDto(int Id, string Nombre, decimal Precio);
```

La petición de alta **no** incluye identificador, porque todavía no existe:

```csharp
namespace CursoWeb.Blazor.Models;

public sealed record CrearProductoDto(string Nombre, decimal Precio);
```

Aunque hoy coincidan tres propiedades, `Producto` y `ProductoDto` no son el mismo concepto. La conversión hace explícito el límite:

```csharp
Producto Convertir(ProductoDto dto) =>
    new(dto.Id, dto.Nombre, dto.Precio);
```

Un `record` posicional simplifica la representación en este laboratorio. No equivale a una entidad de EF Core ni introduce persistencia. La API del capítulo mantendrá su catálogo en memoria; reiniciar el proceso puede restaurar los datos iniciales.

### 4.1.4. JSON y serialización con System.Net.Http.Json

En JSON los nombres de propiedades no llevan mayúsculas obligatorias. La configuración web habitual de `System.Text.Json` usa nombres en *camelCase*, de manera que `Nombre` se representa como `nombre`.

```json
{
  "id": 3,
  "nombre": "Regla",
  "precio": 1.75
}
```

Para transformar objetos .NET en JSON o a la inversa, .NET 8 ofrece las extensiones de `System.Net.Http.Json`. `GetFromJsonAsync<T>` combina la lectura HTTP con la deserialización; `PostAsJsonAsync` serializa un objeto antes de enviarlo.

No obstante, **deserializar no es validar el negocio**: si la API devuelve un nombre vacío o un precio inválido con 200, el JSON puede ser técnicamente legible. La validación de los datos recibidos o de la petición sigue siendo una responsabilidad explícita.

### 4.1.5. HttpClient, dirección base e inyección de dependencias

`HttpClient` es el objeto mediante el cual un programa .NET envía solicitudes HTTP. Se configura a través del contenedor de servicios, en vez de crear uno nuevo por cada pulsación de botón. Para el laboratorio de M04 usaremos un cliente con nombre:

```csharp
// Program.cs de la aplicación Blazor (ejemplo de configuración para M04)
builder.Services.AddHttpClient("ProductosApi", client =>
{
    client.BaseAddress = new Uri(
        builder.Configuration["ProductosApi:BaseUrl"]
        ?? "http://localhost:5081/");
    client.Timeout = TimeSpan.FromSeconds(10);
});
```

La dirección se puede declarar en `appsettings.json`:

```json
{
  "ProductosApi": {
    "BaseUrl": "http://localhost:5081/"
  }
}
```

La barra final en `BaseAddress` evita confusiones al combinar rutas relativas. Con una ruta como `"api/productos"` (sin barra inicial), `HttpClient` construye la dirección completa usando esa base.

En Blazor Interactive Server, esta llamada se efectúa **desde el proceso servidor de Blazor**, no directamente desde JavaScript del navegador. Por tanto, un escenario HTTP servidor-a-servidor no tiene las mismas restricciones CORS que una llamada fetch desde el navegador. Aun así, un servidor API apagado o una URL equivocada impiden obtener datos.

### 4.1.6. GET asíncrono y carga de productos

Una primera aproximación dentro de un componente Blazor sería:

```razor
@page "/catalogo-remoto"
@rendermode InteractiveServer
@inject IHttpClientFactory Clientes

<h1>Productos de la API</h1>

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
            error = "La respuesta no contiene un catálogo válido.";
        }
        finally
        {
            cargando = false;
        }
    }
}
```

**Lectura razonada del ejemplo:**

- `@inject IHttpClientFactory Clientes` pide al contenedor la fábrica registrada en `Program.cs`.
- `OnInitializedAsync` se ejecuta cuando el componente se inicializa; `await` permite esperar la respuesta sin bloquear manualmente un hilo.
- `GetFromJsonAsync` puede lanzar una excepción ante un estado HTTP no satisfactorio, un problema de red o JSON inválido. No es suficiente asumir que siempre devuelve una lista.
- `?? []` trata una respuesta deserializada como `null` como lista vacía para este ejemplo. No debe confundirse con un error de comunicación: ese caso se muestra por separado.
- `finally` actualiza el indicador de carga independientemente de éxito o error.
- `role="status"` y `role="alert"` hacen los estados más claros también para tecnologías de asistencia.

El modelo `ProductoDto` debe estar importado mediante `@using CursoWeb.Blazor.Models` o en `Components/_Imports.razor`. Este ejemplo presupone el registro de cliente y los DTO anteriores; no se presenta como archivo aislado que funcione sin ellos.

### 4.1.7. POST asíncrono y resultado de una creación

El envío de un producto debe diferenciar la entrada del usuario del resultado que asigna el servidor:

```csharp
using System.Net.Http.Json;
using CursoWeb.Blazor.Models;

public static async Task<ProductoDto> CrearProductoAsync(
    HttpClient cliente,
    string nombre,
    decimal precio)
{
    var solicitud = new CrearProductoDto(nombre.Trim(), precio);

    using var respuesta = await cliente.PostAsJsonAsync(
        "api/productos", solicitud);

    // No confundimos una respuesta de error con un alta correcta.
    respuesta.EnsureSuccessStatusCode();

    return await respuesta.Content.ReadFromJsonAsync<ProductoDto>()
           ?? throw new InvalidOperationException(
               "La API confirmó el alta sin devolver un producto.");
}
```

`PostAsJsonAsync` crea el cuerpo JSON y envía POST. **No lanza automáticamente una excepción por todos los estados 4xx/5xx**: por eso invocamos `EnsureSuccessStatusCode`. Solo tras confirmar el estado leemos el producto creado y podemos incorporarlo a la interfaz.

En una interfaz real también hay que deshabilitar el botón durante el envío, informar del fallo y decidir qué hacer si se pierde la respuesta después de que el servidor ya haya procesado el POST. Para esta práctica no implementaremos reintentos automáticos de POST, pues podrían generar duplicados.

### 4.1.8. Respuestas HTTP, errores y decisiones de presentación

| Situación | Interpretación | Respuesta de la interfaz |
|---|---|---|
| 200 OK en GET | El catálogo se devolvió correctamente | Mostrar colección |
| 201 Created en POST | Se creó un recurso | Mostrar producto creado |
| 400 Bad Request | Datos de alta rechazados | Corregir los campos; no añadir el producto |
| 404 Not Found | No existe la ruta o el recurso pedido | Mostrar fallo de consulta |
| 500 Internal Server Error | Error del servidor | Mostrar mensaje no técnico |
| Conexión rechazada | API inaccesible | Mostrar problema de comunicación |
| Tiempo agotado | No llegó respuesta a tiempo | Permitir reintentar GET de forma explícita |
| JSON incompatible | El cuerpo no se ajusta al contrato | Mostrar error y revisar cliente/API |

El código de estado y la excepción no son equivalentes: una respuesta HTTP 400 demuestra que **sí** se ha alcanzado algún servidor; un error de conexión puede significar que no se ha alcanzado ninguno.

Para un tratamiento más fino podemos leer `HttpResponseMessage` de forma explícita y distinguir `StatusCode`, como veremos en el ejercicio de error controlado. Los detalles internos y trazas del servidor no deben exponerse directamente al usuario de la aplicación.

### 4.1.9. API auxiliar: contrato disponible antes de construir la práctica

Para que P4.1 no dependa de una API aprendida «en el futuro», el laboratorio facilita al inicio del módulo una pequeña aplicación ASP.NET Core con:

- `GET /api/productos`: devuelve un catálogo inicial con 200.
- `POST /api/productos`: valida nombre y precio, asigna un ID y responde 201.
- `GET /api/productos/{id}`: puede servir para mostrar el caso 404 (operación auxiliar del laboratorio).

La API reside en un proyecto independiente del cliente Blazor. La aplicación utiliza almacenamiento **en memoria** deliberadamente: el alumno ya conoce Web API y EF Core, y este módulo no pretende repetir esos cursos. En 4.3 se abrirá ese código, se explicará su funcionamiento y se modificará su respuesta.

Ejemplo de endpoint mínimo que materializa el contrato, con el modelo declarado dentro de su propio proyecto API:

```csharp
using System.Collections.Concurrent;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var productos = new ConcurrentDictionary<int, ProductoApi>();
productos[1] = new ProductoApi(1, "Cuaderno", 2.50m);
productos[2] = new ProductoApi(2, "Lápiz", 0.80m);
var siguienteId = 2;

app.MapGet("/api/productos", () =>
    Results.Ok(productos.Values.OrderBy(p => p.Id)));

app.MapPost("/api/productos", (CrearProductoApi entrada) =>
{
    if (string.IsNullOrWhiteSpace(entrada.Nombre) ||
        entrada.Precio <= 0)
        return Results.BadRequest("Nombre y precio deben ser válidos.");

    var id = Interlocked.Increment(ref siguienteId);
    var creado = new ProductoApi(id, entrada.Nombre.Trim(), entrada.Precio);
    productos[id] = creado;
    return Results.Created($"/api/productos/{id}", creado);
});

app.MapGet("/api/productos/{id:int}", (int id) =>
    productos.TryGetValue(id, out var producto)
        ? Results.Ok(producto)
        : Results.NotFound());

app.Run();

record ProductoApi(int Id, string Nombre, decimal Precio);
record CrearProductoApi(string Nombre, decimal Precio);
```

La colección concurrente protege las operaciones básicas de lectura y escritura entre peticiones, y `Interlocked.Increment` asigna identificadores distintos. No estamos creando una capa de persistencia ni una arquitectura empresarial. El contrato JSON debe seguir siendo compatible con los DTO usados por Blazor.

### 4.1.10. Una secuencia razonable de trabajo

Una integración HTTP se comprende mejor comprobando cada capa por separado: primero ejecutamos la API y comprobamos GET; después iniciamos Blazor y verificamos la lista; a continuación enviamos POST; por último apagamos la API para reconocer un error real. Si hacemos todos los cambios de golpe, un puerto incorrecto, una ruta inexistente y un DTO incompatible se manifestarán como «no funciona», sin aportar pistas sobre su causa.

Esta secuencia también evita un error pedagógico frecuente: **modificar la aplicación de M03 sin explicar qué funciones conserva y cuáles se sustituyen**. La primera versión remota será deliberadamente pequeña, separada de `/productos`. Así el alumno podrá comparar ambos flujos, sin perder los filtros, la selección y la edición local que ya ha aprendido.

### Síntesis de 4.1

Consumir una API no consiste únicamente en escribir `await cliente.GetFromJsonAsync`. Requiere conocer el contrato HTTP, representar correctamente los datos intercambiados, configurar el cliente, distinguir éxito y fracaso y actualizar el estado visible de Blazor con una respuesta confiable. En el siguiente punto, 4.2, retiraremos esa responsabilidad de los componentes y la situaremos en un servicio especializado.

## 4.2. Extraer el consumo HTTP a una capa de servicio

### De un componente que hace todo a dos responsabilidades

En 4.1 `CatalogoRemoto.razor` aprendió a hablar HTTP: creó un `HttpClient`, conoció la ruta `api/productos`, interpretó respuestas JSON y mostró resultados. Esa mezcla fue útil para comprender el mecanismo, pero ahora presenta un inconveniente: cualquier componente que necesite productos debería repetir esos detalles de red. Cambiar la ruta, el tratamiento de un error o el contrato JSON obligaría a editar varias páginas.

La mejora consiste en separar **qué hace la interfaz** de **cómo se recuperan los datos**. El componente mantiene los formularios, los mensajes, la carga y el estado visual. Una clase de servicio conoce la API y concentra `GetFromJsonAsync`, `PostAsJsonAsync` y la conversión de errores.

### 4.2.1. El contrato IProductosApiService

Declaramos una interfaz con operaciones del negocio que necesita nuestra pantalla, no con detalles de transporte:

```csharp
using CursoWeb.Blazor.Models;

namespace CursoWeb.Blazor.Services;

public interface IProductosApiService
{
    Task<IReadOnlyList<ProductoDto>> ObtenerAsync();
    Task<ProductoDto> CrearAsync(CrearProductoDto solicitud);
}
```

El nombre `ObtenerAsync` expresa la intención de consultar productos; no revela si la implementación utiliza HTTP, un fichero o datos de prueba. El `Task` indica que la operación puede completarse más tarde. `IReadOnlyList` impide que un consumidor suponga que puede modificar la colección interna del servicio. La interfaz no valida formularios HTML ni determina cuándo aparece un botón de carga: esas decisiones pertenecen a Blazor.

### 4.2.2. Implementación HTTP y gestión de errores

La clase `ProductosApiService` recibe un `HttpClient` configurado por el contenedor y ejecuta las operaciones:

```csharp
using System.Net.Http.Json;
using CursoWeb.Blazor.Models;

namespace CursoWeb.Blazor.Services;

public sealed class ProductosApiService(HttpClient cliente)
    : IProductosApiService
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

El constructor primario de C# 12 deja explícita una única dependencia: `HttpClient`. `GetFromJsonAsync` puede lanzar `HttpRequestException` ante fallo de red o estado HTTP insatisfactorio, `TaskCanceledException` ante una operación cancelada o un tiempo límite, y `JsonException` ante JSON incompatible. La implementación no captura estas excepciones para devolver silenciosamente una lista vacía: hacerlo confundiría un error con un catálogo legítimamente vacío.

En `CrearAsync`, la respuesta POST se examina antes de leer su JSON. `EnsureSuccessStatusCode` evita registrar como creado un producto cuando el servidor devolvió una respuesta de error. `using` libera el mensaje de respuesta. Este servicio no registra contraseñas, no escribe en la base de datos y no sustituye a la API.

### 4.2.3. Registrar el servicio en Program.cs

Una interfaz no es instanciable por sí misma. El contenedor de inyección de dependencias necesita saber qué implementación proporcionar y cómo construir sus dependencias. El registro **typed HttpClient** hace ambas cosas:

```csharp
builder.Services.AddHttpClient<IProductosApiService, ProductosApiService>(
    cliente =>
    {
        cliente.BaseAddress = new Uri(
            builder.Configuration["ProductosApi:BaseUrl"]
            ?? "http://localhost:5081/");
        cliente.Timeout = TimeSpan.FromSeconds(10);
    });
```

Con este registro, cuando una página solicita `IProductosApiService`, el contenedor crea una instancia de `ProductosApiService` con un `HttpClient` ya configurado. `AddHttpClient` está diseñado para gestionar la creación de clientes y la reutilización de manejadores HTTP sin que cada componente gestione su vida útil.

En 4.1 utilizábamos un cliente **con nombre**, recuperado con `IHttpClientFactory.CreateClient("ProductosApi")`. En este punto lo sustituimos por un cliente **tipado**. Son dos patrones legítimos, pero **no hace falta registrar los dos** para el mismo recorrido didáctico. Elegimos el cliente tipado porque el componente solo necesita la interfaz de negocio.

### 4.2.4. Inyectar la interfaz desde Razor

La página ya no necesita `IHttpClientFactory`:

```razor
@inject IProductosApiService CatalogoApi
```

Durante la inicialización, el componente espera un resultado que ya son DTO:

```csharp
protected override async Task OnInitializedAsync()
{
    try
    {
        productos = (await CatalogoApi.ObtenerAsync()).ToList();
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
```

El formulario sigue validando nombre y precio antes de enviar los datos. El método de alta construye `CrearProductoDto`, llama a `await CatalogoApi.CrearAsync(...)` y añade a la colección el objeto que devolvió el servidor. **El HTML y el resultado que observa el usuario no tienen por qué cambiar** al reorganizar las dependencias.

### 4.2.5. Distinguir responsabilidades y alcance

| Responsabilidad | Componente Blazor | Servicio HTTP | API |
|---|---|---|---|
| Mostrar campos y mensajes | Sí | No | No |
| Decidir cuándo cargar | Sí | No | No |
| Construir petición HTTP y leer JSON | No | Sí | No |
| Asignar ID del producto | No | No | Sí |
| Validar reglas del servidor | No | No | Sí |
| Gestionar indicadores visuales de carga | Sí | No | No |

La validación preliminar de un formulario no sustituye la validación de la API. El cliente puede cambiarse o saltarse: la API debe seguir rechazando entradas inválidas.

Esta separación facilita pruebas: un componente puede recibir una implementación falsa de `IProductosApiService` que devuelva datos conocidos, y el servicio real puede contrastarse contra la API de laboratorio. No añadimos aquí un framework de mocking ni una arquitectura compleja: el propósito es comprender por qué resulta útil tener un contrato inyectable.

### 4.2.6. Comportamiento observable del refactor

La comprobación decisiva no es que exista una clase nueva: es que, tras sustituir el acceso directo, `/catalogo-remoto` siga listando Cuaderno y Lápiz, permita crear Regla, notifique un rechazo o un servidor apagado y mantenga funcional la página local `/productos` de M03. En esta práctica modificamos la organización del código sin cambiar el contrato HTTP ni la API.

En P4.3 abriremos la implementación de la API que ya proporcionamos al comenzar 4.1. De ese modo el alumno ya conoce el consumo y puede comprender ahora el origen de las respuestas sin introducir otra aplicación ajena al laboratorio.

## 4.3. Comprender y modificar la API auxiliar de Productos

### Por qué estudiamos ahora el servidor

En 4.1 y 4.2 hemos consumido una API que ya estaba disponible: primero desde el componente Razor, después mediante \`IProductosApiService\`. Sabemos que \`GET /api/productos\` devuelve un catálogo y \`POST /api/productos\` crea una entrada, pero todavía no hemos seguido esa petición dentro del servidor. En este punto abriremos **el mismo proyecto** que se entregó al comenzar M04. No escribiremos una API empresarial ni repetiremos el temario previo de Web API: queremos entender las piezas que hacen posible el contrato que Blazor ya utiliza.

El recorrido completo es:

\`\`\`text
Blazor /catalogo-remoto
  → IProductosApiService
  → ProductosApiService (HttpClient)
  → GET o POST http://localhost:5081/api/productos
  → aplicación API: endpoint y reglas
  → respuesta HTTP + JSON
  → servicio cliente
  → estado de la pantalla
\`\`\`

La API del laboratorio funciona en un proceso separado. Su modelo \`ProductoApi\` es propio; el cliente utiliza \`ProductoDto\`. Coinciden las propiedades públicas del contrato HTTP, pero no comparten necesariamente el mismo ensamblado.

### 4.3.1. El host mínimo en Program.cs

La API se inicia con el patrón habitual de .NET 8:

\`\`\`csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
// Aquí se declaran rutas mediante app.MapGet y app.MapPost.
app.Run();
\`\`\`

\`CreateBuilder\` prepara configuración y servicios; \`Build\` crea la aplicación; \`MapGet\` y \`MapPost\` asocian un método HTTP y una ruta a un delegado que procesa la petición; \`Run\` mantiene el servidor atendiendo solicitudes. Este proyecto es pequeño porque el alumno ya conoce Web API: **Minimal APIs** nos permiten mostrar el contrato y las reglas sin añadir controladores y capas que no aportan aprendizaje a M04.

### 4.3.2. Qué devuelve realmente GET

La colección se crea en memoria al arrancar:

\`\`\`csharp
var productos = new ConcurrentDictionary<int, ProductoApi>();
productos[1] = new ProductoApi(1, "Cuaderno", 2.50m);
productos[2] = new ProductoApi(2, "Lápiz", 0.80m);
\`\`\`

\`ConcurrentDictionary\` permite accesos concurrentes seguros a las operaciones de diccionario que usamos. Los registros iniciales son datos del laboratorio, no datos de SQL Server. Esta línea publica el catálogo:

\`\`\`csharp
app.MapGet("/api/productos", () =>
    Results.Ok(productos.Values.OrderBy(p => p.Id)));
\`\`\`

\`Results.Ok\` devuelve **200 OK**. ASP.NET Core serializa la colección en JSON: los nombres de propiedades se exponen en *camelCase* bajo las opciones web habituales. \`OrderBy\` evita presentar el orden interno de un diccionario concurrente como si fuera un criterio estable de listado.

Si consultamos \`/api/productos/999\`, el endpoint de detalle devuelve \`Results.NotFound()\`. **404 no es una excepción de C# obligatoria**: es una decisión explícita de protocolo que el cliente debe interpretar.

### 4.3.3. Cómo procesa POST la entrada

La API recibe un objeto de entrada:

\`\`\`csharp
record CrearProductoApi(string Nombre, decimal Precio);
\`\`\`

Ese contrato **no tiene Id**: el identificador lo asigna el servidor. El delegado de POST valida nombre y precio:

\`\`\`csharp
if (string.IsNullOrWhiteSpace(entrada.Nombre) || entrada.Precio <= 0)
    return Results.BadRequest("Nombre y precio deben ser válidos.");
\`\`\`

Si los datos cumplen las reglas, se ejecuta:

\`\`\`csharp
var id = Interlocked.Increment(ref siguienteId);
var creado = new ProductoApi(id, entrada.Nombre.Trim(), entrada.Precio);
productos[id] = creado;
return Results.Created($"/api/productos/{id}", creado);
\`\`\`

\`Interlocked.Increment\` produce IDs distintos aunque dos peticiones se procesen simultáneamente. \`Results.Created\` devuelve **201 Created**, el cuerpo del producto creado y una cabecera \`Location\` que apunta a su recurso. Por eso nuestra API expone también \`GET /api/productos/{id}\`.

El cliente no debe inventar el ID ni tratar una respuesta 400 como creación satisfactoria. La validación previa de la página Blazor facilita la experiencia de usuario, pero la API siempre vuelve a validar: el servidor no puede confiar en que todas las llamadas provienen de nuestro formulario.

### 4.3.4. Modificar una respuesta de forma controlada

Vamos a añadir una operación de lectura que no cambie el contrato que ya consume Blazor: \`GET /api/productos/resumen\`. Responderá con el número de productos y el valor agregado de sus precios.

\`\`\`csharp
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

El material devuelve, por ejemplo:

\`\`\`json
{ "cantidad": 2, "precioTotal": 3.30 }
\`\`\`

Tras crear Regla a 1,75, el resumen indicará tres productos y un precio total de 5,05. Son valores ilustrativos que dependen de partir del estado inicial de la API. **No cambiaremos** \`GET /api/productos\`, porque 4.1 y 4.2 dependen de que esa ruta siga devolviendo una lista. Esta es la idea del ejercicio: ampliar sin romper un cliente existente.

La ruta literal \`/api/productos/resumen\` no se confunde con \`/api/productos/{id:int}\`, porque esta última exige un parámetro entero. El resultado de resumen tiene su propia forma JSON; no debe deserializarse como \`ProductoDto\`.

### 4.3.5. Diferencias entre JSON válido, reglas de negocio y persistencia

Una petición puede tener JSON sintácticamente válido y, sin embargo, incumplir las reglas: \`{"nombre":"","precio":0}\` contiene JSON legible, pero no un producto aceptable. Una petición de JSON incompatible con el DTO puede producir una respuesta de error antes de que el delegado de POST ejecute su comprobación. Nuestro ejemplo no pretende normalizar todos los mensajes de error posibles.

Tampoco basta con que un POST devuelva 201 para afirmar que existe persistencia: **la información vive en memoria del proceso**. Al reiniciar la API se restauran Cuaderno y Lápiz; el producto añadido desaparece. La persistencia ya fue estudiada con EF Core en el contexto previo del alumnado; reintroducirla aquí impediría concentrarse en la comunicación Blazor–API.

### 4.3.6. Probar el contrato sin depender de la pantalla

Para diagnosticar una integración conviene separar observaciones. Primero ejecutamos la API y probamos GET, POST y errores con un cliente HTTP independiente. Después abrimos Blazor para comprobar que conserva su comportamiento. Si el GET directo funciona, pero la página falla, investigaremos URL configurada, puerto, servicio tipado, DTO o estado del componente. Si el GET directo también falla, examinaremos el proceso API y sus rutas.

En este punto **no** implantamos autenticación sobre el catálogo; la demostración limitada de seguridad corresponde a 4.4. Una API sin protección no se vuelve segura por el mero hecho de que la interfaz oculte un botón. La autorización debe comprobarse en el servidor del recurso protegido.

### Síntesis del punto 4.3

Un endpoint es una asociación entre método HTTP, ruta y ejecución de código. Los DTO establecen el contrato; los resultados HTTP indican éxito o rechazo; el estado en memoria explica la duración de los datos. Hemos añadido una operación de resumen sin romper las rutas existentes, y disponemos de una API reproducible que se puede observar tanto directamente como desde Blazor.
## 4.4. Autenticación, autorización y AuthorizeView

### Identificar al usuario no es darle permisos

**Autenticación** responde quién es el usuario. **Autorización** responde qué puede hacer ese usuario ya identificado. En ASP.NET Core la identidad puede representar datos mediante **claims**: afirmaciones como el nombre o un rol. Un rol de ejemplo, `Formador`, servirá para observar la autorización sin construir una infraestructura de cuentas.

La página Blazor de 4.4 demostrará estos conceptos con una cookie de sesión **solo en el laboratorio local**. No implantaremos ASP.NET Core Identity ni JWT, OAuth u OpenID Connect; mencionar Identity permitirá comprender dónde encaja la gestión real de usuarios y contraseñas en una aplicación profesional. El código fijo de demostración **no es una credencial válida para producción**.

### 4.4.1. Configurar una autenticación de demostración

ASP.NET Core permite registrar autenticación por cookie y autorización con:

```csharp
builder.Services.AddAuthentication("CookiesDemo")
    .AddCookie("CookiesDemo", opciones =>
    {
        opciones.LoginPath = "/seguridad";
    });
builder.Services.AddAuthorization();
builder.Services.AddCascadingAuthenticationState();
```

Tras construir la aplicación se usan `app.UseAuthentication()` y `app.UseAuthorization()`, antes de mapear los recursos protegidos. La autenticación examina la cookie enviada por el navegador. La autorización aplica reglas usando el principal autenticado. `AddCascadingAuthenticationState` hace disponible ese estado a los componentes Razor.

Para construir una identidad de prueba:

```csharp
var claims = new[]
{
    new Claim(ClaimTypes.Name, "AlumnoDemo"),
    new Claim(ClaimTypes.Role, "Formador")
};
var identidad = new ClaimsIdentity(claims, "CookiesDemo");
var principal = new ClaimsPrincipal(identidad);
await contexto.SignInAsync("CookiesDemo", principal);
```

La cookie debe emitirse en una respuesta HTTP normal. Una operación `SignInAsync` dentro de un evento de Blazor Interactive Server que ya ha iniciado su respuesta no es el enfoque apropiado; por ello haremos el acceso mediante un formulario HTML POST y una redirección de página completa.

### 4.4.2. Proteger recursos en el servidor

Un endpoint protegido es distinto de un botón oculto:

```csharp
app.MapGet("/demo/privado", () =>
    Results.Ok(new { mensaje = "Recurso protegido" }))
    .RequireAuthorization(p => p.RequireRole("Formador"));
```

La autorización se evalúa en el servidor. Aunque se conozca la URL, el usuario anónimo no recibe el contenido. Una identidad autenticada sin `Formador` tampoco recibe autorización. La API de Productos utilizada en 4.1–4.3 permanece deliberadamente pública: aquí no añadimos credenciales a todo el proyecto.

### 4.4.3. AuthorizeView: presentación condicional, no seguridad del servidor

```razor
<AuthorizeView>
    <Authorized>
        <p>Sesión: @context.User.Identity?.Name</p>
    </Authorized>
    <NotAuthorized>
        <p>La sesión no está autenticada.</p>
    </NotAuthorized>
</AuthorizeView>
```

`AuthorizeView Roles="Formador"` muestra contenido solo si los claims del usuario satisfacen esa condición. Eso cambia la **interfaz visible**; no reemplaza la regla `RequireAuthorization` del servidor. Para páginas protegidas con `[Authorize]` puede emplearse `AuthorizeRouteView` al resolver las rutas, pero el recurso de demostración será el endpoint HTTP protegido.

### 4.4.4. Formularios HTTP y antifalsificación

El inicio de sesión de laboratorio usará un formulario HTML normal con `method="post"`, `<AntiforgeryToken />` y `data-enhance="false"`. El servidor comprobará el formulario, creará los claims y emitirá la cookie. La salida también se hará mediante POST con token y `SignOutAsync`.

El token antifalsificación dificulta que un sitio externo envíe solicitudes que cambian estado usando la sesión del navegador; **no comprueba la identidad** y no transforma una contraseña fija en un sistema seguro. Nunca debemos desactivar su protección simplemente para que la demo funcione.

### 4.4.5. Casos que debe observar el alumno

| Estado | Resultado |
|---|---|
| Usuario anónimo | `AuthorizeView` presenta `NotAuthorized` |
| Anónimo consulta `/demo/privado` | El servidor deniega el recurso |
| Código local correcto | Se crea una sesión de demostración |
| Sesión con rol `Formador` | Se muestra el rol y se accede al recurso protegido |
| Salida POST | La sesión deja de estar autenticada |

La demostración es intencionalmente superficial. Identity, proveedores externos, permisos de producción y protección del catálogo completo quedan fuera de este curso de 30 horas.

### Conclusión del módulo

4.1 enseña a consumir HTTP; 4.2 separa interfaz y servicios; 4.3 explica el servidor; 4.4 distingue la identidad, la decisión de acceso del servidor y la presentación condicional de Blazor.

## Laboratorio de razonamiento transversal: una operación vista desde cuatro límites

Este apartado relaciona los cuatro conceptos del módulo mediante un mismo caso: una persona desea crear un producto nuevo llamado «Agenda», con precio 6,40. Seguir la operación de un extremo a otro ayuda a detectar errores que quedan ocultos cuando se estudian las tecnologías como listas de instrucciones.

### El límite de la interfaz

En Blazor la persona escribe un nombre y un precio. Estos valores viven inicialmente en el estado del componente. Puede haber un control de formulario que evite enviar campos vacíos, pero no podemos interpretar esa comprobación como una garantía del servidor: cualquiera que conozca la dirección de la API puede enviar otra petición.

El componente debe gestionar un estado de envío: antes del POST desactiva el botón para evitar pulsaciones duplicadas y después muestra el resultado. Si ocurre un fallo, mantiene los valores para facilitar una corrección. Añadir a la lista un producto antes de recibir confirmación sería una **actualización optimista**; aquí preferimos esperar el producto que devuelve la API, porque contiene el identificador real asignado.

### El límite del servicio

El componente no conoce la URL; solo pide al servicio que cree un producto. El servicio transforma la operación de negocio en una petición HTTP, serializando `CrearProductoDto` con `PostAsJsonAsync`. Debe comprobar el estado de respuesta antes de leer el producto creado, porque un 400 representa una operación rechazada.

Este diseño permite cambiar el puerto o la implementación remota sin modificar cada componente. Por el contrario, no elimina las fallas de red: solo ofrece un lugar único para tratar las particularidades de HTTP.

### El límite del servidor

La API recibe el JSON, crea un objeto de entrada y comprueba sus reglas. En nuestro laboratorio, un nombre sin contenido o un precio igual o inferior a cero produce 400. Si la entrada es válida, se asigna un ID y la API responde 201 con el producto. En este punto el servidor no conoce componentes Blazor ni `AuthorizeView`; sus reglas funcionan igualmente para otro cliente HTTP.

Si un servidor devuelve 201 pero el cliente pierde la conexión antes de recibirlo, el cliente podría desconocer que el alta se realizó. Por eso el reintento automático de POST no se presenta como una decisión inocua. Un sistema real necesitaría valorar idempotencia, identificadores de petición o reconciliación, pero no añadiremos esa infraestructura al ejercicio.

### El límite de la identidad

La demostración de 4.4 protege únicamente `/demo/privado`. Es importante evitar una conclusión falsa: que el usuario haya iniciado sesión en Blazor **no convierte el POST público de productos en una operación protegida**. Las políticas se aplican en cada recurso del servidor correspondiente. El control visual de una pantalla no autoriza ni desautoriza una petición HTTP.

Para ampliar la aplicación en un proyecto futuro, habría que determinar qué operaciones requieren autenticación y qué política aplica a cada una. Ese análisis es distinto de decidir si la interfaz muestra un botón.

### Secuencia de diagnóstico de un fallo

Supongamos que «Agenda» no aparece después del envío. Antes de reescribir el componente, realizamos comprobaciones en orden:

1. Comprobar que la API está iniciada y que el GET directo devuelve JSON, diferenciando ausencia de conexión y ausencia de datos.
2. Confirmar que la dirección configurada en `ProductosApi:BaseUrl` y la ruta relativa del servicio componen el destino previsto.
3. Examinar el estado HTTP del POST. Un 400 indica que la API recibió una petición pero rechazó sus datos; un error de conexión indica que no se obtuvo una respuesta HTTP.
4. Si el POST devuelve 201, inspeccionar que el cuerpo puede deserializarse como `ProductoDto` y que el identificador corresponde al devuelto por el servidor.
5. Si el servicio entrega correctamente el DTO pero la pantalla no cambia, revisar la actualización de `productos` y los estados visuales en el componente.

Este recorrido clasifica los errores por responsabilidad: presentación, comunicación, contrato o regla del servidor. Cambiar simultáneamente cuatro archivos ante un único fallo dificulta aprender qué ocurrió.

### Dos pruebas que parecen iguales y no lo son

**Prueba A:** detener la API y abrir `/catalogo-remoto`. Se espera un mensaje de conectividad; no un 404, porque la conexión no ha llegado al endpoint.

**Prueba B:** mantener la API funcionando y cambiar temporalmente la ruta a `api/no-existe`. El servidor sí responde, pero lo hace con 404. El componente puede mostrar un texto parecido al de A si la excepción se trata de manera general; observar el estado HTTP permite distinguir los casos.

Este contraste justifica el reto del punto 4.1 y sirve para decidir si una aplicación necesita mensajes más específicos sin llenar la pantalla de detalles técnicos.

### Cómo razonar sobre una respuesta parcialmente correcta

Imaginemos una API que responde 200 con `{"cantidad":2,"precioTotal":3.30}`. El JSON es válido y la respuesta es satisfactoria, pero **no corresponde a una lista de `ProductoDto`**. Si el servicio de catálogo intenta leerlo como lista, fallará el contrato. En 4.3 añadimos el resumen como ruta diferenciada precisamente para no alterar el cuerpo que espera el cliente existente.

La compatibilidad de contratos es uno de los motivos por los que una API no debería cambiar de forma arbitraria el tipo de respuesta de un endpoint ya consumido.

### Actividad razonada antes de practicar

Sin escribir todavía código, responde: ¿qué componente conoce el puerto 5081? ¿Qué capa debe saber que existe `api/productos`? ¿Quién asigna el identificador? ¿Dónde se comprueba el rol `Formador` para `/demo/privado`? Si las respuestas sitúan el puerto en configuración/cliente HTTP, la ruta en servicio/API, el ID en la API y la autorización en el servidor, la separación de responsabilidades está bien comprendida.

Estas decisiones serán observables en los proyectos de 4.1–4.4 y no dependen de nombres de clases memorísticos: derivan del recorrido completo de la petición.

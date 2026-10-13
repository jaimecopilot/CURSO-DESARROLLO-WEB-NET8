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

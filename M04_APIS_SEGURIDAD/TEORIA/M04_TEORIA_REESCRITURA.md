# M04 — Integración de APIs y seguridad básica
## Manual de teoría · Desarrollo web con ASP.NET Core MVC, Razor y Blazor (.NET 8)

Este módulo continúa la aplicación Blazor Web App, en modo Interactive Server, del módulo 3. El producto que el alumno conoce hasta ahora se consulta desde un servicio de memoria. Nuestra meta consiste en comprender, diseñar y construir una comunicación HTTP entre esa interfaz y una API REST pequeña; después separaremos las responsabilidades del componente y analizaremos una demostración local de autenticación y autorización.

Los ejemplos que siguen forman un itinerario único. Cada ejemplo nace de un problema definido, muestra una implementación íntegra en su contexto y explica los mecanismos que la hacen funcionar. La práctica posterior transformará ese itinerario en ejercicios que el alumno ejecutará por sí mismo.

## 4.1. De un catálogo Blazor local a una API HTTP

### 4.1.1. El problema: el catálogo ya no está dentro de nuestro proceso

Hasta M03, la página de productos consumía un servicio C# mediante inyección de dependencias. Cuando escribimos \`await Catalogo.ObtenerAsync()\`, el método se ejecuta en el mismo proceso ASP.NET Core que aloja los componentes Blazor. Ese recorrido es apropiado para aprender componentes, estado y asincronía, pero no demuestra el límite entre aplicaciones.

Imaginemos ahora dos procesos: una aplicación **Blazor** dedicada a presentar información y una **API** que ofrece productos. Aunque ambos se ejecuten en el mismo ordenador, sus responsabilidades son distintas. Blazor no invoca directamente los métodos internos de la API, sino que le envía una petición HTTP y procesa la respuesta. Al cambiar de proceso aparecen preocupaciones nuevas: puerto, dirección, método, ruta, cuerpo, formato JSON, código de estado, desconexión, tiempo de espera y compatibilidad de los contratos.

La comunicación se puede representar así:

\`\`\`text
Navegador
    │ interacción visual
    ▼
Blazor Interactive Server (proceso cliente HTTP)
    │ HttpClient: GET /api/productos
    ▼
API ASP.NET Core (proceso servidor HTTP)
    │ consulta datos en memoria
    ▼
HTTP 200 + JSON
    │ deserialización
    ▼
Componente Blazor: lista, carga o error
\`\`\`

En **Interactive Server**, las llamadas \`HttpClient\` realizadas desde el código del componente se ejecutan en el servidor de Blazor. No deben confundirse con peticiones \`fetch\` originadas en JavaScript del navegador; por eso no necesitaremos CORS para este intercambio servidor a servidor.

### 4.1.2. El contrato HTTP es más que una dirección

Una petición de consulta puede representarse en texto:

\`\`\`http
GET /api/productos HTTP/1.1
Host: localhost:5081
Accept: application/json
\`\`\`

La operación dice qué recurso se solicita mediante **GET**; la ruta identifica el catálogo y la cabecera \`Accept\` expresa que el cliente prefiere JSON. Un servidor que devuelve el catálogo correctamente puede responder:

\`\`\`http
HTTP/1.1 200 OK
Content-Type: application/json

[
  { "id": 1, "nombre": "Cuaderno", "precio": 2.50 },
  { "id": 2, "nombre": "Lápiz", "precio": 0.80 }
]
\`\`\`

Es importante distinguir **código HTTP** y **cuerpo**. El primero informa del resultado protocolario; el segundo contiene los datos. Un 404 no se convierte en éxito porque su cuerpo incluya JSON. Un 200 con un cuerpo incompatible con la forma esperada puede seguir siendo un problema para la aplicación cliente.

Para crear un producto, el cliente envía **POST** y un cuerpo JSON:

\`\`\`http
POST /api/productos HTTP/1.1
Host: localhost:5081
Content-Type: application/json

{ "nombre": "Regla", "precio": 1.75 }
\`\`\`

Si la API lo acepta, responderá con **201 Created** y el recurso completo, incluido el identificador asignado en el servidor. Si el nombre es vacío o el precio no es positivo, devolverá **400 Bad Request**. Esas reglas no deben depender del formulario de Blazor: otros clientes HTTP podrían acceder a la API.

### 4.1.3. Diseñar DTO diferentes para leer y crear

En M03 existe un modelo local equivalente a:

\`\`\`csharp
namespace CursoWeb.Blazor.Models;
public sealed record Producto(int Id, string Nombre, decimal Precio);
\`\`\`

No vamos a borrar ese tipo: los componentes locales siguen utilizándolo. Crearemos DTO específicos para el contrato remoto. El DTO de lectura contiene ID:

\`\`\`csharp
namespace CursoWeb.Blazor.Models;
public sealed record ProductoDto(int Id, string Nombre, decimal Precio);
\`\`\`

El DTO de creación no tiene ID, pues todavía no existe:

\`\`\`csharp
namespace CursoWeb.Blazor.Models;
public sealed record CrearProductoDto(string Nombre, decimal Precio);
\`\`\`

La separación evita una equivocación conceptual: permitir que el cliente elija el identificador que pertenece al servidor. También expresa que los modelos internos de aplicaciones distintas pueden evolucionar de manera independiente. En este laboratorio los nombres de las propiedades coinciden deliberadamente, porque el objetivo es estudiar HTTP, no introducir un sistema de transformación complejo.

El serializador web habitual de \`System.Text.Json\` utiliza nombres JSON en *camelCase*. Por ello \`Nombre\` corresponde a \`nombre\`. El número \`1.75\` se escribe con punto decimal dentro de JSON, independientemente del formato localizado mostrado en una interfaz.

### 4.1.4. Configurar HttpClient correctamente

\`HttpClient\` es el cliente HTTP de .NET. En lugar de instanciarlo de manera improvisada cada vez que el usuario pulsa un botón, registramos un cliente configurado:

\`\`\`csharp
// Program.cs del proyecto Blazor, junto a los demás servicios.
builder.Services.AddHttpClient("ProductosApi", cliente =>
{
    cliente.BaseAddress = new Uri(
        builder.Configuration["ProductosApi:BaseUrl"]
        ?? "http://localhost:5081/");
    cliente.Timeout = TimeSpan.FromSeconds(10);
});
\`\`\`

La dirección puede declararse en \`appsettings.json\`:

\`\`\`json
{
  "ProductosApi": {
    "BaseUrl": "http://localhost:5081/"
  }
}
\`\`\`

La barra final importa: una ruta relativa \`"api/productos"\` se combina con la dirección base. La dirección no debe dispersarse por diversos componentes porque en otra máquina cambiaría. Diez segundos es un límite didáctico, no un valor universal para producción; una petición que supera ese tiempo debe convertirse en un estado visible y comprensible para el usuario.

El registro utiliza un **cliente con nombre**. En 4.2 sustituiremos esta forma por un cliente tipado asociado a una interfaz, después de entender qué operaciones queremos abstraer.

### 4.1.5. Primera pantalla completa: consultar catálogo y distinguir estados

El siguiente componente se escribe en \`Components/Pages/CatalogoRemoto.razor\`. Requiere que los DTO y el registro anterior ya existan, y que la API esté iniciada en 5081.

\`\`\`razor
@page "/catalogo-remoto"
@rendermode @(new InteractiveServerRenderMode(prerender: false))
@using System.Net.Http.Json
@inject IHttpClientFactory Clientes

<h1>Catálogo remoto</h1>
@if (cargando)
{
    <p role="status">Cargando productos...</p>
}
else if (error is not null)
{
    <p role="alert">@error</p>
}
else
{
    <ul id="productos-api">
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
            error = "No se pudo consultar el catálogo remoto.";
        }
        catch (TaskCanceledException)
        {
            error = "La consulta tardó demasiado.";
        }
        catch (System.Text.Json.JsonException)
        {
            error = "La respuesta de la API no contiene un catálogo válido.";
        }
        finally
        {
            cargando = false;
        }
    }
}
\`\`\`

Analicemos **por qué** funciona. \`@inject\` solicita la fábrica registrada en el contenedor; \`CreateClient\` devuelve un \`HttpClient\` con dirección y timeout configurados. \`OnInitializedAsync\` es el punto del ciclo de vida en el que iniciamos la carga. La instrucción \`await\` espera la petición sin bloquear explícitamente la ejecución con \`.Result\`. \`GetFromJsonAsync<T>\` realiza la consulta, comprueba el estado y deserializa JSON. Sus fallos pueden deberse a red, estado HTTP, cancelación o formato incompatible.

\`cargando\` comienza en \`true\`; por eso el componente muestra un mensaje y no una lista vacía mientras espera. El bloque \`finally\` actualiza ese estado independientemente del resultado. Si se recibe una lista vacía legítima, \`error\` permanece en \`null\`, algo distinto de no haber conseguido conectar. Esa distinción será esencial cuando construyamos diagnósticos.

### 4.1.6. Alta remota: quién asigna el identificador y cuándo cambia la pantalla

Supongamos que el usuario escribe «Regla» y 1,75. El componente no debe generar el identificador ni incorporar el producto a la lista antes de recibir confirmación. Una función de alta puede verse así:

\`\`\`csharp
private async Task<ProductoDto> CrearProductoHttpAsync(
    HttpClient cliente, string nombre, decimal precio)
{
    var solicitud = new CrearProductoDto(nombre.Trim(), precio);
    using var respuesta = await cliente.PostAsJsonAsync(
        "api/productos", solicitud);
    respuesta.EnsureSuccessStatusCode();

    return await respuesta.Content.ReadFromJsonAsync<ProductoDto>()
        ?? throw new InvalidOperationException(
            "La API devolvió un alta sin producto.");
}
\`\`\`

\`PostAsJsonAsync\` serializa la solicitud; \`EnsureSuccessStatusCode\` impide interpretar un 400 como éxito; \`ReadFromJsonAsync\` convierte el cuerpo de respuesta en un DTO que **sí** incorpora el ID real. Solo entonces la interfaz puede añadirlo a su colección local. Si el servidor ya creó el recurso pero se pierde la respuesta, reintentar el POST sin más podría duplicarlo. Por eso el laboratorio no aplica reintentos automáticos de creación.

### 4.1.7. Fallos que se parecen visualmente, pero significan cosas distintas

| Observación | Qué ha ocurrido | Cómo investigarlo |
|---|---|---|
| 200 con dos objetos | GET correcto | Revisar listado |
| 201 y nuevo ID | Alta aceptada | Leer producto devuelto |
| 400 | Petición rechazada por datos inválidos | Revisar cuerpo y validación |
| 404 | Recurso o ruta no encontrado | Revisar URL y endpoint |
| 500 | Error dentro del servidor | Revisar logs del servidor |
| Conexión rechazada | No se llegó a la API | Confirmar proceso y puerto |
| Timeout | No hubo respuesta a tiempo | Comprobar red y carga |
| JSON incompatible | Contrato cliente/servidor no coincide | Revisar DTO y respuesta |

Hay dos pruebas especialmente instructivas. Si apagamos la API y repetimos GET, no obtenemos un código 404 de ese servidor: no existe una respuesta HTTP válida. En cambio, si la API está activa y solicitamos \`api/ruta-inexistente\`, el servidor puede devolver 404. En ambos casos nuestra pantalla puede mostrar un mensaje general; recuperar y observar el estado con \`GetAsync\` permite distinguirlos.

Para ese diagnóstico, la variante es:

\`\`\`csharp
using var respuesta = await cliente.GetAsync("api/productos");
if (!respuesta.IsSuccessStatusCode)
{
    error = $"La API respondió {(int)respuesta.StatusCode}.";
    return;
}
productos = await respuesta.Content.ReadFromJsonAsync<List<ProductoDto>>() ?? [];
\`\`\`

No añadimos las dos alternativas simultáneamente: se sustituye la línea de \`GetFromJsonAsync\` por el bloque anterior. La versión explícita es más larga, pero conserva acceso al estado HTTP y por eso tiene un valor didáctico distinto.

### 4.1.8. Qué hemos construido, y qué todavía no

Ahora conocemos el recorrido de una petición entre dos procesos, los DTO, el comportamiento de GET y POST y la gestión visible de fallos. El componente todavía conoce detalles de comunicación: nombre del cliente y ruta HTTP. Ese acoplamiento fue útil para aprender el mecanismo, pero no será la estructura definitiva. En 4.2 veremos cómo separar esas responsabilidades sin cambiar la interfaz que utiliza el alumno.

## 4.2. Servicio tipado e inyección de dependencias

### 4.2.1. El problema de repetir llamadas HTTP en componentes

Supongamos que el catálogo, una página de resumen y un formulario necesitan consultar productos. Si las tres páginas llaman directamente a \`HttpClient\`, cada una repite rutas, deserialización y errores. Cuando cambie el contrato, habrá que corregir tres componentes. Separar responsabilidades no es un ejercicio ceremonial: evita que los detalles de infraestructura se propaguen a la interfaz.

En M03 ya utilizamos \`IProductosMemoriaService\`. Ahora definiremos \`IProductosApiService\` para expresar las operaciones que requiere la presentación, dejando al servicio la comunicación HTTP.

### 4.2.2. Diseñar la interfaz desde las necesidades del componente

\`\`\`csharp
using CursoWeb.Blazor.Models;

namespace CursoWeb.Blazor.Services;

public interface IProductosApiService
{
    Task<IReadOnlyList<ProductoDto>> ObtenerAsync();
    Task<ProductoDto> CrearAsync(CrearProductoDto solicitud);
}
\`\`\`

La interfaz habla de obtener y crear productos, no de endpoints. \`IReadOnlyList\` advierte al consumidor que no debe modificar la lista del servicio como si fuera un almacenamiento compartido. Los DTO hacen explícito el contrato: se solicita un objeto sin ID y se recibe otro con ID. No agregamos métodos Editar o Eliminar porque la API auxiliar de este módulo no ofrece esas operaciones.

### 4.2.3. Implementación completa y razonada

\`\`\`csharp
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
                "La API confirmó el alta sin devolver un producto.");
    }
}
\`\`\`

El constructor primario de C# 12 recibe el \`HttpClient\` ya configurado. Los componentes no tienen que crear la conexión ni conocer la dirección. Observa también qué **no** hace este servicio: no pinta errores en pantalla, no decide cuándo deshabilitar botones y no asigna un ID. Esas responsabilidades pertenecen a la vista y a la API respectivamente.

No convertimos los errores HTTP en colecciones vacías. Un catálogo vacío es un resultado válido; una desconexión es un fallo. Aunque ambos podrían producir una pantalla sin productos, su significado funcional es diferente.

### 4.2.4. De cliente con nombre a cliente tipado

En \`Program.cs\`, sustituimos el registro del cliente con nombre por:

\`\`\`csharp
builder.Services.AddHttpClient<IProductosApiService, ProductosApiService>(
    cliente =>
    {
        cliente.BaseAddress = new Uri(
            builder.Configuration["ProductosApi:BaseUrl"]
            ?? "http://localhost:5081/");
        cliente.Timeout = TimeSpan.FromSeconds(10);
    });
\`\`\`

El contenedor sabe ahora que una solicitud de \`IProductosApiService\` debe resolverse creando \`ProductosApiService\` con el cliente configurado. No añadimos innecesariamente un segundo \`HttpClient\` para las mismas operaciones. \`IHttpClientFactory\` gestiona los manejadores HTTP que se reutilizan; no necesitamos crear o destruir manualmente un cliente nuevo en cada evento de UI.

### 4.2.5. El refactor del componente: cambia el interior, no la experiencia

Antes:

\`\`\`csharp
var cliente = Clientes.CreateClient("ProductosApi");
productos = await cliente.GetFromJsonAsync<List<ProductoDto>>(
    "api/productos") ?? [];
\`\`\`

Después:

\`\`\`csharp
productos = (await CatalogoApi.ObtenerAsync()).ToList();
\`\`\`

La primera versión necesita \`@inject IHttpClientFactory Clientes\`. La segunda utiliza \`@inject IProductosApiService CatalogoApi\`. El botón de creación pasa a llamar \`CatalogoApi.CrearAsync(new CrearProductoDto(...))\`.

La experiencia del usuario debe permanecer igual: listado, formulario, mensaje de carga, error visible. Si el refactor cambia inadvertidamente el comportamiento, debemos investigar; **extraer código no justifica introducir una regresión funcional**.

### 4.2.6. Qué permite probar esta separación

Con la interfaz podemos pensar en una implementación de prueba que entregue una lista conocida sin ejecutar HTTP. También podemos comprobar el servicio HTTP de forma independiente. El módulo no exige un framework de mocking: basta comprender que los límites explícitos facilitan distinguir un fallo de presentación de uno de infraestructura.

En el siguiente punto abriremos el proceso servidor y construiremos una API mínima desde cero, manteniendo intactas las rutas que nuestro servicio tipado ya consume.

## 4.3. Construir desde cero la API REST auxiliar en ASP.NET Core

### 4.3.1. Por qué construimos una API si ya hemos utilizado otra

Los alumnos llegan al curso con conocimientos previos de Web API, por lo que no dedicaremos una jornada a repasar controladores, ORM o arquitecturas empresariales. Sin embargo, construir aquí una API pequeña completa permite **cerrar el circuito formativo**: en 4.1 recibimos una API ya operativa porque necesitábamos un servidor para practicar; ahora reproducimos su contrato y sustituimos ese servidor por otro que hemos creado nosotros.

La condición es conservar compatibilidad. Blazor seguirá llamando \`GET /api/productos\` y \`POST /api/productos\`. Si cambiáramos las rutas o el JSON al reconstruir el servidor, el cliente ya creado dejaría de funcionar.

### 4.3.2. El proyecto más pequeño que hospeda HTTP

Creamos la carpeta y el proyecto con el SDK:

\`\`\`powershell
dotnet new web -n CursoWeb.ProductosApi -f net8.0
cd CursoWeb.ProductosApi
dotnet run --urls http://localhost:5081
\`\`\`

\`dotnet new web\` genera un proyecto ASP.NET Core mínimo. No es la plantilla MVC, ni una API con controladores. \`Program.cs\` arranca un host web que podremos ampliar mediante Minimal APIs. Es importante detener primero la API suministrada en 4.1 para que dos procesos no intenten utilizar el mismo puerto.

Una primera respuesta útil consiste en:

\`\`\`csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/", () => "API de Productos disponible");
app.Run();
\`\`\`

Este estado sirve para separar problemas de arranque de problemas de serialización. Si no podemos consultar \`/\`, todavía no necesitamos investigar \`ProductoDto\` ni Blazor.

### 4.3.3. Modelos del servidor y almacenamiento deliberadamente simple

Añadimos los modelos del servidor:

\`\`\`csharp
record ProductoApi(int Id, string Nombre, decimal Precio);
record CrearProductoApi(string Nombre, decimal Precio);
\`\`\`

No son tipos del proyecto Blazor: están definidos en otro ensamblado. Lo que vincula ambas aplicaciones es el JSON intercambiado.

El catálogo inicial residirá en memoria:

\`\`\`csharp
using System.Collections.Concurrent;

var productos = new ConcurrentDictionary<int, ProductoApi>();
productos[1] = new ProductoApi(1, "Cuaderno", 2.50m);
productos[2] = new ProductoApi(2, "Lápiz", 0.80m);
var siguienteId = 2;
\`\`\`

\`ConcurrentDictionary\` hace seguras las operaciones básicas concurrentes que utilizamos y \`Interlocked.Increment\` evita reutilizar identificadores cuando llegan dos altas. No equivale a transacciones de una base de datos; al reiniciar la aplicación se pierde la información creada durante esa ejecución. Ese límite es intencional.

### 4.3.4. Primer endpoint de catálogo

\`\`\`csharp
app.MapGet("/api/productos", () =>
    Results.Ok(productos.Values.OrderBy(p => p.Id)));
\`\`\`

La ruta se asocia al verbo GET. \`Results.Ok\` crea una respuesta HTTP 200, y ASP.NET Core serializa la colección como JSON. Ordenamos expresamente por ID porque el orden interno del diccionario no forma parte del contrato.

El cliente de 4.2 espera una lista. Si sustituyéramos esa respuesta por un objeto \`{ cantidad: 2 }\`, la comunicación podría devolver 200, pero el servicio fallaría al intentar deserializar una \`List<ProductoDto>\`. La compatibilidad incluye **forma del cuerpo**, no solo URL.

### 4.3.5. Buscar por identificador y comprender 404

\`\`\`csharp
app.MapGet("/api/productos/{id:int}", (int id) =>
    productos.TryGetValue(id, out var producto)
        ? Results.Ok(producto)
        : Results.NotFound());
\`\`\`

El segmento \`{id:int}\` exige un entero. \`TryGetValue\` evita depender de una excepción cuando no existe el producto. El resultado 404 es una respuesta HTTP normal para un recurso desconocido. Este endpoint también permite que la cabecera \`Location\` de una creación señale una URL consultable.

### 4.3.6. Añadir POST y explicar cada decisión

\`\`\`csharp
app.MapPost("/api/productos", (CrearProductoApi entrada) =>
{
    if (string.IsNullOrWhiteSpace(entrada.Nombre) ||
        entrada.Precio <= 0)
    {
        return Results.BadRequest("Nombre y precio deben ser válidos.");
    }

    var id = Interlocked.Increment(ref siguienteId);
    var creado = new ProductoApi(id, entrada.Nombre.Trim(), entrada.Precio);
    productos[id] = creado;

    return Results.Created($"/api/productos/{id}", creado);
});
\`\`\`

ASP.NET Core deserializa el cuerpo JSON al parámetro \`CrearProductoApi\`. Después se aplican las reglas funcionales; un JSON sintácticamente válido puede contener datos que no satisfagan esas reglas. \`Results.BadRequest\` comunica 400 al cliente, mientras que \`Results.Created\` comunica 201 y proporciona el recurso construido por el servidor. El cliente no ha enviado un ID y no debe inventarlo.

Si enviamos \`{"nombre":"","precio":0}\`, obtenemos un rechazo. Si enviamos \`{"nombre":"Regla","precio":1.75}\`, obtenemos un nuevo objeto cuyo ID asigna la API.

### 4.3.7. Program.cs completo de la API construida

Las partes anteriores se integran en un archivo íntegro. En C# los tipos locales se declaran al final del archivo y \`app.Run()\` inicia el proceso que escucha las peticiones:

\`\`\`csharp
using System.Collections.Concurrent;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var productos = new ConcurrentDictionary<int, ProductoApi>();
productos[1] = new ProductoApi(1, "Cuaderno", 2.50m);
productos[2] = new ProductoApi(2, "Lápiz", 0.80m);
var siguienteId = 2;

app.MapGet("/", () => Results.Ok("API de Productos disponible"));

app.MapGet("/api/productos", () =>
    Results.Ok(productos.Values.OrderBy(p => p.Id)));

app.MapGet("/api/productos/{id:int}", (int id) =>
    productos.TryGetValue(id, out var producto)
        ? Results.Ok(producto)
        : Results.NotFound());

app.MapPost("/api/productos", (CrearProductoApi entrada) =>
{
    if (string.IsNullOrWhiteSpace(entrada.Nombre) || entrada.Precio <= 0)
        return Results.BadRequest("Nombre y precio deben ser válidos.");

    var id = Interlocked.Increment(ref siguienteId);
    var creado = new ProductoApi(id, entrada.Nombre.Trim(), entrada.Precio);
    productos[id] = creado;
    return Results.Created($"/api/productos/{id}", creado);
});

app.Run();

record ProductoApi(int Id, string Nombre, decimal Precio);
record CrearProductoApi(string Nombre, decimal Precio);
\`\`\`

El código es deliberadamente compacto, pero ya expresa los comportamientos que estudiaremos: arranque, GET, detalle 404, POST válido, POST inválido y almacenamiento temporal. No añade EF Core ni Identity porque esas tecnologías no son necesarias para comprender la interacción actual.

### 4.3.8. Probar primero el servidor y después Blazor

El mejor orden de diagnóstico es empezar por el proceso API. Consultamos \`http://localhost:5081/api/productos\` y debemos ver Cuaderno y Lápiz. Enviamos un POST válido y observamos 201; enviamos uno inválido y observamos 400. Consultamos un ID inexistente y obtenemos 404. Solo cuando el servidor satisface ese contrato iniciamos Blazor y volvemos a abrir \`/catalogo-remoto\`.

Si la API responde correctamente a un cliente HTTP directo, pero Blazor no muestra datos, el problema se ha acotado: revisaremos la configuración de base URL, el servicio tipado o los DTO. Si la API ni siquiera responde a GET, revisar los componentes Razor no es una forma eficiente de investigar.

### 4.3.9. Ampliar sin romper lo existente: resumen

Como ejercicio de extensión podemos añadir un endpoint distinto:

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

Tras arrancar con dos productos, devolverá cantidad 2 y precioTotal 3,30. Tras crear Regla por 1,75, cantidad 3 y precioTotal 5,05. Esa salida **no** se lee como una lista de \`ProductoDto\`; es un contrato diferente en una ruta diferente.

\`/api/productos/resumen\` no entra en conflicto con la ruta \`{id:int}\` porque «resumen» no es un entero. Podemos ampliar el resultado con \`hayProductos = actuales.Length > 0\` sin afectar la lista que consume Blazor. La práctica pedirá activar estas variantes por separado, conservando un estado compilable.

## 4.4. Seguridad básica: identificar, autorizar y presentar

### 4.4.1. Las tres preguntas que no deben confundirse

**Autenticación** pregunta quién es el usuario. **Autorización** pregunta qué recursos puede utilizar ese usuario. **Presentación condicional** decide qué parte de una interfaz se muestra según el estado conocido. Son operaciones relacionadas, pero ocultar un botón no equivale a impedir que una petición llegue a un endpoint.

Una identidad en ASP.NET Core puede expresarse mediante claims. Un claim contiene una afirmación como nombre o rol:

\`\`\`csharp
var claims = new[]
{
    new Claim(ClaimTypes.Name, "AlumnoDemo"),
    new Claim(ClaimTypes.Role, "Formador")
};
var identidad = new ClaimsIdentity(claims, "CookiesDemo");
var principal = new ClaimsPrincipal(identidad);
\`\`\`

El esquema de autenticación permite a ASP.NET Core reconocer la identidad. Un rol como \`Formador\` es útil para demostrar autorización. No implica que exista gestión real de usuarios.

### 4.4.2. Qué aporta Identity y qué no construiremos aquí

ASP.NET Core Identity ofrece gestión real de usuarios, contraseñas y otras funciones de identidad. El objetivo de M04 no es configurar una aplicación completa con Identity, base de datos, restablecimiento de contraseñas y proveedores externos. Usaremos un inicio de sesión **local de demostración**, con un código fijo para comprobar el flujo de cookies.

Ese código no es una contraseña segura. La demostración debe permanecer en entorno de desarrollo y no utilizarse como mecanismo de autenticación de una aplicación publicada. Para un sistema real se necesita un proveedor legítimo de identidades, HTTPS, gestión adecuada de cookies y secretos, y políticas de seguridad revisadas.

### 4.4.3. Registrar autenticación por cookies

\`\`\`csharp
builder.Services.AddAuthentication("CookiesDemo")
    .AddCookie("CookiesDemo", opciones =>
    {
        opciones.LoginPath = "/seguridad";
    });
builder.Services.AddAuthorization();
builder.Services.AddCascadingAuthenticationState();
\`\`\`

El middleware se incorpora antes de mapear recursos:

\`\`\`csharp
app.UseAuthentication();
app.UseAuthorization();
app.UseAntiforgery();
\`\`\`

El primer middleware interpreta la credencial; el segundo aplica reglas; el antiforgery protege solicitudes que cambian estado cuando se comprueba adecuadamente su token. Para este laboratorio, el servidor debe verificar de forma explícita el token del formulario de inicio y cierre de sesión.

### 4.4.4. AuthorizeView y autorización del servidor

Dentro de un componente:

\`\`\`razor
<AuthorizeView>
    <Authorized>
        <p>Usuario: @context.User.Identity?.Name</p>
    </Authorized>
    <NotAuthorized>
        <p>La sesión no está autenticada.</p>
    </NotAuthorized>
</AuthorizeView>
\`\`\`

\`AuthorizeView Roles="Formador"\` permite mostrar un bloque en función del rol. Si anidamos dos \`AuthorizeView\`, sus plantillas no pueden usar implícitamente el mismo nombre \`context\`: debemos asignar un contexto distinto al componente interior, por ejemplo \`Context="rolContexto"\`. Es una cuestión de plantillas Razor, no de autorización.

El recurso protegido debe declarar su regla en el servidor:

\`\`\`csharp
app.MapGet("/demo/privado", () =>
    Results.Ok(new { mensaje = "Recurso protegido" }))
    .RequireAuthorization(p => p.RequireRole("Formador"));
\`\`\`

Ahora incluso quien conoce la URL tiene que satisfacer la política. En nuestra demostración la API de Productos sigue siendo pública: el inicio de sesión de Blazor no protege automáticamente otro proceso ni sustituye políticas de la API.

### 4.4.5. Por qué utilizamos formularios HTTP normales

Una respuesta HTTP debe poder incluir la cabecera que establece la cookie. En un evento de un componente Interactive Server que ya está funcionando, intentar cambiar cabeceras de una respuesta iniciada es problemático. Por eso el acceso se realiza con un formulario POST convencional y una navegación completa.

\`\`\`razor
<form method="post" action="/demo/entrar" data-enhance="false">
    <AntiforgeryToken />
    <label>Código local:
        <input name="codigo" type="password" />
    </label>
    <button type="submit">Iniciar sesión</button>
</form>
\`\`\`

El servidor comprueba el antiforgery, valida **solo el código de laboratorio**, construye el principal de claims, ejecuta \`SignInAsync\` y redirige al navegador. La salida usa otro formulario POST con \`SignOutAsync\` y protección antiforgery. No usamos GET para cambiar el estado de la sesión.

### 4.4.6. Qué resultados debemos distinguir

| Situación | Observación correcta |
|---|---|
| Anónimo abre la página | Se muestra \`NotAuthorized\` |
| Anónimo solicita recurso protegido | Servidor impide recibir contenido privado |
| Código local incorrecto | No se crea sesión |
| Código correcto y token válido | Navegador recibe cookie de demostración |
| Sesión con rol Formador | \`AuthorizeView\` muestra rol y servidor autoriza recurso |
| Salida POST válida | Se elimina sesión |
| POST sin antiforgery válido | Servidor rechaza solicitud |

**La conclusión del módulo** no es que un inicio de sesión de ejemplo convierta cualquier aplicación en segura. La conclusión es que cada responsabilidad reside en un límite distinto: la interfaz presenta, el servicio comunica, la API valida sus operaciones y la autorización protege los recursos del servidor.

## Cierre conceptual de M04

El aprendizaje de 4.1–4.4 forma una secuencia: primero comprendemos la comunicación HTTP, después encapsulamos esa comunicación en un servicio, a continuación construimos el servidor que satisface el contrato y finalmente observamos qué significa proteger realmente un recurso. En el módulo 5 utilizaremos estas bases para consolidar el proyecto y abordar las demostraciones elementales de publicación sin ampliar innecesariamente la infraestructura.
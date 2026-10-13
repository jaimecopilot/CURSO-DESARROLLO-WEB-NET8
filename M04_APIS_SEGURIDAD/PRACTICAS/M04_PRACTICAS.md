# M04 — Prácticas: integración con APIs y seguridad básica

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

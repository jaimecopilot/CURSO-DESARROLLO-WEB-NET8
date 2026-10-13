# M05 — Consolidación de Blazor y despliegue elemental

## Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8

**CURSO: Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8**

**TIPO: TEORÍA**

**AUTOR: JAIME GALLO**

## Índice del módulo

- [5.1 — Consolidación del proyecto Blazor](#punto-1)
- [5.2 — Ejecutar, compilar y publicar ASP.NET Core](#punto-2)
- [5.3 — Kestrel y la aplicación publicada](#punto-3)
- [5.4 — Hospedaje elemental con IIS](#punto-4)
- [5.5 — Docker: imagen, contenedor y puertos](#punto-5)

## Presentación del módulo

Una aplicación web no está terminada porque sus archivos compilen. Debemos entender cómo cooperan los componentes de interfaz, los servicios y el servidor, y distinguir el proceso de desarrollo del proceso que ejecutará una publicación. Este último módulo reúne dos recorridos que se apoyan en conocimientos ya adquiridos: el cierre funcional del cliente **Blazor B** y la publicación elemental de la aplicación **MVC A**.

El curso continúa utilizando .NET 8, Visual Studio y, cuando corresponde al CRUD, SQL Server Express LocalDB. La base no cambia a SQLite para simplificar un despliegue. Tampoco se presenta el laboratorio como guía de operación empresarial: la configuración de HTTPS público, proxies externos, endurecimiento, contenedores con persistencia y automatización de infraestructura quedan fuera del itinerario.

En el punto 5.1 observaremos un recorrido Blazor → HTTP → API → respuesta → componente. En 5.2–5.5 compararemos la misma aplicación ASP.NET Core MVC bajo tres formas elementales de ejecución: publicación con Kestrel, hospedaje mediante IIS y contenedor Docker. Los ejemplos explicativos de este manual pueden ser independientes; la secuencia de construcción exacta, sus rutas y sus estados pertenecen al manual de prácticas.

La secuencia presencial reserva 60 minutos para conceptos, 270 minutos para construcción y verificación, y 30 minutos para dudas. Los estudios de ampliación no añaden obligaciones a esa jornada.

## 5.1. Consolidación: seguir una operación Blazor desde el navegador hasta la API

### 5.1.1. El sistema es más que la suma de sus archivos

Al terminar M03 la aplicación Blazor representaba información y actualizaba estado mediante componentes interactivos. Durante M04 se incorporó una API HTTP pequeña y se trasladó la comunicación a un servicio tipado. Ahora debemos explicar el comportamiento del conjunto sin perder de vista una separación fundamental: **una lista dibujada en el navegador, una colección que vive en un componente y los datos que conserva la API no son el mismo objeto ni tienen necesariamente la misma duración**.

Pensemos en una tienda de material de oficina. Cuando alguien abre «Catálogo remoto», no es la página HTML la que consulta una base SQL Server. El host Blazor Interactive Server crea o utiliza un circuito interactivo, construye el componente, resuelve el servicio configurado y este hace GET a la API. La API devuelve JSON que el cliente transforma en objetos .NET; finalmente, Blazor renderiza el estado. Si la API deja de responder, no desaparece necesariamente el servidor Blazor: la interfaz sigue siendo capaz de mostrar un error que explica el fallo.

Conviene separar seis responsabilidades:

| Pieza | Qué conoce | Qué no debería decidir |
|---|---|---|
| Componente Razor | Estado de pantalla, presentación y eventos | Direcciones HTTP repetidas y contratos de transporte |
| DTO de producto | Campos intercambiados con la API | Ciclo de vida visual o acceso a una base |
| Interfaz de servicio | Operaciones de consulta y creación | Componentes concretos que las utilizan |
| Servicio HTTP | URL relativa, serialización y errores | Cómo se diseña la pantalla |
| HttpClient | Transporte, cabeceras, conexión y timeout | Reglas de negocio de productos |
| API | Validación del dato, identificador y respuesta HTTP | Vista que el cliente mostrará |

El beneficio no es puramente estético. Si otra interfaz consume la API, el endpoint puede mantenerse. Si la API cambia de dirección, el cliente tipado puede volver a configurarse sin modificar la presentación. Si un producto es inválido, corresponde al servidor rechazarlo aunque la pantalla hubiera realizado comprobaciones previas.

### 5.1.2. Diagrama de comunicación y modelo Interactive Server

~~~mermaid
sequenceDiagram
participant Navegador as Navegador
participant Blazor as Componente Blazor
participant Servicio as Servicio tipado
participant API as API Productos
Navegador->>Blazor: Abrir catálogo remoto
Blazor->>Servicio: ObtenerAsync()
Servicio->>API: GET /api/productos
API-->>Servicio: 200 + JSON
Servicio-->>Blazor: Lista de ProductoDto
Blazor-->>Navegador: Renderizar catálogo
Navegador->>Blazor: Crear un producto
Blazor->>Servicio: CrearAsync(dto)
Servicio->>API: POST /api/productos + JSON
API-->>Servicio: 201 + nuevo producto
Servicio-->>Blazor: ProductoDto creado
Blazor-->>Navegador: Actualizar la pantalla
~~~

El diagrama representa una llamada HTTP desde **el servidor Blazor** en Interactive Server, no un fetch automático iniciado por JavaScript en el navegador. Esta diferencia afecta a las reglas CORS y al diagnóstico de conectividad: en este recorrido quien necesita llegar a la API es el proceso ASP.NET Core que ejecuta Blazor. La web puede abrirse correctamente mientras falla la consulta remota.

Recibir 200 no equivale a disponer de un DTO válido: el cuerpo podría no ser JSON. Por eso existe una etapa de deserialización y después otra de actualización del estado, ambas susceptibles de error. La operación POST añade un identificador que decide el servidor. Si dos personas crean productos al mismo tiempo, la interfaz no debe adivinar el próximo ID a partir del número de elementos visibles.

### 5.1.3. Ejemplo teórico independiente: clasificar fallos HTTP

Antes de estudiar el proyecto de prácticas, consideremos un servicio de lectura de avisos. Permite distinguir una respuesta HTTP de error, un fallo de conexión y una respuesta imposible de deserializar. El ejemplo presupone un proyecto ASP.NET Core con los tipos definidos y el espacio de nombres `System.Net.Http.Json`.

~~~csharp
using System.Net.Http.Json;

public sealed record AvisoDto(int Id, string Texto);

public sealed class AvisosHttpService(HttpClient http)
{
    public async Task<IReadOnlyList<AvisoDto>> ObtenerAsync(
        CancellationToken cancelacion = default)
    {
        using var respuesta =
            await http.GetAsync("api/avisos", cancelacion);

        // Una respuesta recibida también puede ser 404 o 500.
        respuesta.EnsureSuccessStatusCode();

        // HTTP 200 no garantiza por sí solo JSON válido.
        return await respuesta.Content
            .ReadFromJsonAsync<List<AvisoDto>>(cancelacion)
            ?? throw new InvalidOperationException(
                "Se esperaba una colección de avisos.");
    }
}
~~~

La API de avisos es solo un escenario explicativo: **no constituye una tercera aplicación que el alumno tenga que construir**. Para usar este servicio sería necesario registrar un HttpClient con dirección base y proporcionar un endpoint compatible.

Si el servidor devuelve 404, `EnsureSuccessStatusCode` genera `HttpRequestException`. Si no hay conexión, también puede producirse `HttpRequestException`, pero sin una respuesta 404 que examinar: no debe confundirse ausencia de respuesta con «recurso inexistente». Si se supera el timeout, puede manifestarse como `TaskCanceledException`. Una respuesta 200 con JSON incompatible puede producir `JsonException`. Los mensajes del componente deben corresponder a la causa observada, evitando atribuir indiscriminadamente todos los fallos a una misma capa.

### 5.1.4. GET, POST y representación de datos

GET solicita la representación actual de un recurso. POST solicita en este curso crear uno nuevo; una operación satisfactoria devuelve **201 Created** con representación del nuevo producto y una ubicación. Por ejemplo:

~~~http
HTTP/1.1 201 Created
Location: /api/productos/3
Content-Type: application/json

{"id":3,"nombre":"Regla","precio":1.75}
~~~

Un cliente puede añadir el DTO devuelto a la lista que ya representa o consultar de nuevo el catálogo. La primera opción evita otra petición, pero esa lista podría estar desactualizada si existen otros clientes. La segunda opción obtiene otra representación del servidor, con coste de red y con una nueva posibilidad de error.

Ninguna opción cambia el modelo de persistencia. La API docente de M04 aloja una colección de productos **en memoria**. Reiniciar su proceso restaura los productos iniciales. Por el contrario, el CRUD MVC de M02 usa SQL Server Express LocalDB: es otro modelo de almacenamiento y otra competencia. Una recarga del componente, un reinicio del servidor Blazor y un reinicio de la API son acciones distintas, con efectos distintos.

### 5.1.5. Validación local y validación del servidor

Una comprobación local evita envíos innecesarios y permite corregir pronto los datos:

~~~csharp
public sealed record CrearProductoDto(string Nombre, decimal Precio);

public static class ReglasEntrada
{
    public static bool EsValida(CrearProductoDto entrada) =>
        !string.IsNullOrWhiteSpace(entrada.Nombre) &&
        entrada.Precio > 0;
}
~~~

No obstante, el servidor debe comprobar el contrato porque otros clientes pueden llamarlo directamente. La interfaz no es una barrera de integridad. En el laboratorio:

| Resultado | Significado | Acción pedagógica |
|---|---|---|
| 200 OK en GET | Se obtuvo una representación | Comprobar JSON y renderizado |
| 201 Created en POST | El recurso fue creado | Consultar Location y nuevo ID |
| 400 Bad Request | La entrada no satisface el contrato | Corregir nombre/precio |
| 404 Not Found | No existe la ruta/recurso solicitado | Revisar ruta e identificador |
| Error de red | No se obtuvo respuesta HTTP utilizable | Comprobar proceso y puerto |

Esta distinción permite diagnosticar de forma causal: que el botón no funcione no demuestra que el problema esté en Blazor. Debemos observar la petición y la respuesta en el punto adecuado.

### 5.1.6. El servicio tipado e inyección de dependencias

El registro de un cliente tipado asocia `IProductosApiService` con `ProductosApiService` y proporciona HttpClient ya configurado. El componente consume la interfaz, no una URL repetida:

~~~csharp
builder.Services.AddHttpClient<IProductosApiService, ProductosApiService>(
    cliente =>
    {
        cliente.BaseAddress = new Uri("http://localhost:5081/");
        cliente.Timeout = TimeSpan.FromSeconds(10);
    });
~~~

El fragmento presupone que ambos tipos existen. La dirección base de ejemplo es local; puede leerse desde `appsettings.json` para evitar cambiar código al usar otro puerto. Las rutas relativas de los métodos del servicio deben combinarse con esa dirección. No se modifica la clase de presentación simplemente para corregir la ubicación del servidor.

### 5.1.7. Seguridad: recordar límites, no bloquear el laboratorio

La ampliación Identity/JWT de M04 permanece independiente. El catálogo básico de M05 usa una API pública de productos en memoria; no necesita token JWT ni conectarse a las tablas de usuarios. Tampoco una interfaz se vuelve segura por ocultar un botón: la autorización es una decisión del servidor.

Este límite es fundamental para no volver irrealizable una jornada de seis horas. P5.1 necesita **Blazor B y API de productos**. La ampliación Identity/JWT puede revisitarse posteriormente, pero no se añade como dependencia del recorrido principal.

### 5.1.8. Diagnóstico causal antes de modificar código

Si Blazor abre pero no muestra la lista, abrir la URL de la API directamente permite comprobar si hay respuesta. Si devuelve 404, revisar ruta. Si devuelve 200 con contenido inesperado, revisar contrato JSON. Si funciona directamente pero falla desde Blazor, revisar `ProductosApi:BaseUrl`, servicio registrado y errores del componente. Si el nuevo producto aparece y desaparece después del reinicio de la API, recordar que esta utiliza memoria.

La diferencia entre error de red, error HTTP, error de serialización, error de validación y estado local obsoleto debe poder explicarse antes de finalizar este punto. El alumno no necesita crear más arquitectura para demostrarlo; necesita poder seguir un recorrido ya construido y entender cada decisión.

### 5.1.9. Síntesis

El resultado formativo es una aplicación Blazor que consulta, crea, valida, informa de fallos y permite refrescar sus datos. Más importante todavía: el alumno es capaz de identificar quién mantiene cada estado y cuál es el origen de una respuesta. Esa comprensión permite pasar de «la pantalla funciona» a «sé por qué funciona y cómo repararla».

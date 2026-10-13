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



### 5.1.10. Una respuesta útil no es lo mismo que una pantalla actualizada

Conviene estudiar un problema que aparece incluso cuando ninguna línea de código contiene un error sintáctico. Imaginemos que la API conserva dos productos y que una persona abre el catálogo Blazor. El servidor Blazor obtiene dos DTO, los convierte en una lista y el componente dibuja dos elementos. Mientras esa persona sigue mirando la pantalla, otro cliente ejecuta un POST válido y la API pasa a conservar tres productos.

En ese instante existen dos afirmaciones compatibles: **el servidor dispone de tres productos** y **el componente representa dos**. La primera describe el estado del origen de datos; la segunda, una instantánea obtenida anteriormente. La aplicación no ha incorporado un mecanismo de notificación de cambios. Por tanto, no tiene por qué producirse una actualización espontánea en la interfaz.

Esta observación evita un diagnóstico equivocado. El sistema no ha perdido el tercer producto. Tampoco hay evidencia de que el renderizado esté roto. Para afirmar cualquiera de esas cosas habría que consultar al servidor y comparar ambas representaciones.

**Modelo temporal de una consulta.**

| Instante | Acción | API | Lista del componente | Pantalla |
|---|---|---|---|---|
| T0 | Arranca la API | Cuaderno, Lápiz | No creada | Sin catálogo |
| T1 | Se abre Blazor y se completa GET | Cuaderno, Lápiz | Dos elementos | Dos elementos |
| T2 | Un cliente externo crea Regla | Tres elementos | Dos elementos | Dos elementos |
| T3 | El usuario solicita una nueva consulta | Tres elementos | Tres elementos | Tres elementos |
| T4 | Se reinicia únicamente la API en memoria | Cuaderno, Lápiz | Tres elementos | Tres elementos |
| T5 | Una nueva consulta termina con 200 | Cuaderno, Lápiz | Dos elementos | Dos elementos |

La tabla deliberadamente separa un cambio en el servidor de una modificación de la colección local. En T4 todavía pueden verse tres productos, aunque el nuevo proceso de API tenga dos. La interfaz solo se reconciliará con el servidor después de una consulta posterior. Si el GET de T5 falla, el resultado visual dependerá de cómo esté implementado el tratamiento de errores: se podría conservar la lista antigua o sustituirla por un estado de error. No hay que deducir la estrategia únicamente del código de la API.

**Ejemplo conceptual de actualización explícita.** Una función responsable de consultar no necesita conocer cómo se inició la operación; tanto el ciclo de vida como un botón pueden llamarla:

~~~csharp
private async Task ActualizarAsync()
{
    var nuevos = await Servicio.ObtenerAsync();
    productos = nuevos.ToList();
}
~~~

Este fragmento es deliberadamente pequeño para mostrar **una única responsabilidad**: obtener una nueva representación y sustituir la anterior. No contiene manejo de errores, bandera de carga ni HTML. Todos esos aspectos se estudiaron por separado y se integran en el proyecto real. Si se añadieran directamente a este primer fragmento, sería más difícil ver que la sustitución de la colección es el punto exacto en que cambia el estado visible.

### 5.1.11. El ciclo de vida no sustituye los eventos de la interfaz

`OnInitializedAsync` se ejecuta durante la inicialización del componente. Es adecuado para la primera consulta porque el usuario aún no ha tenido ocasión de pulsar un botón. No equivale, sin embargo, a «consultar siempre que alguien necesite datos». Si el componente sigue vivo, un cambio producido en otro sistema no vuelve a llamar automáticamente a `OnInitializedAsync`.

Podríamos copiar las mismas instrucciones HTTP en el método de inicialización y en el manejador del botón. El resultado quizá funcionaría inicialmente, pero tendríamos dos sitios donde mantener los mensajes, el estado de carga, el tratamiento de errores y la lógica de actualización. La duplicación generaría un problema pedagógico y técnico: cada corrección posterior tendría que aplicarse en ambos caminos.

La alternativa es hacer que ambas entradas convoquen **una misma operación con nombre**:

~~~csharp
protected override Task OnInitializedAsync() => ConsultarAsync();

private async Task ConsultarAsync()
{
    cargando = true;
    error = null;

    try
    {
        productos = (await CatalogoApi.ObtenerAsync()).ToList();
    }
    catch (HttpRequestException)
    {
        error = "No se pudo obtener el catálogo remoto.";
    }
    finally
    {
        cargando = false;
    }
}
~~~

El fragmento presupone campos de componente y un servicio ya registrados. Es ilustrativo y no pretende sustituir la implementación definitiva, que también trata cancelación y errores JSON. La transformación importante no es añadir más código sino **sacar una operación reutilizable** de un lugar que solo se ejecuta una vez.

Ahora comparemos dos recorridos. En el primero, Blazor inicializa el componente y llama a `ConsultarAsync`. En el segundo, el navegador envía el evento del botón y vuelve a llamar a `ConsultarAsync`. Después del punto de entrada, el flujo es idéntico: bandera de carga, servicio HTTP, asignación de lista, finalización. Un cambio en el método beneficia a ambos recorridos y evita que el botón se comporte de modo distinto al arranque.

En Interactive Server, el manejador del evento es código .NET ejecutado en el servidor, no JavaScript escrito por nosotros. La conexión interactiva mantiene la comunicación necesaria con el navegador. Este detalle importa cuando se depura: que un botón tenga `@onclick` no significa que se esté efectuando un `fetch` directamente desde el navegador.

### 5.1.12. Cuatro estados visuales que no deben confundirse

Un componente que consulta una API no tiene solamente los estados «funciona» y «falla». Al menos conviene distinguir **consulta pendiente**, **error**, **respuesta válida sin productos** y **respuesta válida con productos**.

Para expresar esas posibilidades mediante las propiedades ya conocidas se puede usar la siguiente condición conceptual:

~~~razor
@if (cargando)
{
    <p>Consultando el servidor...</p>
}
else if (error is not null)
{
    <p role="alert">@error</p>
}
else if (productos.Count == 0)
{
    <p>No hay productos disponibles.</p>
}
else
{
    <ul>
        @foreach (var producto in productos)
        {
            <li>@producto.Nombre</li>
        }
    </ul>
}
~~~

La distinción entre `productos.Count == 0` y `error is not null` es esencial. Un servicio puede devolver correctamente `[]`; esa respuesta no indica una avería. Y un fallo de red puede ocurrir incluso cuando la última lista recibida contiene elementos. La interfaz necesita representar ambas realidades sin decir que el servidor está vacío cuando ni siquiera ha respondido.

Una respuesta HTTP 200 acompañada de `[]` satisface el contrato de una colección. Una respuesta HTTP 200 acompañada de `{"mensaje":"listo"}` **no** satisface necesariamente el contrato esperado por un cliente que deserializa `List<ProductoDto>`. El código de estado HTTP solo responde a una parte de la pregunta. El contenido tiene que ser coherente con el tipo que el servicio ha solicitado.

Finalmente, conviene identificar el problema del **estado anterior visible mientras se carga**. Algunos diseños sustituyen la lista por una indicación de carga; otros conservan la lista e incorporan un indicador discreto. Ambas decisiones pueden ser correctas según el uso. Lo que no es correcto es presentar sin matices una lista anterior como si acabara de confirmarse desde el servidor. En el curso se adopta una solución sencilla: la consulta modifica las banderas de carga y error, y el componente ofrece una respuesta visual inequívoca.

### 5.1.13. El significado de `await` y las transiciones de estado

Una consulta asincrónica devuelve una tarea; no devuelve inmediatamente los productos. Cuando un método hace `await` sobre esa tarea, permite que el entorno gestione otras operaciones mientras llega la respuesta. Eso no quiere decir que el resultado pueda consumirse antes de que la tarea termine.

Examinemos el orden de instrucciones:

~~~csharp
cargando = true;
error = null;

try
{
    var respuesta = await CatalogoApi.ObtenerAsync();
    productos = respuesta.ToList();
}
finally
{
    cargando = false;
}
~~~

La asignación a `productos` se ejecuta **después** de obtener `respuesta`. Si la consulta falla, esa asignación no se ejecuta. En cambio, el bloque `finally` se ejecuta tanto en una terminación satisfactoria como en una excepción. Así se evita dejar el botón inutilizable por una bandera `cargando` que permaneciera en `true` para siempre.

Los `catch` no son sustitutos del `finally`. Sirven para expresar qué error se observó y qué decisión toma el componente. La comprobación de que la operación terminó corresponde a un bloque que se ejecuta con independencia del resultado. Esta separación es una regla útil para otros ejemplos asincrónicos del curso: también la acción de crear tiene una bandera de envío que debe restaurarse.

**Pregunta razonada.** ¿Qué ocurriría si `cargando = false` estuviera exclusivamente después del `await`, fuera de un `finally`, y la llamada fallara? La ejecución abandonaría el bloque antes de llegar a esa línea. La interfaz podría seguir mostrando «Cargando...» e impedir nuevas pulsaciones aunque la solicitud ya hubiera terminado con un error. El fallo sería de gestión de estado local, no de la API.

**Otra pregunta.** ¿Por qué se borra el error anterior antes de consultar? Porque una nueva solicitud representa una oportunidad de recuperarse. Si el servidor había estado caído y vuelve a responder, no es coherente seguir mostrando la advertencia de la petición anterior después de recibir una lista satisfactoria.

### 5.1.14. La creación y el identificador pertenecen al servidor

Un formulario de creación recoge nombre y precio. La pantalla puede comprobar que el nombre no está vacío y que el precio es positivo, pero esa comprobación no crea un recurso en el servidor. Para ello hace falta una solicitud POST que el servidor valide y procese.

Imaginemos que una página muestra dos productos y decide asignar al siguiente el identificador `productos.Count + 1`, que sería 3. Si otro cliente ha creado un producto antes, el identificador 3 podría estar ocupado. Si se eliminara un elemento, la cuenta visible tampoco tendría por qué corresponderse con el siguiente identificador válido. En consecuencia, la interfaz no debe calcular el ID.

El patrón correcto para un alta es:

~~~csharp
var entrada = new CrearProductoDto(nombre.Trim(), precio);
var creado = await CatalogoApi.CrearAsync(entrada);
productos.Add(creado);
~~~

Aquí `creado` es la representación devuelta por el servidor. El servicio HTTP debe comprobar primero que recibió una respuesta satisfactoria y deserializar el cuerpo esperado. Solo después de obtener ese objeto tiene sentido incorporarlo a la colección del componente.

Si el POST devuelve **400**, el componente no debería añadir el producto como si hubiese sido creado. Si la respuesta devuelve **201** pero el cuerpo JSON está incompleto, tampoco debería construir artificialmente el identificador. En ambos casos corresponde mostrar información suficiente para investigar y preservar la coherencia de la interfaz.

La diferencia entre recargar toda la lista después de POST y añadir el resultado del POST a la lista existente debe explicarse como una **decisión de sincronización**. Añadir el resultado es eficiente cuando se acaba de crear un recurso válido. Volver a consultar ofrece una instantánea más reciente del catálogo completo. En este curso se pueden observar ambas alternativas sin introducir sistemas de notificación en tiempo real.

### 5.1.15. Una lista en memoria y una base de datos SQL Server no comparten garantías

En M02 el proyecto MVC A utiliza EF Core y SQL Server Express LocalDB. La aplicación crea un contexto, realiza consultas y guarda cambios en una base de datos. Los datos persisten con independencia de que el proceso web termine, mientras la base esté disponible y no se elimine. En M04 y P5.1 la API docente mantiene un diccionario de productos dentro de su proceso.

Esta diferencia no es un detalle de instalación. Cambia lo que puede afirmarse sobre el resultado de una operación. Si un POST añade Regla a una colección estática en memoria, una consulta posterior al mismo proceso la encontrará. Sin embargo, al detener y reiniciar la API se inicializarán otra vez los valores de partida. Ese comportamiento es esperado, no una pérdida accidental que deba corregirse trasladando la API a SQLite.

Comparación causal:

| Pregunta | API de productos en memoria | MVC con EF Core y LocalDB |
|---|---|---|
| ¿Quién conserva la información? | El proceso ASP.NET Core | El motor SQL Server LocalDB |
| ¿Qué sucede al reiniciar solo el proceso web? | Se recrea la colección inicial | Los datos de la base siguen disponibles |
| ¿Hace falta instalar LocalDB para GET y POST de P5.1? | No | No aplica a esa API |
| ¿Se puede afirmar persistencia por recibir 201? | No | La persistencia se comprueba según el flujo EF |
| ¿Es adecuada para la demostración de despliegue Linux de M05? | No se usa allí | El CRUD de MVC requiere SQL Server real |

La última fila ayuda a entender una restricción posterior: en el contenedor Docker del curso se publica MVC A, pero **no se instala LocalDB dentro del contenedor Linux**. El ejercicio demostrará que el proceso MVC y sus recursos básicos se sirven; no fingirá que el CRUD con base de datos está disponible allí.

### 5.1.16. Recorrido de diagnóstico en seis preguntas

Cuando una operación falla, una secuencia de preguntas reduce las modificaciones improvisadas:

**Primera: ¿existe el proceso que debería atender la solicitud?** Ver un navegador abierto no demuestra que siga vivo el proceso de API. Consultar su consola y su URL directa permite distinguir la ausencia de servicio de un error del componente.

**Segunda: ¿se utiliza la dirección correcta?** `http://localhost:5081/` identifica en el ejemplo el servidor API; `http://localhost:5092/` identifica Blazor. Una respuesta de la página inicial Blazor no demuestra que el endpoint de productos haya recibido la solicitud. Deben verificarse host, puerto y ruta.

**Tercera: ¿la API contesta y con qué estado?** Un 404 demuestra que el servidor recibió la solicitud, pero no encontró el recurso solicitado. Un error de conexión significa que no se consiguió una respuesta HTTP equivalente. Son hechos distintos y requieren actuaciones distintas.

**Cuarta: ¿el cuerpo responde al contrato?** Un 200 puede contener `[]`, una lista de productos válida o un texto que no es JSON. Leer el cuerpo ayuda a separar fallo de transporte y fallo de interpretación.

**Quinta: ¿el servicio transforma correctamente el resultado?** Si la API devuelve datos válidos y Blazor sigue mostrando un error, revisar el servicio tipado, su configuración de dirección base y la excepción concreta. No duplicar rutas HTTP en el componente para eludir la investigación.

**Sexta: ¿la interfaz está presentando el estado recibido?** Aunque la red funcione, una colección no actualizada o una bandera de carga incorrecta pueden hacer que la página parezca rota. Examinar el método que asigna `productos` y el orden de condiciones Razor suele resultar más útil que añadir un nuevo proyecto.

El orden importa. Empezar por cambiar la UI sin comprobar el servidor puede ocultar una avería externa; empezar por la API sin considerar el estado del componente puede atribuir al servidor un fallo de renderizado. La clave es aislar primero la capa donde el resultado deja de coincidir con el contrato.

### 5.1.17. Caso integral resuelto: el producto que parece desaparecer

Una persona crea Regla desde Blazor. La página recibe un DTO con ID asignado por la API y lo añade a la lista. Todo parece correcto. Después, el docente detiene y vuelve a iniciar la API. En la pantalla anterior todavía figura Regla. Al pulsar «Consultar servidor» desaparece.

¿Por qué se produce este comportamiento? El POST creó el producto en memoria, no en SQL Server. El reinicio volvió a poblar la colección inicial. La pantalla mantenía una representación anterior hasta ejecutar una consulta nueva. La actualización no eliminó por error un registro persistente: mostró el contenido del nuevo proceso.

¿Qué observaciones permitirían confirmar la explicación? Antes del reinicio, un GET directo a la API devuelve Regla. Después del reinicio, el mismo GET devuelve solo los productos iniciales. Mientras tanto, antes de recargar Blazor, la pantalla puede conservar Regla. Al consultar explícitamente, la UI coincide con la última respuesta. Se han identificado tres estados y una secuencia de eventos sin introducir herramientas ajenas al temario.

¿Qué corrección no deberíamos aplicar? No deberíamos modificar MVC A ni sustituir LocalDB por SQLite ni incorporar Identity/JWT a esta API para conseguir persistencia. La API en memoria cumple exactamente el papel docente del módulo. Si se quisiera implementar persistencia duradera en otro curso, habría que plantear explícitamente otro contrato, otra infraestructura y nuevas pruebas. Eso no forma parte del objetivo de P5.1.

**Conclusión.** La integración queda comprendida cuando el alumno puede explicar no solo la respuesta correcta, sino también una secuencia aparentemente contradictoria de respuestas correctas obtenidas en instantes distintos.



## 5.2. Ejecutar, compilar y publicar una aplicación ASP.NET Core MVC

### 5.2.1. ¿Por qué compilar no equivale a publicar?

Durante los módulos anteriores utilizamos Visual Studio o `dotnet run` para ejecutar las aplicaciones desde sus proyectos. Eso permite modificar el código, detenerlo con facilidad y observar la consola. Pero un directorio de proyecto incluye archivos de desarrollo, dependencias y un contexto que no se debería presuponer en el equipo que hospedará una aplicación.

**Compilar** transforma código fuente y recursos en artefactos utilizables. **Ejecutar** inicia un proceso. **Publicar** prepara los archivos que necesitaremos para llevar la aplicación a otro directorio o equipo compatible. No son sinónimos: un programa puede compilar correctamente y, sin embargo, fallar durante su arranque porque carece de una configuración o de una base a la que acceder.

Observemos tres instrucciones distintas:

~~~powershell
dotnet build -c Release
dotnet run --no-launch-profile --urls http://localhost:5091
dotnet publish -c Release -o .\publicado
~~~

La primera crea ensamblados en un directorio de salida de compilación. La segunda inicia el host ASP.NET Core desde el proyecto (aunque internamente compile si se necesita). La tercera prepara una carpeta con ensamblados, recursos, dependencias, configuración y archivos necesarios para el despliegue. No debemos confundir la carpeta `bin/Release/net8.0/` con la salida controlada de `dotnet publish`: tienen usos y garantías distintas.

El modificador `-c Release` selecciona una configuración de compilación. No desactiva por sí mismo validaciones del servidor, no hace segura la aplicación y tampoco impide que su entorno de ejecución se configure como `Development`; son conceptos diferentes. El parámetro `-o` establece una salida explícita que facilita inspeccionar exactamente los archivos publicados.

### 5.2.2. Qué contiene la carpeta publicada

Un proyecto web típico de .NET 8 con despliegue dependiente del framework genera, entre otros, los siguientes elementos (los nombres exactos dependen del proyecto y de sus dependencias):

| Elemento | Función habitual |
|---|---|
| `CursoWeb.Mvc.dll` | Ensamblado de la aplicación |
| `CursoWeb.Mvc.deps.json` | Dependencias de ejecución |
| `CursoWeb.Mvc.runtimeconfig.json` | Información del runtime requerido |
| `appsettings.json` | Configuración distribuida con la aplicación |
| `web.config` | Configuración del módulo ASP.NET Core para despliegue IIS cuando corresponde |
| `wwwroot/` | Archivos estáticos que la aplicación sirve |

Un archivo DLL no es una «página web». Es código que el host ejecuta y que, junto con el routing y los controladores, produce respuestas HTTP. Una vista Razor no tiene por qué aparecer como archivo `.cshtml` independiente después de la publicación: dependiendo de la configuración, se compila como parte de los ensamblados. Por eso la comprobación correcta no consiste únicamente en contar archivos, sino en iniciar la salida publicada y solicitar páginas reales.

### 5.2.3. Dos modos de publicación y su diferencia

Para un despliegue **dependiente del framework**, el equipo de destino debe disponer de un runtime ASP.NET Core compatible. Podemos ejecutar la salida con:

~~~powershell
dotnet .\publicado\CursoWeb.Mvc.dll
~~~

En un despliegue **autocontenido**, la publicación incorpora los componentes del runtime para una plataforma concreta, con mayor tamaño y opciones diferentes de ejecución. Es un concepto útil, pero no hace falta utilizarlo para entender el laboratorio. El itinerario emplea la publicación dependiente del framework en Windows y las imágenes oficiales .NET 8 en Docker. No mezclaremos distintas modalidades en un mismo experimento sin explicar sus requisitos.

La arquitectura y el sistema operativo también importan. Los recursos de publicación para Windows y Linux no pueden considerarse idénticos en todas las dependencias nativas, aunque el mismo código C# pueda compilar para ambas plataformas. En nuestros ejemplos no introduciremos paquetes nativos adicionales.

### 5.2.4. Configuración separada del programa

La aplicación MVC A incluye una cadena de conexión de SQL Server Express LocalDB. Una publicación copia la configuración correspondiente, pero no copia una instancia SQL Server ni los registros de la base. Si se ejecuta en otro equipo Windows sin LocalDB, las páginas dependientes del CRUD pueden fallar durante una consulta o incluso al arrancar si la aplicación inicializa la base en el inicio.

Consideremos una configuración didáctica alternativa:

~~~json
{
  "Despliegue": {
    "SinLocalDb": true
  }
}
~~~

El significado no es «usar otra base», sino **ejecutar solo las rutas que no la necesitan** en un ensayo de despliegue. La aplicación de prácticas conserva la configuración original de SQL Server para el CRUD de Windows; el modo especial se selecciona explícitamente cuando se necesita comprobar el hospedaje sin disponer de LocalDB.

Las variables de entorno de .NET pueden sobrescribir claves de configuración mediante el separador `__`:

~~~powershell
$env:Despliegue__SinLocalDb = "true"
~~~

Es una técnica didáctica válida para aislar una configuración del proceso. Debemos cerrar o restablecer esa variable antes de probar el CRUD persistente en Windows; si permaneciera activada, el experimento dejaría de estar midiendo el mismo comportamiento.

### 5.2.5. Compilación correcta frente a aplicación funcional

Un caso habitual: `dotnet publish` termina con código de salida cero y después `dotnet .\publicado\CursoWeb.Mvc.dll` falla. No implica que la compilación hubiera mentido; significa que la comprobación de compilación no cubría una condición de arranque. Puede faltar una cadena de conexión, estar ocupado un puerto o no estar instalado el runtime.

Conviene trabajar con evidencias diferenciadas:

| Comprobación | Qué demuestra | Qué no demuestra |
|---|---|---|
| `dotnet build` finaliza correctamente | El proyecto compila con las dependencias disponibles | Que pueda llegar a LocalDB |
| `dotnet publish` genera salida | Existen artefactos de publicación | Que el sitio responda HTTP |
| Iniciar la DLL publicada | El proceso arranca con esa configuración | Que todas las rutas funcionen |
| Solicitar `/` y `/Productos/Estado` | Hay respuesta desde rutas sin base | Que las operaciones CRUD estén disponibles |
| Crear un producto en Windows/LocalDB | El recorrido MVC → EF Core → SQL funciona | Que el mismo CRUD funcione en Docker Linux |

### 5.2.6. Síntesis

La transición de ejecutar a publicar se entiende cuando el alumno reconoce qué archivos se han producido, cuáles son las dependencias del destino y qué evidencia requiere un programa que arranca fuera de Visual Studio. Esos conocimientos son prerrequisitos de Kestrel, IIS y Docker.


### 5.2.7. Qué cambia realmente cuando dejamos de ejecutar desde el proyecto

Mientras desarrollamos con Visual Studio, trabajamos con un directorio que contiene el archivo `.csproj`, código C#, vistas, recursos y configuraciones. La herramienta puede compilarlo, iniciar el proceso y ofrecer una experiencia de depuración. Esa comodidad no debe confundirse con los archivos que hay que trasladar al destino.

`dotnet build` permite comprobar que el código y las referencias forman una aplicación compilable. `dotnet publish` prepara una salida adecuada para ejecutar el programa con unas opciones de despliegue determinadas. `dotnet run` inicia la aplicación desde su proyecto, compilando si corresponde. Una publicación no inicia un servidor por sí misma y una compilación correcta no acredita una conexión a SQL Server.

En una publicación dependiente del framework de ASP.NET Core 8, el directorio de destino debe disponer de un runtime compatible. El ensamblado de MVC A está en `CursoWeb.Mvc.dll`, pero no es suficiente por sí solo. Necesita los archivos de dependencias y configuración correspondientes, las bibliotecas pertinentes y, en el caso de una aplicación web, los recursos estáticos que debe servir.

El criterio correcto para observar la transición es identificar tres preguntas independientes: **¿se ha construido el programa?**, **¿se han preparado los archivos para el destino?** y **¿hay un proceso atendiendo peticiones reales con esos archivos?**. Una respuesta afirmativa a la primera no determina las otras dos.

### 5.2.8. Leer la carpeta publicada como un conjunto de responsabilidades

`CursoWeb.Mvc.runtimeconfig.json` aporta información sobre el entorno de ejecución requerido. Si el equipo no tiene instalado el runtime adecuado, el proceso puede fallar antes de atender ninguna ruta MVC. `CursoWeb.Mvc.deps.json` participa en la resolución de dependencias; no es una tabla de rutas que debamos editar para hacer aparecer una vista. La aplicación sigue ejecutando código compilado.

`wwwroot` contiene archivos estáticos; el programa debe tener configurado su servicio. Si `/` responde HTML y `/css/site.css` devuelve 404, el servidor y la ruta inicial pueden funcionar mientras falta un recurso. Por eso la simple visita a la página inicial es una prueba incompleta. Los archivos de configuración, a su vez, pueden contener una cadena de conexión que apunta a un recurso no disponible. Copiar el archivo no crea la base de datos.

Cuando se publica para IIS puede aparecer `web.config`, que describe cómo debe iniciar la aplicación el módulo de hospedaje ASP.NET Core. Ese archivo es significativo para IIS, pero su existencia no instala IIS ni el Hosting Bundle. Más adelante veremos que el mismo programa puede recibir solicitudes mediante otros mecanismos sin cambiar sus controladores.

### 5.2.9. Directorio actual y directorio publicado no son necesariamente iguales

Una ruta relativa se interpreta desde un contexto. El comando `dotnet publish .\CursoWeb.Mvc.csproj` presupone que el proyecto se encuentra en la carpeta actual. Si nos situamos en la raíz del repositorio, habrá que utilizar una ruta distinta, y si abrimos la carpeta de salida publicada tendremos que ejecutar la DLL desde allí o indicar su ruta completa.

Esta diferencia se vuelve visible cuando aparecen errores de «archivo no encontrado». No significa que el programa C# esté mal diseñado. Puede tratarse de una orden ejecutada desde otra carpeta. La respuesta técnica es comprobar el directorio actual, el archivo de proyecto y la ubicación de salida, no copiar código al azar a distintos directorios.

Además, no hay que suponer que editar una vista en el árbol de código modifica una publicación ya construida. Una distribución normalmente conserva la versión de archivos y ensamblados producida cuando se publicó. Para incorporar cambios posteriores se vuelve a publicar y se sustituye la salida que ejecuta el destino.

### 5.2.10. Configuración de compilación y entorno de ejecución son conceptos distintos

La opción `-c Release` determina una configuración de construcción. No significa que el entorno ASP.NET Core vaya a llamarse necesariamente `Production`. Tampoco instala certificados HTTPS ni añade autorización a los controladores. Es un error pedagógico presentar Release como sinónimo de seguridad.

La aplicación puede leer una configuración general y valores específicos del entorno; las variables de entorno suelen utilizar `__` para representar claves jerárquicas como `Despliegue:SinLocalDb`. Una ejecución puede, por tanto, comportarse de manera distinta aunque se inicie exactamente el mismo ensamblado:

~~~powershell
$env:Despliegue__SinLocalDb = "true"
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5091
~~~

El ejemplo presupone que estamos dentro del directorio publicado. Con esta opción la aplicación del curso realiza únicamente el recorrido sin base previsto para demostrar hospedaje; no convierte automáticamente la cadena LocalDB en una conexión válida. Restablecer el valor es imprescindible cuando volvemos a trabajar con el CRUD persistente de M02.

### 5.2.11. Por qué LocalDB puede impedir el arranque antes de que exista una página

El `Program.cs` de MVC A registra un contexto EF Core con `UseSqlServer`. Registrar el contexto no implica que todas las llamadas a SQL Server hayan tenido lugar ya. Sin embargo, el ejemplo del curso también realiza una inicialización elemental de base al inicio bajo la configuración normal. Si esa operación falla, el proceso puede terminar sin haber empezado a escuchar HTTP.

Imaginemos que alguien copia el directorio publicado a un equipo que no dispone de SQL Server Express LocalDB. Ve la DLL y un archivo de configuración correcto, pero la aplicación no arranca. Concluir que Kestrel «no funciona» sería precipitado: la causa inmediata puede estar en una dependencia de datos anterior a la apertura del puerto.

En el modo de ensayo de despliegue, el programa consulta `Despliegue:SinLocalDb`. Cuando vale `true`, omite esa inicialización, pero no pretende habilitar el CRUD con otro proveedor. Para evitar un resultado engañoso, las rutas de productos que requerirían SQL devuelven explícitamente un **503**. Así queda separada la disponibilidad del servidor web de la disponibilidad de la funcionalidad de datos.

### 5.2.12. Historia de una publicación que funciona parcialmente

Un alumno construye MVC A y publica a carpeta. La orden termina correctamente, inicia la aplicación y abre `/` con respuesta 200. Sin embargo, cuando intenta acceder a `/Productos`, recibe 503. ¿Qué sabemos realmente?

Sabemos que existe una publicación ejecutable, un proceso que responde, una ruta MVC disponible y una ruta que declara no estar disponible. Todavía no sabemos si está instalada LocalDB ni cuál fue la configuración de arranque. Debemos mirar el valor del indicador de despliegue y el contexto del proceso antes de modificar las vistas o rehacer la base.

En otra máquina puede suceder algo diferente: `/` funciona, pero el CSS falta. Aquí el problema afecta a recursos estáticos, no necesariamente a SQL Server. Y en un tercer equipo la aplicación ni siquiera llega a abrir un puerto porque el runtime esperado no está instalado. Las tres situaciones se describen coloquialmente como «la publicación falla», pero requieren diagnósticos diferentes.

Esa es la finalidad de este apartado: dar significado técnico a la palabra publicar. Los comandos son relevantes porque producen artefactos concretos, pero la capacidad que debe adquirir el alumno consiste en explicar **qué ejecución se ha preparado, qué dependencias conserva y qué evidencias demuestran sus límites**.



## 5.3. Kestrel: proceso, dirección y respuesta HTTP

### 5.3.1. Qué es Kestrel y qué hace

Kestrel es el servidor web multiplataforma utilizado por ASP.NET Core. Cuando iniciamos una aplicación con `dotnet run` o ejecutamos una DLL publicada como aplicación web, un host ASP.NET Core puede abrir un socket y escuchar peticiones HTTP mediante Kestrel. El navegador no ejecuta C#: envía solicitudes a una dirección que el proceso atiende. Un controlador MVC decide qué hacer con cada ruta y devuelve la respuesta correspondiente.

En nuestro laboratorio bastará con ejecutar una publicación desde una carpeta concreta, establecer una dirección local y observar la respuesta. No necesitamos configurar balanceadores, proxies corporativos, certificados de producción ni límites avanzados.

El recorrido conceptual puede describirse así:

~~~mermaid
flowchart TD
A["Iniciar proceso dotnet"] --> B["Construir host ASP.NET Core"]
B --> C["Configurar servicios y middleware"]
C --> D["Kestrel escucha un puerto"]
D --> E["Navegador solicita una URL"]
E --> F["Routing selecciona endpoint MVC"]
F --> G["Acción produce respuesta HTTP"]
~~~

El dibujo diferencia el arranque (una vez por proceso) de las peticiones (tantas como el servidor pueda atender). No debemos atribuir la creación de un nuevo proceso `dotnet` a cada petición.

### 5.3.2. Dirección de escucha, host y puerto

Supongamos esta orden:

~~~powershell
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5091
~~~

`localhost` indica que se pretende escuchar en la máquina local. `5091` es el puerto elegido para el experimento; no es un número obligatorio de ASP.NET Core. En el navegador usaremos `http://localhost:5091/`. Si el comando muestra una dirección distinta porque otra configuración tiene mayor prioridad, debemos atender a la URL efectiva publicada por el host.

No mezclemos sin explicación tres direcciones diferentes: la de la aplicación MVC, la de Blazor y la de la API de productos. Durante 5.3 usamos solamente MVC. El proceso publica recursos HTML; no necesita que funcione la API de productos del otro laboratorio.

### 5.3.3. ¿Qué sucede si el puerto está ocupado?

Dos procesos no suelen poder escuchar simultáneamente la misma combinación de dirección y puerto. Si la aplicación MVC sigue ejecutándose desde Visual Studio y tratamos de arrancar una segunda copia de la publicación en ese puerto, el segundo proceso puede terminar con error de enlace a la dirección. No es un problema del código de una vista ni de Entity Framework Core.

La estrategia de diagnóstico consiste en comprobar si hay otro proceso escuchando y elegir: detenerlo o utilizar otro puerto.

~~~powershell
Get-NetTCPConnection -LocalPort 5091 -ErrorAction SilentlyContinue
~~~

La orden pertenece a PowerShell en Windows y muestra conexiones asociadas al puerto cuando la plataforma la admite. Puede requerirse interpretar estados y procesos. Alternativamente cambiamos temporalmente la prueba a un puerto libre, por ejemplo 5094, y confirmamos qué URL anunció Kestrel.

### 5.3.4. Una respuesta de una ruta no acredita todas las rutas

Si `/` funciona y `/Productos/Estado` devuelve texto, hemos demostrado que Kestrel, el routing y esas acciones responden. Pero el CRUD de productos de M02 puede necesitar LocalDB. No debemos presentar «la página inicial abre» como si probara automáticamente las operaciones de crear, editar y eliminar.

El código HTTP que observamos se compone de una línea de estado, cabeceras y un cuerpo opcional. Podemos consultar desde el navegador o desde una terminal:

~~~powershell
curl.exe -i http://localhost:5091/Productos/Estado
~~~

Una respuesta 200 con texto esperado es un resultado concreto; si se obtiene 503 para `/Productos` bajo el modo sin LocalDB, eso representa una limitación **deliberada y documentada**, no un CRUD funcional.

### 5.3.5. Detención del proceso y restauración del entorno

En una terminal interactiva, `Ctrl+C` suele solicitar el apagado del proceso. Es importante cerrar la aplicación que ya estaba escuchando antes de iniciar otra modalidad de hospedaje. Una terminación limpia facilita liberar el puerto y evita atribuir una respuesta al proceso equivocado.

Kestrel no es exclusivo de `dotnet run`. La publicación ASP.NET Core también puede atender peticiones mediante Kestrel, por lo que la diferencia formativa no reside en «servidor de desarrollo frente a servidor real», sino en los artefactos, su configuración y el modo en que se hospeda y administra el proceso.

### 5.3.6. Síntesis

El alumno podrá explicar qué proceso recibe las solicitudes, cómo conoce su puerto, qué sucede ante una colisión de dirección y cómo demostrar con una petición HTTP que una ruta concreta funciona.


### 5.3.7. El proceso que recibe la petición y el proceso que construyó el programa

La palabra «servidor» puede designar una máquina, un programa o una función de ASP.NET Core. En nuestro laboratorio necesitamos ser precisos: Kestrel es el servidor HTTP integrado en el host ASP.NET Core, mientras que el proceso `dotnet` es la ejecución concreta que lo inicia. La máquina Windows es el entorno que aloja ese proceso.

Cuando ejecutamos la DLL publicada, el código de `Program.cs` construye el host y configura servicios, middleware y rutas. Si no falla una dependencia previa, se inicia la escucha HTTP. Una vez iniciado, **cada petición no vuelve a ejecutar todo `Program.cs` desde cero**. El proceso conserva sus servicios según sus ámbitos de vida y atiende las solicitudes mediante el pipeline configurado.

Esa distinción ayuda a interpretar el ciclo de vida de los recursos. Una instancia de LocalDB puede sobrevivir al proceso web porque es un servicio de datos separado. Una colección estática mantenida dentro de una API de demostración no tiene esa misma garantía al reiniciar el proceso. Aunque ambos servidores se ejecuten con `dotnet`, sus datos no tienen el mismo ciclo de vida.

### 5.3.8. Escuchar, recibir, enrutar y responder son etapas diferentes

Que un programa escriba «Now listening on...» en la consola informa de su dirección de escucha. No demuestra que una ruta específica esté definida ni que la acción MVC pueda completarse. El servidor puede aceptar conexiones correctamente y devolver 404 porque no existe el recurso, o devolver 503 porque una función está deshabilitada para ese escenario.

Consideremos la secuencia completa de una solicitud `GET /Productos/Estado`:

1. Un cliente interpreta la dirección y decide el destino de la conexión.
2. El sistema operativo dirige el tráfico al proceso que escucha el puerto.
3. Kestrel interpreta la solicitud HTTP recibida.
4. El middleware ASP.NET Core participa en el procesamiento.
5. El enrutamiento encuentra un controlador y una acción compatibles.
6. La acción produce un resultado HTTP, con código de estado y cuerpo.
7. El servidor transmite esa respuesta al cliente, que la interpreta.

Si obtenemos un 404, las etapas iniciales pueden haber funcionado perfectamente. Si recibimos un texto esperado con 200, hemos demostrado mucho más que la existencia de un socket: también se ejecutó una acción determinada. Si la página inicial funciona pero el CSS no, el problema puede estar en la ruta de recursos estáticos y no en el arranque del host.

### 5.3.9. `localhost` no es una dirección universal de todas las máquinas

En este curso utilizamos intencionadamente `localhost` porque las demostraciones son locales. Es importante comprender que ese nombre se refiere al propio entorno desde el que se interpreta. Una URL `http://localhost:5091/` utilizada desde el navegador del alumno pretende conectar con el proceso que escucha en su máquina. La misma URL abierta en otro equipo apunta a **ese otro equipo**, no al primero.

Este detalle cobra importancia al introducir Docker. Dentro de un contenedor, `localhost` se refiere al espacio de red del propio contenedor. Para publicar una aplicación desde ese entorno utilizaremos una dirección de escucha apropiada en el contenedor y un mapeo de puertos hacia el host. No debemos trasladar de forma literal la noción de `localhost` entre procesos y entornos de red diferentes.

En Kestrel Windows del laboratorio, la exposición local es suficiente. No configuramos direcciones accesibles desde Internet ni certificados públicos; ese trabajo implicaría decisiones de seguridad e infraestructura que exceden M05.

### 5.3.10. La dirección solicitada puede no coincidir con la dirección efectiva

Una aplicación ASP.NET Core recibe opciones de escucha desde la línea de comandos y otras fuentes de configuración. Es posible que el alumno ejecute un comando con un puerto, pero otra configuración explícita del host lo modifique. Por ello no basta con recordar el número que se pretendía usar: debemos comprobar la dirección anunciada por el proceso y el resultado de una solicitud.

El procedimiento de diagnóstico no empieza cambiando puertos de forma aleatoria. Primero observamos qué URL utiliza realmente el proceso. Después comprobamos si hay otro servicio escuchando en el puerto previsto. Por último, si es necesario, elegimos un puerto distinto y repetimos una petición a una ruta conocida.

En Windows, este ejemplo de PowerShell permite observar los procesos asociados a un puerto sin matar ninguno:

~~~powershell
Get-NetTCPConnection -LocalPort 5091 -ErrorAction SilentlyContinue |
    Select-Object LocalAddress, LocalPort, State, OwningProcess
~~~

La ausencia de filas no prueba por sí sola una única causa; puede depender de permisos, de cómo escucha el proceso o de cuándo se realizó la comprobación. El comando es una evidencia complementaria a los mensajes del host y a una petición HTTP.

### 5.3.11. Una colisión de puerto no es una excepción de controlador

Supongamos que mantenemos la aplicación original abierta desde Visual Studio en el puerto 5091 y luego intentamos iniciar la DLL publicada en ese mismo puerto. Si ambos procesos solicitan una combinación incompatible de dirección y puerto, el segundo no podrá iniciar normalmente su escucha.

¿Qué debemos hacer? Identificar qué proceso está atendiendo la dirección, detener el que ya no necesitamos o elegir una dirección diferente para el ensayo. **No debemos modificar HomeController, reinstalar EF Core ni cambiar el nombre de las vistas**, porque el problema ocurre antes de que una solicitud alcance esas capas.

Cuando el objetivo es aprender, es útil provocar deliberadamente una colisión y observar el error. Pero al terminar debemos dejar solo un proceso utilizando el puerto; de otro modo, la siguiente práctica podría consultar sin darse cuenta una instancia anterior y atribuirle resultados al código recién publicado.

### 5.3.12. La petición HTTP como prueba y como límite de una afirmación

Examinemos este comando:

~~~powershell
curl.exe -i http://localhost:5091/Productos/Estado
~~~

La opción `-i` solicita mostrar las cabeceras junto al cuerpo. Si recibimos `HTTP/1.1 200 OK` y el texto esperado, podemos afirmar que el servidor ha atendido correctamente **esa ruta** en ese momento.

No podemos afirmar sin más que el CRUD funciona o que la base SQL Server está disponible. Esa segunda afirmación requeriría ejecutar una acción real de lectura o modificación que use EF Core y comprobar su resultado. Las pruebas tienen alcance: deben corresponder a lo que decimos haber demostrado.

El código 503 también es una respuesta HTTP válida. En el modo sin LocalDB, el middleware de MVC A la genera para rutas que dependen de SQL. Esto demuestra que el proceso atiende la conexión, identifica la limitación y la expresa. No es la misma situación que un navegador incapaz de conectar porque no hay servidor escuchando.

### 5.3.13. Ejemplo razonado de un diagnóstico de tres capas

El alumno abre `http://localhost:5091/` y recibe una página HTML. Después consulta `/Productos` y recibe 503. Finalmente consulta `/css/site.css` y obtiene 200. ¿Dónde está el fallo?

No es correcto afirmar que Kestrel está caído: ha respondido en las tres solicitudes. Tampoco podemos concluir que falta la hoja de estilos. La evidencia apunta a una restricción aplicada al conjunto de rutas dependientes de SQL Server, algo coherente con el modo `Despliegue:SinLocalDb=true`.

En otro caso, el navegador no logra conectar con ninguna ruta y la consola del proceso muestra un error de dirección ocupada. Aquí la causa se sitúa **antes** del enrutamiento. De nuevo, investigar `ProductosController` sería improductivo.

En un tercer caso, `/` devuelve 200, `/Productos/Estado` devuelve 404 y `/css/site.css` devuelve 200. El servidor parece operativo, pero el endpoint concreto no está disponible. Debemos revisar el código que realmente se publicó y sus rutas, así como asegurarnos de no estar hablando con un proceso antiguo que permanece escuchando.

### 5.3.14. Qué significa detener correctamente la demostración

Al terminar una práctica, detener el proceso no es una formalidad. Permite liberar la dirección de escucha, evitar el consumo de recursos y garantizar que el siguiente resultado proceda del nuevo modo de hospedaje y no de la aplicación anterior.

En una terminal que ejecuta `dotnet`, Ctrl+C normalmente inicia la terminación. Después conviene comprobar que la ventana o el proceso ya no sigue anunciando el puerto y que una solicitud no recibe la misma respuesta. Si todavía responde, puede existir otro proceso distinto usando la dirección.

El alumno debe poder describir tres evidencias: el proceso de publicación se inició desde los artefactos, una ruta concreta respondió por HTTP y el proceso dejó de atender al detenerlo. Ese recorrido de inicio, operación y parada es la base para comprender el hospedaje posterior en IIS y el ciclo de vida del contenedor Docker.



## 5.4. Publicación elemental de ASP.NET Core en IIS

### 5.4.1. El problema que IIS resuelve

En Windows, IIS ofrece mecanismos para administrar sitios, enlaces de direcciones, procesos trabajadores y configuración de hospedaje. No reemplaza el código MVC ni convierte los controladores en páginas estáticas. En un hospedaje ASP.NET Core habitual, IIS trabaja con el **ASP.NET Core Module (ANCM)** y una aplicación publicada.

El esquema se puede simplificar así:

~~~mermaid
flowchart TD
A["Navegador"] --> B["IIS: sitio y binding"]
B --> C["ASP.NET Core Module"]
C --> D["Aplicación ASP.NET Core"]
D --> E["Routing y controlador MVC"]
E --> F["Respuesta HTML/HTTP"]
~~~

El modelo de hospedaje concreto puede ser **in-process** u **out-of-process**. En el primero, la aplicación ASP.NET Core se hospeda dentro del proceso trabajador IIS; en el segundo, IIS reenvía solicitudes a un proceso ASP.NET Core que utiliza Kestrel. Es importante no afirmar que *siempre* existe el mismo proceso Kestrel externo cuando utilizamos IIS. Para esta jornada basta con reconocer que ANCM conecta el mundo IIS con ASP.NET Core.

### 5.4.2. Hosting Bundle y ASP.NET Core Module

Instalar IIS en Windows no garantiza que conozca cómo iniciar una aplicación ASP.NET Core .NET 8. El **ASP.NET Core Hosting Bundle** instala o proporciona los componentes de hospedaje requeridos, incluido el módulo ANCM y los runtimes correspondientes. Si el bundle se instaló antes de habilitar IIS o el servicio no detecta el módulo, puede ser necesario reparar la instalación y reiniciar los servicios según las instrucciones del producto.

Un error habitual es confundir el SDK para desarrollar con el runtime/Hosting Bundle del servidor. El servidor IIS del laboratorio necesita componentes de hospedaje, no necesariamente Visual Studio. Tampoco basta con copiar una carpeta de código fuente al directorio del sitio.

### 5.4.3. Sitio, ruta física y binding

Un sitio IIS asocia una carpeta física de contenido publicado con uno o varios bindings. En el laboratorio utilizaremos HTTP local en un puerto concreto; por ejemplo, `localhost:8091`. En un escenario empresarial se requeriría tratar HTTPS y exposición pública, pero no forma parte de esta práctica introductoria.

El `Application Pool` proporciona un contexto de proceso e identidad. Para aplicaciones ASP.NET Core se configura habitualmente con **No Managed Code** respecto al CLR de .NET Framework; ello no significa que la aplicación carezca de código administrado .NET 8. Significa que el runtime moderno lo gestiona el mecanismo de hospedaje ASP.NET Core, no la configuración tradicional del CLR de .NET Framework del pool.

Los permisos del directorio publicado son otra condición de ejecución. Una identidad que no puede leer la carpeta o sus archivos impedirá iniciar o servir correctamente la aplicación. No concederemos permisos globales a todo el equipo como solución improvisada; delimitaremos los permisos necesarios para la identidad del sitio de ensayo.

### 5.4.4. La trampa de LocalDB bajo una identidad distinta

El CRUD MVC A fue desarrollado desde Visual Studio bajo la sesión interactiva del alumno. **SQL Server Express LocalDB está asociado a un usuario de Windows**, por lo que el hecho de disponer de una instancia desde Visual Studio no garantiza que el proceso de IIS, ejecutado bajo una identidad de Application Pool, pueda acceder a esa misma base.

Tenemos dos objetivos distintos:

1. Comprobar el mecanismo elemental de publicación y hospedaje IIS, para lo cual bastan rutas MVC sin base de datos.
2. Comprobar CRUD y persistencia LocalDB, lo cual exige permisos, usuario y configuración de la instancia adecuados; esa preparación excede la comparación mínima de hospedajes de M05.

Por eso el laboratorio utiliza rutas sin dependencias SQL para la prueba elemental de IIS. **No reemplazamos la base de datos ni eliminamos el CRUD**. En Windows/Kestrel puede utilizarse la configuración normal para demostrar la persistencia; en IIS, la práctica se concentra en mostrar la aplicación y navegar rutas independientes de LocalDB.

### 5.4.5. Reconocer los fallos típicos

| Síntoma | Qué comprobar primero | Qué no debemos concluir |
|---|---|---|
| IIS devuelve una página de error de hospedaje | Hosting Bundle, ANCM y logs | Que el controlador Index contiene un error |
| El sitio responde en un puerto diferente | Binding y conflicto con otro sitio | Que publicar cambia automáticamente el puerto |
| Error de acceso a los archivos | Carpeta física e identidad del pool | Que hay que dar control total a todos los usuarios |
| Página inicial funciona, CRUD falla | LocalDB, identidad y conexión | Que la publicación MVC está completamente rota |
| IIS muestra una versión antigua | Carpeta física y artefactos realmente publicados | Que basta actualizar el código fuente de Visual Studio |

En un entorno de validación sin Windows/IIS es posible comprobar la estructura de la publicación y el archivo `web.config`, pero **no afirmar que el despliegue IIS funciona**. Una prueba de Kestrel no sustituye esta evidencia.

### 5.4.6. Una comparación explicativa

La aplicación MVC construida desde M01 no cambia sus controladores al desplegarse. Si la acción Home/Index devolvía una vista durante `dotnet run`, seguirá devolviéndola cuando reciba una petición válida bajo IIS, siempre que la configuración de hospedaje sea correcta. Esa independencia es precisamente una ventaja del framework: el código HTTP de ASP.NET Core no se reescribe para cada mecanismo elemental de hospedaje.

Lo que sí cambia es cómo se inicia el proceso, cómo llega la petición y qué identidad y recursos tiene el host. Por ello, una comparación correcta evalúa esas condiciones, manteniendo estable la aplicación que recibe las solicitudes.

### 5.4.7. Síntesis

El alumno debe ser capaz de publicar a carpeta, identificar los componentes IIS necesarios, crear un sitio con binding local, comprobar una ruta y distinguir un error de IIS/ANCM de uno causado por una dependencia como LocalDB.


### 5.4.8. Un sitio IIS no es una aplicación compilada ni una base de datos

Cuando hablamos de «publicar en IIS» estamos conectando tres objetos con responsabilidades diferentes: un directorio que contiene una publicación ASP.NET Core, un sitio de IIS que recibe solicitudes y un mecanismo de hospedaje capaz de iniciar la aplicación. Una base de datos SQL Server, si hace falta, constituye una dependencia adicional y no está incluida implícitamente en ninguno de esos tres objetos.

La carpeta publicada se genera con `dotnet publish`. IIS no compila el código C# de la solución durante una petición. El sitio asocia una ruta física con un enlace de escucha. El ASP.NET Core Module participa en la puesta en marcha y el tratamiento del tráfico hacia la aplicación.

Es posible que un sitio figure como «Started» en el administrador IIS y que la aplicación ASP.NET Core no consiga iniciarse. El estado administrativo del sitio no equivale a una respuesta HTTP correcta de Home/Index. Para afirmarlo necesitamos abrir la URL que corresponde al binding y comprobar el resultado real.

También puede suceder lo contrario: una publicación arranca perfectamente como proceso Kestrel independiente, pero falla bajo IIS. Eso no demuestra que la aplicación MVC contenga un error de lógica. El hospedaje IIS añade su módulo, identidad de proceso, configuración y permisos, todos ellos relevantes para el diagnóstico.

### 5.4.9. La relación entre sitio, binding, pool y carpeta física

El **sitio** es una unidad de configuración administrada por IIS. El **binding** indica en qué combinación de protocolo, dirección, puerto y, cuando corresponde, nombre de host acepta solicitudes. La **ruta física** indica dónde se encuentran los archivos publicados. El **Application Pool** define el contexto de ejecución y las condiciones bajo las que se procesan las solicitudes.

En el laboratorio elegimos `http://localhost:8091/`. El número 8091 no surge de ASP.NET Core ni de un controlador: es el puerto que decidimos vincular al sitio. Para solicitar esa dirección, IIS debe tener un binding compatible y el navegador debe conectar al host correcto.

La misma DLL podría copiarse a otra carpeta, pero si el sitio sigue apuntando a la carpeta anterior continuará utilizando los artefactos anteriores. Este es el origen de una situación frecuente: «he publicado la versión nueva y sigo viendo la antigua». No hay que reescribir el controlador para resolverlo; se debe verificar la carpeta física que está utilizando el sitio.

Respecto al Application Pool, **No Managed Code** significa que no seleccionamos un CLR tradicional de .NET Framework para ejecutar la aplicación ASP.NET Core. No significa «aplicación sin .NET», ni autoriza a omitir el Hosting Bundle. El sistema moderno de hospedaje ASP.NET Core requiere sus propios componentes.

### 5.4.10. Por qué el Hosting Bundle importa y cómo reconocer su ausencia

Una instalación de IIS preparada únicamente para páginas o aplicaciones tradicionales no dispone necesariamente del módulo requerido para hospedar ASP.NET Core 8. El Hosting Bundle incorpora los componentes necesarios para que IIS pueda iniciar una aplicación publicada para ese entorno, incluido ANCM.

La instalación de Visual Studio en el equipo de desarrollo no prueba que el servidor IIS de otro equipo tenga ese bundle. Tampoco basta con copiar una DLL o `web.config`. La máquina que recibe las solicitudes debe estar preparada de forma explícita, y la versión de runtime disponible debe ser compatible con la aplicación que se pretende ejecutar.

Cuando se instala IIS y después el Hosting Bundle, puede ser necesario reiniciar los servicios para que detecten el módulo. Si se instaló el bundle antes de habilitar IIS, el procedimiento de preparación del entorno puede requerir reparar su instalación. Lo importante para el alumno no es memorizar cada pantalla del instalador, sino entender **qué capacidad proporciona cada pieza**.

Si el módulo de hospedaje falta, el problema aparece antes de que los controladores MVC puedan atender normalmente sus rutas. Por eso una página de error de arranque bajo IIS debe llevarnos primero a revisar el hosting, la versión de runtime y los registros de inicio, no directamente a cambiar `Views/Home/Index.cshtml`.

### 5.4.11. Dos modelos de hospedaje, una misma responsabilidad MVC

En ASP.NET Core con IIS distinguimos los modelos *in-process* y *out-of-process*. En el primero, la aplicación se hospeda en el proceso trabajador IIS mediante el mecanismo correspondiente. En el segundo, IIS actúa delante de un proceso ASP.NET Core separado que atiende solicitudes mediante Kestrel.

Esta distinción es suficiente para interpretar diagramas y errores. No es necesario construir dos laboratorios distintos con sus configuraciones de rendimiento; eso convertiría una práctica elemental en un curso de administración de IIS.

Lo que debe permanecer estable en ambos conceptos es el papel de nuestra aplicación MVC. Los controladores siguen transformando solicitudes en resultados; las vistas siguen produciendo HTML; `wwwroot` sigue proporcionando recursos estáticos. El mecanismo de alojamiento cambia cómo se inicia y conecta ese código con el servidor externo.

**Afirmación a evitar:** «En IIS todo el tráfico debe pasar siempre por un proceso Kestrel externo». Solo describe de forma aproximada el hospedaje fuera de proceso y no el modelo in-process. La teoría debe permitir reconocer esa diferencia sin convertirla en un problema que el alumno tenga que configurar durante los 270 minutos de prácticas de M05.

### 5.4.12. Una lectura conceptual de `web.config`

En una publicación ASP.NET Core orientada a IIS, podemos encontrar instrucciones de hospedaje como las siguientes, presentadas aquí de forma ilustrativa:

~~~xml
<configuration>
  <system.webServer>
    <handlers>
      <add name="aspNetCore"
           path="*"
           verb="*"
           modules="AspNetCoreModuleV2"
           resourceType="Unspecified" />
    </handlers>
    <aspNetCore processPath="dotnet"
                arguments=".\CursoWeb.Mvc.dll"
                hostingModel="inprocess" />
  </system.webServer>
</configuration>
~~~

El archivo concreto lo genera la publicación según las propiedades del proyecto. No debemos sustituirlo por esta transcripción sin comprobar su contexto: aquí estudiamos **la función de sus elementos**, no una edición manual obligatoria. `AspNetCoreModuleV2` identifica el módulo. El ensamblado indicado representa la aplicación publicada. El modo de hospedaje informa cómo se ejecuta con IIS.

El alumno puede utilizar esta lectura para comprender por qué un `web.config` que apunta a otro ensamblado, una ruta física incorrecta o un módulo no instalado impedirían arrancar la aplicación. Pero la corrección no consiste en modificar a ciegas el XML: la salida generada y las condiciones reales del servidor son la referencia inicial.

### 5.4.13. Identidad del proceso y acceso a recursos externos

El Application Pool utiliza una identidad concreta. Esa identidad necesita acceso de lectura a los archivos publicados. Si el sitio no puede leer su carpeta, los fallos se sitúan en permisos de sistema de archivos o configuración de IIS, no en la sintaxis del controlador MVC.

SQL Server Express LocalDB introduce una segunda dimensión. Una instancia utilizada por el desarrollador al ejecutar Visual Studio suele pertenecer a su sesión o contexto de usuario. El proceso IIS puede utilizar otra identidad y, por tanto, **no compartir automáticamente la posibilidad de acceder a esa instancia**. Una cadena de conexión idéntica en `appsettings.json` no elimina esa diferencia.

El recorrido principal del curso separa estos problemas: verificamos el hospedaje IIS con páginas y rutas sin SQL, y dejamos el CRUD con LocalDB para el contexto Windows en que fue preparado y probado. No se instala otra base, no se asignan permisos globales a todos los usuarios como solución indiscriminada y no se finge que los endpoints de productos funcionan sin infraestructura.

Este criterio no empobrece la demostración. La hace precisa: un alumno puede afirmar «he servido por IIS una aplicación ASP.NET Core real» si ha solicitado sus rutas y recursos y ha observado la respuesta. No puede afirmar «he desplegado el CRUD persistente» si no ha comprobado la base, sus permisos y operaciones.

### 5.4.14. Diagnóstico de una página inicial que no aparece

Imaginemos que IIS tiene un sitio configurado y el navegador devuelve un error en lugar del HTML esperado. La estrategia de diagnóstico puede ordenarse así:

Primero, confirmar la URL, el puerto y el binding. Una solicitud a otro puerto podría estar llegando a un sitio distinto o no llegar a ninguno.

Segundo, confirmar que la ruta física apunta **a la publicación** y no a la carpeta de código fuente o a una publicación antigua. La existencia de `CursoWeb.Mvc.dll` y los demás artefactos es una condición que debemos comprobar.

Tercero, revisar que IIS conoce el ASP.NET Core Module y que está instalado el runtime requerido. Si la aplicación ni siquiera se inicia, estudiar primero sus dependencias de hospedaje.

Cuarto, verificar los permisos mínimos de acceso a la carpeta. Una identidad sin permiso de lectura puede impedir el funcionamiento aunque todos los archivos estén presentes.

Quinto, si la aplicación ha iniciado pero una ruta particular falla, analizar su código y dependencias. Una página inicial que responde no demuestra que las rutas CRUD puedan comunicarse con LocalDB.

Por último, comprobar que se está visitando la versión recién publicada. Si la aplicación parece antigua, comparar el binding, la ruta física y la fecha de los artefactos. Esta comprobación es mejor que volver a compilar repetidamente sin saber qué publicación está ejecutando IIS.

### 5.4.15. Caso explicado: IIS sirve la portada, pero no el catálogo

Un alumno termina el ensayo y presenta las siguientes observaciones:

| Recurso | Resultado observado |
|---|---|
| `/` | HTTP 200, página MVC |
| `/css/site.css` | HTTP 200, hoja de estilos |
| `/Productos/Estado` | HTTP 200, texto esperado |
| `/Productos` | HTTP 503 |

La interpretación es precisa: IIS recibe solicitudes, ANCM hospeda la aplicación, el enrutamiento y los recursos estáticos funcionan, y la aplicación rechaza intencionadamente las rutas de datos en el modo sin LocalDB.

No corresponde «arreglar» esa última respuesta habilitando una base inventada ni editando la acción de listado para devolver siempre una colección fija. Eso haría parecer que el CRUD funciona y borraría precisamente la diferencia que se está enseñando. Para demostrar el CRUD de M02 deberíamos elegir un entorno con SQL Server Express LocalDB real y probar operaciones reales bajo una identidad autorizada.

Esta disciplina de separar hechos comprobados y capacidades no comprobadas es transferible a cualquier tecnología de hospedaje. Una portada disponible es una evidencia limitada; una operación de base funcional sería una evidencia distinta.



## 5.5. Docker: ejecutar la misma aplicación MVC en un contenedor Linux

### 5.5.1. Imagen, contenedor y aplicación no son lo mismo

Una **imagen** es una plantilla de capas con el sistema de archivos y la configuración necesarios para iniciar una aplicación. Un **contenedor** es una instancia de ejecución creada a partir de una imagen. Un Dockerfile describe cómo construir esa imagen; no es por sí mismo una aplicación ejecutándose.

No confundamos estos términos con una máquina virtual completa. El contenedor comparte el kernel del host mediante mecanismos de aislamiento, con las particularidades de Docker Desktop en Windows, que utiliza una infraestructura de virtualización/WSL para ejecutar contenedores Linux.

La aplicación MVC continúa siendo ASP.NET Core. Docker no sustituye el servidor HTTP: el proceso `dotnet CursoWeb.Mvc.dll` inicia ASP.NET Core y su servidor dentro del contenedor. Docker proporciona un entorno de ejecución empaquetado, configuración de red y control del ciclo de vida.

### 5.5.2. El papel de un Dockerfile multietapa

Para un proyecto ASP.NET Core .NET 8 resulta instructivo separar la etapa de compilación, que usa el SDK, de la etapa final de ejecución, que usa un runtime ASP.NET Core más pequeño:

~~~dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS compilacion
WORKDIR /src
COPY . .
RUN dotnet restore CursoWeb.Mvc.csproj
RUN dotnet publish CursoWeb.Mvc.csproj -c Release --no-restore -o /app/publicada

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS ejecucion
WORKDIR /app
COPY --from=compilacion /app/publicada .
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "CursoWeb.Mvc.dll"]
~~~

`FROM` determina una imagen base. `WORKDIR` fija el directorio de trabajo. `COPY` incorpora archivos. `RUN` ejecuta instrucciones **durante la construcción** de la imagen. `ENTRYPOINT` establece el proceso que arrancará **al ejecutar** un contenedor. Confundir ambas fases explica por qué no basta con añadir un `RUN dotnet publish` para servir una página web.

La etapa final no requiere el SDK completo. El ejemplo presupone que ejecutamos `docker build` desde la carpeta que contiene el `.csproj`, porque `COPY . .` depende del **contexto de construcción** que pasamos a Docker. Lanzar el comando desde una carpeta distinta sin adaptar rutas puede producir un error «proyecto no encontrado» aunque el Dockerfile sea correcto.

### 5.5.3. Puerto interno y puerto del host

En una imagen ASP.NET Core 8, el puerto de escucha que utilizaremos es **8080 dentro del contenedor**. La orden:

~~~powershell
docker run --rm -p 8081:8080 cursoweb-mvc:m05
~~~

publica el puerto 8080 del contenedor en el puerto 8081 del host. Desde el navegador de Windows pedimos `http://localhost:8081/`. `EXPOSE 8080` documenta el puerto previsto, pero no realiza por sí mismo la publicación hacia el host. Para acceder desde la máquina utilizamos `-p`.

Al confundir los dos números, alguien puede pedir `http://localhost:8080/` y no ver la aplicación, aunque esté respondiendo correctamente en el puerto 8081 del host. El diagnóstico empieza por revisar el mapeo configurado, no por modificar el controlador MVC.

### 5.5.4. ¿Por qué no usamos LocalDB dentro del contenedor?

La aplicación A de M02 utiliza SQL Server Express LocalDB, instalado en Windows y ligado a una cuenta de usuario. **No existe de modo ordinario dentro de una imagen Linux ASP.NET Core**. Copiar `appsettings.json` no instala SQL Server ni traslada la instancia existente.

Sería técnicamente posible diseñar una arquitectura de contenedores y un SQL Server accesible externamente, con gestión de conexiones y persistencia. Pero ello introduciría conceptos ajenos al objetivo elemental de esta sesión, además de romper la simplificación del temario. Tampoco sería correcto cambiarla sin explicaciones a SQLite: alteraríamos el proveedor y la semántica del ejemplo.

El laboratorio opta por una separación explícita: en el ensayo Docker se activa `Despliegue:SinLocalDb=true`. Esto omite únicamente la inicialización de base del arranque y rechaza con 503 las rutas de productos que dependen de SQL Server. Las páginas y recursos estáticos independientes siguen sirviéndose. La aplicación original conserva su CRUD para Windows y se puede volver a ejecutar allí sin esa opción.

La diferencia entre **servicio HTTP disponible** y **funcionalidad CRUD disponible** debe hacerse observable y explicarse, no ocultarse.

### 5.5.5. Construcción, ejecución y observación

La secuencia mínima que da sentido al Dockerfile es:

~~~powershell
docker build -t cursoweb-mvc:m05 .
docker images cursoweb-mvc
docker run --name cursoweb-m05 --rm `
  -e Despliegue__SinLocalDb=true `
  -p 8081:8080 cursoweb-mvc:m05
~~~

El comando `docker build` crea una imagen. `docker images` permite comprobar que existe. `docker run` inicia una instancia. La variable de entorno define el modo del ensayo sin alterar el repositorio. Desde otra terminal, `docker ps` informa de contenedores activos; `docker logs cursoweb-m05` permite observar la salida de la aplicación. El comando `docker stop cursoweb-m05` solicita detenerla; `--rm` ordena eliminar el contenedor una vez terminado.

Si el puerto del host está ocupado, modificar temporalmente el primer número de `-p` puede resolver el conflicto. Cambiar el puerto interno sin modificar el servidor que escucha en 8080 no lo hará.

### 5.5.6. Ciclo de vida y ausencia de persistencia añadida

Los archivos que genera una aplicación dentro del contenedor no deberían considerarse persistentes por defecto. Cuando se elimina el contenedor, su sistema de archivos de escritura puede desaparecer. El curso no introduce volúmenes ni bases externas en este experimento: basta con entender por qué el resultado es adecuado para demostrar ejecución, pero no para almacenar el catálogo MVC.

Los contenedores también tienen logs y estado de salida. Que `docker build` tenga éxito no implica que `docker run` mantenga el proceso activo. Para investigar si el proceso termina inmediatamente, leeríamos `docker logs`, comprobaríamos que la DLL existe y revisaríamos la configuración. Un navegador mostrando error de conexión puede indicar que no hay un contenedor ejecutándose; no demuestra por sí solo que la imagen se construyó mal.

### 5.5.7. Comparación final de Kestrel, IIS y Docker

| Dimensión | Kestrel en Windows | IIS en Windows | Docker Linux |
|---|---|---|---|
| Aplicación docente | MVC A | La misma MVC A | La misma MVC A |
| Artefactos | Salida `dotnet publish` | Carpeta publicada | Imagen multietapa |
| Inicio | Proceso `dotnet` | IIS + ASP.NET Core Module | `docker run` inicia `dotnet` |
| Puerto de ejemplo | 5091 | 8091 | Host 8081 → contenedor 8080 |
| LocalDB | Disponible si la instancia está preparada | Limitada por identidad del pool | No disponible de forma ordinaria |
| Rutas verificadas mínimas | Inicio y estado sin base | Inicio y estado sin base | Inicio y estado sin base |
| CRUD completo | Solo tras comprobar LocalDB real | No forma parte del ensayo IIS elemental | No forma parte del ensayo Linux |

La intención no es declarar ganadora a una modalidad, sino reconocer que **la misma aplicación puede publicarse de diferentes formas mientras cambian sus condiciones de ejecución**. La capa MVC sigue recibiendo solicitudes HTTP, pero varían los procesos, los permisos y los mecanismos de exposición del puerto.


### 5.5.8. La diferencia entre construir una imagen y ejecutar un proceso

Durante `docker build`, Docker interpreta el Dockerfile y produce una imagen. Los comandos `RUN` de su etapa de compilación se ejecutan en el proceso de construcción y preparan los archivos de aplicación. Al terminar, el hecho de tener una imagen no significa que exista un servidor web atendiendo solicitudes.

`docker run` crea y pone en marcha un contenedor a partir de esa imagen. En nuestro ejemplo, `ENTRYPOINT ["dotnet", "CursoWeb.Mvc.dll"]` define el programa que se ejecuta dentro del contenedor. Ese proceso inicia ASP.NET Core y su servidor HTTP. Si termina, el contenedor deja de estar en ejecución normal. Una imagen correcta puede, por tanto, producir un contenedor que termina inmediatamente debido a una mala configuración de ejecución.

La distinción puede expresarse con tres preguntas:

- ¿Existe una imagen construida con las capas previstas? Lo comprobamos con `docker images`.
- ¿Existe un contenedor en ejecución a partir de esa imagen? Lo comprobamos con `docker ps`.
- ¿El proceso del contenedor atiende una petición HTTP desde el host? Lo comprobamos abriendo la URL publicada mediante `-p`.

Estas observaciones no son sinónimos. Docker puede informar de un contenedor en marcha aunque la aplicación todavía esté inicializándose; también puede permitir crear un contenedor cuya ejecución termina antes de que nadie abra el navegador.

### 5.5.9. Por qué el contexto de construcción tiene tanta importancia como el Dockerfile

El comando `docker build -t cursoweb-mvc:m05 .` termina con un punto. Ese punto identifica el **contexto de construcción**. Las instrucciones `COPY` operan sobre los archivos enviados en ese contexto, no sobre cualquier ruta disponible en el equipo.

En nuestro Dockerfile aparece:

~~~dockerfile
WORKDIR /src
COPY . .
RUN dotnet restore CursoWeb.Mvc.csproj
RUN dotnet publish CursoWeb.Mvc.csproj -c Release --no-restore -o /app/publicada
~~~

Para que `CursoWeb.Mvc.csproj` aparezca en `/src`, debemos usar como contexto la carpeta del proyecto MVC que lo contiene. Si el alumno invoca `docker build` desde la raíz del repositorio con ese mismo Dockerfile y sin ajustar el contexto, puede copiar una estructura de carpetas diferente. El error de restauración posterior no significa que el SDK .NET 8 esté roto; significa que el archivo no está en la ruta esperada dentro de la etapa de construcción.

`.dockerignore` permite excluir archivos que no necesitamos enviar al contexto. Un directorio `bin` o `obj` creado durante el desarrollo no debería presentarse como fuente del nuevo build. La etapa de SDK se encarga de restaurar y publicar a partir de los archivos correctos.

El ejemplo mantiene un Dockerfile multietapa sencillo. En proyectos grandes podríamos reorganizar el orden de copias para aprovechar más capas en caché, pero esa optimización no es necesaria para comprender el recorrido fundamental de esta jornada.

### 5.5.10. La imagen final no necesita las herramientas utilizadas para construirla

La primera etapa del ejemplo utiliza `mcr.microsoft.com/dotnet/sdk:8.0`. Contiene el SDK y herramientas de construcción. La etapa final utiliza `mcr.microsoft.com/dotnet/aspnet:8.0`, que proporciona el runtime ASP.NET Core requerido para ejecutar la publicación.

La instrucción `COPY --from=compilacion /app/publicada .` incorpora a la etapa final la salida preparada en la etapa anterior. El resultado no necesita transportar el código fuente completo ni el SDK para iniciar el servidor HTTP. Esta separación hace más evidente que «compilar» y «ejecutar» son responsabilidades diferentes, incluso cuando se describen en un mismo Dockerfile.

Sin embargo, una imagen final pequeña no elimina requisitos de la aplicación. Si un programa necesita un servicio SQL, seguirá necesitándolo. La etapa runtime de ASP.NET Core no incorpora mágicamente una instancia LocalDB. El ejercicio deja intencionadamente ese CRUD fuera del recorrido Linux para mantener la fidelidad técnica con SQL Server Express LocalDB del curso.

### 5.5.11. Comprender el mapeo de puertos sin cambiar el código MVC

Supongamos un contenedor cuyo proceso ASP.NET Core escucha en 8080. Cuando ejecutamos:

~~~powershell
docker run --name cursoweb-m05 --rm -p 8081:8080 `
  -e Despliegue__SinLocalDb=true cursoweb-mvc:m05
~~~

Docker publica el puerto 8080 del contenedor a través del puerto 8081 del host. El navegador en Windows consulta `http://localhost:8081/`. El primer número de `-p` corresponde al lado del host, el segundo al del contenedor.

Si 8081 ya está ocupado, podemos elegir 8082 como puerto del host sin reescribir el Dockerfile, siempre que el proceso del contenedor continúe escuchando en 8080. Cambiar solamente el primer número resuelve la colisión exterior. Cambiar solamente el segundo a un puerto en el que la aplicación no escucha no proporciona acceso a la web.

La declaración `EXPOSE 8080` comunica la intención de usar ese puerto, pero **no crea automáticamente una publicación accesible desde el host**. Para la prueba elegimos explícitamente el mapeo con `-p`. Se trata de una decisión del entorno de ejecución y no de una ruta de controlador MVC.

### 5.5.12. Tres direcciones que el alumno debe mantener separadas

En la práctica aparecen al menos tres conceptos de dirección. La primera es la dirección que el servidor escucha **dentro del contenedor**; el Dockerfile la establece mediante `ASPNETCORE_URLS=http://+:8080`. La segunda es el puerto que Docker publica **en el host**, como 8081. La tercera es la URL concreta que abre el navegador del alumno, `http://localhost:8081/`.

No hay contradicción en que dos números distintos aparezcan en la misma aplicación. El navegador no tiene que conocer el puerto interno si utiliza el publicado por Docker. El servidor ASP.NET Core tampoco necesita saber qué número de host ha elegido el docente, porque sigue escuchando internamente en 8080.

Una avería típica consiste en abrir `http://localhost:8080/` desde el host y concluir que el contenedor no funciona. Si no se ha publicado ese puerto exterior, la solicitud no corresponde al mapeo real. El diagnóstico empieza por `docker ps`, donde podemos comprobar el nombre del contenedor, su estado y los puertos publicados.

### 5.5.13. Variables de entorno como decisiones de ejecución

Docker permite suministrar variables al iniciar el contenedor:

~~~powershell
docker run --name cursoweb-m05 --rm `
  -e Despliegue__SinLocalDb=true `
  -p 8081:8080 cursoweb-mvc:m05
~~~

La variable hace que la aplicación .NET interprete la clave `Despliegue:SinLocalDb` como verdadera. El mismo ensamblado y la misma imagen podrían iniciarse con otros valores, pero sus dependencias reales cambiarían. No debemos ocultarlo detrás de la frase «Docker adapta automáticamente la base».

Con esta configuración la portada y los recursos sin dependencia SQL siguen disponibles. Las rutas del catálogo MVC que requieren LocalDB deben responder 503. El servidor está operativo; la funcionalidad CRUD no lo está. La variable permite demostrar un límite controlado sin modificar el proveedor EF Core ni inventar persistencia.

En un entorno productivo, la configuración requeriría criterios de seguridad y gestión de secretos que aquí no se desarrollan. La variable utilizada no contiene credenciales: expresa únicamente una opción didáctica de ejecución.

### 5.5.14. La vida de un contenedor y la vida de los datos no son equivalentes

Una imagen se conserva después de detener un contenedor, salvo que se elimine expresamente. Un contenedor creado desde esa imagen tiene un ciclo de vida de ejecución. Sus archivos de escritura no deberían utilizarse como almacenamiento persistente implícito de datos de negocio cuando el contenedor se elimina.

En el ejemplo usamos `--rm` para que Docker retire el contenedor al terminar. Esa elección simplifica la limpieza del laboratorio, pero significa que no esperamos conservar el estado de escritura de ese contenedor. No se incorporan volúmenes ni un SQL Server externo; sería necesario enseñar una infraestructura distinta para explicar correctamente esa persistencia.

Tampoco la presencia de una variable que evita LocalDB crea una base en memoria que admita el CRUD MVC. Al contrario: el middleware explica la indisponibilidad de las rutas que requerirían SQL. El resultado permite aprender el ciclo de vida de una aplicación real sin atribuirle capacidades que no tiene.

### 5.5.15. Leer `docker ps` y `docker logs` como pruebas con distinto alcance

`docker ps` informa de contenedores en ejecución y su configuración general. Nos ayuda a comprobar si el proceso sigue activo y cómo se han publicado los puertos. Si el contenedor no aparece, quizá terminó, no llegó a arrancar o fue eliminado tras su finalización por `--rm`.

`docker logs cursoweb-m05` muestra la salida registrada del contenedor mientras existe. Puede revelar errores de inicio de ASP.NET Core, direcciones de escucha y excepciones de aplicación. Es una evidencia diferente a la del navegador.

`curl.exe -i http://localhost:8081/Productos/Estado` pregunta algo más concreto: «¿qué responde esta ruta desde el host ahora mismo?». Aunque el contenedor figure en ejecución y los logs no contengan errores, debemos solicitar HTTP para demostrar que el mapeo de puertos y la ruta funcionan.

Por tanto, las tres comprobaciones se complementan: contenedor activo, salida del proceso y respuesta de red. Si una falla, conviene localizar en qué etapa se produjo la interrupción antes de reconstruir la imagen.

### 5.5.16. Caso razonado: la imagen se construye y el navegador no conecta

El alumno ejecuta `docker build` y obtiene una imagen. Después intenta abrir `http://localhost:8081/`, pero el navegador informa de que no se puede establecer conexión. ¿Podemos afirmar que el Dockerfile está mal? No todavía.

Primero debemos saber si se ejecutó `docker run`. La construcción no inicia automáticamente el servidor. Segundo, comprobar si el contenedor sigue en ejecución; un proceso que terminó puede haber dejado la imagen intacta. Tercero, examinar el mapeo de puertos efectivo. Si se publicó 8082:8080, la URL 8081 no corresponde al contenedor.

Solo después procede revisar los logs de arranque y el programa. Una excepción durante el inicio de ASP.NET Core, una variable de configuración ausente o una incompatibilidad en los artefactos publicados podrían explicar que el proceso no atendiera nunca una solicitud.

**Conclusión del caso:** debemos separar una imagen disponible, un contenedor activo y una aplicación web accesible. Comprobar una condición no garantiza automáticamente las restantes.

### 5.5.17. Caso razonado: HTTP 200 en la portada y 503 en productos

El mismo contenedor devuelve 200 en `/`, 200 en `/css/site.css` y 200 en `/Productos/Estado`, pero devuelve 503 en `/Productos`. Es un resultado esperado bajo el modo `Despliegue:SinLocalDb=true`.

La observación demuestra ejecución real del host, middleware de archivos estáticos y rutas MVC. La ruta de productos no contiene un catálogo ficticio para el contenedor: declara que la base SQL Server Express LocalDB no está disponible en ese entorno.

Sería improcedente sustituir LocalDB por SQLite solo para conseguir un 200 más. El objetivo pedagógico es comparar hospedajes y sus dependencias, no rediseñar la persistencia ni falsear una función. Si quisiéramos un CRUD Linux con SQL Server, habría que preparar de forma explícita otra infraestructura accesible al contenedor, dentro de un proyecto distinto al recorrido mínimo acordado.

### 5.5.18. Una comparación causal con los otros dos hospedajes

Con Kestrel en Windows iniciamos una publicación como un proceso `dotnet` y elegimos su dirección local. Con IIS en Windows registramos un sitio y el ASP.NET Core Module participa en su hospedaje. Con Docker creamos una imagen y ejecutamos un contenedor que inicia ASP.NET Core en un entorno Linux.

En todos ellos el código MVC conserva su responsabilidad de responder a solicitudes mediante controladores, vistas y archivos estáticos. Lo que cambia es el mecanismo de inicio, la identidad, el sistema de archivos visible, los puertos y las dependencias disponibles.

El objetivo no es decidir qué tecnología es mejor para todos los usos. Una elección empresarial exigiría evaluar mantenimiento, seguridad, redes, datos, observabilidad y operación, asuntos que esta jornada solo menciona para dejar claros sus límites. Aquí aprendemos a describir una publicación sencilla y a demostrar con observaciones verificables qué parte de la misma aplicación funciona bajo cada mecanismo.



### 5.5.19. Conclusión del curso

Tras M05 el alumno habrá recorrido dos ideas complementarias: una aplicación Blazor que se comunica correctamente con una API y una aplicación MVC que puede ser publicada y ejecutada en distintas modalidades de hospedaje. Habrá aprendido a distinguir compilación de ejecución, respuesta HTTP de funcionamiento completo, interfaz de servidor, y estado temporal de persistencia.

El criterio de éxito no es reproducir un comando aislado. Es poder explicar **qué proceso se está ejecutando, qué recurso sirve, qué dependencias utiliza y qué evidencia demuestra realmente que funciona**.


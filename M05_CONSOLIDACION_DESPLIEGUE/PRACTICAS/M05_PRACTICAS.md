# M05 — Prácticas: consolidación y despliegue elemental

## Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8

**CURSO: Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8**

**TIPO: PRÁCTICAS**

**AUTOR: JAIME GALLO**

## Índice del módulo

- [P5.1 — Consolidar Blazor y la API de productos](#punto-1)
- [P5.2 — Compilar y publicar la aplicación MVC](#punto-2)
- [P5.3 — Ejecutar la publicación en Kestrel](#punto-3)
- [P5.4 — Publicar en IIS](#punto-4)
- [P5.5 — Crear y ejecutar un contenedor Docker](#punto-5)

## Cómo utilizar este manual

Aquí se realiza la construcción y comprobación, **después de haber estudiado las explicaciones y ejemplos del manual de teoría**. Las aplicaciones no aparecen mágicamente terminadas: M05 continúa los proyectos ya construidos en módulos anteriores. El repositorio contiene un estado docente de referencia que permite comparar el resultado, pero el alumno realizará cada transformación indicada y observará una respuesta antes de avanzar.

Trabajaremos con dos aplicaciones y una API auxiliar:

| Recurso | Carpeta de referencia dentro del módulo | Utilización |
|---|---|---|
| Aplicación B Blazor Web App Interactive Server | `M05_CONSOLIDACION_DESPLIEGUE/PROYECTO/BLAZOR/CursoWeb.Blazor` | P5.1 |
| API auxiliar de productos | `M05_CONSOLIDACION_DESPLIEGUE/PROYECTO/API/CursoWeb.ProductosApi` | P5.1 |
| Aplicación A MVC con EF Core/LocalDB de M02 | `M05_CONSOLIDACION_DESPLIEGUE/PROYECTO/MVC/CursoWeb.Mvc` | P5.2–P5.5 |

Las tres carpetas son estados del **mismo curso**, no aplicaciones empresariales independientes que deban rediseñarse. P5.1 usa B y API; P5.2–P5.5 usan siempre la misma A. El laboratorio utiliza Windows, Visual Studio con .NET 8 y SQL Server Express LocalDB allí donde el CRUD necesita persistencia. Para IIS se requiere Windows con IIS y Hosting Bundle 8; para Docker se requiere un motor Docker operativo con contenedores Linux. Una infraestructura ausente se anota como **no comprobada**, nunca como prueba aprobada.

### Tiempo de la jornada

| Punto | Teoría | Práctica |
|---|---:|---:|
| 5.1 Consolidación Blazor | 10 min | 90 min |
| 5.2 Ejecutar/publicar | 15 min | 35 min |
| 5.3 Kestrel | 10 min | 45 min |
| 5.4 IIS | 15 min | 55 min |
| 5.5 Docker | 10 min | 45 min |
| **Subtotal** | **60 min** | **270 min** |

Se reservan otros **30 minutos** para dudas y recuperación. Las ampliaciones y el diagnóstico extendido no son nuevos ejercicios presenciales obligatorios.

Conserva una terminal por proceso, comprueba desde qué carpeta ejecutas cada comando y no atribuyas resultados de un servicio a otro. Cada ejercicio concluye con un estado final comprobable, que sirve de punto de partida para el siguiente cuando corresponda.

## P5.1. Consolidar el catálogo Blazor y la API HTTP

### Objetivo, estado inicial y resultado previsto

Partimos de la aplicación Blazor Interactive Server que funciona al finalizar M04 y de la API de productos construida allí. Queremos comprobar toda la cadena: pedir productos, mostrar datos, intentar crear un producto inválido, crear uno válido y consultar de nuevo el servidor. No añadiremos Identity/JWT, no crearemos otra aplicación Blazor y no conectaremos esta API de memoria a LocalDB.

El estado inicial contiene:

- `CursoWeb.Blazor/Program.cs`, que registra `IProductosApiService` como cliente HTTP tipado.
- `Components/Pages/CatalogoRemoto.razor`, que consulta y permite crear productos.
- `Services/IProductosApiService.cs` y `Services/ProductosApiService.cs`, que encapsulan GET/POST.
- `CursoWeb.ProductosApi/Program.cs`, con `GET /api/productos` y `POST /api/productos`.

El resultado observable de salida será una pantalla que obtiene dos productos iniciales, incorpora un tercero sin alterar la API, informa de errores y permite realizar una consulta explícita cuando el catálogo del servidor haya cambiado.

### Paso P5.1.1. Recuperar las aplicaciones correctas

Desde la raíz del repositorio del curso abre dos terminales de PowerShell. En la primera, identifica y compila la API de productos:

~~~powershell
dotnet build .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\CursoWeb.ProductosApi.csproj
~~~

En la segunda compila el proyecto Blazor:

~~~powershell
dotnet build .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\BLAZOR\CursoWeb.Blazor\CursoWeb.Blazor.csproj
~~~

**Qué estamos comprobando:** ambos proyectos tienen sus dependencias y sintaxis válidas. Todavía no sabemos si hay comunicación HTTP porque no hemos iniciado el servidor. Si falla la compilación, comprobar que el SDK 8 aparece con `dotnet --list-sdks`, que los comandos parten de la raíz y que la restauración NuGet ha funcionado.

### Paso P5.1.2. Iniciar la API y observar su contrato

En la primera terminal:

~~~powershell
dotnet run --project .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\CursoWeb.ProductosApi.csproj --no-launch-profile --urls http://localhost:5081
~~~

Sin cerrar la terminal, desde un navegador visita `http://localhost:5081/api/productos`. Debes ver un arreglo JSON con al menos Cuaderno y Lápiz en una API recién iniciada. Comprueba además un producto que no existe:

~~~powershell
curl.exe -i http://localhost:5081/api/productos/999
~~~

Debe devolver **404 Not Found**; no significa que la API esté apagada. El servidor ha recibido la solicitud y ha indicado que ese identificador no corresponde a un producto existente. Si la URL de lista no responde, comprobar que el proceso sigue activo y que no hay otra API utilizando el puerto.

### Paso P5.1.3. Arrancar Blazor y comprobar la primera consulta

En la segunda terminal:

~~~powershell
dotnet run --project .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\BLAZOR\CursoWeb.Blazor\CursoWeb.Blazor.csproj --no-launch-profile --urls http://localhost:5092
~~~

Abre `http://localhost:5092/catalogo-remoto`. Debe mostrarse el catálogo remoto; la página local `/productos` conserva el trabajo de M03 y no sustituye al endpoint HTTP de M04.

Abre `appsettings.json` del proyecto Blazor y comprueba que la dirección de productos es:

~~~json
{
  "ProductosApi": {
    "BaseUrl": "http://localhost:5081/"
  },
  "IdentityJwtApi": {
    "BaseUrl": "http://localhost:5086/"
  }
}
~~~

No hace falta ejecutar la API Identity/JWT: su dirección existe en configuración porque se conservó la ampliación, pero `/catalogo-remoto` consume `ProductosApi`. Si el catálogo remoto no se carga, llama primero directamente a la API y revisa después `ProductosApi:BaseUrl`.

### Paso P5.1.4. Añadir la consulta explícita «Consultar servidor»

La versión de trabajo de M04 obtenía productos durante `OnInitializedAsync`. El archivo de partida se conserva como **variante inicial fuera del proyecto compilable**, en `PROYECTO/VARIANTES/P5.1_ANTES/Components/Pages/CatalogoRemoto.razor`. Si ya has recibido el proyecto final M05, compara con esta variante antes de realizar manualmente la transformación. Queremos permitir una segunda consulta sin reconstruir toda la página. En `Components/Pages/CatalogoRemoto.razor`, debajo del párrafo introductorio, añade:

~~~razor
<button id="recargar-api"
        disabled="@cargando"
        @onclick="ConsultarAsync">
    Consultar servidor
</button>
~~~

La propiedad `disabled` evita iniciar consultas simultáneas desde el mismo botón mientras una operación ya está cargando. No evita por sí sola cualquier concurrencia posible; es una simplificación adecuada para este laboratorio.

Después localiza el método `OnInitializedAsync`. Sustitúyelo por la siguiente delegación y método de consulta. **No crees otro `OnInitializedAsync`**: debe existir una sola implementación del mismo ciclo de vida.

~~~csharp
protected override async Task OnInitializedAsync() =>
    await ConsultarAsync();

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
~~~

El ejemplo supone que el componente conserva sus campos de M04:

~~~csharp
private List<ProductoDto> productos = [];
private bool cargando = true;
private string? error;
~~~

El código final de referencia contiene esos campos y el método ya integrado. Compila y abre la página. Pulsa «Consultar servidor»: debe seguir mostrando la lista. La intención no es producir un nuevo diseño de UI, sino comprobar que el mismo servicio puede reutilizarse desde el ciclo de vida y desde un evento del usuario.

### Paso P5.1.5. Crear y validar sin introducir duplicidades

La página de M04 conserva el formulario Nombre/Precio y su método `CrearAsync`. Antes de pulsar «Crear en API», deja el nombre vacío e indica precio 0: el componente debe responder **«Indica un nombre y un precio mayor que cero»** sin enviar una creación válida.

Después introduce:

| Campo | Valor |
|---|---|
| Nombre | Regla |
| Precio | 1.75 |

Pulsa «Crear en API». El servicio tipado debe enviar POST y recibir un `ProductoDto` con identificador asignado por el servidor. Debe aparecer el mensaje de creación y el producto debe añadirse a la lista. Desde otra terminal solicita directamente la lista de la API y comprueba que también incluye Regla.

**Distinción importante:** si el mensaje aparece porque el DTO devuelto se incorporó a la lista local, todavía no hemos probado que un segundo cliente consulte el estado del servidor. Esa es la razón del siguiente paso.

### Paso P5.1.6. Comparar estado local y servidor

Manteniendo abierta Blazor, añade otro producto a la API directamente. Crea en una carpeta temporal un fichero `producto-prueba.json`:

~~~json
{
  "nombre": "Archivador",
  "precio": 5.25
}
~~~

Ejecuta desde la carpeta que contiene ese archivo:

~~~powershell
curl.exe -i -X POST http://localhost:5081/api/productos -H "Content-Type: application/json" --data-binary "@producto-prueba.json"
~~~

La API responderá 201. **Antes** de pulsar «Consultar servidor», la pantalla Blazor no tiene por qué mostrar Archivador: no ha recibido ninguna notificación push. Al pulsar el botón de consulta, la lista debe incluirlo. Es una demostración observable de la diferencia entre estado mostrado y fuente de datos.

Detén **solo la API**, sin cerrar la ventana Blazor. Pulsa «Consultar servidor» de nuevo: aparecerá un mensaje de fallo de red o de tiempo, según la causa observada. Vuelve a iniciar la API; la consulta recupera los productos iniciales, porque esta API utiliza memoria. No interpretes la desaparición de Regla/Archivador como una pérdida de SQL Server ni como un error de Blazor.

### Paso P5.1.7. Completar la cadena de diagnóstico

Recorre esta matriz antes de considerar la integración terminada:

| Comprobación | Acción | Resultado esperado |
|---|---|---|
| API disponible | GET directo a `/api/productos` | 200 JSON |
| Identificador inexistente | GET a `/api/productos/999` | 404 |
| Blazor disponible | Abrir `/catalogo-remoto` | HTML y componente interactivo |
| Alta inválida desde UI | Nombre vacío, precio 0 | Rechazo local |
| Alta válida desde UI | Regla, 1.75 | Producto creado |
| Alta desde cliente externo | POST de Archivador | 201 y nuevo DTO |
| Estado no actualizado automáticamente | Observar Blazor antes de consultar | No asumir push |
| Actualización explícita | Pulsar «Consultar servidor» | Catálogo actualizado |
| API detenida | Consultar de nuevo | Mensaje de error |
| API reiniciada | Volver a consultar | Datos de inicio |

Si los resultados no coinciden, diagnostica empezando en la API directa, después servicio tipado y finalmente el componente. No copies un `Program.cs` ajeno para resolver un problema de puerto. Esta matriz describe escenarios observables que el alumno puede ejecutar; la confirmación técnica automática se documenta fuera del material docente.


### Paso P5.1.8. Diferenciar ausencia de resultados y error de comunicación

**Relación con la teoría:** apartados 5.1.10, 5.1.12 y 5.1.13. Hemos aprendido que recibir un arreglo vacío no es lo mismo que no recibir respuesta HTTP. La interfaz inicial representaba la lista mediante un `<ul>`; si el servidor devolvía `[]`, el usuario veía una lista sin elementos, pero no una explicación del estado.

**Situación inicial.** El componente `M05_CONSOLIDACION_DESPLIEGUE/PROYECTO/BLAZOR/CursoWeb.Blazor/Components/Pages/CatalogoRemoto.razor` ya posee la propiedad `productos`, el indicador `cargando` y la propiedad `error`. No añadiremos otra llamada al servidor ni otro servicio. Cambiaremos únicamente la presentación de una colección recibida satisfactoriamente.

**Archivo que debes editar:** `PROYECTO/BLAZOR/CursoWeb.Blazor/Components/Pages/CatalogoRemoto.razor`, siempre interpretando esa ruta desde la carpeta `M05_CONSOLIDACION_DESPLIEGUE`.

Busca el bloque de renderizado. Después de la rama que comprueba `error`, y antes del `else` que dibuja el `<ul>`, introduce esta rama:

~~~razor
else if (productos.Count == 0)
{
    <p id="estado-api">
        El servidor respondió correctamente, pero no hay productos disponibles.
    </p>
}
~~~

El orden es parte del ejercicio, no un detalle cosmético. Si pusiéramos la comprobación de lista vacía antes del error, podríamos mostrar «no hay productos» cuando la conexión ha fallado y la lista simplemente no llegó a cargarse. Si la situáramos después de la rama `else` final, sería código inalcanzable dentro de esa secuencia de condiciones.

El conjunto de ramas, una vez construido, debe conservar este orden lógico:

~~~razor
@if (cargando)
{
    <p id="estado-api" role="status">Cargando catálogo remoto...</p>
}
else if (error is not null)
{
    <p id="error-api" role="alert">@error</p>
}
else if (productos.Count == 0)
{
    <p id="estado-api">
        El servidor respondió correctamente, pero no hay productos disponibles.
    </p>
}
else
{
    <p id="estado-api">Catálogo remoto disponible</p>
    <ul id="productos-api">
        @foreach (var producto in productos)
        {
            <li>@producto.Nombre — @producto.Precio.ToString("0.00") €</li>
        }
    </ul>
}
~~~

Este bloque usa los campos que ya creó M04; **no** debes duplicar sus declaraciones ni insertar otra propiedad con el mismo nombre. En el árbol de proyecto de referencia la transformación ya aparece aplicada. Para reconstruirla desde el estado anterior, utiliza `PROYECTO/VARIANTES/P5.1_ANTES/Components/Pages/CatalogoRemoto.razor` y vuelve a incorporar primero los cambios de P5.1.4 y después los de este apartado.

Compila el proyecto:

~~~powershell
dotnet build .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\BLAZOR\CursoWeb.Blazor\CursoWeb.Blazor.csproj
~~~

**Resultado intermedio esperado:** el proyecto compila y, con la API normal, sigue mostrando Cuaderno y Lápiz. Esto confirma que la rama nueva no ha roto el escenario conocido. Todavía no confirma que el mensaje de colección vacía se muestre realmente. Ese escenario se ejecuta a continuación.

**Razonamiento solicitado al alumno:** explica por qué una rama de error tiene prioridad sobre una rama de lista vacía y por qué ninguna de las dos demuestra, por sí sola, que el proceso de Blazor está detenido. La respuesta debe identificar la diferencia entre una respuesta HTTP válida, un error de transporte y la decisión de renderizado.

### Paso P5.1.9. Preparar una variante reversible del mismo servidor

**Relación con la teoría:** 5.1.3, 5.1.12 y 5.1.16. Para estudiar un catálogo vacío y un cuerpo JSON inválido no hace falta crear una tercera aplicación ni modificar el proyecto Blazor. Podemos sustituir temporalmente **un solo archivo** de la API por una variante completa, incluida en el repositorio, con tres modos de salida seleccionados mediante configuración.

El archivo de referencia para esta ampliación se encuentra en:

`M05_CONSOLIDACION_DESPLIEGUE/PROYECTO/VARIANTES/P5.1_DIAGNOSTICO/Program.cs`

No es otro proyecto ni un resultado que el estudiante tenga que inventar. Contiene los mismos endpoints de la API de M04; únicamente cambia la respuesta de `GET /api/productos` cuando se elige expresamente un escenario de diagnóstico. Por defecto, sigue atendiendo el GET normal.

**Preparación segura.** Detén el proceso de la API con Ctrl+C. Puedes mantener Blazor abierto. Abre una terminal PowerShell en la raíz del repositorio y ejecuta las instrucciones completas siguientes:

~~~powershell
$origen = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\Program.cs"
$variante = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\VARIANTES\P5.1_DIAGNOSTICO\Program.cs"
$respaldo = "$origen.p51-copia"

Copy-Item $origen $respaldo -Force
Copy-Item $variante $origen -Force

dotnet build .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\CursoWeb.ProductosApi.csproj
~~~

No suprimas la copia de seguridad hasta haber terminado los tres escenarios. Si al copiar el archivo aparece un error de acceso, comprueba que el proceso de API se ha detenido. Si falla la compilación, restaura inmediatamente el original con el procedimiento final de este apartado y comprueba que sigues partiendo de la misma versión del curso.

**Qué contiene la variante.** Localiza `ObtenerCatalogo` y observa la selección de una respuesta en función del valor `Laboratorio:EscenarioCatalogo`:

~~~csharp
IResult ObtenerCatalogo()
{
    if (escenarioCatalogo == "vacio")
        return Results.Ok(Array.Empty<ProductoApi>());

    if (escenarioCatalogo == "json-invalido")
        return Results.Text("{\"productos\":[", "application/json");

    return Results.Ok(productos.Values.OrderBy(p => p.Id));
}

app.MapGet("/api/productos", ObtenerCatalogo);
~~~

El bloque depende del resto del `Program.cs` **completo** que se ha entregado: la variable de configuración, el diccionario de productos y el tipo `ProductoApi` ya aparecen en él. No copies solo estas líneas en otro proyecto vacío. `Results.Ok(Array.Empty<ProductoApi>())` constituye una respuesta 200 con colección válida vacía. `Results.Text` entrega, intencionadamente, contenido malformado con tipo de medio JSON para mostrar que un HTTP 200 tampoco garantiza poder deserializar el cuerpo. Esta variante se reserva al entorno de aprendizaje.

### Paso P5.1.10. Ejecutar tres respuestas sin modificar el componente Blazor

**Escenario A — servidor y catálogo normales.** En la terminal de API, desde la raíz del repositorio:

~~~powershell
$env:Laboratorio__EscenarioCatalogo = "normal"
dotnet run --project .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\CursoWeb.ProductosApi.csproj --no-launch-profile --urls http://localhost:5081
~~~

Desde otra terminal ejecuta:

~~~powershell
curl.exe -i http://localhost:5081/api/productos
~~~

Debe observarse HTTP 200 con un arreglo que contiene Cuaderno y Lápiz. Pulsa «Consultar servidor» en `http://localhost:5092/catalogo-remoto` y comprueba que aparecen los productos. El resultado confirma que copiar el archivo de variante no cambia el comportamiento normal mientras la configuración sea `normal`.

**Escenario B — servidor disponible, lista vacía.** Detén la API con Ctrl+C y, en su terminal, ejecuta:

~~~powershell
$env:Laboratorio__EscenarioCatalogo = "vacio"
dotnet run --project .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\CursoWeb.ProductosApi.csproj --no-launch-profile --urls http://localhost:5081
~~~

Comprueba otra vez la URL directa. El código de respuesta seguirá siendo **200**; el cuerpo debe representar `[]`. En Blazor pulsa «Consultar servidor». Ahora debe aparecer el mensaje «El servidor respondió correctamente, pero no hay productos disponibles». No debe aparecer el mensaje de error de comunicación. Comprueba que el botón sigue habilitándose después de la consulta.

**Razón:** el servidor funciona y está cumpliendo un contrato de colección, pero esa colección no tiene elementos. Si la interfaz lo presentara como fallo, enseñaría una conclusión falsa.

**Escenario C — servidor disponible, contenido JSON incorrecto.** Vuelve a detener la API y ejecuta:

~~~powershell
$env:Laboratorio__EscenarioCatalogo = "json-invalido"
dotnet run --project .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\CursoWeb.ProductosApi.csproj --no-launch-profile --urls http://localhost:5081
~~~

Consulta mediante `curl.exe -i` el mismo endpoint. Observa que puede responder **HTTP 200**, pero el cuerpo no representa una lista JSON deserializable. En Blazor pulsa «Consultar servidor» y comprueba que se muestra el aviso «La API no devolvió un catálogo JSON válido». La rama de error tiene prioridad sobre la condición de lista vacía.

**Razón:** el transporte y el código de respuesta HTTP han funcionado; el contrato de contenido no. Cambiar de puerto al azar no corregiría el problema porque la respuesta llega al destino correcto.

**Restauración obligatoria del ejercicio.** Detén la API y ejecuta:

~~~powershell
$origen = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\Program.cs"
$respaldo = "$origen.p51-copia"

Copy-Item $respaldo $origen -Force
Remove-Item $respaldo
Remove-Item Env:\Laboratorio__EscenarioCatalogo -ErrorAction SilentlyContinue

dotnet build .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\API\CursoWeb.ProductosApi\CursoWeb.ProductosApi.csproj
~~~

Arranca otra vez la API en su modo normal y pulsa «Consultar servidor». Deben reaparecer Cuaderno y Lápiz. Si decides conservar el proyecto para seguir practicando, la restauración garantiza que el siguiente alumno no encuentre una API que devuelve JSON defectuoso por una prueba anterior.

### Paso P5.1.11. Comprobar un rechazo de servidor que el formulario local no puede ocultar

**Relación con la teoría:** 5.1.5 y 5.1.14. El componente Blazor valida un nombre y un precio antes de enviar el POST. Pero otro cliente HTTP puede saltarse la interfaz; el servidor debe validar por sí mismo.

Con la API normal arrancada, crea un archivo temporal `producto-invalido.json`, fuera de la carpeta de código, con este contenido íntegro:

~~~json
{
  "nombre": "     ",
  "precio": 0
}
~~~

Desde la carpeta donde guardaste el JSON, ejecuta:

~~~powershell
curl.exe -i -X POST http://localhost:5081/api/productos -H "Content-Type: application/json" --data-binary "@producto-invalido.json"
~~~

La API debe devolver **400 Bad Request**. Vuelve a solicitar `GET /api/productos` y comprueba que no aparece un producto nuevo creado por esa petición. Después vuelve a Blazor, intenta enviar el mismo nombre y precio mediante el formulario y observa el rechazo local.

El ejercicio demuestra dos validaciones con responsabilidades diferentes: la interfaz impide un envío evitable, pero el endpoint rechaza de manera independiente cualquier cliente que incumpla el contrato. No debemos considerar la API protegida solo porque la pantalla esté programada correctamente.

**Cierre razonado del caso:** enumera qué pruebas demostrarían que la API está detenida, que ha respondido con una colección válida vacía, que ha respondido 200 con JSON malformado y que ha rechazado un POST. En los cuatro casos el aspecto inicial puede parecerse, pero el diagnóstico correcto exige comparar estado HTTP, cuerpo y mensaje del componente.



### Resultado final y conexión con P5.2

La aplicación B está consolidada cuando GET, POST, validación, error y recarga quedan comprensibles y reproducibles. Detén ambos procesos al terminar. Desde P5.2 dejamos de utilizar Blazor y su API: los tres mecanismos de publicación siguientes se comprobarán **solo con la aplicación MVC A**, evitando ejecutar servicios adicionales que no participan en ese ensayo.

### Ampliación autónoma P5.1: tres causas de una pantalla vacía

Estudia por separado estos casos sin alterar el contrato del proyecto principal: API apagada, endpoint correcto que devuelve lista vacía y endpoint que devuelve JSON incompatible. Una lista vacía válida puede representarse como `[]`; una conexión rechazada no tiene una respuesta HTTP 200; una respuesta con JSON incompatible falla durante la deserialización.

La conclusión no debe depender solo del color de un mensaje en pantalla. Explica en cuál de las capas nace cada resultado y qué comprobación directa lo demuestra. Una vez finalizado, restaura la API original de referencia para que el siguiente alumno comience desde un estado conocido.


## P5.2. Compilar, ejecutar y publicar la aplicación MVC A

### Objetivo y material inicial

Recuperaremos MVC A de M02. Es importante comenzar desde el proyecto correcto: la carpeta `PROYECTO/MVC/CursoWeb.Mvc` conserva controladores, vistas Razor, un ejemplo Razor Pages, EF Core 8 y SQL Server Express LocalDB. No vamos a crear una nueva plantilla MVC, porque ello rompería la continuidad de M01 y M02. Tampoco vamos a copiar archivos de Blazor ni de la API a MVC.

El estado inicial de esta actividad es el proyecto MVC con su cadena `ConnectionStrings:Productos` y el CRUD existente. El estado final será una **publicación independiente de Visual Studio**, comprobada en cuanto a archivos y preparada para ejecutarse mediante Kestrel.

### Paso P5.2.1. Identificar los tres conceptos con acciones concretas

Abre una terminal PowerShell en la raíz del repositorio y define las rutas, sin copiarlas a un directorio dentro de `wwwroot`:

~~~powershell
$proyecto = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc\CursoWeb.Mvc.csproj"
$salida = ".\.work\M05\publicacion-mvc"
New-Item -ItemType Directory -Force ".\.work\M05" | Out-Null
~~~

Primero compila:

~~~powershell
dotnet build $proyecto -c Release
~~~

Observa el mensaje de finalización y la carpeta `bin/Release/net8.0` del proyecto. Una compilación sin errores solo demuestra que se han podido producir los ensamblados; no confirma ni que LocalDB esté accesible ni que el host haya respondido a una petición HTTP.

### Paso P5.2.2. Comprobar que la aplicación sigue siendo la de M02

Abre el archivo `Program.cs`. Puedes contrastarlo con la versión acumulativa original del módulo M02, guardada fuera del proyecto compilable en `PROYECTO/VARIANTES/P5.2_ANTES/Program.cs`; esa variante es solo una referencia inicial para reconocer el añadido de M05. Localiza las dos responsabilidades que llegan del módulo anterior:

~~~csharp
builder.Services.AddControllersWithViews();
builder.Services.AddRazorPages();
~~~

El programa debe seguir registrando el contexto mediante `UseSqlServer` con la cadena `Productos`. No lo sustituyas por SQLite ni elimines los controladores de productos. El código de M05 añade una opción explícita de despliegue que examinaremos más tarde; **por defecto en el laboratorio Windows el modo con LocalDB sigue disponible**.

Desde Visual Studio inspecciona `Views/Productos` y `Pages/Comparacion.cshtml`; comprueba que la estructura permanece. Esta observación es relevante: publicar una aplicación existente no equivale a reconstruirla desde una plantilla nueva.

### Paso P5.2.3. Ejecutar el proyecto desde su origen

Con SQL Server Express LocalDB disponible en Windows y sin un proceso previo en el mismo puerto, ejecuta:

~~~powershell
dotnet run --project $proyecto -c Release --no-launch-profile --urls http://localhost:5091
~~~

Abre `http://localhost:5091/` y `http://localhost:5091/Productos/Estado`. La segunda ruta debe devolver `Catalogo MVC disponible`. Si además abres `/Productos`, el resultado correcto dependerá de que LocalDB funcione realmente bajo tu usuario. Si falta la instancia o no se puede crear la base, no declares que el CRUD ha quedado probado: resuelve esa dependencia antes de usarlo como evidencia.

Detén el proceso con `Ctrl+C` para liberar el puerto. No mantengas al mismo tiempo dos aplicaciones MVC intentando ocupar 5091.

### Paso P5.2.4. Publicar a una carpeta conocida

Ejecuta:

~~~powershell
dotnet publish $proyecto -c Release -o $salida
~~~

Inspecciona el contenido:

~~~powershell
Get-ChildItem $salida | Select-Object Name, Length
Get-ChildItem "$salida\wwwroot" -Recurse | Select-Object FullName
~~~

Localiza la DLL, los archivos `.deps.json` y `.runtimeconfig.json`, la configuración y los recursos estáticos. El archivo `web.config` puede aparecer como parte del soporte de publicación ASP.NET Core para IIS. La ausencia de una vista como `.cshtml` físico separado no demuestra que la vista esté perdida; habrá que abrirla después desde una petición real.

Si `dotnet publish` falla, revisa la salida completa. No borres el proyecto original para volver a empezar: una incidencia de restauración, compilación o permiso de carpeta se diagnostica por separado.

### Paso P5.2.5. Comparar ejecución del proyecto y de publicación

Compara estas dos instrucciones:

~~~powershell
# Ejecuta usando la estructura de proyecto:
dotnet run --project $proyecto -c Release --no-launch-profile --urls http://localhost:5091

# Ejecución de la publicación, desde su directorio:
Push-Location $salida
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5091
Pop-Location
~~~

No ejecutes las dos a la vez. La segunda es el punto de partida de P5.3 y presupone que la salida existe. Si `dotnet .\CursoWeb.Mvc.dll` falla por una dependencia LocalDB, comprueba si la base está disponible y recuerda que ese fallo de arranque no invalida por sí solo que los archivos se hayan publicado correctamente. Para el modo sin base existe una configuración explícita que utilizaremos más tarde.


### Paso P5.2.6. Reconocer los artefactos imprescindibles sin confundirlos con fuentes

**Relación con la teoría:** 5.2.7–5.2.11. Hemos publicado la misma aplicación que desarrollamos en M02; ahora debemos explicar qué representa cada archivo sin atribuirle capacidades que no posee.

Mantén la variable `$salida` establecida en P5.2.1. No necesitas tener el servidor en ejecución para inspeccionar los archivos. Desde PowerShell, recorre el directorio:

~~~powershell
Get-ChildItem -Path $salida -File |
    Sort-Object Name |
    Select-Object Name, Length

Get-ChildItem -Path (Join-Path $salida "wwwroot") -Recurse -File |
    Select-Object Name, DirectoryName
~~~

Localiza `CursoWeb.Mvc.dll`, `.deps.json`, `.runtimeconfig.json`, `appsettings.json` y la carpeta `wwwroot`. Busca además `web.config` si la publicación lo ha generado. No reemplaces archivos porque no conozcas todavía su función. Para aprender a leerlos, responde en orden:

**¿Cuál ejecuta el host?** La DLL del proyecto es un ensamblado de aplicación; se inicia con el host `dotnet` cuando el destino dispone del runtime adecuado.

**¿Cuál ayuda a resolver dependencias?** El archivo `.deps.json` describe componentes que participan en la carga. No contiene instrucciones para modificar `HomeController`.

**¿Cuál identifica condiciones del runtime?** El archivo `.runtimeconfig.json`. No instala por sí mismo un runtime faltante.

**¿Dónde están los recursos estáticos?** Normalmente en `wwwroot`. Revisa si existe `css/site.css`; no basta con ver que la carpeta está creada.

**¿Dónde se definen valores para la ejecución?** En archivos de configuración y otras fuentes como las variables de entorno. La configuración de LocalDB no instala ni copia SQL Server.

**¿Para qué sirve `web.config` si existe?** Para colaborar con el hospedaje IIS mediante el mecanismo ASP.NET Core correspondiente. No convierte la publicación por sí sola en un sitio IIS.

El resultado de este apartado no es un archivo nuevo. Es la capacidad de señalar la pieza correcta cuando una publicación falla por una causa determinada. Guarda la salida sin editar: la utilizaremos más adelante para ejecutar el host.

### Paso P5.2.7. Una comparación reproducible entre dos versiones publicadas

**Relación con la teoría:** 5.2.7 y 5.2.9. Si editamos una vista del proyecto, la publicación anterior no tiene por qué incorporar el cambio. Para comprobarlo construiremos dos salidas separadas de **la misma aplicación MVC**, cambiando una sola vista Razor entre una publicación y la siguiente.

Este paso es una ampliación de consolidación que puede realizarse después de la jornada. No crea otra aplicación ni modifica el resto del curso. La variante de referencia está guardada como archivo Razor **completo** en:

`M05_CONSOLIDACION_DESPLIEGUE/PROYECTO/VARIANTES/P5.2_CAMBIO_VISTA/Views/Home/Index.cshtml`

El archivo contiene el contenido original de `Views/Home/Index.cshtml` y añade un único párrafo identificable. Para reconstruir manualmente el cambio, abre el archivo del proyecto MVC y, debajo del elemento con identificador `resultado-inicial`, introduce:

~~~razor
@* AMPLIACIÓN P5.2: marca visible solo en la segunda publicación. *@
<p id="marca-publicacion-m05">
    Esta versión se publicó después de modificar la vista MVC.
</p>
~~~

**Estado A — publicación original.** Detén cualquier proceso MVC que esté utilizando la carpeta de salida. Desde la raíz del repositorio prepara rutas de trabajo que no se versionan:

~~~powershell
$proyecto = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc\CursoWeb.Mvc.csproj"
$vista = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc\Views\Home\Index.cshtml"
$variante = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\VARIANTES\P5.2_CAMBIO_VISTA\Views\Home\Index.cshtml"
$respaldo = "$vista.p52-original"
$publicacionA = ".\.work\M05\publicacion-original"
$publicacionB = ".\.work\M05\publicacion-cambio"

Copy-Item $vista $respaldo -Force
dotnet publish $proyecto -c Release -o $publicacionA
~~~

**Qué se espera:** `publicacion-original` contiene el estado de la vista antes de añadir la marca P5.2, porque se ha publicado desde el archivo de partida. No hace falta copiar ningún `.cshtml` manualmente a la carpeta de salida: el SDK prepara los artefactos de la aplicación.

**Estado B — modificación de vista y publicación posterior.** Después de conservar el estado A, cambia el origen:

~~~powershell
Copy-Item $variante $vista -Force
dotnet publish $proyecto -c Release -o $publicacionB
~~~

Si prefieres escribir la modificación manualmente en vez de copiar la variante, el resultado del archivo debe ser el mismo, sin duplicar el elemento `marca-publicacion-m05`. Para comprobarlo, abre la vista y verifica que ese identificador aparece **una sola vez**.

Hasta aquí hemos producido dos directorios publicados, pero todavía no se ha probado ninguno por HTTP. Eso es intencional: separa lo que hace `dotnet publish` de la ejecución.

### Paso P5.2.8. Ejecutar ambas publicaciones y localizar el cambio por HTTP

Para esta comparación prescindiremos de la inicialización LocalDB porque solo necesitamos la portada MVC. En una primera terminal PowerShell, desde la raíz del repositorio:

~~~powershell
$env:Despliegue__SinLocalDb = "true"
Push-Location .\.work\M05\publicacion-original
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5091
~~~

Mantén ese proceso iniciado. Abre una segunda terminal independiente en la raíz del repositorio:

~~~powershell
$env:Despliegue__SinLocalDb = "true"
Push-Location .\.work\M05\publicacion-cambio
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5094
~~~

Ambas instancias utilizan puertos diferentes. La primera debe continuar sirviendo la portada de la publicación original; la segunda debe representar la vista nueva. En una tercera terminal o con dos pestañas del navegador compara:

~~~powershell
curl.exe -i http://localhost:5091/
curl.exe -i http://localhost:5094/
~~~

En la segunda respuesta debe aparecer el texto «Esta versión se publicó después de modificar la vista MVC» dentro del elemento `marca-publicacion-m05`. En la primera no debe aparecer. No basta con obtener 200 en ambas: la evidencia buscada es que **las dos publicaciones contienen versiones distintas de una misma vista del mismo proyecto**.

Repite la consulta a `http://localhost:5091/` después de haber publicado B. Debe seguir mostrando la vista original porque ese proceso utiliza los artefactos A. Así comprobamos que publicar a una carpeta diferente no modifica retroactivamente una publicación anterior.

**Si ambas páginas muestran la marca:** comprueba que la publicación A se produjo antes de sustituir la vista y que el proceso 5091 no está ejecutando archivos de la carpeta B. **Si ninguna la muestra:** comprueba que realmente publicaste después de modificar la fuente y que 5094 está sirviendo la salida B. El diagnóstico debe relacionar origen, destino y proceso; no volver a crear un proyecto MVC.

### Paso P5.2.9. Restaurar el estado del curso sin destruir las publicaciones de ensayo

Detén los dos procesos con Ctrl+C en sus respectivas terminales y ejecuta `Pop-Location` en ambas. Después, desde la raíz del repositorio, restaura el archivo de origen:

~~~powershell
$vista = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc\Views\Home\Index.cshtml"
$respaldo = "$vista.p52-original"

Copy-Item $respaldo $vista -Force
Remove-Item $respaldo
Remove-Item Env:\Despliegue__SinLocalDb -ErrorAction SilentlyContinue

dotnet build .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc\CursoWeb.Mvc.csproj -c Release
~~~

Las carpetas de publicación A y B permanecen dentro de `.work` para facilitar una comparación posterior y no pertenecen al material que versiona el alumno. Si quieres repetir el ensayo, vuelve a publicar desde un estado inicial conocido. No modifiques `Views/Home/Index.cshtml` de M02 ni borres su trabajo previo.

**Conclusión razonada de este ejercicio:** no se trata de aprender dos comandos, sino de comprobar que el código fuente, la salida A, la salida B y los dos procesos HTTP son objetos distintos. La publicación nueva solo se manifiesta cuando la ejecución utiliza los artefactos nuevos.



### Resultado y estado final P5.2

La carpeta `.work\M05\publicacion-mvc` contiene los artefactos de MVC. El alumno sabe identificar qué cambió al publicar: no el código fuente ni las acciones, sino los archivos preparados para ejecutarse fuera de la estructura de desarrollo. No edites la fuente para corregir un problema que solo aparece por una variable del entorno de ejecución.

### Ampliación autónoma P5.2: inspección responsable de archivos

Comprueba la presencia y finalidad de seis elementos: DLL, deps, runtimeconfig, appsettings, wwwroot y web.config cuando exista. Explica por qué no debemos copiar manualmente una carpeta `obj` al servidor. Compara el tamaño de la publicación con la carpeta de fuentes, pero no infieras que el tamaño demuestra calidad. Después restaura un único directorio de salida; no produzcas múltiples carpetas «definitivas» difíciles de distinguir.

## P5.3. Ejecutar la aplicación MVC publicada en Kestrel

### Objetivo y estado inicial

La carpeta publicada existe desde P5.2. Ahora vamos a iniciar su aplicación **desde la DLL publicada**, verificar el puerto, obtener respuesta HTML, comprobar recursos y detener el proceso. El objetivo no es investigar nuevos controladores ni aprender una tecnología de persistencia, sino relacionar el proceso Kestrel con las peticiones que recibe.

### Paso P5.3.1. Preparar el directorio y liberar el puerto

Comprueba si el puerto ya está ocupado:

~~~powershell
Get-NetTCPConnection -LocalPort 5091 -ErrorAction SilentlyContinue
~~~

Si ves un listener de un proceso anterior que controlas, detén ese proceso antes de iniciar otro. Si el puerto no está libre o pertenece a una aplicación que no debes cerrar, elige un puerto alternativo como 5094 y mantén ese número coherente al ejecutar y consultar el navegador. No resuelvas un conflicto de puerto editando vistas Razor.

Accede a la publicación:

~~~powershell
$salida = ".\.work\M05\publicacion-mvc"
Push-Location $salida
~~~

### Paso P5.3.2. Iniciar la publicación en el puerto definido

En una terminal interactiva:

~~~powershell
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5091
~~~

Debes observar mensajes de arranque y una dirección de escucha, siempre que el runtime y la configuración sean válidos. No cierres la terminal mientras navegas: es la que mantiene el proceso. Desde otra terminal o el navegador solicita:

~~~powershell
curl.exe -i http://localhost:5091/
curl.exe -i http://localhost:5091/Productos/Estado
curl.exe -i http://localhost:5091/css/site.css
~~~

Los resultados deben indicar una respuesta HTTP útil de la misma aplicación MVC. La ruta de estado responde desde un controlador sin consultar la tabla de productos. La hoja CSS permite observar que `UseStaticFiles` sigue sirviendo recursos publicados.

### Paso P5.3.3. Diferenciar URL inicial y funcionamiento del CRUD

Si LocalDB se encuentra disponible, comprueba además `http://localhost:5091/Productos` y, si el instructor ha preparado los datos, la consulta de un producto. Si no se puede acceder a LocalDB, registra esa limitación como prueba de persistencia **no realizada**. La prueba 200 de Home y Estado no equivale a haber probado la creación y edición de productos.

El experimento de despliegue de este módulo permite una variante explícita sin base:

~~~powershell
# Ejecutar SOLO si el objetivo es verificar el hospedaje sin SQL Server:
$env:Despliegue__SinLocalDb = "true"
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5091
~~~

En ese modo, `/`, `/Productos/Estado` y los recursos estáticos son la demostración de hospedaje. Las rutas CRUD dependientes de SQL Server devuelven **503 Service Unavailable** por una regla deliberada del laboratorio. No presentaremos una respuesta 503 como una consulta de productos correcta.

La opción está en el proyecto M05 y mantiene intacto el proveedor `Microsoft.EntityFrameworkCore.SqlServer`. Cuando terminemos esta variante, debemos restaurar la variable:

~~~powershell
Remove-Item Env:\Despliegue__SinLocalDb -ErrorAction SilentlyContinue
~~~

No confundas un dato configurado en tu terminal con un cambio permanente de los archivos del proyecto.

### Paso P5.3.4. Comprobar una colisión de puertos de forma controlada

Con la publicación escuchando correctamente en 5091, abre **una tercera terminal** y trata de iniciar otra instancia utilizando el mismo puerto. Si LocalDB prepara correctamente el arranque de ambas instancias, la segunda debería informar de una dirección ya utilizada. Si una de las instancias falla antes por LocalDB, registra esa causa en lugar de adjudicarle falsamente una colisión.

Para realizar este experimento de forma aislada, usa la opción `Despliegue__SinLocalDb=true` en ambas terminales y comprueba el mensaje de puerto ocupado. Detén la segunda instancia y conserva la primera hasta finalizar las comprobaciones. El estado final del laboratorio no requiere mantener dos servidores.

### Paso P5.3.5. Detener, comprobar y volver a la raíz

Detén el proceso principal con `Ctrl+C`. Comprueba que la dirección deja de responder cuando realmente no exista otro proceso que la esté atendiendo. Después ejecuta:

~~~powershell
Pop-Location
~~~

El directorio de publicación sigue existiendo. No borres la salida: será reutilizada en P5.4 como fuente de artefactos de despliegue. El estado final de P5.3 consiste en una aplicación MVC publicada capaz de servir HTML/CSS/estado bajo Kestrel y un puerto liberado.


### Paso P5.3.6. Construir una prueba HTTP mínima que distinga conexión y resultado

**Relación con la teoría:** 5.3.8 y 5.3.12. En este ejercicio no cambiaremos el código MVC. Utilizaremos la DLL publicada y una configuración explícita para ver que un mismo servidor puede responder 200 en una ruta y 503 en otra.

Si terminaste P5.3.5, vuelve a la raíz del repositorio y abre una terminal PowerShell. Elimina una variable anterior para que la demostración no herede un valor desconocido; después elige expresamente el modo sin base:

~~~powershell
Remove-Item Env:\Despliegue__SinLocalDb -ErrorAction SilentlyContinue
$env:Despliegue__SinLocalDb = "true"
$salida = ".\.work\M05\publicacion-mvc"

Push-Location $salida
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5091
~~~

Con la ventana abierta, desde otra terminal solicita en este orden:

~~~powershell
curl.exe -i http://localhost:5091/
curl.exe -i http://localhost:5091/Productos/Estado
curl.exe -i http://localhost:5091/Productos
curl.exe -i http://localhost:5091/css/site.css
~~~

Anota la combinación de código HTTP y recurso solicitado. El resultado previsto es 200 en la portada, 200 en Estado, 503 en Productos y 200 en el CSS. El 503 no quiere decir que Kestrel esté detenido: **el servidor ha devuelto expresamente una respuesta** en la ruta dependiente de base. El resultado documenta una capacidad limitada del proyecto para este escenario.

Para comprobar el texto del endpoint de estado independientemente de la representación visual, utiliza:

~~~powershell
curl.exe -s http://localhost:5091/Productos/Estado
~~~

Debes observar `Catalogo MVC disponible`. Una respuesta de texto desde una acción concreta acredita el recorrido hasta el controlador. No acredita que las consultas EF Core se hayan ejecutado.

### Paso P5.3.7. Observar que un puerto pertenece a un proceso

**Relación con la teoría:** 5.3.7, 5.3.10 y 5.3.11. Mientras la aplicación permanece activa en 5091, abre otra terminal PowerShell:

~~~powershell
Get-NetTCPConnection -LocalPort 5091 -State Listen -ErrorAction SilentlyContinue |
    Select-Object LocalAddress, LocalPort, State, OwningProcess
~~~

Si el comando ofrece el identificador del proceso, puedes consultarlo sin detenerlo:

~~~powershell
$conexiones = Get-NetTCPConnection -LocalPort 5091 -State Listen -ErrorAction SilentlyContinue
$conexiones | ForEach-Object {
    Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue |
        Select-Object Id, ProcessName
}
~~~

Es normal que el proceso se llame `dotnet` en una publicación dependiente del framework. No debes interpretar ese nombre como si el navegador ejecutara C#; el navegador sigue enviando HTTP y el proceso se encarga de servir las solicitudes.

Ahora ejecuta en una tercera terminal la misma publicación con el mismo puerto y con el mismo modo sin base:

~~~powershell
$env:Despliegue__SinLocalDb = "true"
Push-Location .\.work\M05\publicacion-mvc
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5091
~~~

El segundo arranque debe fallar al intentar escuchar la dirección ocupada, siempre que la primera instancia siga viva y no haya otra particularidad de configuración. Comprueba que el primer proceso continúa respondiendo a `/Productos/Estado`; el fallo del segundo no ha detenido automáticamente al primero.

**Restauración:** cierra la terminal del segundo proceso con Ctrl+C si continúa abierta y ejecuta `Pop-Location`. No mates por identificador un proceso que no te pertenece. La prueba consiste en comprender la colisión, no en practicar eliminación indiscriminada de procesos.

### Paso P5.3.8. Cambiar únicamente el puerto y comprobar la independencia del código

**Relación con la teoría:** 5.3.9 y 5.3.10. Mantén el primer servidor activo en 5091. Desde la segunda terminal, inicia otra instancia de la misma DLL, esta vez en 5094:

~~~powershell
$env:Despliegue__SinLocalDb = "true"
Push-Location .\.work\M05\publicacion-mvc
dotnet .\CursoWeb.Mvc.dll --urls http://localhost:5094
~~~

La segunda instancia debe poder arrancar si 5094 está libre. No hemos modificado `HomeController`, `ProductosController`, ninguna vista ni el archivo `.csproj`. Solo hemos indicado una dirección de escucha diferente.

Desde otra terminal compara:

~~~powershell
curl.exe -i http://localhost:5091/Productos/Estado
curl.exe -i http://localhost:5094/Productos/Estado
~~~

Ambas respuestas deben proceder de la misma versión de MVC A, aunque atendidas por procesos distintos. Detén primero la instancia 5094 y después la 5091, comprobando que al cerrar una no desaparece necesariamente la otra. Vuelve a la raíz con `Pop-Location` en cada terminal.

**Pregunta razonada:** ¿por qué no habría solucionado la colisión cambiar la URL de una vista Razor? Porque la colisión se produce al abrir el socket de escucha durante el arranque, antes de procesar el HTML de esa vista.

### Paso P5.3.9. Comprobar un fallo de arranque sin diagnosticarlo como fallo HTTP

Un caso diferente aparece si la DLL publicada no puede iniciar por una dependencia previa. En la configuración normal de MVC A, el host prepara LocalDB durante el arranque. Si la instancia falta o no se puede abrir, puede fallar antes de empezar a escuchar.

Para no provocar daños en la base ni en la configuración existente, no elimines instancias ni archivos SQL. En su lugar, razona sobre la salida de error y comprueba primero el estado de la variable `Despliegue__SinLocalDb`. Si estaba activada, el comportamiento 503 de Productos es intencionado. Si estaba desactivada, el host intentará preparar la conexión LocalDB real. En cualquier caso, antes de atribuir un error a Kestrel comprueba si llegó a aparecer una dirección de escucha y si alguna ruta devolvió HTTP.

Este paso no exige forzar una avería en la máquina del docente. Consiste en reconocer la evidencia que distinguiría una excepción de arranque, un puerto ocupado y una acción que responde 503. Un alumno capaz de explicar esas tres posibilidades puede trasladar el diagnóstico al siguiente hospedaje sin confundir subsistemas.

### Paso P5.3.10. Cierre reproducible de la variante

Después de detener todas las instancias Kestrel abiertas para el ensayo, en cada terminal que hubiera configurado la opción temporal ejecuta:

~~~powershell
Remove-Item Env:\Despliegue__SinLocalDb -ErrorAction SilentlyContinue
~~~

Comprueba que la carpeta `.work\M05\publicacion-mvc` continúa disponible. No elimines el proyecto original ni su `ConnectionStrings:Productos`. El siguiente punto seguirá utilizando la **misma publicación MVC**, pero con un sitio IIS que determinará su propio mecanismo de entrada.

El resultado que debes ser capaz de explicar es una secuencia completa: arranque de un proceso desde una DLL publicada, lectura de su puerto, solicitud de varias rutas, diagnóstico de un segundo arranque conflictivo, ejecución en un puerto alternativo y parada controlada. Todos esos pasos pertenecen a un único proyecto y pueden reproducirse sin alterar el proveedor de datos.



### Diagnóstico P5.3: qué comprobar y por qué

| Problema | Comprobación directa | Corrección proporcionada |
|---|---|---|
| DLL no encontrada | `Get-Location`, `Get-ChildItem` | Entrar en la publicación real |
| Runtime ausente | `dotnet --list-runtimes` | Instalar ASP.NET Core Runtime 8 compatible |
| Puerto ocupado | Listener en el puerto | Detener proceso propio o elegir otro |
| Fallo SQL al arrancar | Mensaje de LocalDB | Revisar instancia o habilitar modo sin base para hospedaje |
| CSS responde 404 | Archivos en `wwwroot` y ruta | Revisar publicación y middleware estático |
| `/Productos` devuelve 503 en modo sin base | Valor de `Despliegue__SinLocalDb` | Interpretar la limitación; desactivarla solo con LocalDB preparado |

### Resultado del punto

Ya hemos visto la misma aplicación MVC ejecutándose a partir del proyecto y a partir de su publicación. Entendemos que Kestrel recibe peticiones en una dirección determinada y sabemos separar un problema de puerto, una dependencia de ejecución y una ruta que usa SQL Server. El siguiente punto cambiará el mecanismo de hospedaje, no el código de nuestros controladores.



## P5.4. Publicar la aplicación MVC en IIS

### Objetivo y prerrequisitos

Seguimos trabajando con la **misma aplicación MVC A** que acabamos de publicar y ejecutar con Kestrel. Ahora la alojaremos mediante Internet Information Services en Windows. Esta actividad no consiste en convertir MVC en páginas HTML estáticas ni en instalar SQL Server dentro de IIS.

Antes de comenzar necesitamos:

- Windows con la característica IIS habilitada y permisos para administrar un sitio local de laboratorio.
- ASP.NET Core Hosting Bundle 8 instalado, con el módulo ASP.NET Core registrado en IIS.
- La carpeta de publicación creada en P5.2 o la posibilidad de volver a ejecutar `dotnet publish`.
- Una carpeta de destino que no sea el proyecto fuente y un puerto local libre, por ejemplo 8091.
- Una cuenta del laboratorio autorizada para crear un sitio y configurar el Application Pool.

**Importante:** una instalación de Windows que no incluya IIS o en la que no se disponga del Hosting Bundle no permite declarar esta práctica verificada. En ese caso conserva las instrucciones y continúa solo con aquello que pueda comprobarse sin falsear resultados.

### Paso P5.4.1. Identificar las piezas antes de configurarlas

En el Administrador de IIS distinguiremos estos elementos:

| Elemento | Decisión de laboratorio |
|---|---|
| Sitio web | `CursoWeb-M05` |
| Ruta física | `C:\CursoWeb\M05\IIS` |
| Binding | `http`, puerto `8091`, host local |
| Application Pool | `CursoWeb-M05-Pool` |
| Versión CLR del pool | `No Managed Code` |
| Aplicación | Salida publicada de `CursoWeb.Mvc` |
| Configuración de base | Modo de hospedaje sin LocalDB para esta demostración |

La expresión `No Managed Code` no significa que ASP.NET Core deje de ejecutar código administrado. Solo indica que el pool IIS no debe seleccionar un CLR clásico de .NET Framework para hospedar una aplicación moderna .NET 8. El Hosting Bundle y ANCM proporcionan el mecanismo correspondiente.

El sitio y el pool son **recursos de laboratorio**. No debes cambiar el Default Web Site de otras aplicaciones ni utilizar carpetas de producción como destino del experimento.

### Paso P5.4.2. Preparar el directorio de publicación para IIS

Desde PowerShell, en la raíz del repositorio, prepara dos rutas:

~~~powershell
$proyecto = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc\CursoWeb.Mvc.csproj"
$destinoIis = "C:\CursoWeb\M05\IIS"
New-Item -ItemType Directory -Path $destinoIis -Force | Out-Null
dotnet publish $proyecto -c Release -o $destinoIis
~~~

No copies la carpeta del proyecto sin publicar. Comprueba que `CursoWeb.Mvc.dll`, `CursoWeb.Mvc.runtimeconfig.json`, `wwwroot` y `web.config` se encuentran en la ruta de destino. Si falta el `web.config`, revisa que publicaste el proyecto web correcto y que el SDK generó soporte para IIS.

Abre el `web.config` publicado para identificar el elemento `aspNetCore`, que informa al módulo de cómo iniciar la aplicación. **No reemplaces el archivo por una plantilla genérica sin entender sus valores.** La publicación suele generar esos valores a partir del proyecto.

### Paso P5.4.3. Aislar explícitamente la dependencia de LocalDB

Durante M02 ejecutamos el CRUD MVC desde Visual Studio con una instancia LocalDB asociada al usuario del alumno. IIS ejecutará la aplicación con la identidad del Application Pool, que normalmente no tiene acceso directo a esa instancia. Para la **demostración básica de hospedaje**, crearemos una configuración de entorno específica, sin tocar el proyecto fuente ni sustituir `UseSqlServer()`.

En el directorio físico **ya publicado** crea un archivo nuevo `appsettings.Production.json` con este contenido:

~~~json
{
  "Despliegue": {
    "SinLocalDb": true
  }
}
~~~

Esta clave evita inicializar la base al arrancar y permite mostrar el inicio, el estado y los recursos estáticos. Al mismo tiempo, provoca que las rutas que dependen del CRUD respondan 503 para no ocultar una dependencia que no está disponible.

El archivo presupone que el entorno del proceso IIS es `Production`, que es el valor predeterminado si no se configura otro. Si el servidor IIS del laboratorio fija explícitamente un entorno diferente, debe usarse un archivo `appsettings.<Entorno>.json` correspondiente o configurar de forma explícita la clave en ese sitio; **no afirmes que la configuración se ha aplicado sin comprobar el comportamiento**.

No modifiques `ConnectionStrings:Productos` para apuntar a una base de datos inventada. El CRUD completo continúa disponible en Windows desde Visual Studio/Kestrel con LocalDB real, fuera de este modo simplificado.

### Paso P5.4.4. Crear y configurar el pool y el sitio

Abre **Administrador de Internet Information Services (IIS)** como administrador. En «Grupos de aplicaciones» crea `CursoWeb-M05-Pool` y selecciona «Sin código administrado / No Managed Code». Mantén la identidad predeterminada de ApplicationPoolIdentity salvo que el docente haya preparado una identidad específica, y no concedas permisos a Everyone como solución a un error.

En «Sitios», utiliza «Agregar sitio web» y define:

1. Nombre: `CursoWeb-M05`.
2. Ruta física: `C:\CursoWeb\M05\IIS`.
3. Tipo: `http`.
4. Dirección IP: la opción local prevista en el laboratorio.
5. Puerto: `8091`.
6. Nombre de host: vacío para un ensayo local cuando no haya conflicto.
7. Application Pool: `CursoWeb-M05-Pool`.

Comprueba que el puerto 8091 no lo utiliza ya otro sitio. Un fallo de binding es una incidencia de IIS que debe solucionarse antes de interpretar la respuesta de MVC.

### Paso P5.4.5. Verificar permisos y aplicación publicada

El proceso IIS necesita permiso de lectura sobre los archivos publicados. Desde las propiedades de seguridad de la carpeta, identifica la cuenta que realmente ejecuta el pool y verifica los permisos mínimos necesarios. La asignación concreta depende del laboratorio Windows preparado y de su política de cuentas.

No otorgues `Full Control` a todos los usuarios para sortear un error de acceso. Si el sitio no inicia, consulta el diagnóstico de IIS y del módulo ASP.NET Core antes de cambiar permisos. Si instalaste el Hosting Bundle recientemente, puede ser necesario reiniciar los servicios IIS para cargar el módulo según su documentación.

### Paso P5.4.6. Abrir las rutas que sí prueban hospedaje

En el navegador del mismo host abre:

- `http://localhost:8091/`
- `http://localhost:8091/Productos/Estado`
- `http://localhost:8091/css/site.css`

La página inicial debe proceder de la aplicación MVC A y la ruta de estado debe responder `Catalogo MVC disponible`. Comprueba también que la hoja CSS se sirve desde `wwwroot`. La prueba de estas rutas muestra que IIS, ANCM, la aplicación publicada y el routing cooperan correctamente.

Prueba a continuación `http://localhost:8091/Productos`. Bajo el modo `SinLocalDb=true`, la respuesta prevista es **503 Service Unavailable** con una explicación de que el CRUD del ensayo requiere LocalDB. Esta respuesta es deliberada: no la anotes como prueba de consulta de productos satisfactoria.

Si la ruta de Productos ejecuta SQL y falla de otra manera, comprueba que el archivo `appsettings.Production.json` está en la carpeta física correcta y que el entorno efectivo es Production. No presupongas que IIS lee la configuración que modificaste: compruébalo por la respuesta del programa.

### Paso P5.4.7. Diagnosticar un fallo sin borrar y rehacer todo

| Observación | Diagnóstico inicial | Corrección orientada |
|---|---|---|
| Sitio no arranca | Hosting Bundle, ANCM, web.config, logs | Confirmar instalación y ruta publicada |
| Puerto 8091 ocupado | Binding IIS o proceso externo | Elegir binding libre o detener solo proceso propio |
| Error de lectura de archivos | Identidad del pool | Permisos mínimos sobre carpeta |
| Home responde, CSS no | wwwroot y publicación | Revisar archivos publicados |
| Home responde, Productos devuelve 503 | Modo sin LocalDB activo | Resultado previsto del ensayo |
| Productos intenta abrir LocalDB | Configuración de entorno no aplicada | Revisar Production y archivo en destino |
| Aparece una web antigua | Ruta física o sitio equivocados | Comprobar carpeta, sitio y binding |

En una instalación que no proporcione IIS real, esta tabla ayuda a estudiar causas, pero **no sustituye la ejecución del sitio**. Tampoco un `dotnet run` satisfactorio justifica escribir «IIS validado»: son mecanismos de hospedaje distintos.

### Paso P5.4.8. Conservar o desmontar el laboratorio

Al terminar registra el nombre del sitio, el binding utilizado, la carpeta publicada y las rutas realmente comprobadas. Si el equipo es compartido, el docente indicará si se debe detener el sitio y eliminar la configuración de laboratorio. No borres otros sitios ni el CRUD original de M02.

**Estado final:** mismo MVC A, publicado a una carpeta gestionada por IIS, con respuesta comprobada en rutas sin base y con una explicación explícita de por qué el ensayo no acredita acceso a LocalDB bajo la identidad del pool.


### Paso P5.4.9. Relacionar la carpeta publicada con el sitio que realmente la utiliza

**Relación con la teoría:** 5.4.8 y 5.4.9. Este recorrido de observación complementa la creación del sitio que hicimos con la interfaz gráfica. No es necesario instalar otra característica ni crear un segundo sitio: debemos identificar los recursos del mismo laboratorio.

En una ventana PowerShell con permisos adecuados sobre IIS, importa el módulo administrativo:

~~~powershell
Import-Module WebAdministration
Get-Website -Name "CursoWeb-M05" |
    Select-Object Name, State, PhysicalPath, ApplicationPool

Get-WebBinding -Name "CursoWeb-M05" |
    Select-Object Protocol, BindingInformation
~~~

Compara la ruta física mostrada con `C:\CursoWeb\M05\IIS`, que elegiste al publicar. Después confirma que esa carpeta contiene los artefactos de aplicación:

~~~powershell
$destinoIis = "C:\CursoWeb\M05\IIS"

Test-Path (Join-Path $destinoIis "CursoWeb.Mvc.dll")
Test-Path (Join-Path $destinoIis "CursoWeb.Mvc.runtimeconfig.json")
Test-Path (Join-Path $destinoIis "web.config")
Test-Path (Join-Path $destinoIis "wwwroot\css\site.css")
~~~

Los cuatro resultados deberían ser `True` en una publicación correcta del proyecto. Si IIS apunta a otra ruta, no tendrá por qué servir el contenido que acabas de publicar, aunque `dotnet publish` haya terminado sin errores.

**Interpretación:** la publicación prepara archivos y el sitio IIS decide qué carpeta física utiliza. Se trata de dos operaciones diferentes. Una página que sigue mostrando contenido antiguo puede deberse a que IIS esté leyendo otra carpeta, no necesariamente a un fallo de compilación.

### Paso P5.4.10. Verificar el Application Pool sin confundir el CLR clásico con .NET 8

**Relación con la teoría:** 5.4.9, 5.4.10 y 5.4.11. La aplicación debe ejecutarse mediante ASP.NET Core Module. El Application Pool conserva una configuración particular que hemos elegido para ese mecanismo de hospedaje.

Desde PowerShell, con el módulo de IIS importado, consulta:

~~~powershell
Get-ItemProperty "IIS:\AppPools\CursoWeb-M05-Pool" |
    Select-Object Name, ManagedRuntimeVersion, ProcessModel

Get-WebAppPoolState -Name "CursoWeb-M05-Pool"
~~~

El valor de `ManagedRuntimeVersion` configurado para «No Managed Code» suele representarse como cadena vacía. Eso no significa que nuestro proyecto haya pasado a ser una página estática sin .NET. Significa que el CLR tradicional de .NET Framework no se usa para hospedar ASP.NET Core como si fuera una aplicación antigua.

Si el pool está detenido, consulta la causa antes de iniciarlo. Si está iniciado pero la página devuelve un error, no atribuyas automáticamente el fallo al código MVC. Revisa el Hosting Bundle, el ASP.NET Core Module, los permisos y los artefactos publicados.

**Pregunta guiada:** ¿por qué no demuestra una propiedad `State = Started` que Home/Index devuelve HTML? Porque el estado administrativo del pool y la respuesta de una acción MVC son observaciones distintas. Solo una petición HTTP a la URL correcta permite comprobar la segunda.

### Paso P5.4.11. Separar respuesta de hospedaje de respuesta de una función dependiente de SQL

**Relación con la teoría:** 5.4.13–5.4.15. Con el sitio operativo, realiza tres solicitudes que no necesitan acceso a LocalDB:

~~~powershell
curl.exe -i http://localhost:8091/
curl.exe -i http://localhost:8091/Productos/Estado
curl.exe -i http://localhost:8091/css/site.css
~~~

Para una instalación preparada, deben responder 200. Ahora solicita una función que en MVC A utiliza el `AppDbContext` de SQL Server:

~~~powershell
curl.exe -i http://localhost:8091/Productos
~~~

Con el archivo `appsettings.Production.json` de P5.4.3 y el entorno correspondiente, la respuesta prevista es 503. No se ha fingido un catálogo en memoria ni se ha cambiado `UseSqlServer`. En este ensayo nos interesa demostrar que IIS hospeda la aplicación, no que dispone de una instancia SQL Server Express LocalDB asociada a su identidad de proceso.

Si aparece un 500 durante el arranque, no es equivalente a este 503 deliberado. Revisa qué configuración se cargó realmente y los mensajes de ANCM. Si todas las rutas fallan, el problema se sitúa probablemente antes de la acción concreta del catálogo. Si solo una ruta de datos falla y la portada funciona, el análisis deberá considerar la dependencia de base.

**Por qué importa la identidad:** un Application Pool utiliza una cuenta distinta de la sesión interactiva del alumno. LocalDB en Windows está asociado a un contexto de usuario. La misma cadena de conexión que funcionaba desde Visual Studio no demuestra que IIS tenga acceso autorizado a esa instancia.

### Paso P5.4.12. Comparar dos publicaciones sin cambiar un solo controlador

**Relación con la teoría:** 5.4.9 y 5.4.14. En P5.2 aprendimos que modificar una vista de origen no sustituye automáticamente la carpeta publicada. IIS añade otra relación: el sitio sirve la carpeta física que se le configuró.

Imagina dos carpetas con publicaciones del mismo proyecto: `C:\CursoWeb\M05\IIS` y una copia de ensayo bajo `.work`. Aunque ambas contengan una DLL llamada `CursoWeb.Mvc.dll`, solo una de ellas corresponde a la ruta física del sitio `CursoWeb-M05`.

No necesitas cambiar el binding ni crear otro sitio. Consulta el valor `PhysicalPath` y comprueba que coincide con el destino al que ejecutaste `dotnet publish`. Si acabas de modificar una vista del origen y la portada IIS sigue siendo la antigua, identifica primero si repúblicaste y si el sitio utiliza la salida nueva.

El resultado esperado de este razonamiento es una explicación completa: fuente, publicación, ruta física IIS, módulo ASP.NET Core y petición HTTP. Se trata de cinco elementos distintos; cambiar uno no implica que los otros hayan cambiado.

### Paso P5.4.13. Dejar el host IIS preparado para el siguiente ejercicio

La práctica Docker no necesita que IIS permanezca activo en 8091. Si el laboratorio utiliza una máquina compartida, conserva el nombre del sitio y del pool, informa al docente y detén únicamente lo que hayas creado para la sesión siguiendo las reglas del aula. No borres el Default Web Site ni otras publicaciones.

Puedes consultar el estado final sin modificarlo:

~~~powershell
Get-Website -Name "CursoWeb-M05" |
    Select-Object Name, State, PhysicalPath

Get-WebAppPoolState -Name "CursoWeb-M05-Pool"
~~~

El conocimiento que debes conservar no es la posición de un botón de la consola administrativa, sino la relación entre el sitio, su binding, el pool, el módulo de hospedaje, los archivos publicados y el resultado de una petición concreta. Esa misma disciplina permitirá interpretar después las imágenes, los puertos y los procesos de Docker.



### Ampliación autónoma P5.4: explicar una diferencia de proceso

Compara la dirección 5091 utilizada en Kestrel con 8091 de IIS. Argumenta por qué ambos pueden servir la misma acción `HomeController.Index` sin modificar su código, pero dependen de procesos de arranque, identidad y permisos diferentes. Explica además por qué un fallo 503 de `/Productos` deliberadamente producido por el modo sin base no es una avería del módulo IIS.

## P5.5. Crear y ejecutar un contenedor Docker Linux

### Objetivo y estado inicial

En esta última práctica utilizaremos la **misma aplicación MVC A** empleada en P5.2, P5.3 y P5.4. No crearemos una nueva solución MVC ni necesitaremos que Blazor, la API de productos, Identity/JWT o SQL Server estén ejecutándose al mismo tiempo.

El estado inicial es el proyecto MVC acumulativo y el Dockerfile incluido en su carpeta. El estado final será una imagen Docker .NET 8 construida, un contenedor real que responde HTTP desde el host, la inspección de sus logs y la retirada controlada del contenedor.

### Paso P5.5.1. Confirmar el motor y el tipo de contenedor

En Windows abre Docker Desktop, comprueba que el motor esté iniciado y que utiliza **contenedores Linux**. Después abre PowerShell:

~~~powershell
docker version
docker info --format "{{.OSType}}"
~~~

La información de servidor debe ser accesible; para este ejercicio esperamos `linux`. Si la herramienta cliente existe pero no puede conectar con el daemon, no has demostrado que Docker funcione. Debes iniciar o preparar el motor antes de intentar construir imágenes.

No instalaremos SQL Server en el contenedor ni utilizaremos Docker Compose o Kubernetes. Son contenidos de otro nivel.

### Paso P5.5.2. Abrir el Dockerfile de la aplicación real

Entra en la carpeta que contiene el proyecto MVC:

~~~powershell
Push-Location .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc
Get-Content .\Dockerfile
~~~

El Dockerfile de referencia contiene dos etapas y debe terminar con un comando que ejecute nuestra DLL:

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

No se presenta como un bloque misterioso para copiar. Lee las instrucciones en orden:

- `FROM .../sdk:8.0` proporciona herramientas de compilación, como `dotnet restore` y `dotnet publish`.
- `WORKDIR /src` establece el directorio donde se manipularán los archivos.
- `COPY . .` introduce el contexto de construcción: **debemos ejecutar build desde la carpeta adecuada**.
- `RUN dotnet restore` obtiene las dependencias disponibles.
- `RUN dotnet publish` crea la salida para ejecución.
- La segunda etapa parte de `aspnet:8.0`, que incluye el runtime ASP.NET Core pero no necesita el SDK completo.
- `COPY --from=compilacion` introduce solo los artefactos publicados.
- `ASPNETCORE_URLS` permite que Kestrel escuche en 8080 dentro del contenedor.
- `EXPOSE 8080` documenta el puerto interno; no crea por sí solo un acceso desde Windows.
- `ENTRYPOINT` inicia la DLL cuando se ejecuta el contenedor.

El archivo `.dockerignore` excluye carpetas de compilación local (`bin`, `obj`) y archivos de desarrollo. Su función es reducir el contexto enviado a Docker y evitar introducir resultados anteriores que pudieran confundir la construcción.

### Paso P5.5.3. Construir una imagen y distinguir build de run

Desde la misma carpeta, ejecuta:

~~~powershell
docker build -t cursoweb-mvc:m05 .
~~~

El punto final indica que **el contexto de construcción es el directorio actual**. Si lo omites o ejecutas el comando desde una carpeta incompatible, Docker no encontrará necesariamente `CursoWeb.Mvc.csproj`.

Cuando termine sin errores, comprueba la imagen:

~~~powershell
docker images cursoweb-mvc
~~~

Este resultado solo acredita construcción. Aún no hay navegador, proceso ASP.NET Core en ejecución ni respuesta HTTP. Si falla `dotnet restore` durante el build, investiga conectividad, fuentes NuGet y archivo de proyecto. No alteres el contenido de la API Blazor para resolver esa incidencia.

### Paso P5.5.4. Ejecutar el contenedor con el modo SQL explícito

Docker Linux no contiene la instancia SQL Server Express LocalDB de Visual Studio. No podemos trasladarla copiando la cadena de conexión. El proyecto MVC M05 ofrece un modo **sin LocalDB** destinado exclusivamente a ensayos de hospedaje; conserva el CRUD completo para el entorno Windows original.

Ejecuta:

~~~powershell
docker run --name cursoweb-m05 --rm -p 8081:8080 -e Despliegue__SinLocalDb=true cursoweb-mvc:m05
~~~

La opción `-e` define la configuración del proceso dentro del contenedor. `-p 8081:8080` publica el puerto del contenedor **8080** en el puerto del host **8081**. `--name` facilita identificar el proceso. `--rm` elimina el contenedor cuando termina; no elimina automáticamente la imagen.

Mantén esta terminal abierta. El proceso ASP.NET Core debe continuar escuchando. Si termina de inmediato, consulta la salida y los logs antes de modificar el Dockerfile.

### Paso P5.5.5. Comprobar desde una segunda terminal y un navegador

Abre otra terminal PowerShell, sin detener el contenedor:

~~~powershell
docker ps
curl.exe -i http://localhost:8081/
curl.exe -i http://localhost:8081/Productos/Estado
curl.exe -i http://localhost:8081/css/site.css
~~~

En un navegador abre `http://localhost:8081/` y comprueba que aparece la misma aplicación MVC. La ruta `/Productos/Estado` debe devolver el texto esperado. La hoja CSS debe servirse correctamente. Es importante anotar **la URL del host**, no el puerto 8080 que la aplicación utiliza dentro del contenedor.

Consulta también `http://localhost:8081/Productos`. El resultado previsto es **503**, con el mensaje explícito sobre LocalDB, porque el experimento no dispone de una base SQL Server. No declares probado el CRUD. Este punto demuestra publicación y ejecución del host MVC Linux, no persistencia ni migración de base de datos.

### Paso P5.5.6. Consultar logs y reconocer el proceso real

En la segunda terminal:

~~~powershell
docker logs cursoweb-m05
docker ps --filter "name=cursoweb-m05"
~~~

Los logs deben ayudar a localizar el inicio del servidor o posibles errores. Si `docker ps` no muestra el contenedor, comprueba si terminó y consulta su salida en la primera terminal. Un error de navegación no demuestra por sí solo que la imagen sea inválida; podríamos haber publicado un puerto distinto, dejado el proceso detenido o introducido una variable de configuración incorrecta.

Comprueba por separado tres afirmaciones: existe la imagen, está en ejecución un contenedor y su ruta HTTP devuelve una respuesta válida. Son evidencias complementarias.

### Paso P5.5.7. Recuperar un puerto ocupado sin reescribir la aplicación

Si otro proceso ocupa el puerto 8081 **del host**, no es necesario cambiar la escucha interna 8080. Detén el contenedor propio y ejecútalo con un puerto del host libre, por ejemplo:

~~~powershell
docker run --name cursoweb-m05 --rm -p 8082:8080 -e Despliegue__SinLocalDb=true cursoweb-mvc:m05
~~~

La dirección que abrirás ahora será `http://localhost:8082/`. Esta comprobación permite explicar por qué el primer número de `-p` pertenece al host y el segundo al contenedor. No mantengas ejecutándose dos contenedores con el mismo nombre: Docker rechazaría esa duplicación.

### Paso P5.5.8. Detener y retirar el contenedor de ensayo

Desde otra terminal, solicita:

~~~powershell
docker stop cursoweb-m05
~~~

Debido a `--rm`, el contenedor debe desaparecer de la lista de activos tras detenerse. Comprueba:

~~~powershell
docker ps --filter "name=cursoweb-m05"
docker images cursoweb-mvc
~~~

La imagen puede seguir existiendo. El docente decidirá si se conserva para repetir el ejercicio o se retira después de clase. No elimines imágenes de otros proyectos ni utilices comandos de limpieza masiva para completar este paso.

Regresa a la raíz del repositorio:

~~~powershell
Pop-Location
~~~

### Paso P5.5.9. Comparar las tres modalidades sin confundir garantías

Registra los resultados observados en esta matriz:

| Pregunta | Kestrel Windows | IIS Windows | Docker Linux |
|---|---|---|---|
| ¿Se ha publicado MVC A? | Publicación de P5.2 | Carpeta IIS | Imagen multietapa |
| ¿Quién inicia el host? | `dotnet` | IIS/ANCM | `ENTRYPOINT` |
| ¿Qué puerto se abre desde el host? | 5091 | 8091 | 8081 |
| ¿Qué ruta sin base has probado? | `/Productos/Estado` | `/Productos/Estado` | `/Productos/Estado` |
| ¿Has comprobado el CRUD en LocalDB? | Solo si hiciste la prueba con base real | No en el ensayo simple | No |
| ¿Se ha probado el mecanismo real? | Requiere ejecución Kestrel | Requiere IIS funcionando | Requiere `docker run` real |

No debes completar una casilla con «sí» si la herramienta correspondiente no estaba instalada. Si solo leíste el Dockerfile, no construiste la imagen; si solo ejecutaste Kestrel, no probaste IIS; si se sirvió la portada sin base, no confirmaste CRUD persistente.


### Paso P5.5.10. Reconstruir desde el principio el Dockerfile de la aplicación real

**Relación con la teoría:** apartados 5.5.8–5.5.10. El recorrido obligatorio ya ha probado la imagen preparada. Esta ampliación autónoma demuestra que el alumno es capaz de construir su contenido de forma progresiva, sin iniciar una tercera aplicación y sin perder el estado entregado.

Desde la raíz del repositorio, detén el contenedor de la práctica anterior y prepara una copia de referencia:

~~~powershell
Push-Location .\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc
Copy-Item .\Dockerfile .\Dockerfile.p55-referencia -Force
~~~

Abre el Dockerfile en Visual Studio, conserva el respaldo y sustituye temporalmente el contenido por el estado inicial de la **etapa de compilación**:

~~~dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS compilacion
WORKDIR /src
COPY . .
~~~

Explica antes de continuar dónde estará `CursoWeb.Mvc.csproj` después de `COPY`. Este archivo todavía no representa una imagen que sirva HTTP. Hemos elegido herramientas de construcción y una carpeta de trabajo, pero no hemos publicado la aplicación ni definido el proceso que la ejecutará.

Añade dos instrucciones y estudia su propósito por separado:

~~~dockerfile
RUN dotnet restore CursoWeb.Mvc.csproj
RUN dotnet publish CursoWeb.Mvc.csproj -c Release --no-restore -o /app/publicada
~~~

`restore` resuelve dependencias; `publish` prepara los archivos de ejecución. Ambas instrucciones se ejecutan durante `docker build`, no durante cada petición HTTP. Una restauración que falla no puede arreglarse modificando una vista Razor.

Ahora crea una **segunda etapa** para la ejecución:

~~~dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS ejecucion
WORKDIR /app
COPY --from=compilacion /app/publicada .
~~~

Esta etapa usa el runtime ASP.NET Core y copia la publicación producida por el SDK. La imagen final no necesita transportar el SDK de compilación. Sin embargo, todavía falta decirle al contenedor qué proceso debe ejecutar.

Completa el archivo con las instrucciones de escucha, documentación del puerto y arranque:

~~~dockerfile
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "CursoWeb.Mvc.dll"]
~~~

Comprueba el resultado final: debe existir una etapa SDK, otra etapa runtime, una copia de archivos publicados y un `ENTRYPOINT` que apunta a la DLL MVC. Si el nombre de la DLL fuera el de Blazor o el de la API de M04, habríamos roto la continuidad del curso.

### Paso P5.5.11. Construir y ejecutar la variante creada por el alumno

Desde la misma carpeta del proyecto MVC:

~~~powershell
docker build -t cursoweb-mvc:m05-reconstruida .
docker images cursoweb-mvc
~~~

El identificador `m05-reconstruida` diferencia esta imagen de la creada en la práctica principal. Si Docker informa de que no encuentra el proyecto, confirma que el contexto indicado con el punto corresponde a la carpeta que contiene el archivo `.csproj`.

Ejecuta ahora la publicación en un contenedor propio y un puerto de host diferente:

~~~powershell
docker run --name cursoweb-m05-reconstruida --rm `
  -p 8083:8080 `
  -e Despliegue__SinLocalDb=true `
  cursoweb-mvc:m05-reconstruida
~~~

En una segunda terminal PowerShell consulta los tres tipos de recurso y la ruta limitada:

~~~powershell
docker ps --filter "name=cursoweb-m05-reconstruida"
curl.exe -i http://localhost:8083/
curl.exe -i http://localhost:8083/Productos/Estado
curl.exe -i http://localhost:8083/css/site.css
curl.exe -i http://localhost:8083/Productos
~~~

La página inicial, Estado y CSS deben responder satisfactoriamente; Productos debe devolver 503 porque el modo del contenedor no dispone de LocalDB. El resultado permite comparar dos imágenes construidas a partir del mismo programa: la de referencia y la que acabas de reconstruir desde un Dockerfile progresivo.

**Por qué no consideramos suficiente el resultado de `docker images`:** una imagen disponible no garantiza que exista un proceso activo ni que el mapeo de puertos permita llegar a él. Hemos añadido una ejecución real y cuatro peticiones por ese motivo.

Detén el contenedor:

~~~powershell
docker stop cursoweb-m05-reconstruida
~~~

### Paso P5.5.12. Reconocer el contexto de construcción y sus exclusiones

**Relación con la teoría:** 5.5.9. Observa el `.dockerignore` situado junto al Dockerfile. Contiene exclusiones para los directorios locales `bin`, `obj` y archivos propios de Visual Studio. Su propósito es que el contexto de Docker transporte el material de origen necesario y no se confunda con salidas anteriores generadas en el equipo del alumno.

No es una alternativa a `dotnet restore` ni a `dotnet publish`. La etapa SDK sigue realizando estas operaciones dentro de la construcción. Una imagen que se construye correctamente después de eliminar los artefactos locales de desarrollo muestra que no depende de una DLL compilada previamente en Windows.

Este laboratorio no necesita incorporar certificados privados ni credenciales al contexto. Se trabaja con el mismo proyecto MVC y datos de demostración. La imagen no incluye SQL Server LocalDB y la configuración de ejecución declara su ausencia para las rutas que lo necesitan.

### Paso P5.5.13. Restaurar el Dockerfile canónico del curso

Una vez detenido el contenedor de la reconstrucción, vuelve a la terminal inicial, donde conservaste la copia del archivo:

~~~powershell
Copy-Item .\Dockerfile.p55-referencia .\Dockerfile -Force
Remove-Item .\Dockerfile.p55-referencia
Pop-Location
~~~

Si habías dejado un proceso Docker ejecutándose, ciérralo antes de dar por terminada la sesión. La restauración asegura que la próxima persona encuentre el Dockerfile original y no un archivo incompleto del proceso de aprendizaje.

**Explicación final del alumno:** describe la diferencia entre las herramientas SDK de la primera etapa, el runtime de la segunda, el contexto entregado a Docker, el programa que inicia `ENTRYPOINT` y la URL pública del host. Debe poder señalar la función de cada elemento sin cambiar el código MVC.

### Paso P5.5.14. Una avería distinta en cada etapa del recorrido

**Si falla `docker build` al buscar el proyecto**, revisa el contexto y la instrucción `COPY`: el Dockerfile no puede obtener automáticamente un archivo que no está en la estructura copiada.

**Si la imagen existe pero no aparece un contenedor en `docker ps`**, comprueba que ejecutaste `docker run` y que el proceso no terminó inmediatamente. La imagen no es un servidor activo por sí misma.

**Si hay contenedor activo y el navegador no conecta**, compara el puerto 8083 del host con el 8080 del contenedor y consulta los logs del proceso. No cambies HomeController para corregir una dirección equivocada.

**Si `/` responde 200 y `/Productos` devuelve 503**, la limitación coincide con `Despliegue__SinLocalDb=true`. No se ha sustituido SQL Server por SQLite ni se ha habilitado un CRUD ficticio.

El reto se considera comprendido cuando la respuesta a cada incidencia identifica qué capa está implicada y cuál es la corrección más pequeña. Reconocer las causas es más importante que memorizar el orden de los comandos sin entenderlo.



### Ampliación autónoma P5.5: una avería diferente en cada capa

Estudia estos tres casos y expresa la acción correctiva más pequeña:

1. `docker build` falla porque no encuentra `.csproj`: ¿desde dónde has ejecutado el build y cuál es su contexto?
2. La imagen existe pero `http://localhost:8081` no responde: ¿hay contenedor activo?, ¿qué `-p` se usó?, ¿qué puerto escucha ASP.NET Core?
3. El inicio responde pero `/Productos` devuelve 503: ¿la ruta necesita LocalDB?, ¿qué configuración declaramos?, ¿es ese resultado coherente con el objetivo de la práctica?

La respuesta del tercer caso es deliberadamente distinta de «instalar SQLite» o «quitar EF Core». El proyecto base sigue siendo el que construimos en M02; el ensayo Docker solo demuestra que puede servirse una parte independiente de la infraestructura SQL Windows.

## Cierre de M05: interpretar lo aprendido

No es necesario que las cinco tareas se conviertan en una aplicación empresarial ni que todos los servicios de M04 se ejecuten a la vez. Al finalizar, el estudiante debe distinguir:

- Una interfaz Blazor Interactive Server que consume una API mediante servicios tipados y estado de componente.
- Una API en memoria cuyo ciclo de vida no equivale a persistencia de base de datos.
- Una aplicación MVC con Razor y EF Core que se sigue utilizando sin reconstruirla.
- Compilación, ejecución y publicación como operaciones diferentes.
- Kestrel, IIS y Docker como opciones de hospedaje que mantienen el código MVC, pero cambian sus condiciones de arranque, puertos, permisos y dependencias.

Si un resultado no se observa, la práctica no se resuelve escribiendo «correcto» en una tabla. Se investiga el proceso, la ruta, la respuesta HTTP y las condiciones de la máquina y se declara con precisión qué parte ha podido comprobarse.


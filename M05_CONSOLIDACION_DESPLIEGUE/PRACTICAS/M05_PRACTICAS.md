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

La versión de trabajo de M04 obtenía productos durante `OnInitializedAsync`. Queremos permitir una segunda consulta sin reconstruir toda la página. En `Components/Pages/CatalogoRemoto.razor`, debajo del párrafo introductorio, añade:

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

Abre el archivo `Program.cs`. Localiza las dos responsabilidades que llegan del módulo anterior:

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


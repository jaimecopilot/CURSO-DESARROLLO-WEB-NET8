# M01 — Fundamentos de ASP.NET Core MVC
## Material teórico

### Índice del módulo

- **1.1. Introducción al desarrollo web con ASP.NET Core**
- **1.2. Arquitectura Model-View-Controller**
- 1.3. Estructura de un proyecto ASP.NET Core MVC
- 1.4. Controladores, acciones y routing
- 1.5. Introducción a las vistas Razor

# 1.1. Introducción al desarrollo web con ASP.NET Core

## Objetivos de aprendizaje

Al finalizar este punto, el alumno podrá explicar qué función desempeña ASP.NET Core en una aplicación web, diferenciar una respuesta HTML generada por MVC de una respuesta JSON generada por una API, identificar los elementos esenciales de una petición HTTP y seguir la ejecución desde el navegador hasta una acción MVC y una vista Razor.

Se utilizará una primera aplicación del curso, `CursoWeb.Mvc`, que mostrará una página relacionada con el futuro catálogo de productos. No necesitaremos base de datos, autenticación ni conocimientos nuevos de C#.

## 1.1.1. Del conocimiento de Web API a una aplicación web visible

Los alumnos ya conocen ASP.NET Core Web API: una aplicación recibe una petición como `GET /api/productos`, ejecuta un endpoint y devuelve, habitualmente, JSON. Un programa consumidor interpreta después esos datos. Cuando queremos construir una **interfaz web tradicional**, el servidor también puede generar la representación HTML que ve el navegador.

ASP.NET Core es la plataforma de desarrollo web de .NET. Facilita la creación de aplicaciones que atienden HTTP y ofrece infraestructura común: servidor HTTP, enrutamiento, servicios, configuración y una secuencia de procesamiento de las peticiones. Encima de esa plataforma se utilizan distintos estilos de programación: controladores de API, MVC con vistas, Razor Pages y componentes Blazor. Comparten plataforma, pero no son intercambiables.

Para situarnos, imaginemos que un usuario abre en el navegador la dirección del catálogo. La aplicación debe decidir qué recurso se ha solicitado, preparar la información de los productos y producir una respuesta. En una API, el resultado puede ser una colección JSON. En MVC, el resultado habitual de una acción que devuelve una vista es un documento HTML listo para ser interpretado y mostrado por el navegador.

Por ejemplo, una API podría producir una respuesta semejante a esta:

~~~http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

[{"id":1,"nombre":"Cuaderno"},{"id":2,"nombre":"Lápiz"}]
~~~

Una acción MVC que devuelve una vista podría producir este otro contenido:

~~~http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html lang="es">
  <body>
    <h1>Productos</h1>
    <ul><li>Cuaderno</li><li>Lápiz</li></ul>
  </body>
</html>
~~~

Ambos ejemplos utilizan HTTP. La diferencia esencial es el **contrato de presentación**: datos estructurados destinados a un consumidor, frente a marcado preparado para representarse como página. No es una separación absoluta: una API puede devolver otros formatos y una aplicación MVC también puede devolver JSON. Es la forma de trabajar que utilizaremos en el curso la que establece esa comparación.

**Pregunta de razonamiento.** Si una API devuelve el nombre y el precio de un producto, ¿por qué el navegador no presenta automáticamente una ficha de producto con el formato deseado? Porque JSON describe datos, pero no define por sí mismo los elementos HTML, su estructura visual ni los estilos. Una interfaz necesita construir esa representación, y MVC puede hacerlo del lado del servidor.

## 1.1.2. Qué ocurre al escribir una URL

Cuando introducimos `http://localhost:5091/` en el navegador, este actúa como **cliente HTTP**. En nuestro laboratorio, `localhost` identifica el propio ordenador, el puerto `5091` selecciona el proceso servidor y `/` es la ruta solicitada. En un sitio público intervendrían además resolución de nombres, red y, normalmente, HTTPS. Estos elementos no alteran la lógica básica de cliente, petición y respuesta.

Una petición HTTP contiene, como mínimo en términos conceptuales:

- **Método.** Indica el tipo de operación solicitada. En este punto utilizaremos `GET` para consultar una página. El día 2 utilizaremos `POST` para enviar formularios.
- **Destino.** La URL y el camino o *path* que el servidor examina, por ejemplo `/`, `/Home/Index` o `/css/site.css`.
- **Cabeceras.** Metadatos como los formatos que acepta el cliente. No son el cuerpo de la página.
- **Cuerpo.** Datos opcionales asociados a la petición; normalmente una navegación GET sencilla no necesita uno.

La respuesta también tiene partes diferenciadas:

- **Código de estado.** `200 OK` significa que la solicitud se atendió satisfactoriamente; `404 Not Found` significa que el servidor no encontró un recurso o ruta compatible.
- **Cabeceras de respuesta.** Por ejemplo, `Content-Type` indica el tipo del contenido devuelto.
- **Cuerpo de respuesta.** En nuestro ejemplo, el documento HTML de la vista Razor.

Una carga de página puede producir **varias peticiones HTTP**. El navegador primero recibe el HTML; si este enlaza una hoja de estilo con `<link rel="stylesheet" ...>`, solicita además el archivo CSS. Por eso, cuando abrimos la pestaña *Red/Network* de las herramientas de desarrollo, no suele aparecer una sola fila.

La siguiente figura representa el intercambio principal; la solicitud posterior del CSS se muestra como una segunda petición independiente:

~~~mermaid
sequenceDiagram
    participant B as Navegador
    participant S as ASP.NET Core / Kestrel
    B->>S: GET /
    S-->>B: 200 OK + text/html + HTML
    B->>S: GET /css/site.css
    S-->>B: 200 OK + text/css + CSS
    Note over B: Interpreta HTML y CSS y muestra la página
~~~

**Importante:** el navegador **no ejecuta C# ni interpreta código Razor**. Recibe HTML y otros recursos web. Las expresiones Razor se procesan en el servidor al generar la respuesta de esta aplicación MVC. Cuando más adelante estudiemos Blazor, distinguiremos explícitamente su modelo de componentes y su interactividad.

## 1.1.3. Servidor, aplicación, framework y navegador: cuatro responsabilidades

Conviene separar cuatro participantes que a menudo se confunden:

1. **Kestrel**, el servidor web de ASP.NET Core, escucha en una dirección y puerto y recibe conexiones HTTP.
2. **La canalización de ASP.NET Core**, compuesta por middleware y selección de endpoints, procesa la solicitud y decide qué código puede atenderla.
3. **El código de la aplicación MVC**, con controladores y vistas, selecciona la respuesta y genera su contenido. En nuestra primera aplicación, el controlador `HomeController` devuelve `Views/Home/Index.cshtml`.
4. **El navegador** recibe y representa el documento final. Su trabajo visible no implica que conozca las clases del servidor.

Un middleware es un componente que participa en el procesamiento de una petición y puede atenderla directamente o dejar que continúe. En nuestro `Program.cs`, `UseStaticFiles` permite devolver archivos como la hoja de estilos, mientras que `UseRouting` y el mapeo de ruta convencional intervienen en la selección de la acción MVC. No necesitamos dominar todavía cada middleware: basta con reconocer que el servidor no salta mágicamente de la URL a una función cualquiera.

~~~mermaid
flowchart TD
    A["Navegador: GET /"] --> B["Kestrel"]
    B --> C["Canalización ASP.NET Core"]
    C --> D{"¿Recurso estático?"}
    D -->|"Sí: /css/site.css"| E["wwwroot: archivo CSS"]
    D -->|"No: /"| F["Enrutamiento MVC"]
    F --> G["HomeController.Index()"]
    G --> H["Vista Views/Home/Index.cshtml"]
    H --> I["HTML de respuesta"]
    E --> J["Respuesta HTTP"]
    I --> J
    J --> K["Navegador"]
~~~

La figura resume el caso del curso. Una aplicación ASP.NET Core más grande puede utilizar autenticación, sesiones, manejo de excepciones u otros middleware; por ahora no los incorporamos.

## 1.1.4. Cómo se conecta la URL con nuestro primer controlador

Observemos los archivos reales de `M01_MVC/PROYECTO/1.1/CursoWeb.Mvc`. El arranque está definido en `Program.cs`:

~~~csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();

var app = builder.Build();

app.UseStaticFiles();
app.UseRouting();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
~~~

Examinemos cada parte, sin adelantar toda la materia de routing del punto 1.4:

**`CreateBuilder(args)`** prepara un constructor de aplicación con la configuración y los servicios comunes de ASP.NET Core. Aquí no se crea una vista ni se responde todavía a ninguna petición.

**`AddControllersWithViews()`** registra los servicios que necesitan los controladores MVC y su infraestructura de vistas. El verbo *Add* se refiere a configurar servicios; no significa que se esté invocando una acción concreta. Los servicios se configuran al arrancar la aplicación.

**`Build()`** construye la aplicación que utilizará dicha configuración.

**`UseStaticFiles()`** habilita la atención de archivos estáticos ubicados, en nuestro ejemplo, bajo `wwwroot`. Cuando una página hace referencia a `/css/site.css`, ese recurso no necesita pasar por `HomeController`.

**`UseRouting()`** participa en la identificación del endpoint que corresponde a una petición. La aplicación registra después una ruta convencional mediante `MapControllerRoute`. El patrón `{controller=Home}/{action=Index}/{id?}` dice que, si una URL no especifica controlador ni acción, se usan `Home` e `Index` como valores predeterminados. `id?` representa un segmento opcional que utilizaremos posteriormente.

**`Run()`** inicia el host y mantiene la aplicación atendiendo peticiones. Es distinto de la ejecución de una acción: el arranque ocurre una vez por proceso; las peticiones pueden atenderse muchas veces.

Ahora observemos el controlador que ya existe:

~~~csharp
using Microsoft.AspNetCore.Mvc;

namespace CursoWeb.Mvc.Controllers;

public class HomeController : Controller
{
    [HttpGet]
    public IActionResult Index()
    {
        // Response.Headers["X-Curso-Paso"] = "1.1.4";
        return View();
    }
}
~~~

La clase deriva de `Controller` para disponer de la infraestructura y de métodos auxiliares de MVC. `[HttpGet]` limita esta acción a solicitudes HTTP GET. La acción `Index` devuelve un `IActionResult`: en este caso, `View()` crea un resultado que posteriormente localizará y representará la vista. **No devuelve una cadena HTML escrita manualmente** ni significa que el navegador pueda ejecutar la vista.

Por convención, `return View();` en `HomeController.Index` selecciona `Views/Home/Index.cshtml`. Esa convención relaciona nombres de controlador, acción y archivo. La estudiaremos con detalle en los puntos 1.3, 1.4 y 1.5.

## 1.1.5. La vista Razor y el HTML que llega al cliente

El contenido visible de la vista inicial es:

~~~cshtml
@{
    ViewData["Title"] = "Primer recorrido MVC";
}

<h1>1.1 | Primer recorrido MVC</h1>
<p>Esta página HTML ha sido generada en el servidor mediante una acción MVC.</p>
<p id="resultado-inicial">Respuesta HTTP correcta: aplicación MVC disponible.</p>
~~~

Una vista Razor permite combinar HTML con instrucciones Razor del lado del servidor. En este primer ejemplo, la expresión `ViewData["Title"]` proporciona un título que utiliza el diseño general de la página. No necesitamos todavía dominar el paso de modelos tipados; se abordará en el punto 1.5.

El archivo `Views/Shared/_Layout.cshtml` dispone el esqueleto común del documento: `<html>`, `<head>`, navegación, área principal y pie. Su instrucción `@RenderBody()` inserta el contenido principal de la vista. El archivo `Views/_ViewStart.cshtml` indica que las vistas utilizarán ese layout. Como resultado, la respuesta HTML completa tiene más elementos de los que aparecen directamente en `Index.cshtml`.

¿Por qué no colocamos todos los elementos en una sola vista? Porque compartir un layout evita repetir cabeceras, navegación y estilos en muchas páginas. Por el momento basta con **reconocer** esta composición; en el punto 1.5 aprenderemos a modificar layouts y crear vistas parciales.

La hoja de estilos `wwwroot/css/site.css` se sirve por separado. Aunque la apariencia cambie con el CSS, la acción del controlador no necesita conocer detalles del navegador.

## 1.1.6. Observar HTTP en lugar de imaginarlo

La explicación del recorrido anterior se puede comprobar de tres maneras que se complementan:

**En el navegador**, la página visual muestra el contenido procesado. Al abrir las herramientas de desarrollo (F12) y la pestaña *Red/Network*, una navegación permite observar el documento y sus recursos relacionados. Seleccionando la fila de tipo *document* comprobamos el método GET, la URL y el código 200.

**En las cabeceras**, la respuesta de un documento HTML contiene `Content-Type: text/html`, posiblemente acompañado de una indicación de codificación. Al pedir el CSS observaríamos en cambio `text/css`. Las cabeceras describen la respuesta y no deben confundirse con los elementos `<h1>` o `<p>`, que forman parte del HTML.

**En una herramienta HTTP** como `curl`, podemos ver la respuesta sin que intervenga la representación visual del navegador:

~~~bash
curl -i http://localhost:5091/
curl -i http://localhost:5091/ruta-inexistente
~~~

La primera petición debe recibir `200` y una página HTML. La segunda, al no corresponder con una acción de la aplicación, debe recibir `404`. El HTML exacto puede incluir detalles adicionales de framework, pero lo que comprobaremos es el estado HTTP y la marca visible de la vista.

Durante la práctica activaremos dos pequeñas modificaciones y compararemos sus efectos:

- Añadir la cabecera `X-Curso-Paso: 1.1.4` desde la acción MVC **modifica los metadatos HTTP de la respuesta**, no el contenido visual.
- Descomentar un bloque HTML en `Index.cshtml` **modifica el cuerpo HTML**, no necesita añadir una nueva ruta ni cambiar el código HTTP de éxito.

Esta distinción resulta fundamental cuando, más adelante, debamos depurar formularios y llamadas a API: no todos los cambios en el servidor se observan del mismo modo en la pantalla.

## 1.1.7. MVC y Web API: parecido de infraestructura, diferencia de intención

Comparación orientativa, a partir de una misma necesidad de mostrar datos:

| Aspecto | Acción MVC con vista Razor | Endpoint o controlador Web API |
|---|---|---|
| Caso más común | Generar una página para una persona | Facilitar datos/operaciones a un consumidor |
| Respuesta típica | HTML | JSON |
| Presentación | Se construye en el servidor mediante una vista | El consumidor decide cómo presentar los datos |
| Infraestructura HTTP | ASP.NET Core y routing | ASP.NET Core y routing |
| ¿Puede acceder a servicios y EF Core? | Sí | Sí |
| ¿Es obligatoria una base de datos? | No | No |

Un fragmento conceptual de MVC podría ser `return View(productos);`. Su correspondiente estilo de API podría ser `return Ok(productos);`. En el primer caso se solicita la representación de una vista; en el segundo se envían datos con un resultado HTTP apropiado. Son ejemplos de **intención**: no debemos copiar el segundo en el controlador del proyecto 1.1 porque aún no hemos creado ningún modelo `Producto`.

En particular, no es correcto afirmar que *MVC significa servidor y API significa cliente*: ambos códigos se ejecutan en el servidor. Tampoco es correcto afirmar que MVC no utiliza HTTP porque el usuario solo ve un sitio web: cada navegación sigue siendo una comunicación HTTP.

## 1.1.8. Confusiones frecuentes y cómo resolverlas

**«Si abro localhost en el navegador, estoy abriendo un archivo HTML».** En nuestro ejemplo no: el navegador solicita la ruta `/` a un proceso web que escucha en un puerto. La vista se genera como respuesta de una acción MVC. Si apagamos el proceso, esa dirección deja de responder.

**«El archivo Index.cshtml se descarga y Razor se ejecuta en el ordenador del alumno».** No. Razor se evalúa en el servidor. El resultado enviado al navegador es HTML. La extensión `.cshtml` identifica el archivo fuente del proyecto, no el formato de respuesta entregado al usuario.

**«View() devuelve directamente una página HTML».** Más exactamente, `View()` crea un resultado MVC de vista. La infraestructura ejecuta ese resultado, localiza la vista y genera la respuesta HTML. La distinción explica por qué la acción puede permanecer compacta.

**«Una ruta 404 implica que toda la aplicación ha fallado».** No necesariamente. La aplicación puede estar funcionando perfectamente y no tener un endpoint compatible con la URL solicitada. En nuestra primera aplicación es normal que `/ruta-inexistente` devuelva 404.

**«Si no veo cambios en la pantalla, el código del controlador no se ha ejecutado».** No siempre. Una acción puede añadir una cabecera HTTP que solo se aprecia en la respuesta o en las herramientas de desarrollo.

**«ASP.NET Core MVC y ASP.NET Core Web API son frameworks totalmente aislados».** Comparten la misma plataforma web y numerosos servicios. Usan convenciones y tipos de respuesta con objetivos diferentes.

## 1.1.9. Relación directa con la práctica

La práctica `P1.1` reproduce exactamente los hechos descritos aquí: creación de una plantilla MVC, apertura del proyecto inicial del curso, arranque de Kestrel, navegación por `/`, lectura del método y estado de la petición, comparación con una ruta 404, activación de una cabecera y activación de un bloque HTML Razor.

Al finalizar se habrá demostrado un flujo real, no solo memorizado un diagrama. El conocimiento adquirido nos permitirá desarrollar en **1.2** las responsabilidades de Modelo, Vista y Controlador; en **1.3**, la estructura del proyecto; en **1.4**, rutas y acciones; y en **1.5**, vistas Razor más elaboradas.

## Lecturas de referencia

- Microsoft Learn, Información general de ASP.NET Core MVC: https://learn.microsoft.com/es-es/aspnet/core/mvc/overview?view=aspnetcore-8.0
- Microsoft Learn, Tutorial de primera aplicación MVC: https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-mvc-app/?view=aspnetcore-8.0
- Microsoft Learn, Fundamentos de middleware: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/?view=aspnetcore-8.0


---

# 1.2. Arquitectura Model-View-Controller

## Objetivos

Al finalizar el capítulo, el alumno debe poder identificar sin ambigüedades las responsabilidades de **Model**, **View** y **Controller**; explicar cómo se relacionan durante una petición HTTP; entregar objetos desde una acción a una vista fuertemente tipada; y razonar por qué separar datos, decisión de la respuesta y presentación facilita modificar y probar una aplicación.

En el punto 1.1 observamos una acción `HomeController.Index()` que devolvía una vista. En el 1.2 incorporamos una pieza que aún faltaba: un **modelo de producto**. Usaremos un catálogo con tres objetos en memoria para evitar que el aprendizaje de MVC quede oculto tras una base de datos. El acceso mediante EF Core llegará en M02.

## 1.2.1. El problema de una aplicación que mezcla todas las responsabilidades

Supongamos que queremos mostrar una página con tres productos. Una solución apresurada consiste en escribir en una misma acción el contenido de los productos y el marcado HTML que aparecerá en pantalla:

~~~csharp
// Ejemplo conceptual que NO debe copiarse al proyecto.
public IActionResult Index()
{
    string html = "<h1>Productos</h1><p>Cuaderno: 4,50 €</p>";
    return Content(html, "text/html");
}
~~~

Este código es válido como demostración aislada: la acción puede devolver una respuesta HTTP con contenido HTML. Sin embargo, combina dos decisiones diferentes. Por una parte define qué productos existen; por otra decide cómo pintarlos. Si queremos añadir un producto, cambiar un precio, modificar un elemento `<p>` por una tabla o traducir la presentación, tendremos que editar la misma acción. Conforme crece el código, las responsabilidades se superponen.

¿Y si queremos mostrar esos productos además en una ficha de detalle o exportar un listado? Copiar cadenas HTML empeoraría el problema. ¿Y si queremos comprobar que una regla del dominio es correcta sin abrir un navegador? Si toda la lógica está incrustada en el marcado, la comprobación resulta más difícil.

Este es el problema al que responde la separación de responsabilidades: cada elemento se centra en un tipo de decisión y expone una relación clara con los demás. **Separar no significa crear muchas capas empresariales**: para la dimensión didáctica de nuestro catálogo, tres tipos de archivo son suficientes.

## 1.2.2. Tres responsabilidades distintas

El patrón arquitectónico **Modelo–Vista–Controlador (MVC)** organiza una aplicación web en tres familias de responsabilidades. «Familia» es una palabra importante: una aplicación real puede tener múltiples modelos, controladores y vistas; no implica una sola clase de cada tipo.

### Modelo — representar los datos y las reglas de negocio

Un modelo expresa los conceptos que maneja la aplicación. Para nuestro ejemplo, un producto tiene identificador, nombre y precio.

~~~csharp
namespace CursoWeb.Mvc.Models;

public sealed class Producto
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public decimal Precio { get; set; }
}
~~~

El objeto `Producto` **no sabe cuál es la URL** donde se mostrará, **no conoce el navegador** ni necesita saber si su representación final será una lista HTML, una tabla o un documento JSON. Es un tipo de C# que recoge información de nuestro dominio. Se ha elegido `decimal` para el precio porque se trata de una magnitud monetaria, y los valores se expresarán en el código con el sufijo `m`.

Que una clase esté en la carpeta `Models` no la convierte automáticamente en una base de datos. En el 1.2 crearemos los objetos en una lista en memoria; se pierden al detener el proceso. En el día 2 reutilizaremos estos conocimientos para persistir productos con EF Core.

En aplicaciones mayores podemos encontrar modelos de dominio, modelos de persistencia y **view models** (tipos adaptados a una vista). No son necesariamente la misma clase. En este ejercicio utilizaremos directamente `Producto` como modelo de la vista porque es pequeño y evita introducir una arquitectura adicional. Más adelante podremos distinguir cuándo convendría proyectar datos a un tipo específico para la presentación.

### Vista — representar la información para el usuario

La vista define cómo se transforma la información recibida en una interfaz. En MVC, suele ser un archivo `.cshtml` que combina HTML y sintaxis Razor.

Una vista de productos puede recibir una lista y recorrerla:

~~~cshtml
@model IReadOnlyList<CursoWeb.Mvc.Models.Producto>?

@if (Model is null)
{
    <p>El controlador no ha enviado una lista.</p>
}
else
{
    <p>Recibidos: @Model.Count productos.</p>
    <ul>
    @foreach (var producto in Model)
    {
        <li>@producto.Nombre</li>
    }
    </ul>
}
~~~

Este fragmento muestra una vista **tipada**. La directiva `@model` especifica el tipo de datos que espera. La propiedad `Model` permite acceder a los objetos que el controlador le ha proporcionado. Usamos `IReadOnlyList<Producto>?` porque la vista únicamente necesita consultar los datos y durante una etapa inicial el controlador todavía no envía ningún modelo, por lo que puede ser `null`.

El bloque `@if` decide la **presentación** del caso en que no se ha enviado una colección. `@foreach` recorre los productos para crear elementos `<li>`. No introduce productos nuevos, no consulta una base de datos ni toma decisiones empresariales: transforma datos en HTML.

Esto no significa que en una vista esté prohibida toda expresión de C#. Razor permite expresiones y condicionales adecuados para la presentación. Lo que evitaremos es poner en la vista operaciones de persistencia o lógica de negocio compleja.

### Controlador — atender la interacción y coordinar la respuesta

El controlador recibe el resultado del enrutamiento, obtiene o prepara los datos necesarios y elige qué respuesta entregar. En nuestro ejercicio, recibe `GET /Productos`, construye tres productos fijos y los pasa a la vista:

~~~csharp
using CursoWeb.Mvc.Models;
using Microsoft.AspNetCore.Mvc;

namespace CursoWeb.Mvc.Controllers;

public class ProductosController : Controller
{
    [HttpGet]
    public IActionResult Index()
    {
        var productos = new List<Producto>
        {
            new() { Id = 1, Nombre = "Cuaderno", Precio = 4.50m },
            new() { Id = 2, Nombre = "Lápiz", Precio = 1.20m },
            new() { Id = 3, Nombre = "Carpeta", Precio = 3.75m }
        };

        return View(productos);
    }
}
~~~

La acción es intencionadamente sencilla: no ejecuta consultas ni reglas de negocio complejas. La lista fija nos permite seguir el recorrido sin ruido técnico. En un sistema de producción normalmente delegaría la recuperación de productos en otro servicio, repositorio o mecanismo de acceso a datos, pero esos elementos no son necesarios para comprender este capítulo.

**La línea decisiva es `return View(productos);`.** Se crea un resultado de vista asociado al modelo que se quiere representar. MVC localiza la vista correspondiente a `ProductosController.Index` y establece su propiedad `Model` con la lista suministrada. En ese momento, la vista ya no necesita inventarse cuáles son los tres productos: los conoce a través de un contrato tipado.

### Mapa de responsabilidades

| Pregunta | Componente principal |
|---|---|
| ¿Qué atributos tiene un producto? | Modelo `Producto` |
| ¿Qué respuesta se prepara para `GET /Productos`? | `ProductosController.Index` |
| ¿Qué productos se entregan a la pantalla en esta demostración? | El controlador prepara la lista; en un sistema mayor consultaría un servicio |
| ¿Qué HTML representa la cantidad y los nombres? | `Views/Productos/Index.cshtml` |
| ¿Qué parte solicita y representa el HTML? | Navegador, que **no** forma parte de las tres piezas del patrón |

El controlador puede conocer el modelo y seleccionar la vista. La vista suele recibir datos del modelo. **El modelo no necesita depender del controlador ni de la vista**: esa independencia es una de las ventajas más relevantes de MVC.

## 1.2.3. El recorrido completo de una petición

La separación cobra sentido cuando vemos las tres piezas trabajando juntas. En `Program.cs`, el patrón de ruta convencional registrado es:

~~~csharp
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");
~~~

Para `GET /Productos`, el segmento «Productos» identifica el controlador y, al omitirse la acción, se utiliza el valor predeterminado «Index». La infraestructura MVC selecciona `ProductosController.Index()`; la acción pasa la lista al resultado de vista; y Razor genera la página que se devuelve al navegador.

~~~mermaid
sequenceDiagram
    autonumber
    participant N as Navegador
    participant R as Routing MVC
    participant C as ProductosController
    participant M as Modelo Producto
    participant V as Vista Productos/Index.cshtml
    N->>R: GET /Productos
    R->>C: Ejecutar Index()
    C->>M: Crear tres instancias de Producto
    M-->>C: Objetos Producto
    C->>V: View(productos)
    V-->>N: HTML: cantidad y nombres
    Note over N,V: La vista se ejecuta en el servidor y el navegador recibe HTML
~~~

Este diagrama representa relaciones **lógicas**: crear objetos del modelo no implica hacer una llamada HTTP a una clase ni que el modelo sea un servicio activo; son instancias C# creadas dentro del mismo proceso. Asimismo, la vista no envía por sí sola un paquete de red al navegador: ASP.NET Core ejecuta el resultado de vista y construye la respuesta HTTP.

El flujo también puede resumirse así:

~~~mermaid
flowchart LR
    A["GET /Productos"] --> B["Routing MVC"]
    B --> C["Controller: Index()"]
    C --> D["Datos del modelo: Producto"]
    D --> C
    C --> E["Resultado View(productos)"]
    E --> F["Vista Razor tipada"]
    F --> G["HTML de respuesta"]
    G --> H["Navegador"]
~~~

Es importante entender dos diferencias temporales:

1. **En el arranque**, `Program.cs` registra servicios y rutas. No construye la lista para esta vista.
2. **Ante cada petición**, la acción `Index()` se ejecuta y crea una lista nueva en memoria. En este ejemplo no existe un repositorio persistente: cambiar un producto en el código requiere reconstruir o volver a ejecutar el programa para observarlo.

¿Qué ocurre con `/Productos/Index`? La ruta expresa controlador y acción de forma explícita y, por tanto, llega a la misma acción. Esta es una **convención de rutas** que ampliaremos en el capítulo 1.4; en 1.2 solo necesitamos reconocerla y comprobarla.

## 1.2.4. Qué significa «pasar un modelo a una vista»

Para distinguir entrega de datos y representación, construiremos el proyecto en estados sucesivos.

**Estado A: la acción devuelve `View()` sin datos.** La vista existe y puede renderizarse, pero su propiedad `Model` es `null`. Nuestra plantilla muestra «El controlador todavía no ha entregado una lista a la vista». La ruta es válida y puede responder HTTP 200: no recibir datos de modelo no implica necesariamente una respuesta 404.

**Estado B: la acción devuelve `View(productos)`.** La vista recibe tres objetos y muestra «El controlador ha enviado **3** productos». Todavía no hemos activado el bloque HTML de listado. Esto permite comprobar primero el **traspaso de información** entre controlador y vista sin atribuir el resultado a un bucle visual.

**Estado C: se activa `@foreach` en la vista.** Entonces aparecen Cuaderno, Lápiz y Carpeta. No hemos cambiado el controlador: la vista simplemente utiliza un modelo que ya recibía. Este cambio ilustra con claridad la separación entre suministrar datos y representarlos.

**Estado D: habilitamos un enlace Productos en el layout.** El navegador puede ir del inicio al listado. No necesitamos modificar la clase `Producto` para cambiar la navegación; tampoco necesitamos crear un nuevo controlador.

| Estado | Controlador | Vista | Navegación |
|---|---|---|---|
| A, base | `View()` | Mensaje sin modelo | Solo Inicio |
| B, datos | `View(productos)` | Cuenta los tres objetos | Solo Inicio |
| C, listado | `View(productos)` | Cuenta y muestra los nombres | Solo Inicio |
| D, completo | `View(productos)` | Cuenta y muestra los nombres | Inicio y Productos |

La práctica no requiere escribir cuatro aplicaciones distintas. En `PROYECTO/1.2/CursoWeb.Mvc` están preparados los fragmentos que el alumno activa paso a paso, y una batería E2E reconstruye cada estado sobre una copia temporal.

## 1.2.5. Ventajas reales de separar responsabilidades

**Modificación localizada.** Si queremos presentar precios con dos decimales, cambiaremos el marcado de la vista. Si queremos variar la lista fija, editaremos el código que prepara los datos. La clase de producto puede seguir representando las mismas propiedades en ambos casos. Esto reduce el número de archivos afectados por una modificación.

**Comprobación independiente.** Podemos verificar que `Producto` almacena identificador, nombre y precio como cualquier otro objeto C#. Podemos comprobar que un controlador entrega una lista y observar mediante HTTP el HTML de la vista. En nuestro laboratorio también podemos verificar los estados intermedios con peticiones reales a Kestrel.

**Reutilización.** El modelo `Producto` podrá utilizarse en una lista, una vista de detalle y, cuando llegue el momento, en un formulario. No necesitamos duplicar la definición de identificador y precio en cada página.

**Colaboración y evolución.** Una persona puede modificar el aspecto de una vista mientras otra amplía un controlador, siempre que ambas respeten el contrato de datos. Esta separación no elimina toda dependencia: si cambia el nombre o tipo de una propiedad requerida, habrá que actualizar el código que la consume.

**Costes y límites.** MVC añade convenciones y archivos. Para una página estática pequeña puede parecer más trabajo que escribir un único HTML. Un proyecto mal organizado puede seguir siendo complejo aunque utilice carpetas llamadas Models, Views y Controllers. MVC **ayuda** a separar responsabilidades; no garantiza automáticamente que el diseño sea correcto.

En el capítulo 1.4 ampliaremos las acciones, parámetros y tipos de resultado; en 1.5 aprenderemos a construir vistas con un diseño reutilizable. En esta introducción no añadiremos patrones Repository, Clean Architecture ni otras capas empresariales que no aporta el ejercicio.

## 1.2.6. Errores conceptuales frecuentes

**«El modelo es la base de datos».** No. El modelo representa conceptos y datos. Puede estar asociado a persistencia o existir solo en memoria. La clase `Producto` de 1.2 no abre ninguna conexión a una base de datos.

**«El controlador debe escribir todo el HTML».** No es su responsabilidad principal. Devuelve un resultado de vista y proporciona datos. El archivo `.cshtml` define el marcado de presentación.

**«La vista no puede contener ningún C#».** Las vistas Razor permiten expresiones, bucles y condicionales de presentación. Lo que evitaremos es añadir lógica empresarial o de acceso a datos dentro de la vista.

**«Si la vista recibe `null`, la ruta siempre devuelve 404».** No. Una vista bien diseñada puede mostrar un mensaje informativo y responder HTTP 200. Un 404 corresponde a un recurso o endpoint no encontrado, no automáticamente a la ausencia de un objeto.

**«El navegador recibe instancias de `Producto`».** En esta aplicación MVC, el navegador recibe HTML generado a partir de esas instancias. El objeto C# permanece en el servidor.

**«El nombre de la vista es arbitrario».** Si se utiliza `return View()` sin especificar un nombre, MVC recurre a convenciones basadas en el controlador y la acción. Por eso nuestro archivo está en `Views/Productos/Index.cshtml`. Más adelante veremos cómo personalizarlo.

**«MVC y Razor Pages son lo mismo porque ambos emplean Razor».** No. La vista MVC es un elemento de presentación asociado a una acción de controlador. Una Razor Page estructura la gestión de solicitudes alrededor de una página y su PageModel. La comparación detallada será en el capítulo 2.5.

## 1.2.7. Relación con la práctica P1.2

La práctica construye un recorrido comprobable en cuatro estados, partiendo del resultado de 1.1: inspeccionar la clase `Producto`, navegar a un controlador que aún no envía datos, activar una lista fija y pasarla mediante `View(productos)`, habilitar el `@foreach` de la vista y, finalmente, mostrar un enlace de navegación. Después se modifica el nombre de un producto para constatar que la vista utiliza los valores del modelo en vez de tener nombres escritos directamente en su HTML.

Es necesario **observar cada estado antes de activar el siguiente**, porque el objetivo principal no es acabar cuanto antes una página sino explicar por qué apareció cada elemento: la cantidad depende de la entrega del modelo, el listado depende de la lógica de presentación y el enlace depende del layout.

Al finalizar, debe poder responderse a la pregunta: *«Cuando cambio el nombre de Cuaderno por Bloc, ¿qué archivo modifico y por qué no tengo que reescribir la vista?»*. La respuesta debe enlazar las responsabilidades de Modelo, Controlador y Vista que acabamos de estudiar.

### Referencias técnicas

- Microsoft Learn, patrón MVC y separación de responsabilidades: https://learn.microsoft.com/aspnet/core/mvc/overview?view=aspnetcore-8.0
- Microsoft Learn, tutorial de controladores MVC: https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-mvc-app/adding-controller?view=aspnetcore-8.0
- Microsoft Learn, sintaxis Razor y vistas tipadas: https://learn.microsoft.com/en-us/aspnet/core/mvc/views/razor?view=aspnetcore-8.0

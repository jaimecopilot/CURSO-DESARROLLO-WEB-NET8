# M01 — Fundamentos de ASP.NET Core MVC
## Material teórico

### Índice del módulo

- **1.1. Introducción al desarrollo web con ASP.NET Core**
- 1.2. Arquitectura Model-View-Controller
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

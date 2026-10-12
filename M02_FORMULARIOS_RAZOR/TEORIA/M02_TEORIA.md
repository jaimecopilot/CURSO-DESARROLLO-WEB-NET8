# M02 — Formularios, validación y Razor Pages en ASP.NET Core MVC

## Teoría del módulo 2 — Formularios y persistencia de productos

**CURSO: Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8**

**TIPO: TEORÍA**

**AUTOR: JAIME GALLO**

Este manual continúa directamente el catálogo de productos construido en M01. El alumno ya sabe relacionar una solicitud HTTP con una ruta MVC, seleccionar una acción del controlador, entregar un modelo tipado a una vista Razor y reutilizar un layout. El nuevo problema no es mostrar datos existentes, sino recibir información que escribe otra persona, entender cómo se transforma en objetos C#, decidir si puede aceptarse y, finalmente, conservarla.

La progresión acordada para este módulo abarca cinco puntos: **2.1** formularios HTML, GET/POST, model binding y antiforgery; **2.2** Tag Helpers; **2.3** DataAnnotations, ModelState y validación; **2.4** CRUD con EF Core y SQL Server Express LocalDB; y **2.5** una comparación breve con Razor Pages dentro del mismo host MVC. La edición de trabajo comienza por el capítulo 2.1. Los demás capítulos se desarrollarán dentro de este mismo archivo; no se crearán cinco manuales separados.

Al finalizar el día, el producto será un catálogo que permita crear, consultar, modificar y eliminar datos persistidos. La aplicación Razor Pages será solamente una demostración alternativa de recepción de información, no otro proyecto empresarial. Seguimos usando **.NET 8** y los conocimientos previos de C#, Web API y Entity Framework Core; no volveremos a impartir esas tecnologías desde el principio.

# 2.1. Formularios HTML, GET y POST, model binding y antiforgery

## El problema que resuelve un formulario

Hasta ahora, el usuario de nuestro catálogo podía navegar entre la portada, la lista de productos y una ficha individual. Las tres posibilidades pertenecían, principalmente, al mundo de las **consultas**. Una URL como `/Productos/Detalle/2` permite identificar qué información queremos recuperar; el servidor determina qué objeto `Producto` corresponde al identificador y genera una página HTML.

Para introducir información nueva necesitamos que el navegador envíe valores al servidor. Imaginemos que un empleado de una papelería necesita comunicar el nombre y el precio de un producto que todavía no aparece en el catálogo. No tiene sentido modificar el código fuente y volver a compilar cada vez. La página debe proporcionar controles de edición y un mecanismo para remitir esos valores a ASP.NET Core MVC. Ese mecanismo es el **formulario HTML**.

Un formulario no es, por sí solo, una operación de base de datos. Es un contrato de entrada entre el navegador y un destino HTTP. Nuestra primera versión únicamente recibirá un nombre y un precio y los volverá a mostrar en una página de confirmación. Esa decisión es intencionada: si incorporáramos SQL Server en el primer ejemplo, sería difícil distinguir los errores de envío y enlace de datos de los errores de almacenamiento. La persistencia aparecerá en 2.4, una vez comprendidos y comprobados los pasos anteriores.

## Un mismo recurso web puede responder de forma distinta según el método

En M01 aprendimos que el enrutamiento determina qué código puede atender una URL. Esa explicación necesita ahora una precisión: **no basta con la URL; también importa el método HTTP**.

El navegador puede solicitar la página del formulario mediante:

~~~http
GET /Productos/Crear HTTP/1.1
Host: localhost:5091
Accept: text/html
~~~

Una solicitud GET significa aquí que queremos obtener una representación del formulario. El servidor utiliza la acción marcada con `[HttpGet]`, crea un objeto inicialmente vacío y selecciona la vista `Crear.cshtml`. El navegador recibe HTML: etiquetas `label`, controles `input`, botón de envío y un campo oculto para la protección antifalsificación.

Cuando el usuario pulsa el botón, el navegador puede enviar otra petición a **la misma ruta**, esta vez con método POST:

~~~http
POST /Productos/Crear HTTP/1.1
Host: localhost:5091
Content-Type: application/x-www-form-urlencoded

Nombre=Rotulador&Precio=7
~~~

Este segundo mensaje es deliberadamente simplificado: una solicitud aceptada por la aplicación incluirá también un token antiforgery y normalmente una cookie asociada, además de otras cabeceras. El ejemplo ilustra una diferencia fundamental: los valores se transportan como **datos de una petición**, no como el nombre de un archivo `.cshtml` ni como parámetros de código que se ejecuta en el navegador.

El método POST no significa automáticamente «guardar en la base de datos». Indica que el navegador está enviando información al endpoint para que el servidor la procese. Qué hace después la acción es una decisión del programa. En nuestro punto 2.1 la acción solo devuelve una vista de confirmación. En 2.4 ese POST validado también creará una entidad persistente.

Para el alumnado con experiencia en Web API, esta separación resultará familiar: distintas operaciones HTTP pueden actuar sobre recursos relacionados. Aquí la novedad es que la petición procede de una **interfaz HTML Razor**, y que el resultado puede ser otra página HTML en lugar de una respuesta JSON.

## Leer el formulario real antes de construir su POST

El proyecto del curso incluye una vista `Views/Productos/Crear.cshtml` que podemos estudiar en términos de HTML ordinario:

~~~cshtml
@model CursoWeb.Mvc.Models.Producto
@{
    ViewData["Title"] = "Crear producto";
}
<h1>Crear producto — P2.1</h1>
<form method="post" action="/Productos/Crear">
    @Html.AntiForgeryToken()
    <div>
        <label for="Nombre">Nombre</label>
        <input id="Nombre" name="Nombre" value="@Model.Nombre" />
    </div>
    <div>
        <label for="Precio">Precio</label>
        <input id="Precio" name="Precio" type="number" step="0.01"
               value="@Model.Precio.ToString(System.Globalization.CultureInfo.InvariantCulture)" />
    </div>
    <button type="submit">Enviar producto</button>
</form>
~~~

Es importante distinguir tres responsabilidades. El elemento `form` declara **cómo y adónde enviar** los datos mediante `method="post"` y `action="/Productos/Crear"`. Las etiquetas `input` describen **qué campos** puede modificar el usuario y qué nombres se enviarán. Las expresiones Razor, por ejemplo `@Model.Nombre`, se evalúan **en el servidor** cuando se genera el HTML inicial. El navegador recibe una página ya procesada, no una instrucción para ejecutar C#.

La etiqueta `name="Nombre"` es especialmente importante: el model binder utilizará ese nombre para asociar el valor enviado con la propiedad `Nombre` del objeto de entrada. `id="Nombre"`, en cambio, identifica el control dentro del documento HTML y permite vincularlo con la etiqueta `label for="Nombre"`. En nuestro primer formulario ambos atributos tienen la misma cadena, pero cumplen funciones distintas.

El atributo `type="number"` ofrece un control apropiado para cantidades numéricas. `step="0.01"` facilita la introducción de precios con decimales. No debemos interpretarlo como una validación suficiente para un servidor de producción: las peticiones HTTP pueden construirse sin utilizar el formulario ni su interfaz. La validación que define qué valores aceptaremos se estudiará en 2.3.

En este primer ejemplo expresamos el valor inicial del precio usando `CultureInfo.InvariantCulture`. Esto evita introducir un número con coma en el atributo HTML `value` que espera un formato numérico compatible con el control. **No resuelve por sí solo la globalización del enlace de modelos en todos los países**: una aplicación destinada a distintos formatos regionales debe configurar y comprobar su cultura de solicitud. Para el laboratorio reproducible utilizaremos precios enteros al comprobar el transporte inicial y trataremos los límites de validación más adelante.

### El campo oculto que también envía el navegador

La vista contiene `@Html.AntiForgeryToken()`, que genera un elemento de entrada oculto con un valor de comprobación:

~~~html
<input name="__RequestVerificationToken" type="hidden"
       value="un-valor-generado-por-el-servidor" />
~~~

El valor mostrado es una representación didáctica; el token real no es una contraseña escrita por nosotros ni debe copiarse de este ejemplo. ASP.NET Core lo genera al producir la página. El navegador también conserva la cookie pertinente. Cuando el formulario se envía, el servidor puede verificar que la solicitud incorpora la información antiforgery que corresponde.

¿Por qué se escribe el token de forma explícita en este formulario? Porque hemos utilizado un atributo HTML `action` con una URL literal. Es conveniente no depender aquí de condiciones implícitas de generación del token: `@Html.AntiForgeryToken()` hace visible la decisión de proteger el POST. En el apartado 2.2 sustituiremos progresivamente la construcción manual por **Form Tag Helpers**, que normalmente generan ese token de manera automática cuando se utilizan como corresponde. Consulta también la [documentación oficial de Microsoft sobre antiforgery](https://learn.microsoft.com/aspnet/core/security/anti-request-forgery?view=aspnetcore-8.0).

## El controlador: dos acciones llamadas Crear

Una característica de MVC es que un controlador puede contener dos métodos C# con el mismo nombre de acción, diferenciados mediante atributos de método HTTP. En nuestro proyecto, el código GET está disponible desde el principio:

~~~csharp
[HttpGet]
public IActionResult Crear() => View(new Producto());
~~~

Al navegar a `/Productos/Crear`, MVC selecciona este método para GET. `View(new Producto())` prepara la representación de la vista `Crear.cshtml` con un objeto cuyo `Nombre` está vacío y cuyo `Precio` es cero. Todavía no se ha recibido ningún producto nuevo. Crear un objeto C# para presentar el formulario no equivale a guardar un registro.

El proyecto incluye también **comentada** la acción POST. El alumno la activará después de comprobar el GET y el comportamiento anterior a la existencia del POST:

~~~csharp
[HttpPost]
[ValidateAntiForgeryToken]
public IActionResult Crear(Producto producto)
{
    return View("Confirmacion", producto);
}
~~~

La presencia de `[HttpPost]` restringe esa acción al método POST. `[ValidateAntiForgeryToken]` solicita al framework comprobar el token antes de permitir que el método procese la solicitud. Finalmente, el parámetro `Producto producto` recibe un objeto rellenado por el model binder con los valores del formulario.

Este diseño evita una confusión muy común: la cadena `Nombre=Rotulador` no es código C# ni una instrucción para cambiar la propiedad directamente desde el navegador. Es texto transportado por HTTP. ASP.NET Core interpreta los campos de la solicitud y construye el objeto de entrada. La acción trabaja con ese objeto **después** de haber tenido lugar el enlace de modelos.

### Cómo actúa el enlace de modelos

Podemos narrar el recorrido sin convertirlo en una lista de mecanismos internos que el alumno deba memorizar:

1. El usuario introduce `Nombre=Rotulador` y `Precio=7` en el navegador.
2. Al enviar el formulario, el cliente crea una petición POST con esos campos y la información antiforgery.
3. MVC identifica la acción `Crear(Producto producto)` correspondiente al método y a la ruta.
4. El model binder toma los valores que corresponden a las propiedades del tipo `Producto`. Intenta convertir `Precio` al tipo decimal de la clase.
5. La acción ejecuta `View("Confirmacion", producto)`; Razor usa ese objeto para generar el HTML final.

~~~mermaid
sequenceDiagram
    participant N as Navegador
    participant MVC as Routing y MVC
    participant B as Model binder
    participant C as ProductosController
    participant V as Confirmacion.cshtml
    N->>MVC: POST /Productos/Crear + formulario
    MVC->>MVC: Comprobar antiforgery
    MVC->>B: Resolver datos del formulario
    B-->>C: Producto { Nombre, Precio }
    C->>V: View("Confirmacion", producto)
    V-->>N: HTML de datos recibidos
~~~

El diagrama muestra responsabilidades lógicas dentro del servidor; el binder no es un servicio remoto. Es igualmente importante observar **qué no ocurre**: no hay una instrucción `SaveChanges()`, ningún objeto `DbContext` ni escritura SQL. La vista de confirmación no puede demostrar que el producto haya quedado persistido. En realidad, basta con volver al catálogo para comprobar que conserva los tres productos originales.

La clase `Producto` procede del módulo anterior. No necesitamos estudiar de nuevo qué significa una propiedad automática en C#. Su función aquí es ser el **destino tipado** de los valores recibidos. Más adelante distinguiremos el modelo del dominio de un modelo específico para la entrada de formulario, de modo que no tengamos que aceptar todas las propiedades de la entidad desde una solicitud externa.

## Antiforgery: por qué el POST requiere una protección adicional

Cuando un navegador conserva cookies de una aplicación, otras páginas podrían intentar inducirlo a enviar solicitudes no deseadas utilizando ese contexto. Los ataques de falsificación de solicitud entre sitios, conocidos como CSRF, aprovechan esa posibilidad. ASP.NET Core proporciona un mecanismo antiforgery basado en tokens para dificultar el envío de formularios falsificados desde contextos no autorizados.

Nuestra acción incluye `[ValidateAntiForgeryToken]` para que el procesamiento del POST dependa de la comprobación del token. En una navegación normal, la vista genera el campo oculto; el navegador conserva la cookie y envía ambos valores cuando corresponde. Si realizamos el POST sin el token exigido, el framework puede devolver **400 Bad Request** antes de que se ejecute el cuerpo de la acción.

**No significa que el token valide los datos del negocio.** La protección antiforgery responde a «¿está autorizada esta forma de enviar la petición desde la sesión o contexto correspondiente?», pero no a «¿es correcto el precio del producto?» ni «¿hay otro producto con ese nombre?». La segunda familia de preguntas pertenece a la validación del modelo y al dominio.

Asimismo, antiforgery no sustituye autenticación, autorización, HTTPS ni un diseño seguro de permisos. En este curso trabajamos únicamente el escenario local necesario para comprender una solicitud HTML; no construiremos un sistema de Identity desde cero.

### Lo que veremos cuando falte el POST

Antes de activar la acción `[HttpPost]`, el GET puede devolver correctamente el formulario y un envío POST a la misma dirección no encontrará una acción compatible. Es razonable obtener una respuesta **405 Method Not Allowed**. Esto no significa que el HTML esté mal: revela que el servidor reconoce un camino para consultar la página, pero todavía no tiene el endpoint esperado para procesar ese método.

Después de activar el POST, una solicitud de formulario correctamente construida puede terminar en 200 y representar `Confirmacion.cshtml`. Una solicitud sin token válido puede terminar en 400. Las dos respuestas no son contradictorias: MVC distingue ruta, método, autorización del envío y, cuando esos controles se superan, el procesamiento del cuerpo.

No confundiremos un 404 (dirección sin endpoint correspondiente), un 405 (método no admitido para ese destino) y un 400 por antiforgery. En las prácticas se presentan como observaciones de la respuesta HTTP que el alumno podrá relacionar con una causa concreta.

## Qué representa la página de confirmación

La vista `Views/Productos/Confirmacion.cshtml` declara el mismo tipo de modelo que la acción POST:

~~~cshtml
@model CursoWeb.Mvc.Models.Producto

<h1>Datos recibidos del formulario</h1>
<p id="producto-recibido">Nombre: <strong>@Model.Nombre</strong></p>
<p id="precio-recibido">Precio:
    <strong>@Model.Precio.ToString("0.00")</strong> €</p>
~~~

Este archivo no contiene la etiqueta `<form>` principal. Su responsabilidad consiste en mostrar el resultado de una operación previa. Como aprendimos en M01, **Razor genera el HTML en el servidor**. La expresión `@Model.Nombre` representa el dato recibido, y el motor Razor codifica como corresponde las cadenas que se insertan en HTML. Por eso debemos utilizar expresiones Razor ordinarias en lugar de concatenar HTML de procedencia desconocida y marcarlo como no codificado.

La confirmación es el lugar adecuado para un primer ejercicio de transferencia: el alumno escribirá una condición `@if` que presente una etiqueta adicional solamente cuando `Model.Precio >= 4m`. No deberá copiar la solución del catálogo de M01; tendrá que decidir dónde colocar la condición y cómo comprobarla con dos solicitudes de precios distintos.

El cambio será exclusivamente **visual**. Si un producto llega con `Precio=7`, la etiqueta aparecerá en el HTML de confirmación. Si llega con `Precio=2`, desaparecerá. El GET del formulario, la cookie y el enlace de modelos continuarán funcionando sin alteraciones. El alumno debe poder explicar por qué el lugar de ese código es la vista y no una nueva ruta.

## El primer límite: todavía no estamos validando el negocio

En este punto el modelo `Producto` tiene propiedades ordinarias. El atributo HTML `type="number"` puede ayudar a introducir valores, pero un cliente HTTP puede enviar contenido mal formado o valores que no sean apropiados para el catálogo. También es posible que una conversión falle y que el binder registre el problema en `ModelState`. La acción inicial simplificada todavía no consulta `ModelState.IsValid` y no debe utilizarse como ejemplo de formulario listo para producción.

En 2.3 construiremos un `ProductoFormulario` específico con `[Required]`, `[StringLength]` y `[Range]`, mostraremos los errores junto a los campos y evitaremos procesar una solicitud inválida. Conviene anticipar aquí la diferencia sin explicarla dos veces:

**Model binding** intenta obtener valores y convertirlos a las propiedades del parámetro de acción. **Model validation** decide si los valores representan una entrada aceptable según las reglas declaradas. **Persistencia** guarda el resultado cuando corresponde. Son operaciones relacionadas, pero no intercambiables.

Existe otra diferencia con las Web API del curso previo. Un controlador MVC que devuelve vistas no debe suponer que las respuestas 400 por validación se producen automáticamente de la misma forma que en controladores de API con `[ApiController]`. En los formularios MVC el patrón habitual será verificar `ModelState.IsValid` y devolver la misma vista con los mensajes de error para que el usuario pueda corregir los valores.

## Una manera fiable de investigar fallos de formulario

En esta jornada aprenderemos a formular preguntas técnicas antes de tocar archivos al azar. Si el formulario no aparece, comprobaremos la ruta GET, la vista `Crear.cshtml` y el puerto real de Kestrel. Si aparece pero al enviarlo recibimos 405, revisaremos el atributo `[HttpPost]` y el código activado en el controlador. Si recibimos 400, investigaremos si se ha generado y remitido correctamente el token antiforgery. Si recibimos una confirmación con el precio incorrecto, compararemos el `name` del campo, el tipo de la propiedad y la cultura usada al convertir el valor.

Para una misma incidencia habrá distintas fuentes de información. La página HTML permite ver los controles y la confirmación. La pestaña **Red** del navegador muestra el método y la respuesta HTTP de cada solicitud. El código fuente del controlador explica las acciones disponibles. El catálogo permite comprobar que todavía no existe persistencia. Ninguna de estas comprobaciones requiere inventar un sistema nuevo.

El método de aprendizaje será el mismo que aprobamos en M01: formular una hipótesis, cambiar una sola responsabilidad, ejecutar, observar el resultado y explicar por qué ha cambiado. Solo después avanzaremos hacia la automatización de formularios mediante Tag Helpers.

## Conexión con los puntos siguientes

El recorrido completado hasta aquí es **consulta GET → formulario Razor → POST protegido → enlace de modelos → confirmación HTML**. Hemos añadido entrada de datos al catálogo sin introducir todavía reglas de negocio ni almacenamiento. Es una evolución limitada pero real del producto anterior.

En **2.2** dejaremos de escribir manualmente cada asociación HTML y utilizaremos los Tag Helpers `asp-for`, `asp-action` y `asp-controller`. Esto hará más sencilla la correspondencia entre propiedades del modelo, etiquetas de los campos y destino de la solicitud.

En **2.3** aparecerá el problema de la entrada inválida y sus mensajes de error. En **2.4**, el flujo validado pasará de mostrar una confirmación a crear un producto persistido mediante EF Core, con SQL Server Express LocalDB en el laboratorio Windows. En **2.5** compararemos este patrón de controlador y vista con `PageModel`, `OnGet` y `OnPost` en una Razor Page mínima.

La teoría y la práctica P2.1 deben estudiarse juntas, pero no es necesario leer toda la teoría de M02 en voz alta durante la clase. La actividad esencial consiste en observar y completar un envío real; las secciones de diagnóstico ofrecen material de consulta y ampliación.

## Lecturas de referencia del punto 2.1

- Microsoft Learn, Model binding en ASP.NET Core MVC: https://learn.microsoft.com/aspnet/core/mvc/models/model-binding?view=aspnetcore-8.0
- Microsoft Learn, Protección antiforgery de solicitudes: https://learn.microsoft.com/aspnet/core/security/anti-request-forgery?view=aspnetcore-8.0
- Microsoft Learn, Tag Helpers de formularios: https://learn.microsoft.com/aspnet/core/mvc/views/working-with-forms?view=aspnetcore-8.0
- Microsoft Learn, Validación de modelos en ASP.NET Core MVC: https://learn.microsoft.com/aspnet/core/mvc/models/validation?view=aspnetcore-8.0

# 2.2. Tag Helpers: de los atributos HTML escritos a mano al enlace tipado con MVC

## La misma aplicación, un nuevo problema de mantenimiento

En el capítulo anterior conseguimos que un formulario enviara el nombre y el precio de un producto al servidor. El controlador disponía de dos acciones llamadas Crear: una GET para mostrar la página y otra POST para procesar los campos. También comprobamos que un token antiforgery permite distinguir un envío normal desde el navegador de una petición que intenta omitir esa protección. Ahora vamos a conservar esas responsabilidades, pero mejorar la **manera de describir el formulario y sus enlaces dentro de Razor**.

Observemos cómo era la primera solución. En el HTML de la vista escribíamos explícitamente el destino de la petición, los nombres de los campos, los identificadores y las asociaciones entre etiquetas y entradas. No había nada intrínsecamente incorrecto en ello: el navegador recibió controles HTML válidos. El problema aparece cuando el programa crece. Si la acción Crear se renombra o una propiedad del modelo cambia de nombre, las cadenas escritas manualmente no expresan esa dependencia con tanta claridad. Un formulario puede seguir dibujándose correctamente y, sin embargo, enviar campos con nombres que ya no coincidan con las propiedades del modelo.

En M01 vimos una situación equivalente al pasar de enlaces con rutas escritas a mano a enlaces generados mediante **Anchor Tag Helper**. El sistema de routing conocía las acciones MVC y sus parámetros, mientras que un enlace literal dependía de que nosotros recordásemos sus segmentos. El punto 2.2 amplía esa misma idea a formularios, etiquetas, campos y botones. No introduce otra arquitectura, no altera la base de datos —todavía inexistente en P2.2— y no sustituye HTML por un lenguaje de interfaz nuevo.

**Un Tag Helper es una funcionalidad de ASP.NET Core que participa en la generación de HTML a partir de un elemento Razor dotado de atributos especiales.** Escribimos marcado que conserva la estructura habitual de HTML y añadimos atributos como asp-for o asp-action. Al procesar la vista, el servidor interpreta esos atributos y produce elementos HTML ordinarios para el navegador. No es un componente Blazor interactivo; los componentes Razor se estudiarán en M03 y tienen otro modelo de ejecución.

No debemos interpretar el cambio como una «magia» que elimina la necesidad de comprender HTTP o HTML. De hecho, el ejercicio más útil consiste en comparar el código fuente Razor con el **HTML realmente devuelto**. Esa comparación hace visible la responsabilidad del Tag Helper y ayuda a detectar errores cuando no se reconoce una directiva.

## Dos documentos distintos: la vista Razor y el HTML recibido

La vista es un archivo CSHTML que puede contener sintaxis de Razor y Tag Helpers. Por ejemplo, el atributo especial de la siguiente etiqueta no pertenece al HTML estándar:

~~~cshtml
<label asp-for="Nombre"></label>
~~~

El navegador no debería recibir un atributo asp-for sin procesar. El Label Tag Helper lo transforma, para la propiedad Nombre del modelo, en un resultado conceptualmente equivalente a:

~~~html
<label for="Nombre">Nombre</label>
~~~

Ahora sí estamos ante HTML ordinario: la etiqueta señala un control identificado por Nombre. La expresión asp-for no se ha ejecutado en JavaScript ni aparece como un «comando» para el navegador. La transformación se ha realizado **en el servidor durante la representación de la vista**.

Compárese con lo que ocurría en P2.1:

~~~cshtml
<label for="Nombre">Nombre</label>
<input id="Nombre" name="Nombre" value="@Model.Nombre" />
~~~

Ambas representaciones pueden producir un resultado visual indistinguible. El valor del nuevo enfoque no se mide contando píxeles diferentes: se mide observando que la vista describe una asociación tipada, que la infraestructura puede producir atributos coherentes con el modelo y que dejamos de repetir tantas cadenas manuales.

Conocer la diferencia fuente/resultado resulta imprescindible para depurar. Si alguien dice «he añadido asp-for y no se ve ningún cambio», quizá no exista un problema: puede que el resultado HTML correcto de la nueva etiqueta sea casi idéntico al anterior. Lo que interesa comprobar es el vínculo entre la propiedad C# y los atributos finales, la continuidad del model binding y las comprobaciones de entrada que ya aprendimos.

## Dónde se habilitan los Tag Helpers

Antes de modificar un formulario conviene averiguar por qué los atributos especiales funcionan en nuestro proyecto. El archivo **Views/_ViewImports.cshtml** contiene:

~~~cshtml
@using CursoWeb.Mvc
@addTagHelper *, Microsoft.AspNetCore.Mvc.TagHelpers
~~~

La directiva addTagHelper hace disponibles los Tag Helpers integrados de ASP.NET Core MVC para las vistas que quedan dentro de ese ámbito de importación. No es un controlador y no constituye una llamada HTTP. Tampoco instala Entity Framework Core, añade propiedades a Producto ni define por sí mismo rutas de negocio.

La posición del archivo es importante. Situado en Views, su contenido se aplica a las vistas de ese directorio y sus subdirectorios, como Views/Productos/Crear.cshtml. Esta decisión evita repetir la directiva en cada CSHTML. El alumnado ya conocía el archivo desde M01, porque allí se utilizaban Tag Helpers de parciales y enlaces; ahora va a comprender su función de forma más explícita.

El prefijo asp- puede inducir a pensar que todo atributo que comienza así es una propiedad HTML. No lo es: ciertos atributos se interpretan específicamente durante el procesamiento de Razor, por un Tag Helper que se ha registrado. Si la directiva correspondiente no está habilitada o el elemento está fuera del ámbito, esos atributos podrían terminar sin procesarse en el HTML que recibe el navegador. Ésta es una de las primeras hipótesis que conviene comprobar cuando una vista «muestra asp-for» en lugar del id y name esperados.

**No desactivaremos _ViewImports.cshtml** para realizar la práctica. Ya existen otras vistas del proyecto que dependen de Tag Helpers, especialmente la vista parcial del catálogo. El objetivo de P2.2 no es romper la funcionalidad anterior para observar un fallo artificial, sino ampliar su uso a un formulario nuevo.

La documentación oficial de Microsoft sobre [Tag Helpers y _ViewImports](https://learn.microsoft.com/aspnet/core/mvc/views/tag-helpers/intro?view=aspnetcore-8.0) explica tanto el registro mediante addTagHelper como la diferencia con los antiguos HTML Helpers. El archivo del curso es un ejemplo deliberadamente pequeño de ese mecanismo.

## Primer cambio: Form Tag Helper y la dirección de destino

El formulario de P2.1 expresaba su destino con un atributo HTML literal:

~~~cshtml
<form method="post" action="/Productos/Crear">
    @Html.AntiForgeryToken()
    <!-- campos de entrada -->
</form>
~~~

Con el **Form Tag Helper** podemos describir el controlador y la acción en lugar de escribir toda la ruta en una única cadena:

~~~cshtml
<form asp-controller="Productos" asp-action="Crear" method="post">
    <!-- campos de entrada -->
</form>
~~~

Aquí asp-controller identifica el controlador lógico Productos y asp-action identifica la acción Crear. El atributo method continúa siendo HTML estándar: determina que el formulario se envía por POST. El Form Tag Helper utiliza la configuración de routing de la aplicación para generar el atributo action final. En nuestro proyecto y con la ruta convencional disponible, el navegador recibe una apertura equivalente a:

~~~html
<form method="post" action="/Productos/Crear">
~~~

Es tentador concluir que no hemos ganado nada porque la dirección generada es la misma. Sin embargo, ahora el origen de esa dirección está relacionado con los elementos de MVC, en lugar de ser una ruta literal dispersa por una vista. Cuando en otra práctica estudiemos rutas diferentes o se cambien convenciones, el resultado podrá evolucionar con ellas. No significa que cualquier cambio de nombre quede arreglado automáticamente, ni que el compilador garantice siempre la existencia de una acción: habrá que seguir comprobando la ruta final.

El proyecto P2.2 empieza conservando activo el formulario HTML de P2.1. Dentro de Crear.cshtml se entrega, comentada, la alternativa de Form Tag Helper. El alumno sustituirá la apertura original, sin duplicar formularios. La etiqueta de cierre permanece, porque no se está creando otra estructura HTML: es el mismo formulario descrito con otros atributos.

### El token antiforgery: continuidad funcional y una precaución importante

Recordemos que P2.1 utilizaba Html.AntiForgeryToken() para escribir explícitamente el campo oculto. En P2.2 emplearemos el Form Tag Helper integrado, con method="post", asp-controller y asp-action. En ese contexto ASP.NET Core **puede generar automáticamente el token antiforgery**. En este ejemplo concreto, con un formulario POST generado por el Tag Helper, esa generación forma parte del resultado esperado.

Por esa razón, al reemplazar la etiqueta original eliminaremos la llamada explícita a Html.AntiForgeryToken(). No es una invitación a retirar la protección, sino a evitar introducir dos mecanismos de escritura del mismo campo cuando el propio Form Tag Helper se encarga de generar el token. **El controlador conserva el atributo ValidateAntiForgeryToken** y el navegador sigue enviando su información antiforgery.

La comprobación se realiza sobre el HTML final. Debemos encontrar **un campo oculto** con el nombre __RequestVerificationToken en el formulario que se genera. Si el alumno elimina la llamada explícita pero la etiqueta sigue siendo HTML sin intervención de Form Tag Helper, el token podría desaparecer; el POST empezaría a responder 400. Esa incidencia es precisamente el tipo de síntoma que permite relacionar una decisión de maquetación de formulario con una consecuencia HTTP.

No confundiremos la generación del token con la autorización de un usuario. El token antiforgery ayuda a defender frente a falsificación de solicitudes entre sitios, pero no determina quién puede crear productos y no valida las reglas del precio. De nuevo, tenemos tres preguntas independientes: cómo se genera la petición, si su origen cumple las comprobaciones previstas y si los datos del negocio son aceptables.

La [documentación oficial de Form Tag Helper](https://learn.microsoft.com/aspnet/core/mvc/views/working-with-forms?view=aspnetcore-8.0) explica la generación del action y del token oculto. La comprobación práctica consistirá en cargar una página real, inspeccionarla y enviar el formulario, no en copiar tokens desde una captura.

## Segundo cambio: Label Tag Helper y asociación de etiquetas

En HTML ordinario se asocian un label y un input escribiendo sus atributos explícitamente:

~~~html
<label for="Nombre">Nombre</label>
<input id="Nombre" name="Nombre" />
~~~

Esta asociación tiene un valor funcional y de accesibilidad. Al seleccionar la etiqueta con el puntero, el navegador puede enfocar el control correspondiente. También aporta información útil a las tecnologías de asistencia. El texto Nombre no debe estar separado de su campo por razones puramente estéticas.

Con el Label Tag Helper escribimos:

~~~cshtml
<label asp-for="Nombre"></label>
~~~

El resultado es conceptualmente equivalente al HTML original. El nombre de la propiedad se interpreta en el contexto de la directiva @model de la vista, que en P2.2 sigue siendo CursoWeb.Mvc.Models.Producto. El Label Tag Helper no procesa la cadena enviada por el usuario: utiliza **metadatos del modelo de la vista** para decidir a qué control corresponde la etiqueta.

Esta diferencia será aún más útil en el punto 2.3, cuando aparezcan anotaciones como Display o Required en modelos de entrada. Por ejemplo, una propiedad técnica podría tener un nombre de presentación distinto para el usuario. El Tag Helper está preparado para utilizar esa información, mientras que un literal escrito en HTML debe revisarse manualmente en cada vista afectada.

En P2.2 las etiquetas de Nombre y Precio se transforman por separado. Es importante que el alumno no cambie a la vez etiquetas, campos y destino del formulario sin observar los estados intermedios. Primero deberá comprobar que el atributo for de ambas etiquetas se genera correctamente y que los campos todavía mantienen sus valores y nombres originales. Si algo deja de funcionar, el cambio responsable estará acotado.

### No hay una diferencia entre «label con Tag Helper» y «label sin HTML»

El resultado sigue siendo un elemento label de HTML. Un Tag Helper no inventa una interfaz visual alternativa. En esta actividad, la etiqueta no aparecerá en una pantalla distinta ni mostrará necesariamente un texto espectacular. El criterio observable será que, al inspeccionar el HTML, for apunta al id del input y el atributo asp-for ya no aparece sin procesar.

Esa forma de evaluar protege contra una mala costumbre pedagógica: dar por terminado un ejercicio porque «la página se ve igual». El alumnado ha de demostrar que sabe por qué es apropiado el elemento generado y cómo se conecta con el modelo.

## Tercer cambio: Input Tag Helper y generación de nombre, id y valor

El Input Tag Helper es uno de los mecanismos que más fácilmente conecta los conocimientos de M01 con el nuevo model binding de M02. Hasta ahora, el formulario tenía entradas explícitas:

~~~cshtml
<input id="Nombre" name="Nombre" value="@Model.Nombre" />
<input id="Precio" name="Precio" type="number" step="0.01"
       value="@Model.Precio.ToString(System.Globalization.CultureInfo.InvariantCulture)" />
~~~

La primera entrada utiliza el nombre de campo Nombre y la segunda, Precio. Cuando el navegador construye el POST, esas claves indican al binder dónde encontrar cada valor. El atributo value de cada entrada representa el valor inicial escrito al renderizar la vista.

La forma con Input Tag Helper es más breve:

~~~cshtml
<input asp-for="Nombre" />
<input asp-for="Precio" type="number" step="0.01" />
~~~

En los dos casos asp-for apunta a una propiedad del modelo tipado. El resultado generado incluye atributos id y name apropiados para el enlace de modelos, y el valor inicial procede del modelo. Para Nombre se obtendrá un control textual. Para Precio conservamos explícitamente type="number" y step="0.01", porque estamos explicando cómo se usa un control numérico concreto y no queremos convertir una inferencia de tipo HTML en el objetivo de la práctica.

Es esencial recordar que **el atributo asp-for no valida por sí solo los valores del negocio**. Que el navegador proporcione un control de tipo number no significa que el servidor deba aceptar cualquier cantidad, ni que un cliente HTTP no pueda enviar campos con valores arbitrarios. En P2.3 utilizaremos un modelo de entrada y reglas declarativas de validación.

El alumno debe comparar el nombre y el identificador del control generado con los de la versión anterior. Si el formulario deja de construir un Producto cuyos campos coincidan con el valor enviado, no basta con cambiar el código del controlador sin investigar: hay que inspeccionar el atributo name del HTML realmente enviado.

### La cultura del precio: qué podemos y qué no podemos concluir

El formulario de P2.1 convertía inicialmente el valor decimal a una cadena utilizando InvariantCulture. Con Input Tag Helper es el framework quien construye parte de la representación a partir del tipo y de los metadatos de la propiedad. Esta automatización no constituye, por sí sola, una solución universal para diferentes culturas, separadores decimales y reglas de validación.

En las comprobaciones principales del curso enviaremos precios enteros, como 7 y 2, de modo que podamos observar el model binding sin introducir simultáneamente la globalización. Si necesitásemos ofrecer un formulario público para diferentes idiomas y regiones, tendríamos que establecer y probar una política de cultura de solicitud coherente. La explicación completa de ese escenario excede este punto de seis horas.

No debemos recomendar que el alumno «arregle» cualquier error de precio cambiando todas las propiedades a string. Precio representa una cantidad y continuará siendo decimal en el dominio. Lo que cambiaremos cuando corresponda es el contrato de entrada y las reglas que permiten informar correctamente al usuario de un error de conversión.

## Cuarto cambio: Anchor Tag Helper para volver al catálogo

La navegación también forma parte de la experiencia de un formulario. El usuario debe poder abandonar la pantalla de alta sin introducir datos o volver al catálogo después de revisar una confirmación. En la versión HTML original escribimos:

~~~html
<a href="/Productos">Volver al catálogo</a>
~~~

Con Anchor Tag Helper podemos indicar el destino mediante los elementos MVC:

~~~cshtml
<a asp-controller="Productos" asp-action="Index">Volver al catálogo</a>
~~~

El HTML generado incluirá un atributo href que el navegador entiende. El Tag Helper no envía la petición en nombre del usuario: únicamente genera un enlace. Cuando el usuario pulse ese enlace, el navegador iniciará una nueva solicitud GET al destino representado.

No confundiremos el atributo asp-action de una etiqueta a con el atributo asp-action de un formulario. Ambos utilizan los datos de routing, pero el primero participa en la generación de un enlace de navegación, mientras que el segundo determina el destino al enviar el formulario. El método HTTP de la navegación ordinaria sigue siendo GET. En cambio, el formulario de creación mantiene method="post".

Esta diferencia es un ejemplo de por qué no conviene estudiar Tag Helpers como una colección de palabras clave sin contexto. En la práctica se utilizarán tres tipos de elementos: form, input/label y a. Cada uno produce una parte distinta del HTML final y participa en una operación distinta del usuario.

## Un paso adicional: enlaces cuyo identificador procede de un producto

El catálogo contiene tres productos con identificadores 1, 2 y 3. Sus enlaces originales ya funcionan:

~~~cshtml
<a class="enlace-detalle" href="/Productos/Detalle/@producto.Id">Ver detalle</a>
~~~

La expresión Razor produce la parte variable de la cadena. Para un producto con Id igual a 2, la URL final debe permitir visitar la ficha de Lápiz. Esta solución es correcta para el ejemplo, pero sigue escribiendo de forma literal la parte fija de la ruta.

Podemos expresar el mismo enlace de acuerdo con el routing de MVC:

~~~cshtml
<a class="enlace-detalle"
   asp-controller="Productos"
   asp-action="Detalle"
   asp-route-id="@producto.Id">Ver detalle</a>
~~~

El atributo asp-route-id aporta el valor de la ruta llamado id. En nuestro proyecto, la ruta convencional incluye el segmento opcional {id?}; por eso un valor como 2 puede incorporarse a la URL final de detalle. El nombre que aparece tras asp-route- debe corresponder al valor de ruta que quiere suministrarse; no es una propiedad arbitraria del navegador.

La prueba correcta no consiste en generar un enlace fijo para Lápiz. El listado debe contener **tres enlaces diferentes** y cada uno debe llegar a su ficha. Si la acción se trasladara a otra ruta convencional o se ajustase su configuración, habría que revisar la URL producida, pero el objetivo del Tag Helper es describir el destino utilizando los conceptos de MVC y sus valores de ruta.

Este es el **reto de P2.2**. El alumno deberá activar una alternativa comentada dentro del foreach del listado y retirar el enlace literal que sustituye. Así se evita terminar con dos enlaces de detalle por producto. No se modifica el controlador ni se guarda información en una base de datos.

### El caso especial del producto recién enviado

En P2.2, el modelo Producto que llega desde el formulario puede tener Id igual a cero, porque el formulario no envía un identificador y todavía no se guarda nada. Por eso **no vamos a crear automáticamente en la confirmación un enlace de detalle utilizando Model.Id**: hacerlo llevaría a una dirección que no identifica necesariamente un producto guardado.

Esta observación conecta directamente con el problema que resolverá el CRUD de P2.4. Una vez guardado un producto en la base de datos, tendrá un identificador persistente y la aplicación podrá redirigir a su detalle. Hasta entonces, el botón correcto de la confirmación es «Enviar otro formulario» o «Volver al catálogo», no «Ver el producto recién creado» como si existiera en almacenamiento.

Es una distinción pequeña pero pedagógicamente importante: **un Tag Helper puede generar una URL sintácticamente válida y, aun así, esa URL puede no representar un recurso existente**. La infraestructura de routing no sustituye las reglas de negocio.

## De los HTML Helpers a los Tag Helpers: una decisión, no una competición

En P2.1 utilizamos @Html.AntiForgeryToken(), un HTML Helper. En P2.2 utilizamos atributos de Tag Helpers. Ambos mecanismos pueden convivir en una misma aplicación; la plataforma no obliga a convertir de inmediato todos los HTML Helpers a otra sintaxis.

La elección depende de qué resultado queremos producir y de cómo deseamos expresar el código Razor. El Form Tag Helper reduce el trabajo de escribir rutas y, en el caso apropiado, incorpora la generación del token. El Label y el Input Tag Helper aprovechan los metadatos de las propiedades y mantienen coherencia entre etiquetas y controles. El Anchor Tag Helper permite expresar enlaces en términos de controlador, acción y valores de ruta.

Un error sería enseñar que los Tag Helpers impiden todas las equivocaciones o que generan interfaces de usuario seguras sin más comprobaciones. Son una ayuda para describir elementos HTML a partir del contexto del servidor. La aplicación necesita seguir considerando la validación, las autorizaciones cuando corresponda, la accesibilidad, la representación cultural de los datos y el mantenimiento de sus rutas.

En esta jornada evitaremos introducir Tag Helpers personalizados. Su creación es una técnica útil para otras aplicaciones, pero excede el alcance reducido del curso. La prioridad es trabajar con los Tag Helpers incorporados a ASP.NET Core MVC y entender sus efectos en un formulario real.

## Diagnóstico razonado de un formulario convertido

Imaginemos que hemos sustituido la apertura del formulario, ambos labels, los dos inputs y el enlace de vuelta al catálogo. La página se sigue viendo igual. ¿Cómo demostramos que hemos hecho un buen trabajo?

En primer lugar, el HTML generado no debe contener asp-controller, asp-action ni asp-for como atributos sin procesar en los elementos transformados. Si aparecen literalmente en el DOM, revisaremos el archivo _ViewImports.cshtml y la ubicación de la vista. No cambiaremos de forma aleatoria las acciones del controlador.

En segundo lugar, la etiqueta form debe disponer de un action apropiado y mantener method="post". El atributo action es el que comprende el navegador; asp-action es la instrucción utilizada para generarlo. El formulario no ha cambiado su finalidad por haber cambiado su sintaxis Razor.

En tercer lugar, hay que comprobar que cada label dispone de un atributo for que coincide con el id del campo correspondiente. La comprobación aporta significado y accesibilidad, no solamente un resultado estético.

En cuarto lugar, los inputs deben conservar name="Nombre" y name="Precio" en el HTML generado. Si se cambia accidentalmente una de esas claves, el enlace de modelos puede recibir valores vacíos o predeterminados, aunque el usuario haya escrito algo en pantalla. El HTML que sale del servidor y el POST que llega al controlador son las dos caras del contrato.

Por último, hay que examinar el token: debe existir un campo oculto __RequestVerificationToken que se envía al servidor cuando corresponde, y la acción POST debe seguir comprobándolo. Una petición sin token válido continúa obteniendo 400, mientras que una solicitud enviada correctamente desde la página puede mostrar la confirmación.

No se necesita una pantalla nueva para cada comprobación. Basta con **seguir el mismo recorrido del usuario y examinar evidencias concretas**. Este criterio hace que las prácticas de P2.1 y P2.2 sean comparables y que el alumnado no pierda lo que ya había conseguido.

### Errores que parecen similares, pero tienen causas diferentes

Si el formulario responde con 405, la ruta de la acción POST puede no estar disponible. La conversión a Tag Helpers no crea automáticamente una acción que no exista.

Si responde con 400, hay que considerar el token antiforgery y otros problemas de solicitud. Después de haber cambiado el form, un error común sería eliminar la llamada manual al token sin haber activado realmente el Form Tag Helper: el HTML dejaría de contener el campo necesario.

Si el POST devuelve confirmación pero con Nombre vacío, podemos investigar el atributo name generado en el input, sin cambiar de inmediato el código que representa Confirmacion.cshtml.

Si el enlace de regreso al catálogo lleva a una dirección incorrecta, debemos comparar el href generado y las reglas de routing. La apariencia de un enlace subrayado no demuestra que el destino sea correcto.

Si se representan dos enlaces de detalle por producto, probablemente el alumno ha **añadido** la variante del reto sin retirar el enlace original. Éste es un problema de duplicación del marcado, no del motor MVC.

La forma de resolver estas incidencias consiste en formular una hipótesis, encontrar la capa responsable y cambiar el archivo correcto. El diagnóstico no se basa en copiar una configuración desconocida desde Internet ni en eliminar protecciones para hacer que el navegador avance.

## El límite de P2.2 y el puente hacia P2.3

Ya podemos describir la entrada y la navegación utilizando los servicios que MVC proporciona durante la representación de Razor. Hemos mejorado el formulario y sus enlaces **sin alterar el contrato funcional**: el navegador sigue enviando Nombre y Precio; el controlador sigue recibiendo Producto; antiforgery sigue comprobándose; y la confirmación sigue mostrando lo que llegó.

La pregunta que todavía no hemos contestado es si todos esos valores deben aceptarse. ¿Qué hacemos si alguien deja Nombre vacío, introduce un precio negativo o supera una longitud admitida por la aplicación? Ni asp-for ni la presentación de un campo con type="number" ofrecen por sí solos la respuesta completa. El siguiente capítulo construirá un modelo de entrada específico, utilizará anotaciones como Required, StringLength y Range y observará el estado de ModelState.

En P2.3 añadiremos mensajes visibles junto a los campos y comprobaremos qué ocurre cuando el formulario debe volverse a representar sin perder los valores enviados. Ese paso ya no será una transformación puramente estructural del HTML: introducirá decisiones de aceptación de datos en el servidor y un mecanismo para informar al usuario de los errores.

Después, en 2.4, usaremos la base SQL Server Express LocalDB con Entity Framework Core que el alumnado ya conoce. La entrada validada pasará a las operaciones reales de creación, edición y eliminación. Finalmente, en 2.5 compararemos la coordinación mediante controlador y vista con los métodos OnGet y OnPost de una Razor Page mínima alojada en la misma aplicación.

## Fuentes y documentación relacionada

- Microsoft Learn, [Tag Helpers en formularios de ASP.NET Core](https://learn.microsoft.com/aspnet/core/mvc/views/working-with-forms?view=aspnetcore-8.0).
- Microsoft Learn, [Introducción a los Tag Helpers](https://learn.microsoft.com/aspnet/core/mvc/views/tag-helpers/intro?view=aspnetcore-8.0).
- Microsoft Learn, [Anchor Tag Helper](https://learn.microsoft.com/aspnet/core/mvc/views/tag-helpers/built-in/anchor-tag-helper?view=aspnetcore-8.0).
- Microsoft Learn, [Model binding](https://learn.microsoft.com/aspnet/core/mvc/models/model-binding?view=aspnetcore-8.0).

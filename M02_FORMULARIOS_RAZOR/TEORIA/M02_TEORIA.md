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

Hasta ahora, el usuario de nuestro catálogo podía navegar entre la portada, la lista de productos y una ficha individual. Las tres posibilidades pertenecían, principalmente, al mundo de las **consultas**. Una URL como \`/Productos/Detalle/2\` permite identificar qué información queremos recuperar; el servidor determina qué objeto \`Producto\` corresponde al identificador y genera una página HTML.

Para introducir información nueva necesitamos que el navegador envíe valores al servidor. Imaginemos que un empleado de una papelería necesita comunicar el nombre y el precio de un producto que todavía no aparece en el catálogo. No tiene sentido modificar el código fuente y volver a compilar cada vez. La página debe proporcionar controles de edición y un mecanismo para remitir esos valores a ASP.NET Core MVC. Ese mecanismo es el **formulario HTML**.

Un formulario no es, por sí solo, una operación de base de datos. Es un contrato de entrada entre el navegador y un destino HTTP. Nuestra primera versión únicamente recibirá un nombre y un precio y los volverá a mostrar en una página de confirmación. Esa decisión es intencionada: si incorporáramos SQL Server en el primer ejemplo, sería difícil distinguir los errores de envío y enlace de datos de los errores de almacenamiento. La persistencia aparecerá en 2.4, una vez comprendidos y comprobados los pasos anteriores.

## Un mismo recurso web puede responder de forma distinta según el método

En M01 aprendimos que el enrutamiento determina qué código puede atender una URL. Esa explicación necesita ahora una precisión: **no basta con la URL; también importa el método HTTP**.

El navegador puede solicitar la página del formulario mediante:

~~~http
GET /Productos/Crear HTTP/1.1
Host: localhost:5096
Accept: text/html
~~~

Una solicitud GET significa aquí que queremos obtener una representación del formulario. El servidor utiliza la acción marcada con \`[HttpGet]\`, crea un objeto inicialmente vacío y selecciona la vista \`Crear.cshtml\`. El navegador recibe HTML: etiquetas \`label\`, controles \`input\`, botón de envío y un campo oculto para la protección antifalsificación.

Cuando el usuario pulsa el botón, el navegador puede enviar otra petición a **la misma ruta**, esta vez con método POST:

~~~http
POST /Productos/Crear HTTP/1.1
Host: localhost:5096
Content-Type: application/x-www-form-urlencoded

Nombre=Rotulador&Precio=7
~~~

Este segundo mensaje es deliberadamente simplificado: una solicitud aceptada por la aplicación incluirá también un token antiforgery y normalmente una cookie asociada, además de otras cabeceras. El ejemplo ilustra una diferencia fundamental: los valores se transportan como **datos de una petición**, no como el nombre de un archivo \`.cshtml\` ni como parámetros de código que se ejecuta en el navegador.

El método POST no significa automáticamente «guardar en la base de datos». Indica que el navegador está enviando información al endpoint para que el servidor la procese. Qué hace después la acción es una decisión del programa. En nuestro punto 2.1 la acción solo devuelve una vista de confirmación. En 2.4 ese POST validado también creará una entidad persistente.

Para el alumnado con experiencia en Web API, esta separación resultará familiar: distintas operaciones HTTP pueden actuar sobre recursos relacionados. Aquí la novedad es que la petición procede de una **interfaz HTML Razor**, y que el resultado puede ser otra página HTML en lugar de una respuesta JSON.

## Leer el formulario real antes de construir su POST

El proyecto del curso incluye una vista \`Views/Productos/Crear.cshtml\` que podemos estudiar en términos de HTML ordinario:

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

Es importante distinguir tres responsabilidades. El elemento \`form\` declara **cómo y adónde enviar** los datos mediante \`method="post"\` y \`action="/Productos/Crear"\`. Las etiquetas \`input\` describen **qué campos** puede modificar el usuario y qué nombres se enviarán. Las expresiones Razor, por ejemplo \`@Model.Nombre\`, se evalúan **en el servidor** cuando se genera el HTML inicial. El navegador recibe una página ya procesada, no una instrucción para ejecutar C#.

La etiqueta \`name="Nombre"\` es especialmente importante: el model binder utilizará ese nombre para asociar el valor enviado con la propiedad \`Nombre\` del objeto de entrada. \`id="Nombre"\`, en cambio, identifica el control dentro del documento HTML y permite vincularlo con la etiqueta \`label for="Nombre"\`. En nuestro primer formulario ambos atributos tienen la misma cadena, pero cumplen funciones distintas.

El atributo \`type="number"\` ofrece un control apropiado para cantidades numéricas. \`step="0.01"\` facilita la introducción de precios con decimales. No debemos interpretarlo como una validación suficiente para un servidor de producción: las peticiones HTTP pueden construirse sin utilizar el formulario ni su interfaz. La validación que define qué valores aceptaremos se estudiará en 2.3.

En este primer ejemplo expresamos el valor inicial del precio usando \`CultureInfo.InvariantCulture\`. Esto evita introducir un número con coma en el atributo HTML \`value\` que espera un formato numérico compatible con el control. **No resuelve por sí solo la globalización del enlace de modelos en todos los países**: una aplicación destinada a distintos formatos regionales debe configurar y comprobar su cultura de solicitud. Para el laboratorio reproducible utilizaremos precios enteros al comprobar el transporte inicial y trataremos los límites de validación más adelante.

### El campo oculto que también envía el navegador

La vista contiene \`@Html.AntiForgeryToken()\`, que genera un elemento de entrada oculto con un valor de comprobación:

~~~html
<input name="__RequestVerificationToken" type="hidden"
       value="un-valor-generado-por-el-servidor" />
~~~

El valor mostrado es una representación didáctica; el token real no es una contraseña escrita por nosotros ni debe copiarse de este ejemplo. ASP.NET Core lo genera al producir la página. El navegador también conserva la cookie pertinente. Cuando el formulario se envía, el servidor puede verificar que la solicitud incorpora la información antiforgery que corresponde.

¿Por qué se escribe el token de forma explícita en este formulario? Porque hemos utilizado un atributo HTML \`action\` con una URL literal. Es conveniente no depender aquí de condiciones implícitas de generación del token: \`@Html.AntiForgeryToken()\` hace visible la decisión de proteger el POST. En el apartado 2.2 sustituiremos progresivamente la construcción manual por **Form Tag Helpers**, que normalmente generan ese token de manera automática cuando se utilizan como corresponde. Consulta también la [documentación oficial de Microsoft sobre antiforgery](https://learn.microsoft.com/aspnet/core/security/anti-request-forgery?view=aspnetcore-8.0).

## El controlador: dos acciones llamadas Crear

Una característica de MVC es que un controlador puede contener dos métodos C# con el mismo nombre de acción, diferenciados mediante atributos de método HTTP. En nuestro proyecto, el código GET está disponible desde el principio:

~~~csharp
[HttpGet]
public IActionResult Crear() => View(new Producto());
~~~

Al navegar a \`/Productos/Crear\`, MVC selecciona este método para GET. \`View(new Producto())\` prepara la representación de la vista \`Crear.cshtml\` con un objeto cuyo \`Nombre\` está vacío y cuyo \`Precio\` es cero. Todavía no se ha recibido ningún producto nuevo. Crear un objeto C# para presentar el formulario no equivale a guardar un registro.

El proyecto incluye también **comentada** la acción POST. El alumno la activará después de comprobar el GET y el comportamiento anterior a la existencia del POST:

~~~csharp
[HttpPost]
[ValidateAntiForgeryToken]
public IActionResult Crear(Producto producto)
{
    return View("Confirmacion", producto);
}
~~~

La presencia de \`[HttpPost]\` restringe esa acción al método POST. \`[ValidateAntiForgeryToken]\` solicita al framework comprobar el token antes de permitir que el método procese la solicitud. Finalmente, el parámetro \`Producto producto\` recibe un objeto rellenado por el model binder con los valores del formulario.

Este diseño evita una confusión muy común: la cadena \`Nombre=Rotulador\` no es código C# ni una instrucción para cambiar la propiedad directamente desde el navegador. Es texto transportado por HTTP. ASP.NET Core interpreta los campos de la solicitud y construye el objeto de entrada. La acción trabaja con ese objeto **después** de haber tenido lugar el enlace de modelos.

### Cómo actúa el enlace de modelos

Podemos narrar el recorrido sin convertirlo en una lista de mecanismos internos que el alumno deba memorizar:

1. El usuario introduce \`Nombre=Rotulador\` y \`Precio=7\` en el navegador.
2. Al enviar el formulario, el cliente crea una petición POST con esos campos y la información antiforgery.
3. MVC identifica la acción \`Crear(Producto producto)\` correspondiente al método y a la ruta.
4. El model binder toma los valores que corresponden a las propiedades del tipo \`Producto\`. Intenta convertir \`Precio\` al tipo decimal de la clase.
5. La acción ejecuta \`View("Confirmacion", producto)\`; Razor usa ese objeto para generar el HTML final.

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

El diagrama muestra responsabilidades lógicas dentro del servidor; el binder no es un servicio remoto. Es igualmente importante observar **qué no ocurre**: no hay una instrucción \`SaveChanges()\`, ningún objeto \`DbContext\` ni escritura SQL. La vista de confirmación no puede demostrar que el producto haya quedado persistido. En realidad, basta con volver al catálogo para comprobar que conserva los tres productos originales.

La clase \`Producto\` procede del módulo anterior. No necesitamos estudiar de nuevo qué significa una propiedad automática en C#. Su función aquí es ser el **destino tipado** de los valores recibidos. Más adelante distinguiremos el modelo del dominio de un modelo específico para la entrada de formulario, de modo que no tengamos que aceptar todas las propiedades de la entidad desde una solicitud externa.

## Antiforgery: por qué el POST requiere una protección adicional

Cuando un navegador conserva cookies de una aplicación, otras páginas podrían intentar inducirlo a enviar solicitudes no deseadas utilizando ese contexto. Los ataques de falsificación de solicitud entre sitios, conocidos como CSRF, aprovechan esa posibilidad. ASP.NET Core proporciona un mecanismo antiforgery basado en tokens para dificultar el envío de formularios falsificados desde contextos no autorizados.

Nuestra acción incluye \`[ValidateAntiForgeryToken]\` para que el procesamiento del POST dependa de la comprobación del token. En una navegación normal, la vista genera el campo oculto; el navegador conserva la cookie y envía ambos valores cuando corresponde. Si realizamos el POST sin el token exigido, el framework puede devolver **400 Bad Request** antes de que se ejecute el cuerpo de la acción.

**No significa que el token valide los datos del negocio.** La protección antiforgery responde a «¿está autorizada esta forma de enviar la petición desde la sesión o contexto correspondiente?», pero no a «¿es correcto el precio del producto?» ni «¿hay otro producto con ese nombre?». La segunda familia de preguntas pertenece a la validación del modelo y al dominio.

Asimismo, antiforgery no sustituye autenticación, autorización, HTTPS ni un diseño seguro de permisos. En este curso trabajamos únicamente el escenario local necesario para comprender una solicitud HTML; no construiremos un sistema de Identity desde cero.

### Lo que veremos cuando falte el POST

Antes de activar la acción \`[HttpPost]\`, el GET puede devolver correctamente el formulario y un envío POST a la misma dirección no encontrará una acción compatible. Es razonable obtener una respuesta **405 Method Not Allowed**. Esto no significa que el HTML esté mal: revela que el servidor reconoce un camino para consultar la página, pero todavía no tiene el endpoint esperado para procesar ese método.

Después de activar el POST, una solicitud de formulario correctamente construida puede terminar en 200 y representar \`Confirmacion.cshtml\`. Una solicitud sin token válido puede terminar en 400. Las dos respuestas no son contradictorias: MVC distingue ruta, método, autorización del envío y, cuando esos controles se superan, el procesamiento del cuerpo.

No confundiremos un 404 (dirección sin endpoint correspondiente), un 405 (método no admitido para ese destino) y un 400 por antiforgery. En las prácticas se presentan como observaciones de la respuesta HTTP que el alumno podrá relacionar con una causa concreta.

## Qué representa la página de confirmación

La vista \`Views/Productos/Confirmacion.cshtml\` declara el mismo tipo de modelo que la acción POST:

~~~cshtml
@model CursoWeb.Mvc.Models.Producto

<h1>Datos recibidos del formulario</h1>
<p id="producto-recibido">Nombre: <strong>@Model.Nombre</strong></p>
<p id="precio-recibido">Precio:
    <strong>@Model.Precio.ToString("0.00")</strong> €</p>
~~~

Este archivo no contiene la etiqueta \`<form>\` principal. Su responsabilidad consiste en mostrar el resultado de una operación previa. Como aprendimos en M01, **Razor genera el HTML en el servidor**. La expresión \`@Model.Nombre\` representa el dato recibido, y el motor Razor codifica como corresponde las cadenas que se insertan en HTML. Por eso debemos utilizar expresiones Razor ordinarias en lugar de concatenar HTML de procedencia desconocida y marcarlo como no codificado.

La confirmación es el lugar adecuado para un primer ejercicio de transferencia: el alumno escribirá una condición \`@if\` que presente una etiqueta adicional solamente cuando \`Model.Precio >= 4m\`. No deberá copiar la solución del catálogo de M01; tendrá que decidir dónde colocar la condición y cómo comprobarla con dos solicitudes de precios distintos.

El cambio será exclusivamente **visual**. Si un producto llega con \`Precio=7\`, la etiqueta aparecerá en el HTML de confirmación. Si llega con \`Precio=2\`, desaparecerá. El GET del formulario, la cookie y el enlace de modelos continuarán funcionando sin alteraciones. El alumno debe poder explicar por qué el lugar de ese código es la vista y no una nueva ruta.

## El primer límite: todavía no estamos validando el negocio

En este punto el modelo \`Producto\` tiene propiedades ordinarias. El atributo HTML \`type="number"\` puede ayudar a introducir valores, pero un cliente HTTP puede enviar contenido mal formado o valores que no sean apropiados para el catálogo. También es posible que una conversión falle y que el binder registre el problema en \`ModelState\`. La acción inicial simplificada todavía no consulta \`ModelState.IsValid\` y no debe utilizarse como ejemplo de formulario listo para producción.

En 2.3 construiremos un \`ProductoFormulario\` específico con \`[Required]\`, \`[StringLength]\` y \`[Range]\`, mostraremos los errores junto a los campos y evitaremos procesar una solicitud inválida. Conviene anticipar aquí la diferencia sin explicarla dos veces:

**Model binding** intenta obtener valores y convertirlos a las propiedades del parámetro de acción. **Model validation** decide si los valores representan una entrada aceptable según las reglas declaradas. **Persistencia** guarda el resultado cuando corresponde. Son operaciones relacionadas, pero no intercambiables.

Existe otra diferencia con las Web API del curso previo. Un controlador MVC que devuelve vistas no debe suponer que las respuestas 400 por validación se producen automáticamente de la misma forma que en controladores de API con \`[ApiController]\`. En los formularios MVC el patrón habitual será verificar \`ModelState.IsValid\` y devolver la misma vista con los mensajes de error para que el usuario pueda corregir los valores.

## Una manera fiable de investigar fallos de formulario

En esta jornada aprenderemos a formular preguntas técnicas antes de tocar archivos al azar. Si el formulario no aparece, comprobaremos la ruta GET, la vista \`Crear.cshtml\` y el puerto real de Kestrel. Si aparece pero al enviarlo recibimos 405, revisaremos el atributo \`[HttpPost]\` y el código activado en el controlador. Si recibimos 400, investigaremos si se ha generado y remitido correctamente el token antiforgery. Si recibimos una confirmación con el precio incorrecto, compararemos el \`name\` del campo, el tipo de la propiedad y la cultura usada al convertir el valor.

Para una misma incidencia habrá distintas fuentes de información. La página HTML permite ver los controles y la confirmación. La pestaña **Red** del navegador muestra el método y la respuesta HTTP de cada solicitud. El código fuente del controlador explica las acciones disponibles. El catálogo permite comprobar que todavía no existe persistencia. Ninguna de estas comprobaciones requiere inventar un sistema nuevo.

El método de aprendizaje será el mismo que aprobamos en M01: formular una hipótesis, cambiar una sola responsabilidad, ejecutar, observar el resultado y explicar por qué ha cambiado. Solo después avanzaremos hacia la automatización de formularios mediante Tag Helpers.

## Conexión con los puntos siguientes

El recorrido completado hasta aquí es **consulta GET → formulario Razor → POST protegido → enlace de modelos → confirmación HTML**. Hemos añadido entrada de datos al catálogo sin introducir todavía reglas de negocio ni almacenamiento. Es una evolución limitada pero real del producto anterior.

En **2.2** dejaremos de escribir manualmente cada asociación HTML y utilizaremos los Tag Helpers \`asp-for\`, \`asp-action\` y \`asp-controller\`. Esto hará más sencilla la correspondencia entre propiedades del modelo, etiquetas de los campos y destino de la solicitud.

En **2.3** aparecerá el problema de la entrada inválida y sus mensajes de error. En **2.4**, el flujo validado pasará de mostrar una confirmación a crear un producto persistido mediante EF Core, con SQL Server Express LocalDB en el laboratorio Windows. En **2.5** compararemos este patrón de controlador y vista con \`PageModel\`, \`OnGet\` y \`OnPost\` en una Razor Page mínima.

La teoría y la práctica P2.1 deben estudiarse juntas, pero no es necesario leer toda la teoría de M02 en voz alta durante la clase. La actividad esencial consiste en observar y completar un envío real; las secciones de diagnóstico ofrecen material de consulta y ampliación.

## Lecturas de referencia del punto 2.1

- Microsoft Learn, Model binding en ASP.NET Core MVC: https://learn.microsoft.com/aspnet/core/mvc/models/model-binding?view=aspnetcore-8.0
- Microsoft Learn, Protección antiforgery de solicitudes: https://learn.microsoft.com/aspnet/core/security/anti-request-forgery?view=aspnetcore-8.0
- Microsoft Learn, Tag Helpers de formularios: https://learn.microsoft.com/aspnet/core/mvc/views/working-with-forms?view=aspnetcore-8.0
- Microsoft Learn, Validación de modelos en ASP.NET Core MVC: https://learn.microsoft.com/aspnet/core/mvc/models/validation?view=aspnetcore-8.0

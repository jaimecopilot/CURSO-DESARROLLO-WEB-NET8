# M02 — Formularios, validación y Razor Pages en ASP.NET Core MVC
## Cuaderno de prácticas

**CURSO: Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8**

**TIPO: PRÁCTICAS**

**AUTOR: JAIME GALLO**

## Cómo trabajar con este cuaderno

En M01 el alumnado construyó un catálogo que responde a peticiones HTTP, utiliza rutas MVC, obtiene productos en un controlador y los muestra mediante vistas Razor y un layout. Durante M02 el problema cambia: el navegador debe poder enviar datos al servidor, recibir mensajes de validación y, finalmente, crear, editar y eliminar productos que se conservan en SQL Server Express LocalDB. La comparación final con Razor Pages mostrará otra manera de organizar la misma idea de entrada y salida, sin desarrollar una aplicación empresarial adicional.

El **recorrido obligatorio** se ajusta a las seis horas del segundo día. Las secciones de investigación, las aplicaciones autónomas y los retos son material de profundización que puede realizarse después de las demostraciones. No es necesario leer el manual entero en voz alta. Debe preservarse la relación entre cada modificación, el archivo que se cambia y la respuesta observable.

La organización consta de cinco prácticas: **P2.1**, HTML, GET, POST, model binding y antiforgery; **P2.2**, Tag Helpers de formularios; **P2.3**, DataAnnotations y ModelState; **P2.4**, CRUD con EF Core y LocalDB; **P2.5**, una Razor Page mínima. Cada punto utiliza una instantánea del proyecto situada en PROYECTO/2.x/CursoWeb.Mvc. Los proyectos de M01 no se modifican. Los estados de los ejercicios principales se conservan entre instantáneas; las variantes opcionales no tienen por qué venir activadas en las siguientes.

El trabajo del alumno distingue tres acciones: **observar** código ya activo para comprender su efecto; **activar** un bloque preparado y comentado que forma parte de un paso; y **escribir** una solución propia, sin disponer de su resultado ya implantado. Después de cada paso, hay que identificar la entrada, el componente responsable y la evidencia de salida. Las soluciones del manual se consultan solamente tras haber intentado resolver el enunciado.

## Índice

- P2.1. El formulario HTML, el método HTTP, model binding y antiforgery.
- P2.2. Tag Helpers para campos, formularios y navegación.
- P2.3. Validación con DataAnnotations y ModelState.
- P2.4. Operaciones CRUD persistentes con EF Core y SQL Server Express LocalDB.
- P2.5. Una Razor Page: PageModel, OnGet y OnPost.

# P2.1. Mostrar un formulario y recibir sus datos con MVC

## Objetivo y punto de partida

**Objetivo.** Comprender una interacción completa de formulario: GET para mostrar controles, POST para enviar los campos, construcción de un objeto de entrada mediante model binding y respuesta HTML generada por una vista de confirmación. Observar, además, por qué un POST sin token antiforgery debe ser rechazado. La práctica **no añade persistencia**: el catálogo inicial sigue mostrando tres productos.

**Teoría relacionada:** capítulo 2.1 del manual teórico de M02. Conviene estudiar primero la diferencia entre método, ruta, campos enviados y datos del modelo. No hace falta aprender EF Core otra vez para esta actividad.

**Proyecto a abrir:** M02_FORMULARIOS_RAZOR/PROYECTO/2.1/CursoWeb.Mvc/CursoWeb.Mvc.csproj. Trabajaremos con Visual Studio y .NET 8 en Windows, aunque los ejemplos de compilación y navegación también pueden comprenderse con una terminal. No es necesario tener instalado LocalDB hasta P2.4.

Desde la raíz del repositorio, ejecuta:

~~~bash
cd M02_FORMULARIOS_RAZOR/PROYECTO/2.1/CursoWeb.Mvc
dotnet restore
dotnet build
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

Si Visual Studio inicia la aplicación por otro puerto, utiliza la dirección que muestra su consola o el perfil de ejecución. Para seguir los comandos exactamente, el ejemplo de este cuaderno utiliza el puerto 5091. Detén cualquier instancia anterior de MVC que siga usando esa dirección.

### Mapa de trabajo de P2.1

| Paso | Archivo | Acción del alumno | Evidencia observable |
|---|---|---|---|
| 2.1.1 | Controllers/ProductosController.cs y Views/Productos/Index.cshtml | Observar la aplicación heredada | GET /Productos muestra tres productos |
| 2.1.2 | Views/Productos/Crear.cshtml | Analizar el formulario entregado y sus campos | GET /Productos/Crear devuelve 200 y el formulario HTML |
| 2.1.3 | Controllers/ProductosController.cs | Activar POST en el bloque PASO 2.1.3 | Una petición protegida representa Confirmacion.cshtml |
| 2.1.4 | Crear.cshtml y acción POST | Comparar el envío normal con uno sin token | La solicitud sin token obtiene 400 |
| 2.1.5 | Views/Productos/Confirmacion.cshtml | Escribir una condición Razor propia | Mostrar aviso solo si el precio es al menos 4 |
| Reto 2.1 | Confirmacion.cshtml | Activar y razonar una condición de longitud | Aviso solo si Nombre supera ocho caracteres |

No ejecutes P2.2 sobre este proyecto: abre su instantánea cuando hayas terminado de comprender el resultado del POST.

## Paso 2.1.1 — Confirmar que conservamos la aplicación del módulo anterior

Abre http://localhost:5091/ y comprueba que aparece la portada conocida. Visita después http://localhost:5091/Productos y verifica los nombres Cuaderno, Lápiz y Carpeta, con precios. Finalmente, abre http://localhost:5091/Productos/Detalle/2: la ficha debe mostrar Lápiz e identificador 2. No estamos reconstruyendo desde cero las vistas ni el enrutamiento del M01; partimos de una aplicación MVC navegable.

Abre el archivo Controllers/ProductosController.cs. Localiza ObtenerProductosEjemplo() y observa cómo se construye una lista fija de tres objetos. Compara ese método con Index(): la acción de catálogo solicita los productos y se los entrega a la vista. El navegador no accede directamente a la colección C# ni conoce cómo se creó.

**Pregunta antes de cambiar código:** ¿si más adelante una acción POST recibe un producto y devuelve su nombre en otra vista, eso hará que aparezca automáticamente como cuarto elemento en la lista? No. Recibir y presentar un objeto no lo incorpora a ObtenerProductosEjemplo(). Tampoco lo inserta en SQL Server. La persistencia será un paso diferente y explícito en P2.4.

Para comprobar el estado HTTP sin depender del estilo visual, puedes usar otra terminal:

~~~bash
curl -i http://localhost:5091/Productos
curl -i http://localhost:5091/Productos/Detalle/2
~~~

Confronta el resultado con lo que ves en el navegador. Una página bien renderizada no implica que se haya ejecutado una operación de escritura; de momento todas estas solicitudes son GET.

## Paso 2.1.2 — Mostrar el formulario con GET

En ProductosController.cs localiza el método que prepara la nueva vista:

~~~csharp
[HttpGet]
public IActionResult Crear() => View(new Producto());
~~~

Este método no recibe los datos del formulario. Su responsabilidad es **crear un modelo inicial para la página**. Un objeto Producto nuevo tendrá Nombre vacío y Precio igual a cero. Ese objeto se entrega al archivo Views/Productos/Crear.cshtml, el cual comienza declarando que trabaja con un único Producto mediante @model.

Abre Crear.cshtml y examina sus controles:

~~~cshtml
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

Estudia la diferencia entre las propiedades del formulario. method="post" indica el método de la siguiente petición, no el de la solicitud que está representando ahora esta vista. action="/Productos/Crear" define adónde se enviará esa petición. name="Nombre" y name="Precio" son las claves que viajarán en el cuerpo de datos. El binder las buscará para asignarlas a las propiedades del objeto C#.

Por su parte, el atributo id identifica un elemento en el documento HTML; una etiqueta label puede referirse a él mediante for. En este ejemplo el id y el name utilizan cadenas iguales, pero no debemos confundir la asociación de etiquetas HTML con el enlace de datos del servidor. Las expresiones @Model.Nombre y @Model.Precio ya se habrán evaluado antes de que el navegador reciba la respuesta.

Abre http://localhost:5091/Productos/Crear y comprueba la existencia de dos campos y del botón Enviar producto. En las herramientas de desarrollo (F12), selecciona Red e inspecciona la solicitud del documento: es **GET**, y el resultado esperado es **200**. Desde la pestaña Elementos busca el formulario y localiza un campo oculto con name="__RequestVerificationToken". Su valor lo genera ASP.NET Core; no lo copies ni lo utilices como texto fijo en el material.

### Experimento negativo antes de activar el POST

Escribe Nombre = Rotulador y Precio = 7, pulsa Enviar y anota el método de la nueva petición. En este estado del proyecto, la acción POST sigue comentada. Por tanto, GET está disponible, pero POST no debe procesar el formulario: es esperable **405 Method Not Allowed**.

Explica por qué no se trata de una página HTML inexistente: has obtenido el formulario con GET hace un momento. Lo que falta es una acción seleccionable para este **otro método HTTP**. Si la confirmación aparece ya en este paso, revisa que estás abriendo la carpeta 2.1 y que no has activado el POST en una ejecución anterior.

Detén Kestrel antes de editar los comentarios del controlador.

## Paso 2.1.3 — Activar el POST y examinar el model binding

En Controllers/ProductosController.cs localiza el bloque que empieza con **PASO 2.1.3 INICIO** y termina en **PASO 2.1.3 FIN**. Está dentro de un comentario C#. Elimina únicamente las marcas de apertura y cierre del comentario para que la acción se compile. Debes conservar ambos atributos:

~~~csharp
[HttpPost]
[ValidateAntiForgeryToken]
public IActionResult Crear(Producto producto)
{
    return View("Confirmacion", producto);
}
~~~

**No añadas instrucciones de persistencia**, ni cambies la lista de productos, ni retires la protección antiforgery. El bloque de código preparado contiene comentarios que explican el papel del binder: no son instrucciones para guardarlo todo en la base de datos.

Contrasta las dos acciones. Crear() GET no tiene parámetros y devuelve la vista del formulario con un objeto vacío. Crear(Producto producto) POST recibe un objeto cuyos valores provienen de los campos enviados por el navegador y devuelve la vista Confirmacion.cshtml. El framework elige la acción a partir de la ruta y el método HTTP; no está ejecutando dos métodos arbitrarios por el mero hecho de llamarse Crear.

**Predicción:** cuando el navegador envía Nombre=Rotulador y Precio=7 con un token válido, la segunda acción recibe un Producto con esos valores. Su Id sigue siendo cero, porque ese campo no se envía en el formulario. El binder construye un objeto, pero nadie lo guarda ni calcula un nuevo identificador de base de datos.

Compila de nuevo, ejecuta la aplicación y vuelve a cargar el formulario. Introduce Nombre = Rotulador y Precio = 7. Pulsa Enviar. Debe abrirse la página de confirmación con un encabezado Datos recibidos del formulario. Comprueba en su HTML que aparece el nombre Rotulador y el precio 7,00 o 7.00 según la cultura de presentación configurada.

Localiza Views/Productos/Confirmacion.cshtml. La vista recibe un único Producto y presenta sus propiedades mediante expresiones Razor. El resultado confirma que el binder obtuvo datos y que MVC los entregó a la vista. **No demuestra** que exista un cuarto producto en el catálogo. Regresa a /Productos y comprueba que la lista sigue mostrando exactamente Cuaderno, Lápiz y Carpeta.

## Paso 2.1.4 — Comparar el POST legítimo con uno sin antiforgery

La vista Crear contiene @Html.AntiForgeryToken(), que inserta un campo oculto. El controlador utiliza [ValidateAntiForgeryToken], que exige comprobar el token al recibir la petición. Ambas partes intervienen en una misma protección. El token no es una regla que determine si el nombre o el precio son apropiados para el negocio; esa validación será el objeto de P2.3.

**Primera observación, envío correcto:** abre de nuevo /Productos/Crear y envía Nombre=Carpeta grande y Precio=9. En F12 → Red selecciona la petición POST y observa sus campos: Nombre, Precio y __RequestVerificationToken. Puedes inspeccionar la presencia del campo sin publicar su valor en un documento. La acción debe responder con la confirmación HTML cuando el envío es válido.

**Segunda observación, solicitud sin token:** desde otra terminal realiza un POST directo sin haber obtenido ni enviado el token. En PowerShell, escribe:

~~~powershell
curl.exe -i -X POST http://localhost:5091/Productos/Crear --data "Nombre=Rotulador&Precio=7"
~~~

El resultado esperado es **400 Bad Request** porque la acción requiere la validación antiforgery. No intentes obtener un 200 eliminando [ValidateAntiForgeryToken]; eso destruiría el sentido del experimento. Comprueba que el fallo se produce **antes** de procesar la operación del cuerpo.

| Situación | Estado previsto | Qué debes concluir |
|---|---|---|
| GET /Productos/Crear | 200 | La ruta y la vista del formulario funcionan |
| POST antes de habilitar la acción | Normalmente 405 | Falta el destino para el método POST |
| POST después de habilitar la acción pero sin token | 400 | La protección antiforgery impide procesar el envío |
| POST desde el formulario normal con token válido | 200 | Antiforgery, binder, controlador y vista intervienen correctamente |

Si observas un 404, comprueba la ruta y el puerto. Si el POST sin token consigue un 200, confirma que mantienes el atributo del controlador y no estás enviando datos a otro endpoint. Si el POST desde el navegador obtiene 400, revisa la presencia del campo oculto, las cookies correspondientes y cualquier alteración del formulario. No supongas que todos los errores de entrada proceden del model binding.

### Análisis: las responsabilidades permanecen separadas

Dibuja en papel la secuencia navegador → HTTP POST → antiforgery → model binding → acción Crear(Producto) → View(Confirmacion, producto) → HTML. Aclara que antiforgery y model binding son mecanismos del servidor ASP.NET Core, no servidores HTTP independientes. Identifica qué dato se transmite y en qué momento queda disponible como una propiedad decimal.

Explica también por qué esta acción es distinta de una Web API: hemos recibido campos de un formulario HTML y respondido con una vista Razor. Los conceptos HTTP fundamentales siguen siendo los mismos, pero la representación de salida es un documento HTML generado en el servidor.

## Paso 2.1.5 — Aplicación autónoma: escribir Razor según un dato recibido

Hasta aquí has observado y activado bloques preparados. En este paso tendrás que **escribir** código propio. Abre Views/Productos/Confirmacion.cshtml y localiza el comentario **APLICACION 2.1.5**. Sustitúyelo por un condicional Razor con @if que muestre un elemento:

~~~html
<strong id="precio-elevado">Importe elevado para el ejemplo</strong>
~~~

Ese elemento debe aparecer solamente cuando **Model.Precio >= 4m**. La letra m denota un literal decimal de C#, coherente con el tipo de la propiedad Precio. No cambies el controlador ni el modelo. El cambio solicitado es una regla de presentación que pertenece a la vista de confirmación.

Prueba dos entradas por separado. Envía primero Rotulador con precio 7 y verifica que aparece el texto de aviso. Regresa a Crear y envía Goma con precio 2: el elemento debe desaparecer. Una implementación que introduce la etiqueta sin condición pasaría la primera comprobación pero fallaría la segunda. Por eso hay que examinar tanto el caso positivo como el negativo.

Si el HTML no cambia, recuerda que un comentario Razor @* ... *@ no se representa en el documento. Asegúrate de haber escrito el bloque fuera del comentario. Si aparece siempre, comprueba dónde abriste y cerraste las llaves del @if. Si aparece nunca, revisa qué vista ejecuta la acción POST y cuál es el precio recibido.

Esta actividad no valida ningún precio real de negocio ni cambia la colección de productos. Su objetivo es poner en relación **la entrada de datos por POST** con **la presentación Razor** que ya conoces desde M01.

### Solución de referencia, solo después de intentar el ejercicio

~~~cshtml
@if (Model.Precio >= 4m)
{
    <strong id="precio-elevado">Importe elevado para el ejemplo</strong>
}
~~~

La vista evalúa la expresión cada vez que MVC representa una respuesta de confirmación. No hay una variable JavaScript ni un enlace a una nueva acción: la condición se ejecuta en el servidor.

## Reto 2.1 — Un segundo criterio visual independiente

El archivo Confirmacion.cshtml contiene un bloque marcado **RETO 2.1 INICIO / RETO 2.1 FIN**. En esta ocasión se entrega el código comentado y el alumno debe activarlo después de comprenderlo. El objetivo es mostrar el aviso nombre-extenso cuando la longitud del nombre recibido **supere ocho caracteres**.

Predice antes de ejecutarlo qué debe ocurrir si Nombre tiene exactamente ocho caracteres, nueve caracteres o está vacío. La condición preparada comprueba primero que el texto no sea nulo ni espacios en blanco y luego compara su longitud; ese orden evita consultar Length sobre un valor nulo.

Activa el bloque quitando sus delimitadores de comentario. Envía Rotulador, cuyo nombre supera ocho caracteres, y después Goma, que no los supera. Comprueba la aparición y ausencia de la etiqueta respectivamente.

~~~cshtml
@if (!string.IsNullOrWhiteSpace(Model.Nombre) && Model.Nombre.Length > 8)
{
    <p id="nombre-extenso">El nombre tiene más de ocho caracteres.</p>
}
~~~

El operador && utiliza evaluación de cortocircuito: la segunda condición solo se evalúa cuando la primera lo permite. El ejercicio no impide que lleguen nombres vacíos al servidor: solamente controla qué se dibuja en esta vista. En P2.3 estudiaremos cómo rechazar realmente entradas inválidas.

Si realizaste también la aplicación autónoma anterior, envía un nombre largo con precio 7 y otro corto con precio 2. Deben aparecer los avisos correspondientes sin afectar a los otros. La coexistencia de dos condiciones distintas sobre un mismo modelo demuestra que la vista puede presentar varias propiedades sin duplicar acciones del controlador.

## Diagnóstico aplicado y transferencia a P2.2

**Caso A: la vista Crear aparece, pero no se llega a Confirmación.** Observa el estado HTTP. Un 405 indica que conviene revisar la acción POST; un 400 puede señalar antiforgery; un 500 requiere consultar la excepción de la aplicación. No «corrijas» todos esos casos modificando los campos de HTML sin examinar primero la respuesta.

**Caso B: el nombre se representa correctamente pero el precio es incorrecto.** Comprueba el campo name="Precio", el valor enviado realmente por el navegador y la propiedad decimal del objeto. Si la entrada falla por cultura o por un formato incompatible, no alteres de manera arbitraria el valor de la entidad. La explicación completa de validación y conversión pertenece a P2.3.

**Caso C: se ve una confirmación correcta pero al volver al catálogo no aparece el producto nuevo.** Ese es precisamente el estado de P2.1: la acción devuelve View("Confirmacion", producto) y no guarda ni modifica la colección. Describe qué operaciones serán necesarias en P2.4: obtener DbContext, añadir entidad, guardar los cambios y volver a consultar el catálogo.

**Caso D: el botón funciona solo cuando se quita el atributo ValidateAntiForgeryToken.** La «solución» está debilitando el mecanismo de protección y por tanto no es una solución. Hay que examinar cómo se genera el campo oculto y se conserva la cookie antiforgery.

La meta de P2.1 es poder explicar el recorrido entero sin confundir entrada HTTP, enlace de modelos, selección de la acción, protección antiforgery y presentación Razor. En **P2.2** sustituiremos progresivamente atributos escritos a mano por Tag Helpers (asp-for, asp-action, asp-controller). Conservaremos el mismo formulario conceptual antes de estudiar la validación en P2.3 y la persistencia con LocalDB en P2.4.

**Estado final del recorrido esencial:** GET representa el formulario, POST protegido recibe Nombre y Precio y muestra una confirmación. El catálogo todavía contiene tres productos. Ese resultado es correcto y prepara la siguiente práctica.

# P2.2. Tag Helpers: construir formularios y enlaces sin duplicar cadenas de rutas

## Qué vamos a conseguir y cómo se relaciona con P2.1

La primera práctica del módulo demostró que una vista podía ofrecer un formulario GET, enviar sus campos con POST y presentar el objeto recibido en una página de confirmación. También comprobamos que una solicitud POST sin el token antiforgery válido debe rechazarse. Ahora **mantendremos exactamente ese recorrido funcional** y cambiaremos la manera de escribir sus elementos Razor, introduciendo progresivamente los Tag Helpers de ASP.NET Core MVC.

Esta decisión es deliberada. Cuando se aprende una técnica nueva, cambiar a la vez el modelo, la acción, las rutas, el HTML y la base de datos dificulta identificar por qué algo funciona o falla. En este punto el único componente que vamos a transformar es la **vista**. Conservaremos la misma acción `ProductosController.Crear` y los mismos campos `Nombre` y `Precio`; todavía no guardaremos registros en SQL Server.

**Objetivos concretos:** reconocer el papel de `_ViewImports.cshtml`; sustituir un `form` HTML por un Form Tag Helper; generar las asociaciones de `label` e `input` mediante `asp-for`; utilizar Anchor Tag Helpers para la navegación; comprobar que el token antiforgery y el model binding siguen funcionando; y aplicar las mismas ideas a enlaces de detalle cuyo identificador proviene de un objeto del catálogo.

**Teoría relacionada:** apartado 2.2 del manual teórico del M02, especialmente la distinción entre CSHTML y HTML final, los Tag Helpers incorporados, los atributos generados y el diagnóstico de problemas de enrutamiento.

**Proyecto que debes abrir:** `M02_FORMULARIOS_RAZOR/PROYECTO/2.2/CursoWeb.Mvc/CursoWeb.Mvc.csproj`. Es una instantánea del recorrido central de P2.1; la acción POST ya está activa. No hay que copiar a mano los cambios de otras carpetas ni modificar el M01 aprobado.

El recorrido esencial se compone de los pasos **2.2.1 a 2.2.5**. La aplicación autónoma y el reto final permiten practicar el razonamiento sin consumir tiempo del resto de la jornada. Todas las comprobaciones están planteadas para que el alumno pueda realizarlas desde el navegador y Visual Studio, sin ejecutar controles internos del repositorio.

### Preparar el entorno

Desde la raíz del repositorio puedes iniciar la aplicación con estos comandos:

~~~bash
cd M02_FORMULARIOS_RAZOR/PROYECTO/2.2/CursoWeb.Mvc
dotnet restore
dotnet build
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

Si existe otro proyecto ejecutándose en el mismo puerto, detenlo antes. Si trabajas desde el perfil de Visual Studio, utiliza la dirección que muestre el navegador o la consola de ejecución. Para que las comprobaciones sean reproducibles, los ejemplos siguientes usan `http://localhost:5091`.

Comprueba primero tres direcciones: `/`, `/Productos` y `/Productos/Crear`. La portada, el catálogo y el formulario deben abrirse. Envía **Nombre = Rotulador, Precio = 7** y verifica que la confirmación muestra los datos, sin añadir un cuarto producto al catálogo. Ese comportamiento es la **línea base** que no debemos alterar.

### Mapa de pasos, archivos y comprobaciones

| Paso | Archivo del proyecto | Trabajo y resultado esperado |
|---|---|---|
| 2.2.1 | `Views/_ViewImports.cshtml` y `Views/Productos/Crear.cshtml` | **Observar.** Identificar dónde se habilitan los Tag Helpers y cómo queda el HTML original |
| 2.2.2 | `Views/Productos/Crear.cshtml` | **Sustituir** la apertura del formulario y retirar el token manual. Conservar un token generado automáticamente |
| 2.2.3 | `Views/Productos/Crear.cshtml` | **Sustituir** los dos `label`. Verificar `for` para Nombre y Precio |
| 2.2.4 | `Views/Productos/Crear.cshtml` | **Sustituir** los dos `input`. Verificar `name`, `id`, `type` y envío de datos |
| 2.2.5 | `Views/Productos/Crear.cshtml` | **Sustituir** el enlace de regreso al catálogo. Comprobar su `href` |
| Aplicación autónoma 2.2.6 | `Views/Shared/_TarjetaProducto.cshtml` | **Escribir** un Anchor Tag Helper para el producto de la tarjeta |
| Reto 2.2 | `Views/Productos/Index.cshtml` | **Activar y explicar** tres enlaces dinámicos con `asp-route-id` |

Los comentarios del proyecto contienen los identificadores exactos `PASO 2.2.2` a `PASO 2.2.5`, `APLICACION 2.2.6` y `RETO 2.2`. En los pasos guiados se presenta una alternativa comentada: el alumno debe **sustituir el elemento original**, no añadir otra copia al lado.

## Paso 2.2.1 — Observar cómo Razor transforma el marcado

Abre `Views/_ViewImports.cshtml` y encuentra estas líneas:

~~~cshtml
@using CursoWeb.Mvc
@addTagHelper *, Microsoft.AspNetCore.Mvc.TagHelpers
~~~

La segunda directiva hace disponibles los Tag Helpers integrados en el ámbito de las vistas. El archivo `Crear.cshtml` se encuentra debajo de `Views/Productos`, por lo que puede utilizarlos. Esta directiva no establece una ruta HTTP ni añade una acción al controlador; interviene cuando Razor procesa los elementos del archivo CSHTML.

En `Views/Productos/Crear.cshtml` localiza la apertura del formulario original:

~~~cshtml
<form method="post" action="/Productos/Crear">
    @Html.AntiForgeryToken()
~~~

Aquí `method` y `action` son atributos HTML ordinarios. La llamada `Html.AntiForgeryToken()`, en cambio, es un HTML Helper ejecutado por Razor en el servidor. El navegador no ejecuta ese método C#: recibe su **resultado**, que incluye un elemento oculto.

Abre `/Productos/Crear` y utiliza F12 → **Elementos** para encontrar la etiqueta `form`. Identifica su `action`, su `method` y el campo oculto con `name="__RequestVerificationToken"`. Localiza también los controles Nombre y Precio. No copies el valor real del token en el material de clase ni lo confundas con un dato permanente.

**Predicción previa:** ¿qué cambiará en la pantalla al utilizar Form Tag Helper? Posiblemente nada. Nuestro objetivo no es rediseñar la interfaz. Esperamos que el servidor genere un HTML funcionalmente equivalente, pero que el código Razor describa el destino por su controlador y su acción.

Una segunda predicción es más importante: si algún atributo `asp-controller` apareciera literalmente en el HTML final, ¿qué significaría? Que el Tag Helper no habría intervenido como esperamos. La primera comprobación sería el ámbito de `_ViewImports.cshtml` y la forma de escribir el elemento, no modificar al azar `ProductosController`.

## Paso 2.2.2 — Form Tag Helper y continuidad de antiforgery

En `Crear.cshtml` busca **PASO 2.2.2**. Sustituye la apertura del formulario por:

~~~cshtml
<form asp-controller="Productos" asp-action="Crear" method="post">
~~~

**Retira también** la línea `@Html.AntiForgeryToken()`, que se utilizaba en el formulario HTML manual. Con Form Tag Helper integrado y el método POST, ASP.NET Core genera la entrada antiforgery correspondiente. La protección no debe desaparecer: ahora la genera otro mecanismo.

Este ejercicio exige precisión: se sustituye una apertura de formulario, se mantiene el contenido interior y se conserva exactamente un cierre `</form>`. No es correcto acabar con dos formularios ni con dos tokens generados por mecanismos distintos.

Detén la aplicación, compila y ejecútala otra vez. Abre `/Productos/Crear` y examina el HTML desde las herramientas de desarrollo. Comprueba que la etiqueta final tiene un `action` relacionado con `/Productos/Crear`, un `method="post"` y **un campo oculto** `__RequestVerificationToken`. Los atributos especiales `asp-controller` y `asp-action` no deberían aparecer sin procesar en el documento final.

Envía **Rotulador, 7**. La confirmación debe aparecer como antes; el controlador no ha cambiado. Después repite la prueba negativa enviando un POST sin token desde PowerShell:

~~~powershell
curl.exe -i -X POST http://localhost:5091/Productos/Crear --data "Nombre=Rotulador&Precio=7"
~~~

El servidor debe devolver **400 Bad Request** porque la acción mantiene `[ValidateAntiForgeryToken]`. Si una petición del formulario real devuelve 200 y otra sin token obtiene 400, acabamos de demostrar que el cambio de sintaxis no ha eliminado la protección.

### Diagnóstico de un formulario que dejó de enviar

Un error habitual consiste en quitar `Html.AntiForgeryToken()` pero dejar activo el formulario original sin el nuevo Form Tag Helper. En ese caso falta la generación del campo oculto, y es razonable que la acción protegida rechace el envío normal. Para diagnosticarlo, comprueba primero el HTML recibido por el navegador y después los campos efectivamente transmitidos en F12 → Red.

**No resuelvas un 400 quitando `[ValidateAntiForgeryToken]`.** Eso desactivaría una protección y ocultaría la causa. Tampoco confundas un 405 con un 400: el primero puede indicar que no existe una acción POST compatible, mientras que el segundo puede proceder de antiforgery. Son hipótesis distintas que se verifican mirando las solicitudes y el código.

## Paso 2.2.3 — Label Tag Helper y asociaciones accesibles

Localiza ambos comentarios **PASO 2.2.3** en `Crear.cshtml`. Sustituye los dos elementos `label` por:

~~~cshtml
<label asp-for="Nombre"></label>
<label asp-for="Precio"></label>
~~~

Cada uno debe permanecer junto a su campo. **Todavía no cambies los inputs**, porque queremos observar el efecto del Label Tag Helper de forma aislada.

Después de compilar, inspecciona las etiquetas generadas. Deben producir asociaciones como `for="Nombre"` y `for="Precio"`. Compara esos valores con los `id` existentes en los inputs. Si la asociación es correcta, seleccionar el texto de la etiqueta enfoca el campo correspondiente. Esa relación también aporta información a las tecnologías de asistencia.

La propiedad `Nombre` del modelo no se convierte en una variable JavaScript por usar `asp-for`. El Tag Helper utiliza los metadatos de la vista tipada durante el renderizado. Los campos del formulario siguen enviándose con las mismas claves, y la acción del controlador continúa siendo la misma.

En P2.3 estudiaremos cómo utilizar atributos como `[Display]`, `[Required]` y `[StringLength]` para describir los datos que queremos aceptar. Aquí no necesitamos adelantar esas reglas: basta con comprender **cómo se vincula una etiqueta con una propiedad del modelo**.

## Paso 2.2.4 — Input Tag Helper y contrato de model binding

Busca los dos comentarios **PASO 2.2.4** y reemplaza los inputs originales por sus alternativas:

~~~cshtml
<input asp-for="Nombre" />
<input asp-for="Precio" type="number" step="0.01" />
~~~

No dejes los controles originales junto a los nuevos. Eso podría introducir dos entradas con el mismo `name` y dificultar la interpretación de lo que el navegador envía.

Compila y abre nuevamente el formulario. El resultado HTML debe contener los atributos `name` e `id` apropiados para `Nombre` y `Precio`. El campo Precio conserva el control numérico y el paso de centésimas que hemos indicado explícitamente. El atributo `asp-for` no debe aparecer como parte de la representación HTML final.

Envía primero **Rotulador, 7**. Comprueba que la acción POST recibe el dato y que la vista Confirmacion lo representa. Regresa al catálogo: los tres productos iniciales deben seguir existiendo y no debe haber un producto «Rotulador» añadido automáticamente.

Esta observación demuestra dos ideas complementarias. Por una parte, el Input Tag Helper ha generado los nombres necesarios para el enlace de modelos. Por otra, **nada de esto ha implementado persistencia** ni validación completa. `type="number"` es una indicación útil para la interfaz del navegador; las reglas de aceptación de datos en el servidor serán responsabilidad de P2.3.

### Investigar un precio que no llega correctamente

Si el POST funciona pero el precio recibido no coincide con lo escrito, no modifiques a ciegas el controlador. Comprueba el `name` generado, el valor transmitido en F12 → Red y la cultura utilizada para la conversión. Para el recorrido básico utilizamos un precio entero, 7, precisamente para no añadir el problema independiente de los separadores decimales de distintas culturas.

El hecho de utilizar un Input Tag Helper no transforma un campo inválido en un dato correcto. El model binder puede encontrar problemas de conversión, y la acción debería comprobar `ModelState` cuando se incorporen las reglas de P2.3. **No presentes P2.2 como un formulario de producción plenamente validado**.

## Paso 2.2.5 — Anchor Tag Helper para volver al catálogo

En `Crear.cshtml`, sustituye el enlace original por la alternativa del comentario **PASO 2.2.5**:

~~~cshtml
<p><a asp-controller="Productos" asp-action="Index">Volver al catálogo</a></p>
~~~

Inspecciona el HTML generado. El navegador debe recibir un elemento `a` con un `href` adecuado para la lista `/Productos`. Haz clic y comprueba que recuperas el catálogo.

Reflexiona sobre un posible malentendido: tanto la etiqueta `form` como la etiqueta `a` pueden utilizar `asp-action`, pero **no hacen la misma operación**. El formulario se envía con el método indicado, POST en nuestro caso. Un enlace ordinario inicia una nueva navegación GET cuando el usuario lo selecciona.

Con ello queda completado el itinerario esencial de P2.2. El alumno ha mantenido el mismo contrato HTTP y ha mejorado la relación entre el HTML de la vista, las propiedades del modelo y las acciones MVC. Antes de pasar a la ampliación, verifica conjuntamente los elementos principales: el `form` tiene destino correcto, el token existe una vez, las etiquetas están asociadas con los campos, el POST protegido funciona y el enlace regresa al catálogo.

## Aplicación autónoma 2.2.6 — Escribir un enlace dentro de una parcial compartida

El siguiente ejercicio **exige escribir código**, no activar una solución preparada. En `Views/Shared/_TarjetaProducto.cshtml` encontrarás el comentario **APLICACION 2.2.6**, junto al enlace que actualmente utiliza una URL escrita a mano:

~~~cshtml
<a href="/Productos/Detalle/@Model.Id">Ver detalle de @Model.Nombre</a>
~~~

Debes sustituirlo por un Anchor Tag Helper propio que indique `Productos` como controlador, `Detalle` como acción y suministre el identificador de `Model.Id` mediante `asp-route-id`. Conserva el texto «Ver detalle de» y el nombre del producto.

**Predice antes de ejecutar:** la parcial es reutilizada por el catálogo de tarjetas y por la ficha individual. Por tanto, modificar **un solo archivo** debe afectar a los enlaces que se generan en ambos lugares. La prueba no consiste únicamente en que el enlace se vea subrayado; hay que comprobar que conduce a la ficha del producto correcto.

Abre `/Productos`, inspecciona la primera tarjeta y comprueba que su enlace conduce a la ficha del producto 1. Repite con las tarjetas 2 y 3. Después abre `/Productos/Detalle/2` y comprueba que la tarjeta insertada en esa página sigue enlazando al detalle de Lápiz.

No introduzcas un enlace fijo con identificador 2 dentro de la parcial. La misma vista se utiliza para varios objetos y la ruta debe depender de `Model.Id`.

### Solución de referencia, solo después de intentarlo

~~~cshtml
<a asp-controller="Productos"
   asp-action="Detalle"
   asp-route-id="@Model.Id">Ver detalle de @Model.Nombre</a>
~~~

El resultado que debe llegar al navegador es un enlace HTML con un `href` generado a partir de la configuración de routing de MVC. `asp-route-id` suministra el valor del parámetro de ruta denominado `id`; no es un atributo HTML estándar ni guarda información en la base de datos.

## Reto 2.2 — Enlaces dinámicos en el listado principal

En `Views/Productos/Index.cshtml` localiza **RETO 2.2**. El archivo contiene un enlace literal dentro del bucle `foreach`, y una alternativa comentada para reemplazarlo. El reto consiste en activar la alternativa y retirar el enlace anterior.

La alternativa debe expresar el controlador Productos, la acción Detalle y el valor de ruta `id` tomado de `producto.Id`. Como el catálogo tiene tres objetos con identificadores distintos, deben generarse **tres enlaces diferentes**.

~~~cshtml
<a class="enlace-detalle"
   asp-controller="Productos"
   asp-action="Detalle"
   asp-route-id="@producto.Id">Ver detalle</a>
~~~

Después de editar, cuenta los enlaces «Ver detalle» dentro del listado: debe existir exactamente uno por elemento. Si aparecen dos por producto, has añadido el nuevo sin retirar el anterior. Si los tres enlazan a la misma ficha, revisa que hayas usado `producto.Id` dentro del bucle en lugar de un número constante.

Navega a cada ficha desde el listado y comprueba que los identificadores, nombres y precios corresponden a Cuaderno, Lápiz y Carpeta. Regresa después al formulario de creación y comprueba que aún admite el POST protegido. Esas comprobaciones muestran que el nuevo uso de Anchor Tag Helpers no ha roto la funcionalidad que ya conocíamos.

## Diagnóstico final y continuidad hacia P2.3

Cuando una página se ve correctamente pero un formulario deja de funcionar, conviene dividir el problema por responsabilidades. Si el botón de envío devuelve 405, inspecciona la ruta y la acción POST disponible. Si devuelve 400, busca el token y su cookie antes de cambiar reglas del modelo. Si devuelve una confirmación con campos vacíos, investiga los atributos `name` generados. Si el enlace al catálogo no funciona, inspecciona el `href` final y su ruta.

Estas comprobaciones no requieren modificar cuatro archivos simultáneamente. La propia progresión de P2.2 —formulario, labels, inputs y enlaces— ayuda a identificar cuál de las transformaciones introdujo un resultado inesperado.

**Resultado de aprendizaje:** sabemos generar formularios y enlaces mediante las capacidades integradas de MVC, pero aún no hemos definido qué datos debe aceptar el servidor. En **P2.3** crearemos un modelo de entrada específico, declararemos reglas mediante DataAnnotations y utilizaremos ModelState para mostrar errores sin perder los valores enviados. En **P2.4** añadiremos las operaciones de persistencia con SQL Server Express LocalDB y Entity Framework Core. La introducción a Razor Pages quedará para **P2.5**.

El formulario de P2.2 termina siendo más mantenible, pero la responsabilidad de aceptar datos válidos continúa estando en el servidor y no en la apariencia del HTML.

# P2.3. Validar los datos del formulario y representar sus errores

## Objetivo y relación con las prácticas anteriores

Hasta ahora el alumno ha conseguido obtener un formulario mediante GET, enviarlo con un POST protegido y representar la respuesta mediante Razor. Además, en P2.2 ha sustituido las asociaciones HTML escritas a mano por Tag Helpers. Nuestro siguiente problema es diferente: **no basta con que el navegador envíe datos y el servidor sepa recibirlos; deben cumplir unas reglas antes de convertirse en un producto válido**.

En P2.3 aprenderás a separar el contrato de entrada del modelo que representa la entidad; activarás reglas DataAnnotations, investigarás cómo registra MVC los errores de conversión y validación en `ModelState`, mostrarás mensajes junto a los campos sin borrar lo que ya había escrito el usuario y compararás la validación de servidor con la anticipada de cliente. Mantendremos expresamente **desactivada la persistencia**: en el catálogo seguirán Cuaderno, Lápiz y Carpeta, sin un cuarto elemento nuevo.

El recorrido troncal de esta práctica comprende los pasos **2.3.1 a 2.3.4**. La activación de scripts en 2.3.5 se hará como demostración breve, cuando la conectividad del laboratorio lo permita; el ejercicio de presentación 2.3.6 y el reto son ampliaciones que pueden completarse después. Así respetamos el horario del día sin renunciar a que el manual sea un recurso de aprendizaje profundo.

**Teoría relacionada:** punto 2.3 del manual del módulo. Si un resultado sorprende, vuelve a consultar la distinción entre model binding, validación declarativa y visualización de errores.

**Proyecto a abrir:** `M02_FORMULARIOS_RAZOR/PROYECTO/2.3/CursoWeb.Mvc/CursoWeb.Mvc.csproj`. No modifiques el M01 aprobado ni las carpetas de 2.1 o 2.2. La carpeta 2.3 es el punto de partida propio de este ejercicio y conserva los mecanismos HTML y Tag Helpers estudiados antes.

### Arranque reproducible

Desde la raíz del repositorio:

~~~bash
cd M02_FORMULARIOS_RAZOR/PROYECTO/2.3/CursoWeb.Mvc
dotnet restore
dotnet build
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

Detén cualquier aplicación anterior que siga ocupando el puerto 5091. Abre `http://localhost:5091/Productos/Crear`; debe mostrarse el formulario con dos campos, «Nombre» y «Precio», y el botón **Validar producto**. Comprueba también `/Productos`, donde aparecen los mismos tres productos del módulo anterior.

No necesitas SQL Server Express LocalDB para esta práctica. Aunque estudiaremos qué ocurre con una entrada inválida, no habrá ninguna escritura persistente que se deba deshacer: esta separación permite investigar el formulario sin introducir una segunda fuente de errores.

### Correspondencia completa entre pasos, archivos y resultados

| Paso | Archivo concreto | Intervención | Comprobación prevista |
|---|---|---|---|
| 2.3.1 | `Models/ProductoFormulario.cs`, `Controllers/ProductosController.cs`, `Views/Productos/Crear.cshtml` | Observar la separación entre entrada y entidad | No llega Id desde el formulario; la confirmación sigue disponible |
| 2.3.2 | `Models/ProductoFormulario.cs` | Descomentar cuatro DataAnnotations | Los valores ausentes, demasiado cortos y fuera de rango producen errores |
| 2.3.3 | `Controllers/ProductosController.cs` | Inspeccionar `ModelState.IsValid`; activar diagnóstico comentado opcional | Entrada incorrecta vuelve a Crear; en la depuración se identifican campos |
| 2.3.4 | `Views/Productos/Crear.cshtml` | Observar `asp-validation-for` y comparar `ModelOnly` con `All` | Mensajes visibles junto al campo, valor válido conservado |
| 2.3.5 | `Crear.cshtml`, `_Layout.cshtml`, `_ValidationScriptsPartial.cshtml` | Activar una sección Razor comentada | Validación cliente opcional; la del servidor sigue funcionando |
| 2.3.6 | `Models/ProductoFormulario.cs`, `Crear.cshtml` | Escribir `Display(Name=...)` en el modelo de entrada | La etiqueta cambia sin cambiar la clave HTTP `Nombre` |
| Reto 2.3 | `Controllers/ProductosController.cs` | Activar un bloque `ModelState.AddModelError` | Nombres que comienzan por TEST se rechazan aunque tengan longitud válida |

Los comentarios `PASO 2.3.2`, `PASO 2.3.3`, `PASO 2.3.4`, `PASO 2.3.5`, `APLICACION 2.3.6` y `RETO 2.3` permiten localizar directamente el código correspondiente. Cada intervención tiene su propia comprobación observable. No actives todos los comentarios simultáneamente antes de observar sus efectos.

## Paso 2.3.1 — Observar el nuevo modelo de entrada

Abre `Models/ProductoFormulario.cs` y compáralo con `Models/Producto.cs`. El modelo de dominio posee `Id`, `Nombre` y `Precio`; el de entrada se reduce a los dos campos que el usuario debe rellenar.

~~~csharp
public sealed class ProductoFormulario
{
    public string? Nombre { get; set; }
    public decimal? Precio { get; set; }
}
~~~

**Predicción previa:** ¿qué sucederá con el identificador del producto si alguien añade a mano `Id=99` en la petición de creación? La acción POST utiliza `ProductoFormulario`, que no expone esa propiedad. Por tanto, el binder de ese parámetro no tiene un campo Id en el contrato de entrada que deba completar. Más tarde el controlador construye explícitamente un `Producto` de demostración; no interpreta el valor Id del cliente como identificador definitivo.

Localiza en `ProductosController.cs` la acción GET de creación:

~~~csharp
[HttpGet]
public IActionResult Crear() => View(new ProductoFormulario());
~~~

La vista `Crear.cshtml` también declara `@model CursoWeb.Mvc.Models.ProductoFormulario`. Así, el objeto que se utiliza para construir los campos y el que recibe la acción POST comparten contrato. En P2.2 trabajábamos directamente con `Producto`; ahora hemos evitado aceptar desde el formulario una propiedad que corresponde al sistema.

Inspecciona los atributos de entrada que genera la vista. Deben conservar `name="Nombre"` y `name="Precio"`. El tipo C# de destino ha cambiado, pero el navegador continúa enviando los mismos pares de claves y valores. Esto demuestra que **el contrato HTTP y la representación interna de la entidad no necesitan ser la misma clase**.

### Estado inicial antes de activar reglas de negocio

Observa que las cuatro anotaciones de validación están comentadas en `ProductoFormulario.cs`. Por ahora una entrada como Nombre = «X», Precio = 7 puede llegar a la confirmación, porque la longitud mínima no se ha activado. El controlador mantiene una salvaguarda provisional para datos ausentes, de forma que ese estado de aprendizaje no intente desreferenciar un precio nulo; esa salvaguarda todavía no sustituye una validación declarativa adecuada.

**Ejecuta una comprobación controlada:** con las anotaciones sin activar, envía Nombre = X y Precio = 7. Si recibes una confirmación, has demostrado que **recibir correctamente el valor no equivale a considerarlo válido según una regla que todavía no existe**. Después activaremos StringLength y repetiremos exactamente los mismos campos.

No intentes resolver la diferencia insertando un `if` nuevo en cada vista o sustituyendo Precio por un string. El cambio docente previsto consiste en declarar reglas claras dentro del modelo de entrada.

## Paso 2.3.2 — Activar Required, StringLength y Range

Abre de nuevo `Models/ProductoFormulario.cs`. Encontrarás las reglas precedidas por comentarios de una línea `//`, junto a las marcas **PASO 2.3.2**. Quita los prefijos de comentario de **las cuatro anotaciones**, no de las explicaciones que las acompañan. El resultado debe ser:

~~~csharp
using System.ComponentModel.DataAnnotations;

public sealed class ProductoFormulario
{
    [Required(ErrorMessage = "Indica el nombre.")]
    [StringLength(60, MinimumLength = 2,
        ErrorMessage = "El nombre debe tener entre 2 y 60 caracteres.")]
    public string? Nombre { get; set; }

    [Required(ErrorMessage = "Indica el precio.")]
    [Range(typeof(decimal), "0.01", "9999.99",
        ErrorMessage = "El precio debe estar entre 0,01 y 9999,99.")]
    public decimal? Precio { get; set; }
}
~~~

El ejemplo omite el espacio de nombres de la clase porque estamos destacando las reglas. En el archivo real **conserva** `namespace CursoWeb.Mvc.Models;` y la declaración completa. Debes cambiar únicamente las anotaciones indicadas.

Compila de nuevo, ejecuta el formulario y repite la entrada Nombre = X, Precio = 7. Ahora el resultado es diferente: aparece el formulario nuevamente con un error junto a Nombre. En el archivo de modelo puedes encontrar el mismo mensaje que acaba de mostrarse. La acción no ha cambiado su nombre ni su ruta; ha cambiado el criterio utilizado para aceptar la entrada.

### Cuatro experimentos en los que cambia una sola variable

Primero envía **Nombre vacío y Precio 7**. Debe aparecer el mensaje «Indica el nombre». Comprueba que el precio se conserva al volver a representar la página. Un error en un campo no debe obligar a escribir otra vez el resto de información que sí era correcta.

Después envía **Nombre X y Precio 7**. Esta vez Nombre no está ausente, pero tiene menos de dos caracteres. Debe mostrarse el mensaje de `StringLength`. Explica por qué no sería apropiado diagnosticar el problema como un fallo del model binder: el binder puede representar perfectamente «X» como string.

En el tercer envío utiliza **Nombre Rotulador y Precio 0**. El precio existe y puede convertirse a decimal, pero está por debajo del mínimo 0,01 definido en `Range`. El mensaje debe aparecer junto al campo Precio. Con **Precio 7** la misma entrada nominal debería ser aceptada.

Por último, comprueba el caso de **Nombre Rotulador y Precio vacío**. El tipo `decimal?` permite expresar un valor ausente antes de aplicar las reglas, y `[Required]` lo considera inválido. Es distinto de un cero fuera de rango. **No confundas tipo anulable y campo de negocio opcional:** hemos elegido una propiedad anulable precisamente para poder representar y diagnosticar la ausencia en la entrada HTTP.

| Entrada | Regla que debe intervenir | Resultado del formulario |
|---|---|---|
| Nombre vacío, Precio 7 | `Required` de Nombre | Se repite Crear con mensaje |
| Nombre X, Precio 7 | `StringLength` de Nombre | Se repite Crear con mensaje |
| Nombre Rotulador, Precio 0 | `Range` de Precio | Se repite Crear con mensaje |
| Nombre Rotulador, Precio vacío | `Required` de Precio | Se repite Crear con mensaje |
| Nombre Rotulador, Precio 7 | Todas se cumplen | Se muestra Confirmacion |

Los primeros cuatro casos son negativos, pero **no son fallos de ejecución del proyecto**. La aplicación debe representarlos de forma comprensible, permitir su corrección y no tratarlos como productos válidos.

### Una condición que el navegador puede impedir escribir

Cuando un input tiene `type="number"`, algunos navegadores impiden introducir letras ordinarias en el control. Eso no demuestra que el servidor sea invulnerable a `Precio=abc`. Puedes estudiar la variante usando la pestaña Red y una herramienta de repetición de peticiones que te permita modificar el contenido del POST, siempre manteniendo el token antiforgery real obtenido de una carga actual del formulario.

La entrada `Precio=abc` no se convierte en un decimal. ModelState registra un **error de conversión**, diferente del mensaje de `Range` que corresponde a un número real fuera de los límites. No desactives antiforgery para simplificar la prueba: si el POST no incluye un token válido, recibirás 400 por otro motivo y dejarás de estudiar model binding.

## Paso 2.3.3 — Comprender y observar ModelState

En `Controllers/ProductosController.cs` localiza la acción POST. Ahora recibe un `ProductoFormulario entrada` y consulta el estado del enlace y de la validación:

~~~csharp
[HttpPost]
[ValidateAntiForgeryToken]
public IActionResult Crear(ProductoFormulario entrada)
{
    if (!ModelState.IsValid)
    {
        return View(entrada);
    }

    // Construir Producto y mostrar Confirmacion...
}
~~~

Este fragmento es la parte esencial del método, no una sustitución literal de todo el archivo. En el código real hay comentarios, una salvaguarda del estado inicial sin anotaciones y la conversión posterior al tipo de dominio. Conserva esos elementos.

**Predicción:** si `Nombre="X"`, `ModelState.IsValid` será falso después de activar `StringLength`. La acción ejecutará `return View(entrada)`, sin construir el Producto de confirmación. Si en cambio el nombre es Rotulador y el precio 7, ambas propiedades pueden validarse y el controlador construye el modelo de dominio.

Coloca un punto de interrupción en Visual Studio sobre `if (!ModelState.IsValid)`. Envía primero los datos correctos y después los incorrectos. Observa la propiedad `IsValid` y examina la colección de errores del estado del modelo. No necesitas aprender cada miembro de la API: basta con entender que el estado contiene claves asociadas a los campos y mensajes recogidos durante el procesamiento de la solicitud.

El controlador entrega también un bloque opcional **PASO 2.3.3 INICIO/FIN** que recorre `ModelState` y escribe la clave y el texto de sus errores mediante `Debug.WriteLine`. Si quieres estudiar ese recorrido, quita los delimitadores del comentario C#, compila y envía Nombre = X. Comprueba que el diagnóstico identifica un error asociado a Nombre. Después, desactiva otra vez el bloque si ya no lo necesitas.

**No confundas observar con corregir.** Un mensaje escrito en la ventana de depuración no modifica la validez de los datos. La decisión de la acción sigue determinada por ModelState. El control de flujo que devuelve la vista es lo que impide que los datos inválidos se traten como aceptados.

### ¿Por qué aquí no devolvemos automáticamente HTTP 400?

Quien conoce Web API puede recordar el comportamiento de un controlador con `[ApiController]`, donde una entrada inválida puede recibir automáticamente un error HTTP 400. Este formulario MVC devuelve normalmente **200 con el HTML de Crear** cuando la acción hace `return View(entrada)`. El usuario puede ver los mensajes de validación y corregir sus datos.

Eso no significa que el dato inválido haya sido aceptado. La respuesta 200 pertenece a la **representación correcta del formulario con errores**, no a la creación de un producto. Contrástalo con el fallo de antiforgery de P2.1: una petición sin token obtiene 400 antes de ejecutar el procesamiento previsto en la acción. Los dos escenarios tienen objetivos distintos.

## Paso 2.3.4 — Mostrar errores sin perder lo que se escribió

Abre `Views/Productos/Crear.cshtml`. Los controles mantienen los Tag Helpers de P2.2, pero ahora el modelo se llama `ProductoFormulario`, y la página contiene elementos para visualizar mensajes:

~~~cshtml
<div asp-validation-summary="ModelOnly" class="text-danger"></div>

<div>
    <label asp-for="Nombre"></label>
    <input asp-for="Nombre" />
    <span asp-validation-for="Nombre" class="text-danger"></span>
</div>

<div>
    <label asp-for="Precio"></label>
    <input asp-for="Precio" type="number" step="0.01" />
    <span asp-validation-for="Precio" class="text-danger"></span>
</div>
~~~

Envía **Nombre = Carpeta grande, Precio = -2**. La página debe representar un error asociado al precio, pero no debe borrar «Carpeta grande». En el HTML generado, inspecciona el input Nombre para comprobar que mantiene el valor anterior. El servidor volvió a presentar la vista con `View(entrada)`, y los Tag Helpers pueden utilizar el estado de los valores intentados para reconstruir el formulario.

Ahora cambia temporalmente `asp-validation-summary="ModelOnly"` por `asp-validation-summary="All"`. Repite la misma prueba. Con All, los errores de propiedades pueden mostrarse también dentro del resumen general; con ModelOnly, en cambio, es normal que se vean junto a sus campos sin repetirse arriba. Compara el comportamiento y **restaura ModelOnly** después del experimento.

La validación no depende de que un error sea visualmente rojo. La clase CSS `text-danger` ayuda a distinguir el mensaje, pero la causa es el estado que produce ASP.NET Core cuando comprueba la entrada. Si quitas el span `asp-validation-for`, el error puede seguir existiendo en ModelState aunque el usuario deje de verlo junto al campo. Por eso importan ambas partes: **la regla y su presentación**.

### Un mensaje que no es de Range

Envía una cantidad numérica pero fuera de rango, por ejemplo `-5`: debes obtener el mensaje configurado en la anotación Range. Después estudia, si tu herramienta HTTP lo permite, el envío de `Precio=abc` con un token válido. El valor no puede convertirse a decimal; el error es de **model binding**, no de la restricción `Range`.

Anota ambas causas. Cambiar el texto del mensaje de Range no explica un error de conversión. Si el navegador impide introducir letras en el campo numérico, eso no hace innecesaria la validación del servidor, porque otro cliente puede construir directamente una solicitud HTTP.

## Paso 2.3.5 — Comparar validación de servidor y validación de navegador

El servidor ya sabe representar los errores. Ahora vamos a añadir, como demostración breve, una mejora de experiencia de usuario: mostrar restricciones en el navegador sin necesitar enviar cada petición inválida.

Abre `Views/Shared/_Layout.cshtml` y observa que contiene `@await RenderSectionAsync("Scripts", required: false)`. Esa sección opcional permite a una página declarar sus propios recursos JavaScript sin obligar a que las demás vistas del catálogo los incluyan.

En `Views/Productos/Crear.cshtml` localiza **PASO 2.3.5 (ACTIVAR)**. El bloque está dentro de un comentario Razor. Quita las marcas de comentario para habilitar lo siguiente:

~~~cshtml
@section Scripts
{
    <partial name="_ValidationScriptsPartial" />
}
~~~

La parcial `Views/Shared/_ValidationScriptsPartial.cshtml` incluye referencias a tres bibliotecas en orden: **jQuery**, **jQuery Validation** y **jQuery Validation Unobtrusive**. El proyecto usa una CDN, de manera que **necesita conectividad** para completar esta demostración. Un entorno sin Internet debe recibir una copia local preparada de esos recursos; no atribuyas un fallo de descarga a una regla incorrecta del modelo.

Recarga el formulario con F12 → Red abierto y comprueba que los tres scripts se han descargado correctamente. Inspecciona los inputs: sus atributos `data-val` describen reglas derivadas de DataAnnotations. Esos atributos no ejecutan validación por sí solos: necesitan las bibliotecas correspondientes.

Intenta enviar **Nombre = X, Precio = 7**. Si los scripts están cargados y la validación cliente interviene, el navegador puede impedir el POST y mostrar el error sin recorrer el servidor. Comprueba en la pestaña Red si realmente ha existido una nueva petición POST, en vez de deducirlo del aspecto de la pantalla.

### Repetir la prueba con JavaScript deshabilitado

Deshabilita temporalmente JavaScript para esa página mediante las herramientas de desarrollo del navegador y recarga el formulario. Repite la entrada inválida. Aunque ya no actúen las bibliotecas cliente, el servidor debe recibir el POST protegido, evaluar ModelState y volver a mostrar Crear con sus mensajes. **La validación de servidor permanece obligatoria.**

Vuelve a habilitar JavaScript después del experimento para evitar confusiones durante el resto del curso. Si alguna biblioteca no puede descargarse, comprueba la consola del navegador y el estado de cada solicitud de script. El comportamiento del servidor sigue siendo el resultado principal, independientemente de la disponibilidad de esa CDN.

No hagas una regla duplicada y contradictoria en JavaScript. Las DataAnnotations representan la definición central de estas restricciones. El cliente proporciona una experiencia más inmediata cuando puede interpretar sus metadatos, pero no es una frontera de confianza.

## Paso 2.3.6 — Aplicación autónoma: modificar una etiqueta sin cambiar el contrato HTTP

Hasta ahora has observado y activado código preparado. En esta actividad debes **escribir una anotación propia**. Abre `Models/ProductoFormulario.cs` y localiza **APLICACION 2.3.6**. Coloca sobre la propiedad `Nombre` el atributo que permite mostrar la etiqueta «Nombre del producto»:

~~~csharp
[Display(Name = "Nombre del producto")]
~~~

No cambies el identificador de la propiedad C#. Sigue llamándose `Nombre` y el controlador seguirá recibiéndola con esa clave. Compila, recarga Crear y comprueba que el Label Tag Helper muestra el nuevo texto. Inspecciona el input y verifica que el atributo `name` sigue correspondiendo a `Nombre`.

Este ejercicio exige explicar **dos resultados diferentes**. Visualmente puede cambiar el texto de la etiqueta, porque se ha añadido un metadato de presentación. Funcionalmente no debe cambiar el contrato que utiliza el model binder: el campo de entrada sigue siendo Nombre y las reglas Required y StringLength siguen aplicándose a la misma propiedad.

Envía Rotulador y 7. Si llega a Confirmacion, puedes concluir que el nuevo metadato de presentación no ha roto el flujo POST. Repite Nombre = X para confirmar que continúa funcionando el error de longitud mínima. Si los mensajes aparecen, la propiedad no ha sido renombrada ni la validación se ha eliminado.

La anotación Display no sustituye Required, StringLength o Range. Expresa cómo se presenta un campo, no si el usuario está obligado a rellenarlo.

## Reto 2.3 — Una regla adicional introducida desde el controlador

El controlador incluye un bloque comentado **RETO 2.3 INICIO/FIN**. Este ejemplo añade un error específico a ModelState cuando el nombre comienza por `TEST`, ignorando mayúsculas y minúsculas. El objetivo es comprender que la acción puede aportar un error contextual que se presenta con el mismo mecanismo de la vista.

Activa únicamente ese bloque y compila. Envía `Nombre=TESTProducto`, `Precio=7`. El nombre tiene longitud suficiente y el precio cumple el intervalo, pero la acción debe añadir un error y devolver Crear. A continuación, envía `Nombre=Rotulador`, `Precio=7` y verifica que se representa Confirmacion.

El bloque preparado incluye el núcleo:

~~~csharp
if (entrada.Nombre?.StartsWith("TEST", StringComparison.OrdinalIgnoreCase) == true)
{
    ModelState.AddModelError(nameof(entrada.Nombre),
        "El nombre no puede comenzar por TEST en este ejemplo.");
}
~~~

No coloques la llamada a AddModelError **después** del `if (!ModelState.IsValid)` si esperas que ese mismo control la detecte. La condición del reto se evalúa antes de tomar la decisión sobre IsValid; el orden es parte de lo que debes razonar.

Este ejemplo demuestra una posibilidad técnica, no una invitación a escribir todas las reglas empresariales dentro de controladores. Para un sistema amplio, la ubicación de esas reglas requiere diseño. En este curso nos interesa comprender que los errores de las anotaciones, los errores de conversión y los añadidos por la acción pueden terminar en la misma presentación Razor.

### Probar el resultado conjunto sin falsear la persistencia

Si has realizado la aplicación autónoma de Display y el reto, comprueba finalmente que el catálogo de M01 conserva sus tres productos. Un POST válido todavía devuelve Confirmacion sin guardar, mientras que los POST inválidos se quedan en el formulario. La representación, la protección antiforgery y la validación funcionan conjuntamente sin necesidad de una base de datos.

## Diagnóstico de los problemas más habituales

**Aparece un 400 antes de que el controlador llegue al bloque de validación.** Confirma que la petición contiene un token antiforgery válido y que se dirige a la acción correcta. No deshabilites ValidateAntiForgeryToken para estudiar Required o Range. De lo contrario, habrás cambiado la causa del error que querías observar.

**Aparece un 200 pero no hay página de confirmación.** Comprueba si el controlador ha devuelto la vista Crear debido a un ModelState inválido. La respuesta 200 puede ser el HTML correcto del formulario con mensajes; no significa que un producto se haya aceptado.

**Los mensajes no aparecen junto a los campos.** Comprueba las reglas activadas, `ModelState.IsValid` y los `span asp-validation-for` de la vista. Si utilizas `ModelOnly` en el resumen, recuerda que los errores de propiedades pueden no aparecer allí. Prueba temporalmente `All` para estudiar la diferencia.

**El precio se borra o no conserva lo escrito.** Observa el valor recibido, los atributos que genera Input Tag Helper, la conversión decimal y el contenido de ModelState. Si un formato no puede convertirse, el valor intentado puede conservarse en el estado de enlace; no reemplaces a ciegas el modelo entero por un Producto nuevo al devolver la vista.

**La validación funciona con JavaScript, pero deja de hacerlo al desconectarse de Internet.** Diferencia los dos mecanismos. La CDN afecta a los scripts de cliente. Una entrada inválida que se envía al servidor con token válido debe seguir siendo detectada mediante ModelState. Investiga por separado la descarga del JavaScript y la ejecución del POST.

**Un producto inválido llega a Confirmacion.** Comprueba si quedaron comentadas las DataAnnotations del modelo o si algún cambio ha omitido la comprobación de IsValid. Una regla que existe solo como comentario no valida nada. Y un Input Tag Helper no crea de forma automática reglas de negocio que nunca declaramos.

## Resultado final de P2.3 y puente hacia P2.4

Al completar el recorrido esencial, el alumno debe poder describir sin ambigüedad las responsabilidades de cada elemento: **el navegador envía campos; el binder los convierte; DataAnnotations expresa restricciones; ModelState reúne errores; el controlador decide si devuelve el formulario o la confirmación; y Razor representa valores y mensajes**.

El proyecto conserva las reglas activadas y los elementos de validación en el flujo principal. La demostración de scripts y los retos no deben impedir que la jornada avance hacia las operaciones persistentes. **P2.4** incorporará SQL Server Express LocalDB y Entity Framework Core para que crear, editar o eliminar productos produzca cambios reales en el catálogo. Como el alumnado ya conoce EF Core, la atención estará puesta en cómo se combina el modelo de entrada validado con las acciones MVC y las vistas Razor.

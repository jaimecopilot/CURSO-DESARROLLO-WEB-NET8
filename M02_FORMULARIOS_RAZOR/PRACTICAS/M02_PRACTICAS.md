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

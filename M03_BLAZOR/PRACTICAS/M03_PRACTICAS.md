# M03 — Prácticas de Blazor Web App y componentes

## Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8

**CURSO: Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8**

**TIPO: PRÁCTICAS**

**AUTOR: JAIME GALLO**

## Itinerario de trabajo y condiciones del laboratorio

Durante esta jornada utilizaremos una única aplicación B de Blazor Web App en .NET 8, organizada en seis **estados reproducibles** dentro de la carpeta `M03_BLAZOR/PROYECTO/`. Cada punto tiene un proyecto `CursoWeb.Blazor` independiente que conserva la misma estructura general. Eso permite repetir un experimento desde su estado inicial sin desmontar el código de prácticas anteriores; no representa seis aplicaciones de negocio distintas. El alumno conoce C# y las bases de Web API, pero no se presupone que conozca Blazor. No se requiere SQL Server, LocalDB ni API remota para M03.

Los proyectos están preparados con comentarios pedagógicos identificados por paso. En archivos C#, se activa el bloque delimitado por `/* PASO X INICIO` y `PASO X FIN */` retirando **únicamente los delimitadores**. En archivos Razor se retiran `@*` y `*@` del fragmento correspondiente. Cuando se proponen variantes completas de un componente, hay que **sustituir** una por otra, no dejar varias instancias visibles simultáneamente. El alumno no tiene que adivinar qué líneas aparecieron entre un estado y el siguiente.

Antes de cada práctica detén el proceso de la anterior y abre el `CursoWeb.Blazor.csproj` de la carpeta concreta. Para P3.1, por ejemplo:

~~~powershell
cd M03_BLAZOR/PROYECTO/3.1/CursoWeb.Blazor
dotnet restore
dotnet build
dotnet run --no-launch-profile --urls http://localhost:5092
~~~

Abre después `http://localhost:5092`. Si Visual Studio utiliza un puerto distinto, sigue la dirección anunciada por Kestrel. El proyecto debe ejecutarse con el SDK de .NET 8. No copies los cambios en M01 ni M02; son aplicaciones y materiales anteriores. Los pasos esenciales forman la práctica de clase; los experimentos de transferencia y retos amplían la comprensión sin requerir una infraestructura adicional.

## Índice del cuaderno

- P3.1. Comparación de SSR estático e Interactive Server.
- P3.2. Página Productos y navegación con NavLink.
- P3.3. Parámetros y componente TarjetaProducto.
- P3.4. Estado, eventos y binding.
- P3.5. Comunicación padre–hijo con EventCallback.
- P3.6. Servicio asíncrono, OnInitializedAsync y estados de carga.

# P3.1. Crear la aplicación Blazor B y comprobar interactividad real

## Objetivo y estado inicial

El objetivo es identificar el problema que resuelve Interactive Server y comprobarlo empíricamente. La carpeta inicial es `M03_BLAZOR/PROYECTO/3.1/CursoWeb.Blazor`. Dispone de dos páginas equivalentes en lo esencial: `Estatica.razor` sin modo interactivo y `Interactiva.razor` con ese modo declarado. El primero permite observar que escribir un manejador de clic no es suficiente; el segundo comprueba que el mismo tipo de manejador sí funciona cuando la aplicación está configurada correctamente.

### 3.1.1. Abrir y compilar el estado de partida

Abre exactamente `M03_BLAZOR/PROYECTO/3.1/CursoWeb.Blazor/CursoWeb.Blazor.csproj`. Comprueba que el archivo de proyecto declara `net8.0`. En una consola situada en esa carpeta, ejecuta `dotnet restore` y `dotnet build`. Si alguna operación falla, verifica la versión del SDK y que abriste este proyecto, no uno de los módulos MVC.

Ejecuta con `dotnet run --no-launch-profile --urls http://localhost:5092`. El resultado esperado es que Kestrel anuncie la URL. Abre el navegador y visita la raíz. Debes encontrar el título «Aplicación B · Blazor Web App», una descripción del catálogo en memoria y enlaces a las dos formas de renderizado.

**Relación con la teoría:** 3.1 explica por qué Blazor sigue ejecutándose dentro del host ASP.NET Core aunque cambie el modelo de interacción. En `Program.cs` verifica las dos instrucciones que preparan el servidor:

~~~csharp
builder.Services.AddRazorComponents().AddInteractiveServerComponents();
app.MapRazorComponents<App>().AddInteractiveServerRenderMode();
~~~

La primera configura servicios; la segunda expone endpoints de componentes con soporte de interactividad en servidor. Si falta una parte, no debemos concluir que un método `@onclick` funcionará solo porque el proyecto contiene código C#.

### 3.1.2. Identificar las piezas del proyecto

Abre `Components/App.razor` y localiza el documento HTML, `<Routes />` y el script `_framework/blazor.web.js`. Abre `Components/Routes.razor` y encuentra `Router` y `RouteView`. Abre `Components/Layout/MainLayout.razor` y localiza `@Body`. Comprueba que `Components/Pages/Home.razor` declara `@page "/"`.

Explica en tu cuaderno el recorrido de la ruta inicial: el navegador solicita una URL; ASP.NET Core atiende el endpoint; el router identifica la página; el layout la representa dentro de una estructura común. Esta explicación se parece conceptualmente al recorrido MVC que ya conoces, pero ahora no existe `HomeController` para esta pantalla.

Como caso negativo, abre `/una-ruta-inexistente`. Debes ver el contenido de la rama `NotFound` del router. La aplicación debe continuar respondiendo en `/`. Esta observación ayuda a distinguir una ruta inexistente de una aplicación que no ha arrancado.

### 3.1.3. Observar un botón bajo SSR estático

Abre `Components/Pages/Estatica.razor`. Comprueba que existe:

~~~razor
@page "/estatica"
<p id="contador-estatico">Pulsaciones: @contador</p>
<button id="boton-estatico" @onclick="Incrementar">Pulsar (sin interacción)</button>

@code {
    private int contador;
    private void Incrementar() => contador++;
}
~~~

Visita `http://localhost:5092/estatica` y pulsa el botón tres veces. **Resultado esperado:** «Pulsaciones: 0» continúa visible. Esto no constituye un fallo del ejercicio. El componente tiene código y se ha representado desde el servidor, pero no está habilitado como componente interactivo capaz de procesar ese clic C# después de la respuesta inicial.

No intentes solucionar este resultado sustituyendo el método por JavaScript. El propósito es aislar una condición del modelo de ejecución. En las herramientas de desarrollo observa que pulsar no desencadena una navegación completa con una nueva acción MVC, y describe qué necesitaría el componente para responder.

### 3.1.4. Observar el mismo evento con Interactive Server

Abre `Components/Pages/Interactiva.razor`. Sus primeras líneas son:

~~~razor
@page "/interactiva"
@rendermode InteractiveServer
~~~

El resto conserva un contador y un botón con manejador de clic. Abre `http://localhost:5092/interactiva`, deja que la conexión se establezca y pulsa una vez. Debes ver «Pulsaciones: 1». Vuelve a pulsar: el número pasa a dos. No se modifica el servidor SQL ni una colección global: el campo `contador` pertenece a la instancia interactiva del componente.

Compara qué cambia en los dos archivos: no necesitas escribir otro lenguaje de programación; el elemento diferenciador es `@rendermode InteractiveServer` y el soporte configurado en `Program.cs`. Revisa también que en `App.razor` el proyecto utiliza `<Routes />` sin hacer interactivo todo el árbol; por eso ambas páginas pueden coexistir con comportamientos distintos.

### 3.1.5. Diagnóstico y verificación negativa

Retira temporalmente la directiva `@rendermode InteractiveServer` de `Interactiva.razor`, recompila y abre esa página desde cero. El botón deja de incrementar el valor, como en `/estatica`. Restablece la directiva y verifica que vuelve a funcionar. En una explicación de una o dos frases, relaciona ambos resultados con la diferencia entre representación estática y circuito interactivo, sin atribuirlos a la apariencia de los botones.

Si la página interactiva continúa sin responder, comprueba por este orden: ruta correcta, directiva de renderizado, registro de servicios en `Program.cs`, mapeo de endpoints, script en `App.razor` y errores de conexión que muestre el navegador. Un compilador con salida correcta no garantiza por sí solo la interacción de navegador: debes observar un clic que cambie el texto.

### Reto 3.1 — Incrementos dobles

**Enunciado:** modifica una sola línea del método de evento de `Components/Pages/Interactiva.razor` para sumar dos unidades por pulsación, manteniendo intacta `Estatica.razor`. El objetivo es demostrar que el comportamiento depende de la lógica de C# y que la posibilidad de ejecutarla depende del modo de renderizado.

**Código de solución para consulta:**

~~~csharp
private void Incrementar() => contador += 2;
~~~

Reemplaza temporalmente `contador++` por la línea anterior. Compila, navega a `/interactiva` y comprueba los valores 2 y 4 tras dos clics. **Control negativo:** `/estatica` sigue sin variar al pulsar. Restaura después `contador++`. La solución no añade nuevos endpoints, ni un formulario POST, ni persistencia. La modificación consiste únicamente en la operación realizada en el manejador.

### Profundización opcional

Explica por qué el primer GET de una página interactiva sigue utilizando HTTP, aunque los eventos posteriores no se gestionen mediante una nueva acción MVC completa. Analiza qué puede ocurrir si el navegador pierde su conexión con el servidor mientras el contador está visible. No necesitas estudiar SignalR avanzado ni capturar los mensajes de protocolo: basta comprender que Interactive Server mantiene lógica y estado en el servidor y depende de esa comunicación.

# P3.2. Página Productos y navegación con NavLink

## Objetivo y estado inicial

El proyecto `M03_BLAZOR/PROYECTO/3.2/CursoWeb.Blazor` conserva las páginas anteriores y añade el modelo `Producto` y la página `/productos`. La ruta **ya funciona**, pero el enlace del menú permanece comentado para aprender que declarar un endpoint y ofrecer navegación son responsabilidades diferentes.

### 3.2.1. Abrir el proyecto y probar la ruta directamente

Detén el host de P3.1 y abre `M03_BLAZOR/PROYECTO/3.2/CursoWeb.Blazor/CursoWeb.Blazor.csproj`. Compila y ejecuta en el puerto 5092. Sin utilizar el menú, abre directamente `http://localhost:5092/productos`. Debes encontrar un listado de Cuaderno, Lápiz y Carpeta. Si la dirección funciona pero todavía no existe el enlace «Productos» en la cabecera, ese es exactamente el estado inicial esperado.

Abre `Components/Pages/Productos.razor` y encuentra las directivas `@page "/productos"` y `@rendermode InteractiveServer`. La primera declara la dirección. La segunda anticipa la interactividad que añadiremos después, aunque por ahora solo representemos una lista.

### 3.2.2. Activar el enlace preparado en el layout

Abre `Components/Layout/MainLayout.razor` y localiza la marca `PASO 3.2.2 (ACTIVAR)`. Justo debajo aparece:

~~~razor
@* <NavLink href="/productos">Productos</NavLink> *@
~~~

Elimina los delimitadores de comentario, conservando:

~~~razor
<NavLink href="/productos">Productos</NavLink>
~~~

Guarda y recompila. Abre `http://localhost:5092/`. El menú debe mostrar «Productos». Haz clic, observa la ruta final y regresa al inicio. El elemento `NavLink` ofrece el enlace y la indicación de navegación activa, pero **no crea por sí mismo la página**; esta ya existía gracias a la directiva `@page`.

### 3.2.3. Leer el código de modelo y lista

Abre `Models/Producto.cs` y comprueba la declaración del record con Id, Nombre y Precio. En `Components/Pages/Productos.razor` localiza:

~~~razor
<ul id="lista-productos">
    @foreach (var producto in productos)
    {
        <li>@producto.Nombre — @producto.Precio.ToString("0.00") €</li>
    }
</ul>
~~~

Dentro de `@code` se crea una colección con tres elementos. Relaciona la lista C# con los tres elementos `li` del HTML representado. Abre las herramientas del navegador e inspecciona `id="lista-productos"`. No existe ninguna petición SQL ni HTTP a una API para rellenarla: el estado pertenece al componente.

**Ejercicio de diagnóstico:** si el menú no muestra Productos, investiga el layout; si aparece el menú pero `/productos` no existe, investiga `@page` y el router. No cambies los archivos de M02 para arreglar un problema de esta nueva aplicación.

### 3.2.4. Comparar tres nombres parecidos que representan ideas distintas

Explica la diferencia entre `Views/Productos/Index.cshtml` de MVC, `Pages/Comparacion.cshtml` de Razor Pages y `Components/Pages/Productos.razor` de Blazor. Los tres generan contenido de interfaz a partir de Razor, pero el primero se elige desde una acción MVC, el segundo usa handlers de PageModel y el tercero es un componente que puede tener renderizado interactivo. Esta comparación enlaza expresamente con los módulos anteriores y evita una confusión que suele aparecer al comenzar con Blazor.

### Ejercicio autónomo 3.2 — Añadir una fila controlada

**Enunciado:** añade un producto «Regla», con Id 4 y precio 2.50, dentro de la colección que declara `Productos.razor`. No dupliques el elemento HTML ni crees otro archivo. **Código que debes escribir:** incorpora un cuarto elemento:

~~~csharp
new(4, "Regla", 2.50m)
~~~

Compila y recarga `/productos`. Deben aparecer **cuatro elementos de lista**. El formato del precio debe seguir la expresión `ToString("0.00")`. Si solo ves tres elementos, verifica que editaste el proyecto 3.2 que estás ejecutando. Si el precio se representa con un formato diferente, investiga cómo se convierte el decimal a texto. Después recupera la colección inicial de tres elementos para continuar con P3.3 tal como se entrega.

### Profundización opcional

Cambia temporalmente el texto visible del enlace de menú sin modificar su `href`. Observa que la ruta sigue siendo la misma. Ahora imagina que cambiaras `@page "/productos"` a otro nombre sin actualizar el menú: ¿qué enlace quedaría roto? No hace falta alterar definitivamente la ruta; basta explicar que la dirección es un contrato distinto del texto que la representa. Este criterio es útil en MVC, Razor Pages y Blazor.

# P3.3. Componente TarjetaProducto, parámetros y composición

## Objetivo y preparación

Ahora convertimos una lista HTML sencilla en tres tarjetas generadas mediante un componente reutilizable. El estado inicial de `M03_BLAZOR/PROYECTO/3.3/CursoWeb.Blazor` sigue compilando y mostrando los productos mediante `<ul>`. El proyecto incluye además `Components/TarjetaProducto.razor` y una variante comentada de composición. Necesitamos activar la segunda **sustituyendo** el bloque antiguo para no duplicar la interfaz.

### 3.3.1. Verificar el estado de salida de P3.2

Detén P3.2, abre el proyecto 3.3, compila y ejecuta. Abre `/productos`. Debes encontrar una lista de tres elementos. El objetivo inmediato no es añadir datos nuevos; es cambiar **cómo** se representan los mismos tres objetos.

En `Components/Pages/Productos.razor` localiza el comentario `PASO 3.3.2` y el bloque activo que comienza con `<ul id="lista-productos">`. Más abajo encuentra `PASO 3.3.3 (ACTIVAR)`, que incluye una variante de tarjetas dentro de un comentario Razor.

### 3.3.2. Comprender el contrato de la tarjeta

Abre `Components/TarjetaProducto.razor`. Encontrarás un artículo con nombre, precio e identificador:

~~~razor
<article class="tarjeta" data-producto-id="@Producto.Id">
    <h2>@Producto.Nombre</h2>
    <p>Precio: @Producto.Precio.ToString("0.00") €</p>
    <small>Referencia @Producto.Id</small>
</article>
~~~

Debajo aparece:

~~~csharp
[Parameter, EditorRequired]
public Producto Producto { get; set; } = default!;
~~~

Explica por qué `[Parameter]` establece un contrato de entrada. La tarjeta no conoce la colección completa, no tiene que consultar una API y no declara `@page`. Solo necesita el producto que recibe del componente padre. La marca `EditorRequired` ayuda a las herramientas a identificar que se espera ese parámetro; no introduce por sí sola un mecanismo de validación HTTP.

### 3.3.3. Sustituir la lista por tres tarjetas

En `Components/Pages/Productos.razor`, comenta temporalmente el bloque de lista completo, desde `<ul id="lista-productos">` hasta `</ul>`, incluidos los elementos de iteración que contiene. Activa el bloque siguiente retirando `@*` y `*@`:

~~~razor
<div class="tarjetas" id="tarjetas-productos">
    @foreach (var producto in productos)
    {
        <TarjetaProducto Producto="producto" />
    }
</div>
~~~

Compila y abre `/productos`. **Resultado positivo:** tres tarjetas, una por producto, con sus nombres, precios e identificadores. En el inspector del navegador busca `data-producto-id="1"`, `data-producto-id="2"` y `data-producto-id="3"`. El atributo ayuda a comprobar qué producto recibió cada tarjeta.

**Caso negativo de transformación:** si conservaste activo el bloque `<ul>` además del nuevo bloque, aparecerán dos representaciones del catálogo. Eso no demuestra que `[Parameter]` haya fallado; indica que has dejado dos bucles activos. Deja solo la versión de tarjetas.

### 3.3.4. Explicar el vínculo entre padre e hijo

En el padre, la variable `producto` procede del `foreach`. En el hijo, la propiedad `Producto` recibe ese objeto. La expresión `Producto="producto"` es el punto donde las dos piezas se encuentran. Si sustituyes temporalmente la variable por `productos[0]`, las tres tarjetas pueden representar el mismo objeto Cuaderno aunque haya tres iteraciones. Restablece `Producto="producto"` y comprueba que vuelven los tres productos distintos. La prueba demuestra que el componente reutilizable necesita datos correctos del padre; no crea por sí mismo una lista independiente.

### 3.3.5. Observar un cambio centralizado

En `Components/TarjetaProducto.razor` sustituye temporalmente el texto «Precio:» por «Importe:» y compila. El cambio aparece en las tres tarjetas. No es necesario modificar el padre varias veces. Después restaura el texto original. Esta observación justifica la extracción del componente: una misma responsabilidad de representación está concentrada en un lugar.

Si los elementos se dibujan sin tarjetas visuales, comprueba la clase `tarjeta` y la carga de `wwwroot/app.css`. Si no se muestran los nombres correctos, inspecciona los valores que el padre transmite. No confundas un problema de estilos con un problema de parámetros.

### Reto 3.3 — Indicar productos que superan un precio

**Enunciado:** modifica exclusivamente `Components/TarjetaProducto.razor` para que un producto cuyo precio sea superior a cuatro euros muestre el texto «Precio superior a 4 euros». Se trata de un ejercicio autónomo de representación condicional, no de una nueva regla de negocio o de una llamada a un servicio.

**Código de solución razonada:**

~~~razor
@if (Producto.Precio > 4m)
{
    <p class="mensaje">Precio superior a 4 euros</p>
}
~~~

Escribe el bloque dentro del artículo, después del precio. Compila y observa el resultado: Cuaderno tiene precio 4.50 y debe mostrar la advertencia; Lápiz y Carpeta no. **Caso negativo:** no deben aparecer mensajes en productos que cuestan menos de cuatro euros. Para explorar la frontera entre `>` y `>=`, puedes cambiar temporalmente el precio de Carpeta a exactamente 4.00, observar el comportamiento y restaurarlo.

**Explicación:** esta responsabilidad pertenece al hijo porque es una variación de cómo se representa **un** producto. No hace falta duplicar el bucle en el padre ni crear una vista Razor MVC. El componente recibe el objeto y decide qué HTML adicional producir.

### Profundización opcional: reutilización y responsabilidades

Imagina que la página Productos se utiliza más adelante para mostrar resultados de una API. ¿Debería `TarjetaProducto` hacer por sí misma una petición HTTP cada vez que se representa? En nuestro diseño, no: el padre o un servicio coordinador obtiene datos, y las tarjetas reciben los objetos que deben mostrar. Este planteamiento permite reutilizar la representación sin acoplarla al origen de datos y prepara el servicio de P3.6.

**Relación con la teoría:** 3.3 desarrolla el contrato `[Parameter]`, la composición y la propiedad de los datos. Al terminar debes poder explicar por qué la tarjeta no necesita una ruta `@page` para funcionar dentro de la página.

# P3.4. Eventos, @onclick, @bind y estado de componentes

## Objetivo, ubicación y relación con P3.3

En P3.3 las tarjetas mostraban productos mediante parámetros. Ahora veremos que los componentes no solo representan información: también pueden reaccionar a eventos y alterar datos en memoria. Para aislar el concepto, durante P3.4 los botones de selección estarán escritos **directamente en la página padre**. En P3.5 los trasladaremos al hijo y aprenderemos EventCallback. No introducimos una API remota, guardado en EF Core ni administración de estado global.

La ubicación exacta es `M03_BLAZOR/PROYECTO/3.4/CursoWeb.Blazor/`, y el archivo principal `Components/Pages/Productos.razor`. El estado inicial contiene tres tarjetas, un texto «Seleccionado: ninguno», botones comentados y métodos C# asociados también comentados. **La compilación inicial debe funcionar sin activar ninguno de ellos**.

### 3.4.1. Abrir el estado inicial y reconocer el campo de selección

Detén la aplicación de P3.3. Abre el archivo `CursoWeb.Blazor.csproj` de la carpeta 3.4, ejecuta `dotnet build` y arranca con `dotnet run --no-launch-profile --urls http://localhost:5092`. Visita `http://localhost:5092/productos` y localiza el elemento `id="seleccion"`. Debes leer «Seleccionado: ninguno». Cuenta los tres artículos con clase `tarjeta`; no debe haber botones Seleccionar activos.

Abre el archivo de página y localiza la directiva `@rendermode InteractiveServer`. Encuentra también el campo:

~~~csharp
private string seleccion = "ninguno";
~~~

El campo pertenece al componente y sirve para mostrar el valor actual. No es una propiedad de `Producto`, no se guarda en LocalDB y no se transmite a un controlador. Esta observación anticipa el paso siguiente: un evento modificará ese campo y el framework volverá a representar el texto.

### 3.4.2. Activar el evento de selección

En `Components/Pages/Productos.razor`, localiza el comentario Razor identificado como `PASO 3.4.2 (ACTIVAR)`. El botón real del proyecto aparece en una única línea:

~~~razor
@* <button @onclick="() => Seleccionar(producto.Id)">Seleccionar</button> *@
~~~

Retira exclusivamente `@*` y `*@`, dejando el botón activo. En el bloque `@code`, localiza el fragmento delimitado por `PASO 3.4.2 INICIO` y `PASO 3.4.2 FIN` y activa su método:

~~~csharp
private void Seleccionar(int id)
{
    seleccion = productos.First(p => p.Id == id).Nombre;
}
~~~

Compila. En `/productos` debe aparecer un botón Seleccionar por tarjeta. Pulsa en Lápiz y observa «Seleccionado: Lápiz». Después pulsa en Carpeta y observa el cambio a ese nombre. **El dato cambia dentro de la misma página** y no se necesita realizar una nueva operación MVC por cada clic.

**Caso negativo de activación:** si activaste el botón pero no el método C#, el compilador puede comunicar que `Seleccionar` no existe. Revisa ambos bloques del mismo paso; no inventes un método con otro nombre. **Caso negativo de ejecución:** si el botón está visible pero no produce cambios, comprueba primero que estás ejecutando `/productos` del proyecto 3.4, y después que el circuito Interactive Server funciona; recuerda la comparación de P3.1.

**Por qué funciona:** la expresión lambda captura el Id del producto que se está representando en esa tarjeta. El método del componente encuentra su nombre y modifica `seleccion`. Blazor programa una actualización de la representación al finalizar el evento. No es necesario llamar manualmente a `StateHasChanged()` para este clic ordinario.

### 3.4.3. Incorporar un campo con @bind

Localiza `PASO 3.4.3 (ACTIVAR)` y retira los delimitadores de comentario del campo:

~~~razor
<label>Nombre nuevo:
    <input id="nombre-nuevo" @bind="nuevoNombre" />
</label>
~~~

En `@code` activa también el fragmento `PASO 3.4.3 INICIO / FIN`, que declara:

~~~csharp
private string nuevoNombre = string.Empty;
~~~

Compila, abre `/productos` y escribe «Regla». De momento **no se añade** ninguna tarjeta porque todavía falta el método del paso siguiente. Esta separación resulta intencionada: estamos comprobando el vínculo entre el control HTML y el estado C#, sin introducir simultáneamente todas las operaciones.

A diferencia de `asp-for` del formulario MVC, aquí `@bind` participa en el enlace de datos de una interfaz interactiva. Si escribes sin abandonar el campo, recuerda que el enlace predeterminado del `input` se actualiza conforme a su evento de cambio; el itinerario principal no necesita la variante avanzada `@bind:event="oninput"`.

### 3.4.4. Activar el alta de un producto en memoria

Localiza `PASO 3.4.4 (ACTIVAR)` y descomenta exactamente el botón:

~~~razor
<button id="agregar" @onclick="Agregar">Añadir producto</button>
~~~

A continuación, en `@code`, activa **todo** el bloque `PASO 3.4.4 INICIO / FIN`, incluida la declaración del nuevo identificador:

~~~csharp
private int siguienteId = 4;

private void Agregar()
{
    if (string.IsNullOrWhiteSpace(nuevoNombre))
        return;
    productos.Add(new Producto(siguienteId++, nuevoNombre.Trim(), 5m));
    nuevoNombre = string.Empty;
}
~~~

Ahora compila y ejecuta. Escribe «Regla» y pulsa Añadir. Debe aparecer una cuarta tarjeta y vaciarse el campo. Comprueba que el nuevo producto tiene un Id distinto de los tres anteriores y el precio fijo 5.00 que proporciona esta demostración.

**Caso negativo:** intenta añadir un nombre vacío y después uno compuesto exclusivamente por espacios. En ambos casos la cantidad de tarjetas debe mantenerse igual. No confundas esta condición sencilla con todas las reglas DataAnnotations de M02: aquí aprendemos el ciclo de eventos y la representación, no repetimos todo el CRUD persistente.

**Estado persistente:** recarga la ruta completamente para iniciar otra instancia de componente. Lo normal es que reaparezcan los tres productos originales. Es coherente: la lista pertenece a la sesión/instancia de interfaz y no se almacena en SQL ni se envía a la API que todavía no existe. Un resultado visual de «cuatro tarjetas» no demuestra un INSERT.

### Reto 3.4 — Limpiar la selección sin alterar el catálogo

El proyecto contiene un botón y un método comentados bajo la marca `RETO 3.4`. Su objetivo es practicar que un mismo estado puede cambiar por otra acción distinta de Seleccionar.

Activa en el Razor:

~~~razor
<button id="limpiar" @onclick="Limpiar">Limpiar selección</button>
~~~

Y activa en `@code`:

~~~csharp
private void Limpiar() => seleccion = "ninguno";
~~~

Compila. Selecciona Cuaderno, comprueba que la pantalla muestra su nombre y pulsa Limpiar. El texto debe volver a «Seleccionado: ninguno». **Control negativo:** ninguna tarjeta debe desaparecer ni cambiar de precio. El método solo asigna un nuevo valor a `seleccion`; no tiene motivos para modificar la lista.

**Solución razonada:** el botón y el método están dentro del componente dueño de ese estado, por lo que no necesitamos EventCallback. Si se activara la línea del botón sin el método, el error de compilación indicaría una correspondencia incompleta entre vista y código. Si se cambiara `seleccion` pero no la interfaz, revisaríamos el contexto interactivo antes de introducir una operación de red.

### Profundización aplicada: diagnóstico de cinco síntomas parecidos

Una interfaz que «no hace nada» puede fallar por causas distintas. Si el botón no aparece, inspecciona el comentario Razor. Si aparece pero no compila, comprueba el método correspondiente. Si compila pero el clic no actualiza, confirma el modo interactivo y la conexión. Si el clic llega a `Agregar` pero no crea una tarjeta, verifica el valor de `nuevoNombre` y la condición `IsNullOrWhiteSpace`. Si el objeto se añade y no se representa, comprueba que el `foreach` lee la misma colección a la que se ha agregado.

La lección es localizar la fase exacta: **entrada → enlace → evento → estado → representación**. No modifiques `Program.cs` cada vez que un dato es incorrecto, ni cambies el modelo cuando lo que falta es activar un botón. La teoría 3.4 explica las responsabilidades de cada pieza y el comportamiento esperado cuando no existe persistencia.

# P3.5. Comunicación padre–hijo mediante EventCallback

## Objetivo y preparación

En P3.4 el botón estaba en el mismo componente que poseía la lista. Ahora queremos que cada `TarjetaProducto` muestre su propio botón, pero que sea `Productos.razor` quien actualice la selección o quite el elemento. Esta diferencia nos obliga a expresar un **contrato de evento del hijo hacia el padre**. El proyecto se encuentra en `M03_BLAZOR/PROYECTO/3.5/CursoWeb.Blazor/`.

El estado inicial ya compila con tres tarjetas, «Seleccionado: ninguno» y «Total: 3». Los dos archivos que cambiarán son `Components/TarjetaProducto.razor` y `Components/Pages/Productos.razor`. Evita introducir una colección global o compartir campos a través de un singleton; para esta relación directa basta `EventCallback<int>`.

### 3.5.1. Inspeccionar la propiedad de los datos

Detén P3.4, abre 3.5, compila y ejecuta. Comprueba el estado inicial. Abre `Productos.razor` y señala dónde se crea la lista. Abre `TarjetaProducto.razor` y localiza:

~~~csharp
[Parameter, EditorRequired] public Producto Producto { get; set; } = default!;
~~~

Esta propiedad recibe un dato desde el padre. Ahora queremos otro contrato: el hijo comunicará un Id, pero **no será dueño de la lista que el padre representa**. Antes de activar código, dibuja el flujo: parámetro Producto desde padre a hijo; evento de selección desde hijo a padre.

### 3.5.2. Declarar el callback en la tarjeta

En `Components/TarjetaProducto.razor` activa el bloque C# delimitado por `PASO 3.5.2 INICIO / FIN`:

~~~csharp
[Parameter] public EventCallback<int> AlSeleccionar { get; set; }

private Task NotificarSeleccion() =>
    AlSeleccionar.InvokeAsync(Producto.Id);
~~~

Activa también el botón Razor señalado por `PASO 3.5.2 (ACTIVAR)`:

~~~razor
<button @onclick="NotificarSeleccion">Seleccionar</button>
~~~

El botón invoca un método del propio hijo; ese método notifica al callback mediante `InvokeAsync`. De momento no has cambiado el padre. La unidad funcional completa requiere conectar el callback al método que modificará la selección.

### 3.5.3. Conectar el callback al padre

En `Components/Pages/Productos.razor` activa el bloque C# `PASO 3.5.2 INICIO / FIN`:

~~~csharp
private void Seleccionar(int id)
{
    seleccion = productos.First(p => p.Id == id).Nombre;
}
~~~

Busca la línea que representa cada tarjeta:

~~~razor
<TarjetaProducto Producto="producto" />
~~~

El proyecto contiene debajo una variante comentada. **Sustituye la línea activa** por:

~~~razor
<TarjetaProducto Producto="producto" AlSeleccionar="Seleccionar" />
~~~

No debes dejar activas ambas versiones, porque obtendrías seis tarjetas. Guarda, compila y abre `/productos`. Pulsa Seleccionar en Lápiz. Debe aparecer «Seleccionado: Lápiz» en el componente padre. Pulsa Carpeta y comprueba que cambia el texto.

**Explicación:** el hijo no modifica directamente `seleccion`. Comunica el identificador con `EventCallback<int>`; el padre recibe el dato, busca el nombre y cambia un campo propio. Esa separación permite reutilizar TarjetaProducto sin acoplarlo a una única pantalla.

### 3.5.4. Reconstruir la comunicación desde el navegador

Sigue un clic con puntos de interrupción en Visual Studio si lo deseas. El orden debe ser: botón de la tarjeta → `NotificarSeleccion` → `AlSeleccionar.InvokeAsync(Producto.Id)` → método `Seleccionar(int)` del padre → campo `seleccion` → texto actualizado. No hay un nuevo controlador ni una nueva acción POST como en M02.

Como caso negativo de código, si la propiedad `AlSeleccionar` está comentada en la tarjeta pero el padre intenta pasar ese parámetro, puedes obtener un error de compilación o de parámetro desconocido. Si el botón no aparece, revisa el comentario Razor. Si aparecen duplicados, revisa las dos variantes de TarjetaProducto en el padre.

### Reto 3.5 — Solicitar que se quite una tarjeta

**Enunciado:** cada tarjeta tendrá un botón «Quitar». Al pulsarlo, la tarjeta **solicita** al padre que elimine ese Id de la lista en memoria. No debe modificar una colección privada del padre por acceso oculto.

En `Components/TarjetaProducto.razor` activa el bloque `RETO 3.5 INICIO / FIN`:

~~~csharp
[Parameter] public EventCallback<int> AlQuitar { get; set; }

private Task NotificarQuitar() =>
    AlQuitar.InvokeAsync(Producto.Id);
~~~

Y activa el botón del reto:

~~~razor
<button @onclick="NotificarQuitar">Quitar</button>
~~~

En `Components/Pages/Productos.razor` activa el bloque `RETO 3.5 INICIO / FIN`:

~~~csharp
private void Quitar(int id)
{
    productos.RemoveAll(p => p.Id == id);
    seleccion = "ninguno";
}
~~~

Por último, **reemplaza** la versión activa de TarjetaProducto por la tercera variante preparada en el proyecto:

~~~razor
<TarjetaProducto Producto="producto"
                AlSeleccionar="Seleccionar"
                AlQuitar="Quitar" />
~~~

Compila y ejecuta. Selecciona Lápiz y comprueba que el padre refleja su nombre. Ahora pulsa Quitar en esa tarjeta: el total debe pasar de tres a dos y la tarjeta de Lápiz debe desaparecer. Además, la selección vuelve a «ninguno».

**Caso negativo:** al recargar completamente el componente pueden volver los tres productos, porque la lista es local. No interpretes esta operación como un DELETE de SQL Server. La persistencia no es el objetivo de P3.5.

**Solución razonada:** la tarjeta comunica únicamente una intención y el Id del producto. El padre es dueño de la lista, por lo que decide cómo aplicar `RemoveAll`. Esta solución es coherente con el flujo de datos padre→hijo mediante `[Parameter]` y la notificación hijo→padre mediante `EventCallback<int>`. La teoría 3.5 contiene la explicación de ambos contratos.

### Diagnóstico y consolidación

Si al activar el reto el proyecto falla, revisa que el parámetro `AlQuitar` exista en el hijo y que el método `Quitar` exista en el padre. Si se elimina otro elemento, revisa qué Id envía la tarjeta y qué predicado emplea `RemoveAll`. Si un botón de selección no cambia el texto, sigue la cadena `NotificarSeleccion` → `InvokeAsync` → `Seleccionar`. Si se dibujan seis tarjetas, desactiva las variantes de componente que dejaste duplicadas.

El aprendizaje principal no es memorizar una sintaxis: es mantener una correspondencia clara entre **quién posee el dato**, **quién recibe un parámetro** y **quién comunica una intención**. Esta misma separación será útil cuando M04 conecte la interfaz a una API remota.

# P3.6. OnInitializedAsync, servicio en memoria y estados de carga

## Objetivo y punto de partida

Hasta ahora, la página creaba directamente una colección de productos. En esta práctica aprenderemos a pedirlos a un **servicio en memoria asíncrono** mediante inyección de dependencias. El servicio no realiza HTTP ni utiliza base de datos: esa complejidad se introducirá de forma controlada en M04. El proyecto de trabajo es `M03_BLAZOR/PROYECTO/3.6/CursoWeb.Blazor/`.

La página inicial compila y muestra «Servicio pendiente de activar», pero todavía no llama al servicio porque el bloque de `OnInitializedAsync` permanece comentado. De esa manera puedes observar el estado anterior a la carga, activar un cambio identificado y comprobar su efecto en la interfaz.

### 3.6.1. Localizar el servicio y su registro

Abre `Services/IProductosMemoriaService.cs`. La interfaz declara:

~~~csharp
Task<IReadOnlyList<Producto>> ObtenerAsync();
~~~

La implementación `Services/ProductosMemoriaService.cs` devuelve una colección de Cuaderno, Lápiz y Carpeta después de `await Task.Delay(700)`. Esta espera simula una operación asíncrona para poder ver la transición de estados; no representa acceso a una API externa.

En `Program.cs` comprueba el registro:

~~~csharp
builder.Services.AddScoped<IProductosMemoriaService, ProductosMemoriaService>();
~~~

Y en `Components/Pages/Productos.razor` localiza:

~~~razor
@inject IProductosMemoriaService Catalogo
~~~

El componente solicita una dependencia por interfaz y la recibe del contenedor de ASP.NET Core. El alumno ya conoce el concepto de inyección de dependencias de otros ámbitos de .NET; ahora observa cómo participa en un componente Razor.

### 3.6.2. Ejecutar el estado inicial sin activar el método

Detén P3.5, abre 3.6, compila y ejecuta. Abre `/productos`. Debes encontrar el texto «Servicio pendiente de activar» y ninguna tarjeta. Observa los campos en `@code`:

~~~csharp
private IReadOnlyList<Producto> productos = Array.Empty<Producto>();
private bool cargando = true;
private string estado = "Servicio pendiente de activar";
~~~

Este estado inicial no está «mal hecho»: la interfaz no llama aún al servicio y, por tanto, no tiene datos que representar. La finalidad del paso es comprobar que el alumno entiende la diferencia entre **un componente existente** y **un componente que ya cargó sus datos**.

### 3.6.3. Activar OnInitializedAsync

En `Components/Pages/Productos.razor` retira los delimitadores C# del bloque `PASO 3.6.2 INICIO / FIN`. El método activo debe quedar:

~~~csharp
protected override async Task OnInitializedAsync()
{
    estado = "Cargando productos...";
    productos = await Catalogo.ObtenerAsync();
    cargando = false;
    estado = "Lista preparada";
}
~~~

Guarda, compila y recarga `/productos`. Primero debe aparecer «Cargando productos...»; cuando el servicio termine, debe mostrarse «Lista preparada» y tres tarjetas. Si no alcanzas a leer el primer mensaje por la velocidad del equipo, recuerda que la espera controlada se encuentra en el servicio y no en la vista.

El método no lo llama el alumno desde un botón: **Blazor lo invoca durante la inicialización del componente**. Tampoco es el handler `OnGet` de una Razor Page; esos nombres pertenecen a modelos diferentes. La propiedad `productos` se llena después del `await` y el estado de la interfaz cambia.

### 3.6.4. Interpretar el marcado condicional

En la misma página encontrarás:

~~~razor
<p id="estado-carga">@estado</p>
@if (!cargando && productos.Count > 0)
{
    <div class="tarjetas" id="tarjetas-productos">
        @foreach (var producto in productos)
        {
            <TarjetaProducto Producto="producto" />
        }
    </div>
}
~~~

La bandera `cargando` impide representar tarjetas mientras la operación no ha terminado. El valor de `productos.Count` determina si existe algo que mostrar. Esta separación permite razonar sobre estados reales y no sobre una pantalla que «a veces aparece y a veces no».

**Caso negativo reversible:** comenta temporalmente la asignación `cargando = false`, recompila y observa que, aun después de que el servicio devuelva objetos, la condición de la página no permite representar tarjetas. Restablece la asignación. El resultado ilustra que obtener datos y habilitar su representación son dos operaciones conectadas, pero distintas.

### 3.6.5. Comprender la elección de prerenderizado

En la cabecera de `Productos.razor` aparece:

~~~razor
@rendermode @(new InteractiveServerRenderMode(prerender: false))
~~~

La página desactiva el prerenderizado para facilitar una observación controlada de la carga y evitar una ejecución duplicada durante las fases de prerenderizado e inicialización interactiva. No lo interpretes como recomendación general para producción: el prerenderizado puede ser útil para presentar contenido antes de que la interactividad esté conectada.

En la teoría 3.6 se explica que `OnInitializedAsync` puede ejecutarse dos veces con prerenderizado. La práctica principal no implementa persistencia de estado de prerenderizado ni estrategias avanzadas de caché; basta comprender la razón de esta elección y saber localizarla.

### Reto 3.6 — Lista vacía después de una carga correcta

**Enunciado:** muestra una indicación legible cuando el servicio ha terminado pero no hay productos. La pantalla debe distinguir «cargando» de «terminado con lista vacía».

Activa el comentario Razor `RETO 3.6 (ACTIVAR)`:

~~~razor
@if (!cargando && productos.Count == 0)
{
    <p id="sin-productos">No hay productos para mostrar.</p>
}
~~~

Para probar el caso negativo, abre `Services/ProductosMemoriaService.cs` y sustituye temporalmente el bloque de retorno de tres productos por:

~~~csharp
return Array.Empty<Producto>();
~~~

**Importante:** reemplaza la instrucción `return` original, no añadas otra después de ella. Compila, abre `/productos` y observa que la carga termina con «Lista preparada» y el mensaje «No hay productos para mostrar», sin tarjetas. Esto no es un error de HTTP ni una excepción: el servicio ha devuelto una colección vacía válida.

**Resultado positivo complementario:** restaura la lista original del servicio y recarga. Deben volver a mostrarse tres tarjetas y el mensaje de lista vacía no debe aparecer. La solución es una condición Razor dependiente de `cargando` y del número de elementos; no se necesita una API ni un nuevo componente.

### Cierre y transferencia a M04

Al terminar M03 debes poder explicar un recorrido completo de Blazor: una ruta selecciona un componente, un parámetro entrega datos a una tarjeta, un evento modifica estado, un callback notifica al padre, un servicio se obtiene mediante inyección y `OnInitializedAsync` carga una colección. Las pruebas realizadas deben relacionar cada comportamiento con sus archivos concretos; no basta con decir que los seis proyectos compilan.

En M04 sustituiremos o complementaremos el servicio en memoria por llamadas `HttpClient` a una API auxiliar suministrada por el curso. Precisamente por eso no adelantamos HTTP en P3.6: necesitamos que el alumno comprenda antes los componentes, su ciclo de vida y sus estados.

## Autoevaluación integradora

Al final del módulo, abre P3.6 y describe cinco diferencias entre la aplicación MVC A y la aplicación Blazor B sin recurrir a generalidades. Señala el lugar donde se configura Interactive Server; cómo se declara una ruta `@page`; cómo una tarjeta recibe un producto; cómo un método de clic actualiza un texto; y cómo el servicio obtiene datos sin que la página sepa dónde se construye su colección.

Si puedes relacionar estos cinco aspectos con código real, explicar un caso positivo y negativo y distinguir estado de componente de persistencia, habrás alcanzado el objetivo de la jornada. No hay que construir todavía un CRUD nuevo ni desplegar infraestructura adicional.

## Fuentes de consulta

- Microsoft Learn: [Fundamentos de Blazor](https://learn.microsoft.com/en-us/aspnet/core/blazor/?view=aspnetcore-8.0).
- Microsoft Learn: [Modos de renderizado](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/render-modes?view=aspnetcore-8.0).
- Microsoft Learn: [Componentes, parámetros y composición](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/?view=aspnetcore-8.0).
- Microsoft Learn: [Eventos y EventCallback](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/event-handling?view=aspnetcore-8.0).
- Microsoft Learn: [Ciclo de vida de los componentes](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/lifecycle?view=aspnetcore-8.0).

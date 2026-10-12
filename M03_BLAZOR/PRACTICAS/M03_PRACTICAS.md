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

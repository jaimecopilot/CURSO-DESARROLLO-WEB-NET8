# M01 — Fundamentos de ASP.NET Core MVC
## Cuaderno de prácticas

### Índice del módulo

- **P1.1. Primera aplicación MVC y recorrido de una petición HTTP**
- P1.2. El flujo Modelo–Vista–Controlador
- P1.3. Estructura y convenciones del proyecto
- P1.4. Controladores, acciones, parámetros y rutas
- P1.5. Vistas tipadas, layout, parciales y navegación

# P1.1. Primera aplicación MVC y recorrido de una petición HTTP

## A. Identificación

**Objetivo.** Crear una aplicación MVC a partir de la plantilla de .NET 8, ejecutar el proyecto inicial suministrado en el curso, observar una petición real y distinguir los cambios en las cabeceras HTTP de los cambios en el HTML generado por una vista Razor.

**Teoría relacionada.** Punto 1.1, especialmente flujo HTTP, diferencia MVC/API, papel de Kestrel, `Program.cs`, acción MVC, vista Razor y cabeceras HTTP.

**Conocimientos previos.** C# básico, uso de una terminal, HTTP GET y experiencias anteriores con Web API. No se requiere conocer Razor ni su sintaxis en profundidad.

**Producto de esta práctica.** Una aplicación MVC que responde en `http://localhost:5091/`, cuyo estado inicial ya está dispuesto en el repositorio y cuyos dos pequeños cambios pueden activarse de forma independiente.

## B. Preparación

### Herramientas y dependencias

Se necesita .NET SDK 8, navegador, editor C# (preferentemente Visual Studio con soporte ASP.NET Core) y Git. La práctica se describe con comandos de la CLI de .NET, equivalentes al botón de ejecución de Visual Studio. Para inspeccionar HTTP usaremos la pestaña *Red/Network* del navegador; como comprobación alternativa puede usarse `curl.exe` en Windows o `curl` en Linux/macOS.

Comprobar el SDK:

~~~bash
dotnet --list-sdks
~~~

**Resultado esperado:** al menos una entrada cuya versión comience por `8.0.`. Una versión posterior no sustituye necesariamente al SDK 8 en la ejecución de esta práctica, cuyo proyecto apunta explícitamente a `net8.0`.

### Obtener el estado inicial exacto

En una carpeta de trabajo elegida por el alumno:

~~~bash
git clone --branch desarrollo/m01-mvc https://github.com/jaimecopilot/CURSO-DESARROLLO-WEB-NET8.git
cd CURSO-DESARROLLO-WEB-NET8
~~~

El proyecto del capítulo está ubicado en:

~~~text
M01_MVC/
  PROYECTO/
    1.1/
      CursoWeb.Mvc/
        CursoWeb.Mvc.csproj
        Program.cs
        Controllers/
          HomeController.cs
        Views/
          _ViewImports.cshtml
          _ViewStart.cshtml
          Home/
            Index.cshtml
          Shared/
            _Layout.cshtml
        wwwroot/
          css/
            site.css
        appsettings.json
        Properties/
          launchSettings.json
~~~

Este árbol identifica **todos los archivos necesarios** para el primer recorrido. No necesita base de datos, credenciales ni servicios externos. La práctica no depende del código de ningún otro curso.

**Estado inicial para los bloques activables:** la cabecera `X-Curso-Paso` está comentada en el controlador y el bloque `marca-paso-1-1-5` está dentro de un comentario Razor. Por tanto, la página se muestra, pero aún no incorpora las dos variaciones.

## C. Desarrollo paso a paso

### Paso 1.1.1 — Crear una aplicación ASP.NET Core MVC desde la plantilla

Primero generaremos una aplicación de prueba para identificar la plantilla oficial sin modificar el proyecto docente.

Estando en la **raíz del repositorio**, ejecutar:

~~~bash
dotnet new mvc -f net8.0 --no-https -n PlantillaMvc -o .work/PlantillaMvc
~~~

**Qué hace cada opción:**

- `dotnet new mvc` utiliza la plantilla de aplicación web MVC instalada con el SDK.
- `-f net8.0` establece el framework de destino.
- `--no-https` simplifica exclusivamente esta primera prueba HTTP local; no se trata de una recomendación de producción.
- `-n PlantillaMvc` nombra el proyecto temporal.
- `-o .work/PlantillaMvc` coloca los archivos en una carpeta descartable excluida de Git.

Para ver que la plantilla es ejecutable:

~~~bash
dotnet run --project .work/PlantillaMvc/PlantillaMvc.csproj --no-launch-profile --urls http://localhost:5095
~~~

Abrir `http://localhost:5095/`. Debe aparecer la página inicial de la plantilla MVC, con su navegación y su diseño estándar. Detener el proceso con **Ctrl+C**.

**Qué acabamos de comprobar:** la plantilla genera una aplicación con código servidor, vistas Razor y recursos estáticos. No se ha creado una API REST; se ha creado una web que produce HTML.

El resto de la práctica usará el proyecto **CursoWeb.Mvc** del repositorio, de contenido controlado y vinculado exactamente con este cuaderno. No se debe sustituir ese proyecto por `PlantillaMvc`, porque contienen vistas y nombres distintos.

### Paso 1.1.2 — Abrir y ejecutar el proyecto del curso

Desde la raíz del repositorio:

~~~bash
cd M01_MVC/PROYECTO/1.1/CursoWeb.Mvc
dotnet restore
dotnet build
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

**Alternativa Visual Studio:** abrir `CursoWeb.Mvc.csproj`, seleccionar el perfil de ejecución local `CursoWeb.Mvc` (HTTP) y ejecutar. Comprobar el puerto mostrado en la salida. Si se utiliza otro puerto desde Visual Studio, todas las URL siguientes deben adaptarse a ese valor.

Esperar a que la consola indique que el servidor escucha en `http://localhost:5091`. Abrir esa dirección en el navegador.

**Resultado esperado visible:**

- Un enlace `Inicio` en la cabecera.
- El título `1.1 | Primer recorrido MVC`.
- El texto `Esta página HTML ha sido generada en el servidor mediante una acción MVC.`.
- El mensaje `Respuesta HTTP correcta: aplicación MVC disponible.`.
- Un pie con `Curso ASP.NET Core MVC · .NET 8`.

No debe aparecer todavía `Contenido añadido durante la práctica`. Si aparece, probablemente el bloque del paso 1.1.5 ya esté activado.

**Qué ocurre internamente:** Kestrel recibe la petición a `/`. La ruta predeterminada selecciona `HomeController.Index()`. La acción devuelve `View()` y MVC renderiza la vista `Views/Home/Index.cshtml`, rodeada por `Views/Shared/_Layout.cshtml`. El navegador recibe el HTML y solicita después la hoja de estilos. Es el primer recorrido extremo a extremo de la aplicación.

### Paso 1.1.3 — Inspeccionar petición, ruta y archivos responsables

Con la página abierta, pulsar **F12** (o abrir las herramientas para desarrolladores del navegador), seleccionar **Red/Network** y recargar la página. Si no aparece ninguna fila, mantener abierta la pestaña de red y volver a recargar.

Seleccionar la solicitud de tipo **document** cuyo destino sea `http://localhost:5091/`. Identificar:

1. **Request URL:** `http://localhost:5091/`.
2. **Request Method:** `GET`.
3. **Status Code:** `200`.
4. **Response Headers:** una cabecera `Content-Type` cuyo valor comienza por `text/html`.
5. **Response/Respuesta:** el cuerpo HTML; buscar el texto `Primer recorrido MVC`.

También aparecerá una petición a `/css/site.css`, con tipo de contenido CSS. Esa solicitud es otro recorrido HTTP: el recurso físico está bajo `wwwroot/css/site.css` y lo puede devolver el middleware de archivos estáticos.

Ahora abrir en el editor los cuatro archivos siguientes, **sin modificarlos todavía**:

- `Program.cs`: localizar `AddControllersWithViews()`, `UseStaticFiles()` y `MapControllerRoute(...)`.
- `Controllers/HomeController.cs`: localizar la acción `Index()` y su `return View();`.
- `Views/Home/Index.cshtml`: localizar el `<h1>` que aparece en el navegador.
- `Views/Shared/_Layout.cshtml`: localizar la navegación y `@RenderBody()`.

Seguir mentalmente el recorrido **URL → ruta → controlador → vista → layout → HTML**. Anotar qué archivo determina la URL y qué archivo contiene el texto visible. Es importante diferenciar esos dos conceptos antes de añadir más acciones en 1.4.

**Comprobación HTTP alternativa** (manteniendo abierta la aplicación, en una segunda terminal):

~~~bash
curl -i http://localhost:5091/
~~~

En Windows PowerShell también puede utilizarse `curl.exe -i http://localhost:5091/`. La salida debe mostrar una línea de estado `200 OK`, cabeceras y HTML. Las cabeceras concretas pueden variar según sistema y servidor; no se exige un orden determinado.

### Paso 1.1.4 — Activar una cabecera HTTP desde la acción

Dejar de ejecutar la aplicación mediante **Ctrl+C** antes de modificar y volver a construir. Abrir `Controllers/HomeController.cs` y localizar:

~~~csharp
// PASO 1.1.4 — Descomentar solo la siguiente línea para observar
// una cabecera de respuesta HTTP generada desde el controlador.
// Response.Headers["X-Curso-Paso"] = "1.1.4";
~~~

Quitar las dos barras `//` **solo** delante de la asignación; las líneas explicativas permanecen comentadas. El fragmento activo quedará así:

~~~csharp
Response.Headers["X-Curso-Paso"] = "1.1.4";
return View();
~~~

Guardar y ejecutar de nuevo:

~~~bash
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

Recargar la página y observar las cabeceras de **respuesta** en F12 → Red. Debe aparecer:

~~~http
X-Curso-Paso: 1.1.4
~~~

También se puede comprobar con `curl -i http://localhost:5091/`.

**Qué hemos aprendido:** la cabecera se añade desde el controlador a la respuesta HTTP, pero no altera el título ni el texto HTML. Si solo miramos la pantalla, podemos pensar incorrectamente que el cambio no se ha aplicado.

**Comprobación negativa:** la cabecera no tiene por qué aparecer en la petición CSS, porque ese archivo estático no lo sirve la acción `Index()`. La respuesta de la página y la respuesta de la hoja de estilos proceden de solicitudes diferentes.

### Paso 1.1.5 — Activar un bloque HTML de la vista Razor

Detener de nuevo la aplicación. Abrir `Views/Home/Index.cshtml`. Al final aparece este fragmento:

~~~cshtml
@* PASO 1.1.5 (inicio)
<section id="marca-paso-1-1-5">
    <h2>Contenido añadido durante la práctica</h2>
    <p>El navegador ha recibido una nueva versión de la vista Razor.</p>
</section>
PASO 1.1.5 (fin) *@
~~~

En Razor, `@*` abre un comentario de servidor y `*@` lo cierra. **Mientras los delimitadores sigan presentes, el bloque HTML no llegará al navegador**.

Eliminar completamente la línea `@* PASO 1.1.5 (inicio)` y la línea `PASO 1.1.5 (fin) *@`, pero **conservar el bloque `<section>` interior**. Debe quedar:

~~~cshtml
<section id="marca-paso-1-1-5">
    <h2>Contenido añadido durante la práctica</h2>
    <p>El navegador ha recibido una nueva versión de la vista Razor.</p>
</section>
~~~

Guardar, reiniciar `dotnet run` y recargar. En la página, debajo del mensaje inicial, debe verse **Contenido añadido durante la práctica**. En F12 → Red → Response debe aparecer también el elemento `<section id="marca-paso-1-1-5">`.

**Qué hemos aprendido:** modificar una vista modifica el cuerpo HTML de la respuesta. La URL `/` y la acción `Index()` siguen siendo las mismas; ahora el navegador dispone de más elementos para representar.

Los pasos 1.1.4 y 1.1.5 son **compatibles**. Se pueden mantener activados simultáneamente: el primero añade una cabecera, mientras que el segundo añade contenido.

### Paso 1.1.6 — Comprobar una ruta válida alternativa y un 404

Con la aplicación ejecutándose, abrir estas direcciones:

~~~text
http://localhost:5091/
http://localhost:5091/Home/Index
http://localhost:5091/ruta-inexistente
http://localhost:5091/css/site.css
~~~

La primera y la segunda URL deben mostrar **la misma página**. La segunda expresa explícitamente controlador y acción; la primera utiliza los valores por defecto de la ruta convencional.

La tercera debe responder con **404 Not Found**, porque no tenemos una acción correspondiente a `ruta-inexistente`. Es normal que su apariencia sea distinta de la de la página válida: el servidor ha respondido, pero no dispone de una página para ese destino.

La cuarta debe mostrar el texto CSS, no una vista MVC. Esto confirma que una aplicación ASP.NET Core puede servir distintos tipos de recursos HTTP.

Con una segunda terminal, comprobar el 404 sin depender de cómo lo representa el navegador:

~~~bash
curl -i http://localhost:5091/ruta-inexistente
~~~

Si los códigos de respuesta no coinciden con lo esperado, revisar el puerto, la URL exacta y que se esté ejecutando el proyecto `CursoWeb.Mvc` en lugar de `PlantillaMvc`.

## D. Ejecución completa y resultados esperados

Al terminar los cambios, mantener el proceso MVC en ejecución con `dotnet run --no-launch-profile --urls http://localhost:5091`. Al visitar `/` deben coexistir: un código HTTP **200**, la cabecera `X-Curso-Paso: 1.1.4` y el contenido HTML añadido en el paso 1.1.5. La hoja de estilos debe cargarse; la URL desconocida debe responder 404.

Este es el comportamiento observable que prueba que los dos fragmentos están activados y que el recorrido principal funciona.

## E. Comprobación funcional del alumno

| Caso que se debe probar | Operación | Resultado correcto |
|---|---|---|
| Plantilla oficial | Abrir el sitio temporal en 5095 tras `dotnet new mvc` | Página de bienvenida MVC |
| Aplicación del curso | GET `/` en 5091 | 200 y encabezado `Primer recorrido MVC` |
| Cabecera del controlador | GET `/` tras activar 1.1.4 | `X-Curso-Paso: 1.1.4` |
| Contenido de la vista | GET `/` tras activar 1.1.5 | Visible `Contenido añadido durante la práctica` |
| Ruta alternativa | GET `/Home/Index` | 200 y mismo contenido |
| Ruta inexistente | GET `/ruta-inexistente` | 404 |
| Recurso estático | GET `/css/site.css` | 200 y contenido CSS |

La prueba automatizada del proyecto comprueba los recorridos HTTP de la aplicación del curso, incluidos los estados base y activado. Se puede ejecutar desde la raíz del repositorio con `bash M01_MVC/TESTS/1.1_e2e.sh` si se dispone de Bash, curl, Python 3 y SDK 8. La creación de la plantilla temporal es una operación didáctica guiada y no modifica la aplicación distribuida.

**Criterio de finalización:** el alumno debe poder señalar, sobre una petición real, dónde están el método GET, el código 200/404, el encabezado de respuesta, la acción MVC y el HTML de la vista.

## F. Problemas frecuentes y soluciones

**La terminal indica que `dotnet` no existe.** El SDK no está instalado o no está disponible en el PATH. Instalar o reparar SDK .NET 8 y comprobar `dotnet --list-sdks` antes de continuar.

**`dotnet new mvc -f net8.0` no reconoce el framework.** Comprobar con `dotnet --info` que el SDK 8 está instalado y que no existe un `global.json` que obligue a otro SDK incompatible. No cambiar a net9.0 o net10.0 para continuar el curso.

**El puerto 5091 está ocupado.** Cerrar otra instancia de la misma aplicación o identificar qué proceso usa el puerto. Es posible seleccionar temporalmente otro puerto mediante `--urls`, pero en ese caso habrá que actualizar todas las URL de la práctica.

**Se abre la plantilla en lugar de la página del curso.** Se está ejecutando `PlantillaMvc` en el puerto 5095 o se abrió otro proyecto. Detener esa aplicación y arrancar desde `M01_MVC/PROYECTO/1.1/CursoWeb.Mvc` en 5091.

**El navegador muestra una pantalla de error de conexión.** A diferencia de un HTTP 404, eso suele significar que no existe un servidor escuchando en ese puerto o que se cerró el proceso. Comprobar la consola de `dotnet run`.

**No aparece la cabecera personalizada.** Comprobar que se quitó el comentario de la línea correcta, que el archivo se guardó, que el proceso se reconstruyó y que se está inspeccionando la respuesta de `/`, no la de `site.css`.

**No aparece el contenido adicional en la vista.** Revisar que se quitaron *ambos* delimitadores de comentario Razor, que se mantuvo intacto el elemento `<section>` y que se recargó el documento. Para descartar una copia anterior usar una actualización completa en el navegador.

**Se recibe un 404 en `/Home/Index`.** Verificar que existen `HomeController` e `Index()`, el patrón de `MapControllerRoute` y que se ejecuta la aplicación del curso. En 1.4 veremos cómo diagnosticar errores de rutas con mayor detalle.

**En Windows, `curl` parece devolver un objeto en vez de texto HTTP.** Dependiendo de la versión de PowerShell, `curl` puede ser un alias de otro comando. Ejecutar `curl.exe -i http://localhost:5091/` o usar la pestaña Red del navegador.

## G. Ejercicio de consolidación

Sin crear nuevos controladores ni copiar código externo, explica y comprueba lo siguiente:

1. Abre sucesivamente `/` y `/Home/Index`, y verifica que ambas rutas producen la misma página. Identifica en `Program.cs` qué valores predeterminados permiten la primera URL.
2. Compara la solicitud del documento principal con la de `/css/site.css`: observa método, código, tipo de contenido y la presencia o ausencia de la cabecera `X-Curso-Paso`.
3. Responde: «¿Por qué la aplicación puede responder correctamente 200 a `/` y 404 a otra ruta sin haber dejado de funcionar?». Justifica la respuesta desde la selección de endpoints.
4. Señala cuál de los pasos 1.1.4 y 1.1.5 modifica una cabecera HTTP y cuál modifica el cuerpo de respuesta. Compruébalo con las herramientas de red.

**Resultado de consolidación:** puedes explicar el recorrido de una solicitud, no solo reproducir comandos. Esta comprensión será necesaria para organizar modelos, controladores y vistas en los siguientes puntos del módulo.

## H. Continuidad del proyecto

**Conservar el proyecto CursoWeb.Mvc y los archivos modificados.** En los siguientes capítulos añadiremos modelos de productos, nuevas acciones y vistas sin repetir toda la creación inicial. No introducimos EF Core todavía: aparecerá en el día 2. La aplicación temporal `.work/PlantillaMvc` se puede eliminar una vez comprendida la plantilla.

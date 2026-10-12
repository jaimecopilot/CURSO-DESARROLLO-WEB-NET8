# Guía docente — Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8

## Destinatarios y finalidad

Formación presencial de 30 horas lectivas (lunes–viernes, 6 h cada mañana), con prioridad práctica. El alumnado domina C#, programación asíncrona básica, ASP.NET Core Web API y Entity Framework Core; no se vuelve a impartir esas materias. No se da por conocido MVC, Razor Pages, Blazor, IIS ni Docker.

Dos aplicaciones pequeñas, con dominio de productos:
- **A (MVC)**, días 1–2: controladores, vistas Razor, formularios, validación y persistencia SQL Server Express LocalDB con EF Core.
- **B (Blazor Web App, Interactive Server)**, días 3–5: componentes, eventos, binding, servicios y consumo de una API REST auxiliar con datos en memoria.
- **API auxiliar**: parte del material proporcionado; solo GET/POST y gestión simple de errores. No se enseña Web API de nuevo.
- **Seguridad**: demostración preconfigurada y explícitamente limitada; no implementar Identity desde cero.
- **Publicación**: mismo proyecto MVC A para las prácticas Kestrel, IIS y Docker; B se consolida en la primera práctica del quinto día.

## Método de impartición

Cada punto numerado se imparte en el orden: concepto → funcionamiento → ejemplo mínimo → explicación del código → práctica con estado inicial conocido → ejecución y observación → variante de consolidación → dudas.

El docente no debe ejecutar todas las operaciones por el alumno. La mayor parte del tiempo práctico se reserva para que cada persona realice, compruebe y corrija la actividad. Los bloques de código activables/desactivables y las variantes de archivos deben estar asociados de forma inequívoca al número de paso del PDF.

## Plan de jornadas

La matriz exacta de duración por punto y ejercicio se encuentra en TEMARIO_30H.md. Las pautas de acompañamiento son:

### Día 1 — MVC (120 min teoría, 210 min práctica, 30 min dudas)

Explicar el recorrido petición→routing→acción→vista; mostrar las convenciones sin tratar todavía persistencia ni seguridad. Acompañar especialmente P1.4 (parámetros/routing, 95 min totales) y P1.5 (tipado de vistas y parciales, 70 min). Salida: listado y detalle navegables con datos fijos.

### Día 2 — Formularios y Razor Pages (120/210/30)

Centrar la explicación en model binding, antiforgery, Tag Helpers y ModelState. El CRUD P2.4 concentra 115 minutos; se reutiliza EF Core que el alumnado ya conoce. Mantener el ejemplo Razor Pages P2.5 deliberadamente pequeño. Salida: CRUD válido con errores de formulario visibles y SQL Server Express LocalDB.

### Día 3 — Blazor (120/210/30)

Comparar explícitamente las vistas Razor de MVC con los componentes Razor de Blazor y Razor Pages; no confundir su modelo de ejecución. Destacar renderizado interactivo en servidor, @onclick, @bind, parámetros, EventCallback y OnInitializedAsync. Los componentes se activan sobre B; no introducir JS interop ni WebAssembly autónomo.

### Día 4 — API y seguridad (90/240/30)

La API mínima se entrega ya compilable para evitar la dependencia imposible de P4.1 con P4.3. El docente la arranca al comienzo del día y muestra su dirección local. P4.1 verifica GET/POST y errores; P4.2 separa llamadas HTTP en un servicio; P4.3 permite estudiar y modificar la API; P4.4 demuestra acceso autenticado/protegido sin detallar todo Identity. No convertir 4.4 en una implementación empresarial.

### Día 5 — Proyecto y despliegue (60/270/30)

Destinar 90 min prácticos a consolidar Blazor B, NO construir una tercera aplicación. Preparar por adelantado el host Windows de IIS, Hosting Bundle, credenciales de laboratorio, Docker Engine y puertos. Ejecutar la misma A en Kestrel, IIS y Docker, con rutas y puertos distintos. Se demuestran conceptos, no seguridad de producción ni administración del servidor.

## Gestión de errores y contingencias

- **El estudiante no consigue compilar:** comprobar SDK 8, directorio actual, paquetes, sintaxis y estado correcto de los bloques activados antes de avanzar.
- **No aparece una vista MVC:** comprobar nombre de acción, carpeta Views y firma del modelo.
- **El formulario no envía o valida:** comprobar método HTTP, Tag Helpers, token antiforgery, ModelState y etiquetas de errores.
- **Blazor parece estático:** comprobar el modo de renderizado interactivo; explicar que no basta con escribir @onclick si el componente no es interactivo.
- **API no responde:** verificar que está iniciada, puerto real, URL del servicio y códigos de respuesta. Usar URL independiente por proceso.
- **IIS falla al arrancar:** verificar versión de Hosting Bundle, registro del módulo ASP.NET Core, App Pool, permisos de archivos y diagnóstico local.
- **Docker no expone la web:** verificar motor activo, nombre de imagen y mapeo puerto-host:8080-contenedor para la imagen ASP.NET Core 8.
- **Falta infraestructura preparada:** registrar la práctica como no ejecutada y utilizar únicamente la demostración prevista; no presentar como realizada una práctica no ejecutada.

## Evaluación funcional mínima

Se considera completado M01 cuando listado/detalle y navegación funcionan; M02 cuando un producto se crea, edita, elimina y la validación falla/funciona donde corresponde; M03 cuando componentes padre/hijo y eventos actualizan la pantalla; M04 cuando Blazor consume GET/POST y distingue accesos anónimos de autenticados en la demo; M05 cuando se ejecuta/publica la misma aplicación bajo tres mecanismos y el proyecto Blazor final funciona.

Cada estado intermedio indicado al alumno debe estar acompañado de instrucciones de activación y comprobaciones que pueda realizar desde el navegador o la consola.

## Regla obligatoria para los retos

Los **retos y ejercicios de consolidación con código** son parte del material práctico, no sugerencias vagas. Cada reto programable debe contener dentro de `Mxx_PRACTICAS.md`: enunciado, objetivo, preparación, ubicación exacta de los archivos, código completo que se activa o cambia, explicación de cada cambio, comandos de ejecución, resultado esperado y soluciones razonadas para consulta. El código debe estar **también en el proyecto del capítulo**, identificado mediante comentarios o variantes reproducibles para que el alumno comente y descomente los bloques adecuados. Si un cambio no puede expresarse en comentarios sin invalidar el archivo, se proporciona una variante completa de ese archivo con instrucciones precisas.

Cada reto programable debe poder compilarse y ejecutarse en los estados propuestos, incluyendo comprobaciones observables y continuidad de los ejercicios anteriores. El reto puede ser una variante breve de un paso anterior; no debe introducir contenidos fuera del temario ni sobrepasar el tiempo práctico asignado. Los retos conceptuales o de observación no necesitan bloques de código artificiales, pero sí un resultado comprobable.

**Criterio de cierre de capítulo:** teoría, ejercicios guiados **y retos** explicados en Markdown, código localizado en el proyecto y pruebas realmente ejecutadas; nunca considerar completo un reto si solo figura un enunciado o una respuesta verbal.

## Política editorial

Material docente por módulo: TEORIA/Mxx_TEORIA.md, PRACTICAS/Mxx_PRACTICAS.md y sus dos PDF. Construcción punto a punto: cada capítulo N.N se añade a los documentos acumulativos del módulo. Un capítulo reúne teoría completa, práctica íntegra y un proyecto cuyo código corresponde a los pasos descritos. Generar PDF solo al cerrar los Markdown. No incluir anotaciones internas de edición, auditorías ni informes de CI en el material del alumno.

Los tiempos de la matriz son planificaciones docentes; el ajuste real se confirmará tras una clase piloto, sin sumar temas fuera del alcance.

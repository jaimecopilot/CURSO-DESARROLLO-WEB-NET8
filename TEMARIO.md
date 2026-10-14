# Temario — Desarrollo web con ASP.NET Core MVC, Razor y Blazor en .NET 8

## M01 — Fundamentos de ASP.NET Core MVC

### 1.1. Introducción a ASP.NET Core MVC
- ASP.NET Core y arquitectura de aplicaciones web.
- Peticiones y respuestas HTTP; generación de HTML en el servidor.
- Diferencias entre una aplicación MVC y una API Web.

### 1.2. Arquitectura Modelo–Vista–Controlador
- Responsabilidades y separación entre modelos, vistas y controladores.
- Flujo de una petición: enrutamiento, acción del controlador, datos del modelo y vista Razor.
- Transferencia de datos del controlador a una vista.

### 1.3. Estructura y configuración de un proyecto MVC
- Estructura del proyecto ASP.NET Core: `Program.cs`, `Controllers`, `Models`, `Views` y `wwwroot`.
- Configuración de servicios y del procesamiento de solicitudes.
- Convenciones de nombres, archivos de configuración y recursos estáticos.
- Modelos y datos de ejemplo.

### 1.4. Controladores, acciones y enrutamiento
- `Controller`, acciones y resultados de acción.
- Rutas convencionales y rutas por atributos.
- Parámetros de ruta, identificadores y navegación.
- Listados, detalles y respuestas HTTP 200 y 404.

### 1.5. Vistas Razor
- Sintaxis Razor y expresiones C# en vistas `.cshtml`.
- Vistas tipadas y acceso a propiedades del modelo.
- `_Layout`, secciones y elementos comunes de navegación.
- Vistas parciales y representación reutilizable de productos.

## M02 — Formularios, validación y Razor Pages

### 2.1. Formularios web y vinculación de modelos
- Formularios HTML y diferencias entre GET y POST.
- Envío, recepción y vinculación de datos mediante *model binding*.
- Acciones para mostrar y procesar formularios.
- Protección frente a falsificación de solicitudes mediante *antiforgery*.

### 2.2. Tag Helpers
- Generación de formularios, campos y enlaces con Tag Helpers.
- `asp-for`, `asp-action` y atributos relacionados.
- Asociación entre propiedades del modelo y controles HTML.
- Visualización de mensajes de validación.

### 2.3. Validación de datos
- DataAnnotations: `Required`, `StringLength` y `Range`.
- `ModelState` y validación del lado del servidor.
- Validación del lado del cliente y presentación de errores.
- Conservación de los valores introducidos tras una entrada inválida.

### 2.4. CRUD con Entity Framework Core
- Integración de EF Core 8 con una aplicación MVC.
- SQL Server Express LocalDB y cadena de conexión.
- `DbContext` y modelo de producto.
- Listado, creación, consulta de detalles, edición y eliminación.
- Persistencia de datos y comprobación de los cambios tras reiniciar la aplicación.

### 2.5. Introducción a Razor Pages
- Conceptos de Razor Pages y `PageModel`.
- Métodos `OnGet` y `OnPost`.
- Lectura de información y tratamiento de un formulario sencillo.
- Comparación entre Razor Pages y controladores/vistas MVC dentro de una aplicación ASP.NET Core.

## M03 — Blazor Web App y componentes

### 3.1. Introducción a Blazor
- Blazor Web App en .NET 8 y comparación con ASP.NET Core MVC.
- Renderizado estático del lado del servidor y renderizado interactivo.
- Blazor Interactive Server: funcionamiento y conexión con el navegador.
- Diferencias conceptuales entre ejecución en servidor y WebAssembly.

### 3.2. Estructura de una aplicación Blazor
- Organización de componentes Razor y páginas `.razor`.
- Directivas, rutas, navegación y estructura compartida.
- Creación de páginas y enlaces entre componentes.

### 3.3. Componentes reutilizables
- Parámetros de componentes con `[Parameter]`.
- Composición y reutilización de componentes.
- Representación de colecciones mediante tarjetas de producto.
- Comunicación de datos del componente padre al componente hijo.

### 3.4. Eventos, enlace de datos y estado
- Eventos interactivos y `@onclick`.
- Enlace de datos mediante `@bind`.
- Estado interno del componente y actualización de la interfaz.
- Selección y modificación de elementos de una colección en memoria.

### 3.5. Comunicación entre componentes
- Parámetros de entrada y `EventCallback`.
- Comunicación del componente hijo al padre.
- Notificación de selecciones y solicitudes de eliminación.
- Actualización de colecciones y representación del estado.

### 3.6. Ciclo de vida de componentes
- `OnInitializedAsync` e inicialización asíncrona.
- Servicios de datos en memoria e inyección de dependencias.
- Estados de carga y visualización de datos disponibles.
- Tratamiento básico de errores durante la inicialización.

## M04 — Integración con APIs y seguridad básica

### 4.1. Consumo de APIs HTTP desde Blazor
- `HttpClient`, peticiones GET y POST y programación asíncrona.
- Transferencia de datos mediante JSON y objetos DTO.
- Consulta de catálogos y envío de nuevos productos.
- Códigos de respuesta HTTP y errores de comunicación, servidor y deserialización.

### 4.2. Servicios e inyección de dependencias
- Separación entre componentes de interfaz y acceso a la API.
- Interfaces de servicio, como `IProductosApiService`.
- Registro de clientes HTTP tipados mediante inyección de dependencias.
- Configuración de la dirección base del servicio.
- Reutilización de operaciones HTTP desde distintos componentes.

### 4.3. Construcción de una API auxiliar
- API mínima de productos con ASP.NET Core.
- Endpoints GET y POST y contrato de datos JSON.
- Validación de solicitudes y respuestas 200, 201, 400 y 404.
- Integración con un cliente Blazor existente.
- Operaciones complementarias de resumen, búsqueda, actualización PUT y eliminación DELETE.

### 4.4. Autenticación y autorización
- Diferencia entre autenticación y autorización.
- Autenticación local mediante cookies.
- Usuarios, roles, claims y protección de recursos.
- `AuthorizeView` y contenido condicionado al estado de autenticación.
- Introducción a ASP.NET Core Identity y almacenamiento de usuarios/roles en SQL Server Express LocalDB.
- Registro e inicio de sesión, `UserManager`, `SignInManager` e `IdentityDbContext`.
- Tokens JWT Bearer: emisión, firma, validación y protección de endpoints.
- Respuestas 401 y 403 y autorización basada en roles.

## M05 — Consolidación y despliegue elemental

### 5.1. Integración de Blazor con una API
- Recorrido completo entre navegador, componente Blazor, servicio HTTP y API.
- Lectura y creación de productos, formularios y validación.
- Estados de carga, datos disponibles, catálogo vacío y errores.
- Sincronización explícita entre información recibida de la API y estado del componente.
- Diagnóstico de errores de conexión, códigos HTTP y respuestas JSON.

### 5.2. Compilación, ejecución y publicación de ASP.NET Core MVC
- Diferencias entre `dotnet build`, `dotnet run` y `dotnet publish`.
- Archivos y dependencias de una publicación.
- Configuración de entornos y ejecución desde una carpeta publicada.
- Publicación desde Visual Studio y línea de comandos.

### 5.3. Ejecución con Kestrel
- Kestrel como servidor web de ASP.NET Core.
- Proceso de aplicación, direcciones de escucha y puertos.
- Inicio y detención de una aplicación MVC publicada.
- Enrutamiento y comprobación de respuestas HTTP.
- Diagnóstico de puertos ocupados, rutas no encontradas y dependencias no disponibles.

### 5.4. Hospedaje en IIS
- IIS y el módulo ASP.NET Core Module (ANCM).
- ASP.NET Core Hosting Bundle.
- Publicación de MVC en carpeta y configuración de un sitio IIS.
- *Application Pools*, identidades, rutas físicas, enlaces de red y permisos.
- Comprobación de páginas y recursos estáticos.
- Diferencias entre el funcionamiento del servidor web y la disponibilidad de SQL Server Express LocalDB.

### 5.5. Introducción a Docker para ASP.NET Core
- Conceptos de imagen, contenedor y contexto de construcción.
- Dockerfile para una aplicación MVC de .NET 8.
- Construcción multietapa con imagen SDK e imagen de runtime ASP.NET Core.
- `docker build`, `docker run`, `docker ps`, `docker logs` y `docker stop`.
- Exposición de puertos y mapeo entre host y contenedor.
- Configuración mediante variables de entorno.
- Diferencias entre SQL Server Express LocalDB en Windows y ejecución de un contenedor Linux.

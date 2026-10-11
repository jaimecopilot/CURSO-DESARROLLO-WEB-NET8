# Temario definitivo y matriz docente — 30 horas

> **Material de planificación docente.** Este archivo fija el alcance, los tiempos y la trazabilidad antes de redactar teoría, prácticas y código. Los PDF se generan únicamente al cerrar el Markdown de cada módulo.

## 1. Objetivo y perfil

Curso presencial de cinco mañanas, seis horas lectivas por jornada (30 h efectivas, descansos excluidos). Alumnado con experiencia previa en C#, async/await, ASP.NET Core Web API y Entity Framework Core. El contenido debe ser autónomo y no requiere material de otros cursos.

Se aprende mediante **dos aplicaciones didácticas** sobre el dominio «productos»: (A) ASP.NET Core MVC, jornadas 1–2; (B) Blazor Web App con Interactive Server, jornadas 3–5. Se prepara una API REST auxiliar pequeña para la jornada 4; no es una tercera aplicación formativa completa. Razor Pages es solo una comparación de alcance mínimo.

## 2. Distribución horaria canónica

| Módulo | Teoría | Práctica | Repaso y dudas | Total |
|---|---:|---:|---:|---:|
| M01 — Fundamentos MVC | 120 min | 210 min | 30 min | 360 min |
| M02 — Formularios, validación y Razor Pages | 120 min | 210 min | 30 min | 360 min |
| M03 — Blazor y componentes | 120 min | 210 min | 30 min | 360 min |
| M04 — APIs y seguridad | 90 min | 240 min | 30 min | 360 min |
| M05 — Proyecto y despliegue | 60 min | 270 min | 30 min | 360 min |
| **TOTAL** | **510 min (8,5 h)** | **1140 min (19 h)** | **150 min (2,5 h)** | **1800 min (30 h)** |

**Regla de estimación:** los tiempos de práctica incluyen lectura, escritura/descomentado, ejecución, detección de errores y pequeñas variaciones del ejercicio. Los tiempos son hipótesis docentes, pendientes de contraste con una clase piloto; no son mediciones reales.

## 3. Matriz punto → teoría → práctica → proyecto → tiempo

T = explicación en minutos; P = trabajo práctico en minutos. A = aplicación MVC; B = Blazor; API = servicio auxiliar. Cada fila define un ejercicio base verificable; podrá incluir variantes cortas sin ampliar duración.

### M01 — Fundamentos de ASP.NET Core MVC

| Punto y contenidos fundamentales | Práctica guiada y comprobación observable | Proyecto | T | P |
|---|---|---|---:|---:|
| **1.1** ASP.NET Core, petición/respuesta HTTP, MVC frente a API | P1.1: ejecutar plantilla MVC, inspeccionar la respuesta HTML y localizar la petición en el navegador | A | 25 | 25 |
| **1.2** separación Modelo–Vista–Controlador y flujo de petición | P1.2: dibujar y recorrer el flujo Producto→Controller→View con datos fijos; mostrar título y cantidad | A | 25 | 35 |
| **1.3** estructura de proyecto, Program.cs, carpetas, convenciones | P1.3: localizar y explicar archivos; añadir modelo Producto y datos de ejemplo; reiniciar la aplicación | A | 20 | 35 |
| **1.4** acciones, parámetros, resultados y routing | P1.4: ProductosController con Index y Detalle(id), rutas convencionales y un caso por atributo, 200/404 | A | 30 | 65 |
| **1.5** sintaxis Razor, modelos tipados, layouts y parciales | P1.5: vistas Index/Detalle tipadas, menú de navegación, layout y parcial de tarjeta de producto | A | 20 | 50 |
| **Subtotal** | +30 min de repaso y dudas | | **120** | **210** |

**Estado de salida:** el alumno puede navegar un listado y un detalle; los datos todavía no requieren persistencia.

### M02 — Formularios, validación y Razor Pages

| Punto y contenidos fundamentales | Práctica guiada y comprobación observable | Proyecto | T | P |
|---|---|---|---:|---:|
| **2.1** formularios HTML, GET/POST, model binding y antiforgery | P2.1: formulario Create GET/POST y comprobación de los datos recibidos y token antiforgery | A | 25 | 40 |
| **2.2** Tag Helpers de formularios, acciones y errores | P2.2: adaptar Create para utilizar asp-for, asp-action y enlaces; inspeccionar HTML generado | A | 20 | 35 |
| **2.3** DataAnnotations, ModelState, validación servidor/cliente | P2.3: Required, StringLength y Range; probar datos válidos e inválidos y conservar valores | A | 30 | 40 |
| **2.4** CRUD completo con EF Core reutilizado | P2.4: SQLite, List/Create/Edit/Delete y comprobación de persistencia tras reinicio | A | 35 | 80 |
| **2.5** Razor Pages, PageModel, OnGet/OnPost y comparación | P2.5: única página Razor Pages de ejemplo con lectura y envío mínimo, comparada con la acción MVC | A, ejemplo aislado dentro del mismo host | 10 | 15 |
| **Subtotal** | +30 min de repaso y dudas | | **120** | **210** |

**Estado de salida:** CRUD funcional de productos con validación y base SQLite sencilla. Razor Pages no se transforma en una tercera aplicación.

### M03 — Blazor Web App y componentes

| Punto y contenidos fundamentales | Práctica guiada y comprobación observable | Proyecto | T | P |
|---|---|---|---:|---:|
| **3.1** Blazor frente a MVC, SSR estático e interactivo, Server y WebAssembly conceptual | P3.1: crear Blazor Web App .NET 8 Interactive Server; comparar comportamiento de una interacción | B | 30 | 25 |
| **3.2** estructura, componentes Razor, páginas, navegación, directivas | P3.2: crear página Productos y enlazarla en la navegación | B | 15 | 25 |
| **3.3** parámetros, reutilización y composición | P3.3: componente TarjetaProducto reutilizable y lista de tarjetas | B | 20 | 45 |
| **3.4** eventos, @onclick, @bind, estado | P3.4: selección y editor simple con actualización visible de datos en memoria | B | 20 | 50 |
| **3.5** parámetros y EventCallback padre–hijo | P3.5: emitir selección o eliminación solicitada desde hijo y actualizar la lista padre | B | 20 | 40 |
| **3.6** OnInitializedAsync y ciclo de vida esencial | P3.6: carga asíncrona controlada desde servicio en memoria y estados «cargando/listo» | B | 15 | 25 |
| **Subtotal** | +30 min de repaso y dudas | | **120** | **210** |

**Estado de salida:** interfaz Blazor interactiva y reutilizable que trabaja con datos en memoria; no requiere todavía una API.

### M04 — Integración con APIs y seguridad básica

| Punto y contenidos fundamentales | Práctica guiada y comprobación observable | Proyecto | T | P |
|---|---|---|---:|---:|
| **4.1** HttpClient, GET/POST, DTO, JSON, async y fallos HTTP | P4.1: configurar HttpClient; consultar catálogo remoto, publicar producto y mostrar error de petición | B + API disponible | 30 | 80 |
| **4.2** capa de servicio e inyección de dependencias | P4.2: extraer llamadas HTTP de componentes a IProductosApiService e inyectarlo | B | 20 | 55 |
| **4.3** API auxiliar pequeña | P4.3: ejecutar y entender API de Productos (GET/POST, datos en memoria); modificar respuesta simple | API | 15 | 45 |
| **4.4** autenticación/autorización, Identity introductorio, roles/claims conceptual, AuthorizeView | P4.4: usar demo local preconfigurada de inicio de sesión y página protegida; comprobar usuario anónimo/autenticado | B, demo de seguridad limitada | 25 | 60 |
| **Subtotal** | +30 min de repaso y dudas | | **90** | **240** |

**Dependencia resuelta:** el docente entrega al inicio de M04 la API auxiliar ya funcional para P4.1 (no se presupone aprendizaje de un proyecto externo). En P4.3 se recorre su implementación y se realizan modificaciones controladas; en P4.2 se extrae y reorganiza el consumo. La entrega de API es material del curso.

**Estado de salida:** Blazor consume GET/POST y muestra errores; la seguridad se observa en una demostración reproducible, sin enseñar Identity desde cero ni convertirla en requisito del CRUD.

### M05 — Consolidación y despliegue elemental

| Punto y contenidos fundamentales | Práctica guiada y comprobación observable | Proyecto | T | P |
|---|---|---|---:|---:|
| **5.1** recorrido arquitectónico completo | P5.1: completar y comprobar flujos clave del proyecto Blazor (listado, formulario, validación, API) | B + API | 10 | 90 |
| **5.2** ejecutar frente a publicar | P5.2: dotnet run / dotnet publish; inspeccionar y ejecutar archivos publicados | A para despliegue aislado | 15 | 35 |
| **5.3** Kestrel: puertos, URLs y proceso | P5.3: iniciar la aplicación publicada en puerto definido y comprobarla en navegador | A | 10 | 45 |
| **5.4** IIS: Hosting Bundle, App Pool, sitio básico | P5.4: publicar a carpeta, configurar sitio y comprobar respuesta y navegación | A | 15 | 55 |
| **5.5** Docker: Dockerfile, build/run, mapeo de puerto | P5.5: construir imagen .NET 8, ejecutar con mapeo host→8080 y verificarla | A | 10 | 45 |
| **Subtotal** | +30 min de repaso y dudas | | **60** | **270** |

**Decisión de simplificación:** el proyecto final consolida B; para comparar los tres despliegues se usa **la misma aplicación MVC A**, evitando requerir simultáneamente procesos Blazor + API, autenticación y base externa en un laboratorio de seis horas. A se empaquetará con configuración didáctica sencilla; se documentará la diferencia entre funcionamiento de laboratorio y configuración de producción. Si una instalación concreta no permite los tres despliegues, la evidencia se registrará como pendiente en la verificación, no como éxito.

## 4. Dependencias entre prácticas

- P1.1 → P1.2 → P1.3 → P1.4 → P1.5 (creación de estructura, modelos, rutas y vistas).
- P1.5 → P2.1 → P2.2 → P2.3 → P2.4; P2.5 es una comparación breve que reutiliza el host MVC.
- P3.1 → P3.2 → P3.3 → P3.4 → P3.5 → P3.6 (Blazor B independiente de MVC A).
- P3.6 + API suministrada → P4.1 → P4.2; P4.3 explica y modifica la API ya suministrada. P4.4 es demostración aislable.
- P4.2 + P4.3 → P5.1; P2.4 → P5.2 → P5.3/P5.4/P5.5.
- La secuencia escrita mantiene la numeración del temario; la API necesaria para P4.1 aparece completa como recurso inicial de M04, no como proyecto oculto.

## 5. Reglas de correspondencia teoría/práctica/código/test

Cada punto N.N tendrá:
1. Apartado N.N desarrollado en el Markdown de teoría del módulo.
2. Práctica PN.N con estado inicial, archivos exactos, instrucciones comentadas/descomentadas, ejecución, resultados, incidencias y consolidación.
3. Carpeta o referencia identificable N.N dentro del proyecto del módulo, sin duplicar aplicaciones funcionales si una única evolución reproducible es suficiente.
4. Prueba(s) de compilación y funcionales que ejerciten **los estados que se ordene ejecutar**. Los flujos navegador→UI→servidor/datos se validarán E2E cuando proceda.
5. Evidencia técnica en documentación de verificación separada de la destinada al alumno. Ninguna prueba se declarará ejecutada sin logs/resultado real.

En los proyectos debe conservarse la trazabilidad de cada paso, no solo la solución final. Si el cambio afecta a Razor/JSON/configuración u otro archivo incompatible con conmutación por comentarios, se ofrecerá variante de archivo o estado inicial identificable; no se entregará código que compile solo al final.

## 6. Entregables documentales y fases de publicación

- **Diez Markdown docentes y diez PDF docentes:** M01–M05, un TEORIA y un PRACTICAS por módulo.
- La documentación global (README, GUIA_DOCENTE, TEMARIO_30H, REQUISITOS_LABORATORIO) no forma parte de esos diez Markdown.
- Redacción punto a punto; incorporación incremental a ambos Markdown; verificación técnica por punto.
- PDF del módulo solo tras revisar y cerrar sus dos Markdown, con índice, código y diagramas íntegros.
- Rama de trabajo independiente de main; integración solo tras verificación y revisión.

## 7. Límites

No ampliar el curso a Angular/React, JS avanzado, Blazor WebAssembly independiente, SignalR avanzado, patrones empresariales, Identity completo, OAuth/OIDC/JWT avanzados, EF Core/Web API como cursos, Azure, Kubernetes, Docker Compose, CI/CD o infraestructura avanzada. La profundidad principal corresponde a MVC, Razor y Blazor. Despliegue e Identity son demostraciones pequeñas.

# M03 — Contrato de continuidad y trazabilidad pedagógica

Documento de trabajo editorial/técnico. **No incorporar al material docente ni a sus PDF.**
La fuente oficial del alcance y del tiempo es `TEMARIO_30H.md`. Este documento NO añade nuevos temas principales.

## Orden pedagógico definitivo (corrección explícita del responsable del curso)

**NO partir del código del repositorio para redactar o ajustar posteriormente la teoría.** Ni usar el proyecto ya existente como guion principal de las prácticas. La dirección formativa es: **TEMARIO → TEORÍA CON EJEMPLOS DE CÓDIGO → PRÁCTICAS CON EL 100 % DEL CÓDIGO EXPLICADO → PROYECTOS QUE IMPLEMENTAN LA PRÁCTICA → VALIDACIÓN Y DOCUMENTOS FINALES**. Las discrepancias obligan a corregir la fuente que corresponda sin ocultar ni inventar código.

1. Fijar el alcance del temario 3.1–3.6 y revisar **primero** el manual de TEORÍA: enseñar cada concepto desde su fundamento, motivarlo, ilustrarlo con ejemplos de Razor/C# **completos y comprensibles en el propio cuerpo**, explicar cómo funcionan y qué resultado producen. Los ejemplos deben ser técnicamente correctos y coherentes con .NET 8.
2. Diseñar **después** el itinerario PRÁCTICO como una sola aplicación B que evoluciona acumulativamente punto por punto. Escribir el manual práctico como una **construcción íntegra explicada**, cubriendo **el 100 % de los archivos de código fuente utilizados y entregados al alumno**; todos los archivos y sus partes deben estar localizados y explicados, no solo unas líneas destacadas en el cuerpo y un volcado final sin explicación. Cada modificación se muestra con el código completo pertinente y su papel en el conjunto. El alumno debe poder recrear el proyecto desde cero, sin depender de deducir código oculto.
3. Implementar/reestructurar los PROYECTOS siguiendo ese diseño práctico ya definido: instantáneas 3.1–3.6, que retienen la funcionalidad construida previamente. Mantener los fragmentos docentes comentados cuando proceda, y enlazarlos inequívocamente a su ejercicio. No incluir infraestructura o fuente versionada que no esté explicada en las prácticas.
4. Verificar exhaustivamente **TEORÍA ↔ PRÁCTICAS ↔ ARCHIVO/FUNCIÓN/LÍNEA DEL PROYECTO ↔ COMPORTAMIENTO EJECUTABLE** en ambas direcciones, incluyendo archivos generados por plantilla que quedan versionados. Si son configuración, se explican igualmente; `bin/`, `obj/` y otros artefactos no versionados no forman parte del inventario docente.
5. Ejecutar sobre copias temporales la aplicación progresiva y los escenarios positivos/negativos en navegador; las pruebas internas no aparecen en manuales.
6. Generar y revisar PDF desde los dos MD canónicos solo cuando haya cierre formativo y técnico, manteniendo al menos ~75–80 páginas **por manual** sin padding tipográfico.
7. No fusionar `main` sin permiso. **La teoría no puede ser una explicación a posteriori del código, y el anexo de fuentes no reemplaza el desarrollo de código en el cuerpo de la práctica.**

Los ajustes preliminares recientes a P3.4/P3.5 se consideran **provisionales**, NO una implementación cerrada; no continuar modificando código antes de fijar la teoría y el diseño de las prácticas.

## Contrato de una única aplicación evolutiva

Las carpetas `M03_BLAZOR/PROYECTO/3.1` … `3.6` son **instantáneas docentes consecutivas** de una sola aplicación B, no seis aplicaciones independientes con conceptos aislados.

- **3.1** crea la aplicación B Blazor Web App con SSR estático / Interactive Server comparables. Conservar ambas páginas en todos los estados posteriores.
- **3.2** incorpora el modelo Producto, la ruta `/productos` y la navegación con `NavLink`, sin eliminar 3.1.
- **3.3** conserva el catálogo y transforma la representación en `TarjetaProducto` mediante `[Parameter]`; el estado siguiente NO debe regresar a `<article>` duplicado en la página.
- **3.4** conserva `TarjetaProducto` y permite seleccionar/crear/editar en memoria; el filtrado y la ordenación pueden figurar como ampliación activable, pero deben conservarse en las instantáneas siguientes. Los botones de selección todavía pueden permanecer en el padre junto a cada tarjeta, sin introducir `EventCallback` antes de 3.5.
- **3.5** conserva navegación, `TarjetaProducto`, selección, creación, edición y filtros/ordenación y mueve eventos al componente hijo mediante `EventCallback<int>`; añade quitar/deshacer. No puede reemplazar el catálogo por una versión minimalista que pierde el trabajo anterior.
- **3.6** conserva todo lo anterior y cambia la **obtención inicial** por el servicio en memoria cargado con `OnInitializedAsync` y DI; añade «cargando», «vacío», «error» y «reintentar» sin eliminar las operaciones existentes. `OnInitializedAsync` del primer ejercicio y el de reintento son variantes alternativas, no métodos duplicados.

### Resultado pedagógico acumulativo mínimo

| Punto | Antes | Modificación obligatoria | Después (sin perder) |
|---|---|---|---|
| 3.1 | Host de componentes | Mostrar diferencia de modo de renderizado | Dos páginas para comparar |
| 3.2 | Estado de 3.1 | `Producto`, ruta y menú | Catálogo visible y comparación 3.1 |
| 3.3 | Estado de 3.2 | `TarjetaProducto` con `[Parameter]` | Catálogo visible desde componente reutilizable |
| 3.4 | Estado de 3.3 | `@onclick`, `@bind`, selección, alta, edición | Tarjetas reutilizadas, CRUD parcial en memoria, consulta reversible |
| 3.5 | Estado de 3.4 | `EventCallback<int>` en hija y comunicación con padre | Todas las acciones anteriores más eliminación y recuperación |
| 3.6 | Estado de 3.5 | DI, `OnInitializedAsync`, estados de carga | Catálogo funcional completo, ahora con carga asíncrona y reintento |

## Matriz bidireccional TEORÍA ↔ PRÁCTICAS ↔ CÓDIGO

| Contenido teórico concreto | Práctica/aplicación | Artefacto/código estudiante | Observación que debe demostrarse |
|---|---|---|---|
| 3.1 SSR estático vs Interactive Server y eventos C# | P3.1.3–P3.1.5 | `Components/Pages/Estatica.razor`, `Interactiva.razor`, `Program.cs` | Clic estático no modifica contador; interactivo sí |
| 3.2 `@page`, `Routes`, `NavLink`, Razor y modelo | P3.2.1–P3.2.4 | `Productos.razor`, `Models/Producto.cs`, `Layout/MainLayout.razor` | Menú/URL `/productos` y lista de 3 elementos |
| 3.3 reutilización, `[Parameter]`, composición | P3.3.2–P3.3.5 | `TarjetaProducto.razor` + bucle de `Productos.razor` | 3 tarjetas del mismo componente con Id/nombre/precio diferentes |
| 3.4 `@onclick`, lambda, estado y renderizado | P3.4.2 | `Productos.razor`, Seleccionar por Id | Selección visible sin perder tarjetas ni estructura reutilizable |
| 3.4 `@bind`, validación mínima y colecciones | P3.4.3–P3.4.4 | `Productos.razor`, nuevoNombre / Agregar | Alta válida agrega tarjeta; vacío no agrega |
| 3.4 estado de edición, Id, record `with` | P3.4.5 | `Productos.razor`, SeleccionarParaEditar / GuardarCambio | Renombra manteniendo Id, precio y total |
| 3.4 `@bind:event`, LINQ, estado derivado | P3.4.6 (ampliación) | `Productos.razor`, `ProductosVisibles` | Búsqueda/filtro/orden reversible, edición compatible |
| 3.5 parámetro entrante y callback saliente | P3.5.1–P3.5.4 | `TarjetaProducto.razor` + `Productos.razor` | Clic en tarjeta actualiza selección del padre |
| 3.5 eliminación por Id y propietario del estado | Reto P3.5 | Igual: `AlQuitar` y `Quitar` | Eliminar reduce total, sin manipular datos desde hijo |
| 3.5 deshacer un elemento conservando posición | P3.5.5 (ampliación) | `Productos.razor`, `QuitarConDeshacer` / `DeshacerEliminacion` | Eliminar/reponer conserva Id y posición |
| 3.6 ciclo de vida, DI y servicio asíncrono | P3.6.1–P3.6.5 | `Program.cs`, `IProductosMemoriaService.cs`, `ProductosMemoriaService.cs`, `Productos.razor` | Estado inicial carga y termina con 3 tarjetas interactuables |
| 3.6 estado vacío vs carga satisfactoria | Reto P3.6 | `Productos.razor` y servicio | Lista vacía no se presenta como fallo |
| 3.6 error y reintento sin API | P3.6.7 (ampliación) | Servicio + interfaz + `Productos.razor` | Fallo → mensaje → recargar → restaurar catálogo interactivo |

La correspondencia es **bidireccional**: todo ejercicio debe tener explicación teórica previa o vinculada, y todo bloque de código docente imprescindible debe ser utilizado por una práctica concreta. No añadir ejemplos no ejecutables sin identificarlos como pseudocódigo o esquema conceptual.

## Reglas editoriales obligatorias de cada punto P3.x

- Situación/problema realista del **mismo catálogo**, prerrequisitos y archivo/ruta exacta de la instantánea.
- Mostrar en el punto del procedimiento **todo el código C#/Razor/HTML/configuración necesario** para construir el estado didáctico: no solo fragmentos selectivos, y no depender del anexo para cubrir las piezas que faltan.
- Explicar **todos los archivos, miembros, instrucciones y contratos relevantes de los fuentes versionados**; cada bloque debe corresponder al diseño práctico ya definido y a la implementación exacta, no al revés. Un anexo con código completo puede complementar el tutorial, pero no sustituir su explicación detallada.
- Secuencia: objetivo concreto → código/razón → ejecutar → comportamiento observable → caso negativo y solución de diagnóstico → enlace al concepto de teoría.
- El siguiente proyecto parte del final funcional obligatorio del anterior; las ampliaciones opcionales se trasladan cuando forman parte del recorrido integrado del módulo. Si una ampliación es deliberadamente aislada, debe declararse explícitamente.
- La teoría **explica** mecanismos, decisiones y consecuencias; las prácticas **construyen** el mismo programa guiadas por esos mecanismos. Evitar duplicar párrafos solo para ganar páginas.
- Ni informes de auditoría, ni recuentos internos, ni E2E técnico, ni comprobaciones de publicación en el material del alumno. Este documento queda solo en VERIFICACION_INTERNA.
- Las pruebas de compilación/navegador sirven internamente para demostrar funcionalidad antes de cerrar los MD y PDF.

## Estado inicial de reparación (12/10/2026)

Auditoría del estado anterior, **no certificación de resultado**: 3.4 vuelve a dibujar `article.tarjeta` en la página en vez de usar `TarjetaProducto`; 3.5 elimina alta, edición y filtros; 3.6 elimina la interactividad desarrollada, conservando solo representación asíncrona. Las pruebas previas cubren ejercicios separados pero no comprueban regresiones de la aplicación acumulativa. Es imprescindible rehacer esos estados y las comprobaciones cruzadas antes de publicar manuales definitivos.

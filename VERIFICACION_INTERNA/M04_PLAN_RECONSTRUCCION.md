# M04 — Preparación técnica y secuencia de construcción (documento interno)

## Alcance fijado por el temario

- 4.1 — HttpClient, DTO y JSON, GET/POST asíncronos, errores HTTP (30 min teoría, 80 min práctica).
- 4.2 — Servicio `IProductosApiService`, extracción de acceso HTTP e inyección de dependencias (20 min teoría, 55 min práctica).
- 4.3 — API auxiliar pequeña GET/POST con almacenamiento en memoria (15 min teoría, 45 min práctica).
- 4.4 — Introducción a autenticación, autorización, Identity y `AuthorizeView`; demostración local acotada (25 min teoría, 60 min práctica).

El curso utiliza la aplicación Blazor de M03 y una API auxiliar **disponible desde el primer ejercicio de 4.1**, cuyo código se estudia y modifica en 4.3. No se presupone un servicio ajeno al repositorio ni se amplía a seguridad avanzada.

## Punto de partida verificado en el repositorio

`M03_BLAZOR/PROYECTO/3.6/CursoWeb.Blazor/` contiene la aplicación Blazor Web App .NET 8 con Interactive Server, `Components/Pages/Productos.razor`, modelos, componentes y `IProductosMemoriaService`.

En `Program.cs` se registra el servicio de memoria y **no** se registra aún HttpClient. En `Productos.razor` coexisten las operaciones de catálogo en memoria y una implementación de `OnInitializedAsync` dentro del bloque `PASO 3.6.2` comentado, junto a la variante del reto 3.6.7 comentada. Por tanto, **no es correcto tratar el archivo actual como si la carga asincrónica estuviera ya activada**: la transición M03→M04 deberá indicar expresamente cuál de esas variantes se activa y cómo se preservan las funcionalidades aprendidas.

## Orden editorial y técnico obligatorio

1. Redactar teoría 4.1 con explicación de petición/respuesta, contratos DTO, serialización, `HttpClient`, `GetFromJsonAsync`, `PostAsJsonAsync`, códigos HTTP, manejo de error, asincronía y límites de una demostración en memoria; ejemplos completos **explicados en la teoría**.
2. Redactar y revisar teoría 4.2; después 4.3; finalmente 4.4. La teoría define los conceptos que se practicarán, no interpreta retrospectivamente código ya escrito.
3. Consolidar `M04_APIS_SEGURIDAD/TEORIA/M04_TEORIA.md` antes de redactar `M04_APIS_SEGURIDAD/PRACTICAS/M04_PRACTICAS.md`; usar ejercicios paso a paso, con comandos, archivos, variantes, resultados observables y retos reproducibles.
4. Construir estados acumulativos `PROYECTO/4.1` … `PROYECTO/4.4` de la aplicación Blazor más una API auxiliar suministrada desde 4.1. Código de cada paso rastreable por archivo, incluidos estados comentados/activables según corresponda.
5. Ejecutar compilación y pruebas de comportamiento para cada estado relevante, conservando evidencias en `VERIFICACION_INTERNA` fuera de los materiales del alumno.
6. Generar un PDF fiel por Markdown solo después del cierre del contenido. Revisar paginación, bloques de código, tablas e integridad del texto.

## Límites

No modificar `main`, no convertir el ejercicio en un curso de Web API o Identity, ni introducir JWT/OIDC, Docker Compose o infraestructura compleja. Evitar relleno para alcanzar páginas: la extensión debe responder a ejemplos, explicación y ejercicios auténticos.

## Estado

**Preparación y lectura de dependencias realizada; teoría/prácticas/proyectos/PDF de M04 todavía no creados ni validados.** Este documento no se entrega al alumno.

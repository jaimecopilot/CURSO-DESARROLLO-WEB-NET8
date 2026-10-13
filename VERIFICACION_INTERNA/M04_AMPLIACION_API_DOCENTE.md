# M04 — Ampliación didáctica acordada: construcción de API REST

## Motivo

La teoría actual (~5.824 palabras) y las prácticas (~2.899 palabras) son insuficientes para la profundidad docente acordada. No se debe aumentar páginas mediante relleno o tipografía artificial.

## Decisión

Mantener los cuatro puntos oficiales 4.1–4.4 y la duración de 6 horas. En 4.3, el alumno **construirá una API ASP.NET Core minimal desde cero** paso a paso; el proyecto ya suministrado al principio de 4.1 sigue siendo una dependencia funcional para los ejercicios 4.1 y 4.2. En 4.3, el alumno crea su propia versión y sustituye la suministrada, sin modificar el contrato esperado por Blazor.

## Secuencia de teoría → práctica

- Teoría 4.1: fundamentos HTTP/JSON/DTO y cliente Blazor, ejemplos íntegros y progresivos, estados de error.
- Teoría 4.2: DI, HttpClientFactory y servicio tipado, refactor completo motivado.
- Teoría 4.3: arquitectura de petición, Minimal API, endpoints GET colección/por id, POST, modelos y validación, códigos 200/201/400/404, serialización, almacenamiento en memoria, concurrencia básica, documentación OpenAPI opcional como lectura, diagnóstico. No ampliar a EF Core ni autenticación avanzada.
- Teoría 4.4: cookies de demostración, claims, roles, autorización servidor, AuthorizeView, antiforgery, seguridad y límites explícitos de la demo.

- Práctica 4.3: crear `dotnet new web -n CursoWeb.ProductosApi -f net8.0`, configurar puerto, crear modelos de entrada/salida, construir GET, detalle 404, POST validado 201 y Location, probar con curl, añadir resumen, probar rechazo y reinicio, conectar Blazor. Cada paso incluye estado anterior, código íntegro, archivo, instrucciones, resultado y variante activable.

## Restricciones

No borrar código ni resultados previos sin confirmar. No tocar main. La teoría se desarrolla antes de reescribir prácticas; no redactar teoría como comentario retrospectivo de archivos finales. Mantener trazabilidad por ejercicios y retos, y PDF solo tras cierre de los MD. ~80 páginas es objetivo de calidad y extensión, no permiso de relleno.

## Estado

Decisión editorial registrada; la ampliación completa todavía requiere ejecución y verificación.

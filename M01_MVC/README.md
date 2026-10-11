# M01 — Fundamentos de ASP.NET Core MVC

**AUTOR: JAIME GALLO**

**Duración docente:** seis horas. Cinco apartados (1.1 a 1.5).

## Material del alumno

- [Teoría completa en Markdown](TEORIA/M01_TEORIA.md) — [PDF de teoría (80 páginas)](TEORIA/M01_TEORIA.pdf).
- [Prácticas completas, ejercicios y retos en Markdown](PRACTICAS/M01_PRACTICAS.md) — [PDF de prácticas (81 páginas)](PRACTICAS/M01_PRACTICAS.pdf).

Los dos PDF provienen de los Markdown canónicos y cubren los **cinco capítulos**, sin PDFs individuales por punto. La comprobación automatizada de integridad, huellas SHA-256 y paginación está documentada en [verificación PDF](../VERIFICACION_INTERNA/M01_PDFS_VALIDACION.md), y el recuento por cada punto en [equivalencia MD/PDF](../VERIFICACION_INTERNA/M01_FIDELIDAD.md). El PDF no constituye una fuente editorial: únicamente se genera a partir del MD canónico. Se ha repetido la inspección visual sobre la nueva edición de **161 páginas**. La [revisión de cierre](../VERIFICACION_INTERNA/M01_CIERRE_EDITORIAL.md) documenta la reorganización, el cotejo de código y los límites de la comprobación. Antes de integrar en `main` sigue pendiente la aceptación del responsable docente.

## Proyecto y evolución

Cada carpeta de `PROYECTO` guarda **un estado reproducible de la misma aplicación MVC**, sin depender de cambios locales de los ejercicios anteriores.

| Punto | Carpeta | Aprendizaje |
|---|---|---|
| 1.1 | [PROYECTO/1.1](PROYECTO/1.1) | Primera petición HTTP y vista MVC |
| 1.2 | [PROYECTO/1.2](PROYECTO/1.2) | Modelo, controlador y paso de datos a Razor |
| 1.3 | [PROYECTO/1.3](PROYECTO/1.3) | Carpetas, configuración y recursos estáticos |
| 1.4 | [PROYECTO/1.4](PROYECTO/1.4) | Acciones, parámetros, rutas y detalles |
| 1.5 | [PROYECTO/1.5](PROYECTO/1.5) | Vistas tipadas, secciones del layout y parciales |

**Importante:** el estado inicial de cada carpeta corresponde al inicio del ejercicio y puede contener código comentado. Los pasos principales del capítulo anterior ya están activos al comenzar el siguiente. Los retos opcionales se conservan como variantes localizables y no tienen por qué estar activados en los capítulos siguientes.

Para ejecutar una versión, entrar en la carpeta indicada y utilizar `dotnet run --no-launch-profile --urls http://localhost:5091`. No arrancar dos versiones sobre el mismo puerto.

## Comprobación

Para validar todos los estados y retos se utiliza el workflow [M01 E2E](../.github/workflows/m01-ci.yml), que ejecuta `M01_MVC/TESTS/1.1_e2e.sh` hasta `1.5_e2e.sh`. Estas son pruebas de respuesta HTTP real sobre Kestrel; la exploración visual con navegador forma parte de la práctica presencial.

El ejercicio final de 1.5 es un catálogo con listados, detalles y tarjetas Razor reutilizables, todavía con datos en memoria. Su persistencia se abordará en M02.

## Trazabilidad después de la revisión editorial

Los laboratorios ampliados se han integrado en la secuencia del paso correspondiente; ya no existe una segunda lista de apartados A–U. Cada capítulo de prácticas contiene una tabla de pasos y reto con la ruta del archivo del proyecto, la instrucción de activación, el resultado esperado y la prueba E2E.

La auditoría actual comprueba 92 fragmentos de código: 78 aparecen literalmente en el proyecto y 14 son variantes de un estado activado o ejemplos abreviados cuyos elementos se han localizado en el código. La compilación y el HTTP real se verifican con 28 escenarios E2E. Consulta el [informe de cierre editorial y técnico](../VERIFICACION_INTERNA/M01_CIERRE_EDITORIAL.md).

**El Markdown es la única fuente editorial**; los PDF no incorporan explicaciones ajenas a ella. Los cambios deben realizarse primero en los MD y, si requieren código, también en el proyecto y los tests. M01 permanece fuera de `main` hasta la aceptación docente.

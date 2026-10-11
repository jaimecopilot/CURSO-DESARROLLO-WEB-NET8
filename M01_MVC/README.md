# M01 — Fundamentos de ASP.NET Core MVC

**AUTOR: JAIME GALLO**

**Duración docente:** seis horas. Cinco apartados (1.1 a 1.5).

## Material del alumno

- [Teoría completa en Markdown](TEORIA/M01_TEORIA.md) — [PDF de teoría (83 páginas)](TEORIA/M01_TEORIA.pdf).
- [Prácticas completas, ejercicios y retos en Markdown](PRACTICAS/M01_PRACTICAS.md) — [PDF de prácticas (83 páginas)](PRACTICAS/M01_PRACTICAS.pdf).

Los dos PDF provienen de los Markdown canónicos y cubren los **cinco capítulos**, sin PDFs individuales por punto. La comprobación automatizada de integridad, huellas SHA-256 y paginación está documentada en [verificación PDF](../VERIFICACION_INTERNA/M01_PDFS_VALIDACION.md), y el recuento por cada punto en [equivalencia MD/PDF](../VERIFICACION_INTERNA/M01_FIDELIDAD.md). El PDF no constituye una fuente editorial: únicamente se genera a partir del MD canónico. Se ha efectuado la inspección visual de las 165 páginas, con corrección del tamaño de los diagramas y registro de observaciones no bloqueantes en la [revisión visual de M01](../VERIFICACION_INTERNA/M01_REVISION_VISUAL.md). Antes de integrar en `main` sigue pendiente la aceptación editorial del responsable del curso.

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

## Ampliaciones docentes y trazabilidad

Los laboratorios ampliados están incluidos en los apartados adicionales de P1.1 a P1.5 del Markdown de prácticas. Son recorridos de lectura de código, activación de los mismos bloques, análisis de respuestas y diagnóstico; **no requieren proyectos diferentes ni duplicar controladores**. Cada apartado utiliza la carpeta `PROYECTO/1.x` correspondiente y el script `TESTS/1.x_e2e.sh`.

Si en nuevas ediciones se incorpora un ejercicio que requiera código no incluido, debe añadirse el bloque al proyecto con su comentario, actualizarse su prueba y modificar el MD antes de generar el PDF. La regla de publicación es **MD canónico → código reproducible y probado → PDF derivado del MD**.

## Revisión editorial y trazabilidad pendiente

La [revisión editorial de M01](../VERIFICACION_INTERNA/M01_DIAGNOSTICO_EDITORIAL.md) ha detectado duplicaciones y una jerarquía excesiva de epígrafes en los capítulos ampliados. Los tests E2E anteriores confirman el funcionamiento de escenarios concretos, pero **no acreditan por sí solos trazabilidad integral de cada ejemplo de las prácticas**. M01 no se considera cerrado editorialmente ni está integrado en `main`.

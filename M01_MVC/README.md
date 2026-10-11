# M01 — Fundamentos de ASP.NET Core MVC

**Duración docente:** seis horas. Cinco apartados (1.1 a 1.5).

## Material del alumno

- [Teoría completa de M01](TEORIA/M01_TEORIA.md).
- [Prácticas completas, ejercicios y retos](PRACTICAS/M01_PRACTICAS.md).

Los documentos contienen **los cinco capítulos**; no se distribuye un PDF por ejercicio. Las dos ediciones PDF se incorporan a las mismas carpetas cuando se haya comprobado la integridad de los Markdown.

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

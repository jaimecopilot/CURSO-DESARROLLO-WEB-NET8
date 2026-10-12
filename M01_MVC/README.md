# M01 — Fundamentos de ASP.NET Core MVC

**AUTOR: JAIME GALLO**

**Duración docente:** seis horas. Cinco apartados (1.1 a 1.5).

## Material del alumno

- [Teoría completa en Markdown](TEORIA/M01_TEORIA.md) — [PDF de teoría](TEORIA/M01_TEORIA.pdf).
- [Prácticas completas, ejercicios y retos en Markdown](PRACTICAS/M01_PRACTICAS.md) — [PDF de prácticas](PRACTICAS/M01_PRACTICAS.pdf).

Los documentos reúnen los cinco capítulos del módulo. Cada PDF corresponde a su manual completo y no existe un PDF independiente por ejercicio.

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

## Comprobación funcional

Después de cada ejercicio, abre las direcciones indicadas en el cuaderno de prácticas y compara el resultado con el comportamiento esperado. Comprueba el HTML, los códigos HTTP, la navegación y el efecto de activar los bloques del capítulo.

El ejercicio final de 1.5 es un catálogo con listados, detalles y tarjetas Razor reutilizables, todavía con datos en memoria. Su persistencia se abordará en M02.

## Orientación didáctica

El recorrido esencial son los pasos numerados y los resultados observables; las profundizaciones son actividades de ampliación y los retos se intentan antes de consultar el código de referencia. Se trabaja con cinco estados identificables del catálogo MVC. 
# M04 — Revisión de cierre: estado técnico y brechas editoriales

Fecha: 2026-10-13. Rama: `desarrollo/m04-apis-seguridad-trazable`.

## Alcance comprobado

Se ha comprobado en el repositorio la existencia de los puntos 4.1–4.4 en ambos Markdown, de los proyectos acumulativos Blazor 4.1–4.4 y de la API auxiliar 4.1/4.3. Las comprobaciones automatizadas de 4.1, 4.2 y 4.3 finalizaron con SUCCESS. La validación 4.4 registró una compilación inicialmente fallida por dos `AuthorizeView` anidados con el mismo `context`; se corrigió y la siguiente ejecución terminó SUCCESS. Posteriormente se reforzó el ejemplo para exigir antiforgery de forma explícita en POST de entrada/salida y restringir las rutas de demostración a Development; requiere una nueva ejecución de CI.

## Correspondencia teoría → práctica → código

| Punto | Teoría | Práctica | Código materializado | Límite de las pruebas |
|---|---|---|---|---|
| 4.1 | HTTP, GET/POST, DTO, JSON, async, error | P4.1.1–P4.1.7 | Blazor 4.1 + API auxiliar 4.1 | CI compila y comprueba contrato API; no prueba un navegador real en Blazor |
| 4.2 | interfaz, cliente tipado e inyección | P4.2.1–P4.2.6 | Blazor 4.2 | CI compila y verifica ubicación del código HTTP; no prueba E2E de navegador |
| 4.3 | endpoints, validación, respuesta y memoria | P4.3.1–P4.3.5 | Blazor 4.3 y API 4.3, bloques comentados activables | CI activa paso 4.3.3 y ejecuta contrato; reto 4.3.5 no probado |
| 4.4 | cookies demo, claims, roles, AuthorizeView | P4.4.1–P4.4.5 | Blazor 4.4, endpoint protegido | CI compila y consulta el recurso anónimo; falta E2E del recorrido completo inicio/salida con navegador y rol alternativo |

## Hallazgos que impiden declarar M04 cerrado

1. **Alcance editorial insuficiente para el objetivo acordado de ~80 páginas por documento.** Los Markdown tienen aprox. 4.870 palabras de teoría y 2.526 de prácticas (medidas en esta revisión). No se puede conseguir una extensión auténtica de ~80 páginas cada uno aumentando fuentes, márgenes o interlineado. Requiere desarrollo didáctico sustantivo, ejemplos completos e instrucciones minuciosas.
2. **P4.1.4 y P4.2.2 remiten a ejemplos de teoría** en vez de incluir todos los bloques de código y sus estados inicial/intermedio/final de forma autónoma en las prácticas. El alumno debe poder reconstruir cada ejercicio sin depender de un estado final prehecho.
3. **P4.4 carece de prueba E2E con navegador de inicio de sesión, visualización AuthorizeView, salida y rol distinto.** El check de denegación HTTP anónima por sí solo no demuestra la sesión completa.
4. **P4.3.5 y P4.1.7 contienen variantes de reto comentadas cuya activación individual debe compilarse y verificarse.** No basta con que compile el estado final.
5. **No hay PDF M04 fieles verificados ni inspección visual página a página.** De acuerdo con el flujo editorial, no se generan todavía porque el Markdown canónico no está cerrado.

## Criterio de cierre

Reescribir o ampliar la teoría y las prácticas **sin duplicaciones ni relleno**, tomando como fuente la progresión 4.1–4.4 existente. Cada paso programable debe aportar código completo, punto de partida, activación, ejecución y resultado esperado. Ejecutar regresiones reales en estados intermedios/reto, navegar el flujo de seguridad y solo entonces generar los dos PDF desde Markdown, cotejar el contenido y revisar visualmente todas las páginas. Mantener informes técnicos fuera de los manuales del alumno; no integrar en `main` sin autorización.

Este documento informa de lo verificado y de lo pendiente; no acredita el cierre del módulo.

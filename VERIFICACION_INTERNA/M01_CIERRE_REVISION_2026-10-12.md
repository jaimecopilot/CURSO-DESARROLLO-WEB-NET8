# M01 — Informe técnico de la revisión didáctica (12/10/2026)

**Repositorio:** jaimecopilot/CURSO-DESARROLLO-WEB-NET8  
**Rama:** revision-didactica/m01  
**Autor de los manuales docentes:** JAIME GALLO  
**Destino:** control interno; no incorporar al material del alumno.

## Correcciones ejecutadas

- Leídos los cinco capítulos de teoría y de prácticas. Detectadas duplicaciones de instrucciones y de soluciones en P1.1–P1.5.
- Eliminados recorridos repetidos de observación HTTP y activación prematura de Razor en P1.1; inspecciones y activaciones repetidas en P1.3; reexplicaciones de pasos y retos en P1.2, P1.4 y P1.5.
- Conservadas las etapas guiadas, los ejemplos no duplicados, las rutas, los resultados esperados y los cinco retos. Incorporado un intento autónomo previo al código de referencia en cada reto.
- Eliminadas menciones a ejecución de baterías E2E, workflows, informes internos y revisión editorial de los dos manuales, del README general/módulo, de los cinco README de proyecto y de los requisitos visibles al alumno.
- Mantenidos los scripts de comprobación, workflows, diagnósticos y matrices en sus carpetas técnicas.
- Actualizada la planificación general de M02 para **SQL Server Express LocalDB + EF Core 8**, exclusivamente para Windows/Visual Studio Community. La implementación de M02 se realiza en rama separada.
- Corregido el generador de PDF: no impone un mínimo arbitrario de 80 páginas; mantiene comprobaciones de capítulos, fuente MD incrustada, diagramas, autor, cabeceras, texto de páginas y desbordamientos.

## Evidencias ejecutadas

| Evidencia | URL de ejecución | Resultado |
|---|---|---|
| Compilación y HTTP real P1.1–P1.5, verificación de estados y retos | https://github.com/jaimecopilot/CURSO-DESARROLLO-WEB-NET8/actions/runs/38258785335 | SUCCESS |
| Ejecución anterior tras cambios de autonomía en retos | https://github.com/jaimecopilot/CURSO-DESARROLLO-WEB-NET8/actions/runs/38258261164 | SUCCESS |
| Generación PDF desde Markdown, comparación de integridad y publicación en rama | https://github.com/jaimecopilot/CURSO-DESARROLLO-WEB-NET8/actions/runs/38258785387 | SUCCESS |

Los scripts de E2E ejecutados por GitHub Actions inician Kestrel con dotnet 8.0 en Linux; validan los estados de activación definidos en los ejercicios y los resultados HTTP. **No acredita una sesión manual en Visual Studio Community**.

## PDF publicados

| Documento | Palabras MD | Caracteres MD | Páginas PDF | Observaciones |
|---|---:|---:|---:|---|
| M01_TEORIA | 33.312 | 227.779 | 80 | 7 diagramas; fuente Markdown íntegra incrustada |
| M01_PRACTICAS | 21.668 | 152.978 | 61 | Cinco prácticas y retos; fuente Markdown íntegra incrustada |

El generador informa de correspondencia del 100 % en su métrica automática de palabras extraídas, y verifica todas las páginas contra errores de texto vacío, encabezados y cuadros que se salgan de los márgenes horizontales.

**Límite explícito:** la inspección visual humana, página por página, en un visor PDF no ha podido completarse desde esta sesión. Las comprobaciones automatizadas no sustituyen esa aceptación editorial. También está pendiente una clase piloto real para confirmar los tiempos. No declarar esas dos revisiones como superadas.

## Estado de publicación

- **Código y ejercicios automatizados:** comprobados por ejecución satisfactoria en la rama de revisión.
- **Texto didáctico:** revisión selectiva ejecutada. Pendiente aceptación humana final.
- **PDF:** generados/publicados con integridad técnica validada. Pendiente inspección visual humana exhaustiva.
- **main:** sin cambios ni fusión autorizada.
- **M02:** crear rama desde el commit definitivo de la rama revisada, activando expresamente los pasos principales 1.5.2–1.5.5 en su estado de entrada.

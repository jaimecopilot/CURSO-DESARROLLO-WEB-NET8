# M01 — Diagnóstico editorial y trazabilidad del contenido ampliado

**Estado:** revisión editorial abierta; no confundir una compilación satisfactoria con un curso pedagógicamente cerrado.

## Hallazgos comprobados sobre los Markdown

| Punto | Secciones `##` de teoría | Subapartados `###` de teoría | Secciones `##` de prácticas | Subapartados `###` de prácticas | Bloques de código repetidos en prácticas |
|---|---:|---:|---:|---:|---:|
| 1.1 | 29 | 13 | 13 | 26 | 2 |
| 1.2 | 16 | 12 | 15 | 24 | 4 |
| 1.3 | 21 | 8 | 16 | 30 | 8 |
| 1.4 | 32 | 22 | 21 | 45 | 8 |
| 1.5 | 23 | 14 | 18 | 37 | 12 |
| **Total** | **121** | **69** | **83** | **162** | **34** |

Los recuentos se obtienen sobre los cinco capítulos de cada Markdown canónico. Los bloques repetidos son coincidencias literales tras normalizar espacios, por capítulo, y **no** todas son errores: algunas expresan la versión comentada y la versión activa. Se requiere criterio editorial para decidir cuáles conservar.

### Problemas constatados

1. Las primeras versiones de los capítulos siguen un recorrido didáctico inicial; después se añadieron numerosas secciones numeradas, incluyendo hasta `1.4.31`, sin integrarlas con las explicaciones previas. Esto fragmenta el hilo argumental.
2. Los cuadernos prácticos tienen una primera secuencia de tareas (A, B, C…) y después laboratorios ampliados (I–S/U). Frecuentemente vuelven a explicar la misma acción, respuesta HTTP, reto o bloque Razor. La actividad no queda descrita como una única secuencia ejecutable.
3. El aumento hasta 80 páginas no garantiza por sí solo suficiente profundidad práctica. El criterio debe ser: objetivo, código existente, acción del alumno, ejecución y resultado comprobable; no número de epígrafes.
4. La matriz actual de **36 correspondencias** se basa en comprobación estática de marcadores y fragmentos seleccionados. **No prueba** que todos los ejemplos, pasos y retos del Markdown coincidan línea por línea con el repositorio.
5. Los PDF son derivados de los MD, conservan la fuente literal incrustada y superan las pruebas de integridad, pero esas pruebas no sustituyen una lectura pedagógica de cada actividad.


## Auditoría ampliada de todos los ejemplos (11 de octubre de 2026)

La ejecución [M01 — Auditoría completa de ejemplos 38176948021](https://github.com/jaimecopilot/CURSO-DESARROLLO-WEB-NET8/actions/runs/38176948021) ha comparado **93 bloques** de C#, Razor, JSON, CSS y XML de los cinco capítulos de prácticas con sus proyectos correspondientes.

- **78/93** fragmentos aparecen de forma literal en el proyecto del punto correspondiente, sin tener en cuenta los espacios de formato.
- **15/93** son variantes o representaciones de estados editados; sus líneas sustantivas se han localizado en los archivos correspondientes, pero el bloque no coincide de forma literal y exige revisar su activación paso a paso.
- **0/93** se han clasificado como parcial o sin cobertura en esta comparación estática. Esto **no equivale** a demostrar que las quince variantes sean compilables sin instrucciones adicionales o que todas las actividades estén perfectamente alineadas.

En particular, las variantes se concentran en P1.1 (2), P1.2 (7), P1.3 (1), P1.4 (2) y P1.5 (3). Entre ellas aparecen el estado activo de un bloque inicialmente comentado, ejemplos abreviados de clases y controladores, y la parcial Razor representada sin los comentarios docentes que incorpora el archivo real.

El resultado completo se conserva como artefacto de la ejecución. **La decisión editorial pendiente es revisar esas quince variantes y el solapamiento de los laboratorios con los pasos ya existentes.** Hasta ese momento no se declarará trazabilidad pedagógica perfecta.

## Estructura editorial que debe sustituir la actual

Para **teoría 1.1–1.5**, cada capítulo debe seguir un recorrido de pocos bloques de nivel superior: objetivos y contexto, conceptos conectados, ejemplo completo con explicación, variantes y errores, y conexión con la práctica. La profundización debe estar situada junto al concepto correspondiente, no como una segunda teoría añadida al final. Se eliminarán repeticiones sin suprimir explicaciones ni ejemplos únicos.

Para **prácticas P1.1–P1.5**, cada punto debe organizarse en: objetivo y archivos de trabajo; estado inicial; pasos ejecutables en orden; reto integrado tras sus prerrequisitos; pruebas y resultados; diagnóstico de fallos. Las ampliaciones útiles deben pasar al **paso al que pertenecen**; las comprobaciones repetidas se referenciarán desde una única matriz. Desaparecerá la secuencia de letras A–U.

## Criterio de trazabilidad imprescindible

Para cada paso ejecutable se documentará explícitamente:

- Identificador único del paso, nombre y ruta exacta del archivo del proyecto.
- Código inicial tal como está versionado, con delimitadores de activación cuando corresponda.
- Código resultante de la activación, sin pseudocódigo presentado como fuente real.
- Acción que debe realizar el alumno y resultado HTTP/HTML esperado.
- Evidencia de compilación y escenario E2E que reproduce **ese** estado.
- Correspondencia con cualquier explicación teórica necesaria.

Los ejemplos meramente conceptuales deberán marcarse como tales, nunca como fragmentos que el alumno debe buscar o activar en GitHub.

## Identidad editorial de los PDF

La portada y todas las cabeceras posteriores derivan de estos datos de cada Markdown:

- **CURSO:** Curso de Desarrollo Web con ASP.NET Core MVC, Razor y Blazor en .NET 8.
- **MÓDULO/CAPÍTULO:** título de M01 en portada y nombre vigente de cada punto 1.1–1.5 en las páginas interiores.
- **TIPO:** TEORÍA o PRÁCTICAS, declarado en la propia fuente.
- **AUTOR:** JAIME GALLO.

El PDF no debe añadir texto docente que no conste en el Markdown. La sustitución de título de capítulo en la cabecera es una operación de maquetación basada en títulos del MD.

## Condiciones de cierre

La revisión editorial se mantiene abierta hasta disponer de un recorrido coherente por capítulo, eliminar explicaciones duplicadas que no aportan un objetivo distinto, verificar **todos** los fragmentos ejecutables contra el proyecto y probar sus estados con GitHub Actions. Los dos PDF solo se considerarán definitivos cuando esta fuente revisada esté cerrada, se regenere y supere de nuevo la comparación MD/PDF y la inspección visual.

**Protección del repositorio:** no fusionar M01 en `main` antes de ese cierre.

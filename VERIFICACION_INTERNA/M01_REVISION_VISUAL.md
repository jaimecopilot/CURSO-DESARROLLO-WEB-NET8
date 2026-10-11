# M01 — Resultado de la revisión visual de PDF y fidelidad canónica

**Fecha:** 11 de octubre de 2026.  
**Rama:** `desarrollo/m01-mvc`.  
**PDF teoría:** 83 páginas · 7 diagramas vectoriales.  
**PDF prácticas:** 82 páginas.  
**Fuente única:** `M01_MVC/TEORIA/M01_TEORIA.md` y `M01_MVC/PRACTICAS/M01_PRACTICAS.md`.

## Verificaciones realizadas

- Se recuperaron los PDF binarios del artefacto de GitHub Actions [38174288991](https://github.com/jaimecopilot/CURSO-DESARROLLO-WEB-NET8/actions/runs/38174288991), ejecución **SUCCESS**.
- Se renderizaron todas las **165 páginas** y se examinó visualmente cada una en láminas de revisión; se ampliaron las páginas de diagramas y muestras de código.
- No se detectaron páginas vacías, glifos de sustitución, fragmentos de texto fuera del límite de página ni interrupciones visibles de párrafos y tablas.
- La autoría **AUTOR: JAIME GALLO** aparece exactamente una vez por página, en portada o cabecera posterior, sin fallos.
- Cada PDF contiene incrustada su fuente Markdown exacta, cuya huella de Git coincide **byte por byte** con el archivo canónico vigente. El Markdown es la única fuente editorial.
- La prueba automatizada por capítulo registra **0 palabras normalizadas omitidas** en los diez apartados.
- Una comparación adicional de los **269 fragmentos de código** (94 de teoría y 175 de prácticas) confirma **269/269 coincidencias exactas de contenido y puntuación**, eliminando únicamente espacios y saltos de línea propios de la maquetación.
- El generador se ha corregido para escalar mejor los diagramas de flujo altos; la teoría pasa de 82 a **83 páginas**. Ningún MD se ha editado para efectuar esa corrección. La representación visual de las **82 páginas de prácticas** permanece idéntica píxel a píxel.

## Aspectos de maquetación observados

- La página **2** de cada manual tiene el índice y un espacio libre considerable, porque la portada y el índice se presentan en páginas propias.
- Las páginas **21 y 68 de teoría**, y **44 y 65 de prácticas**, contienen cierres de capítulo con bastante blanco por el salto de capítulo. La página 44 de prácticas tiene especialmente poco texto.
- Esas páginas **no carecen de contenido del MD**: la comparación canónica lo verifica. Se mantiene el inicio de cada capítulo en una página nueva para facilitar su uso docente.
- Los diagramas que antes resultaban demasiado pequeños (especialmente teoría p. 6 y el esquema de arranque que ahora está en p. 38) se han ampliado sin cambiar el contenido ni la fuente tipográfica del resto del documento.

## Identidad de los cuatro archivos con la rama GitHub

| Archivo | Git blob SHA-1 |
|---|---|
| Teoría MD | `5a77a974fcdae4bee9f14cbc21f34617a8e7e499` |
| Teoría PDF | `09800376ccebc9218c031548e1da54dfda40c7d3` |
| Prácticas MD | `3be97b749b866891ff48247971b197f7426c51c6` |
| Prácticas PDF | `1b851c3bd9f7bf7cfbd5108acb8ed1a1cc185770` |

## Alcance y límites

Que los PDF lleven el MD idéntico incrustado **no implica que sus bytes sean idénticos a los del Markdown**: un PDF transforma marcas de formato, tablas, enlaces y diagramas a representación visual. El contenido renderizable sí ha sido contrastado por capítulo, por bloques de código y visualmente. No se ha evaluado conformidad con PDF/UA ni lectura mediante tecnologías de asistencia.

La revisión visual se ha realizado usando representaciones de todas las páginas y una inspección de detalle en las páginas más delicadas; no equivale a una lectura manual palabra a palabra de las 165 páginas. Para eso existe además la comparación automatizada de contenido indicada.

**Resultado:** sin omisiones ni fallos visuales bloqueantes detectados. Observaciones de páginas con espacios blancos registradas. Rama `main` intacta.

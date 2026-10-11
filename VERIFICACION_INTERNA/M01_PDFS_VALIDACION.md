# M01 — Verificación automática de PDF y Markdown

**Carácter:** control técnico interno. No aparece en los PDF docentes.

Las dos ediciones se generan directamente de los Markdown canónicos, sin resumir capítulos ni ejemplos.
Se comprueba la existencia de los cinco capítulos, retos, contenido fundamental, diagramas vectoriales y páginas PDF sin texto vacío ni recortes horizontales detectables.

| Archivo | Palabras MD | Caracteres MD | Páginas PDF | Diagramas SVG |
|---|---:|---:|---:|---:|
| TEORIA | 32994 | 225332 | 80 | 7 |
| PRACTICAS | 29124 | 205205 | 82 | 0 |

## Autor procedente del Markdown

Los dos PDF presentan **AUTOR: JAIME GALLO** en portada y en la cabecera de cada página siguiente.
El texto repetido en la cabecera se toma de la línea canónica del Markdown correspondiente; no se introduce un autor independiente en el generador.

## Huellas de fuente canónica

| Documento | SHA-256 del MD que está incrustado en el PDF | Coincidencia byte por byte |
|---|---|---|
| TEORIA | `12ae9871ca4a6c1c38752255e874823d37d8e4d303ca425b856e3f0a65780118` | True |
| PRACTICAS | `22d8b827d7bad24e087be3303692e7d8b33483eb68ff5caebf374f8967e6874f` | True |

## Alcance y límites

La validación calcula conteos, inspecciona texto extraído y cajas de texto mediante PyMuPDF, y comprueba que cada diagrama Mermaid tiene salida SVG. Este resultado **no implica** inspección visual manual de todas las páginas, navegación con lectores de pantalla o una clase piloto.
Las pruebas E2E del código se ejecutan mediante el workflow independiente \`m01-ci.yml\`.

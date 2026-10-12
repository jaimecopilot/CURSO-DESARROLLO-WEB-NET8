# M01 — Verificación automática de PDF y Markdown

**Carácter:** control técnico interno. No aparece en los PDF docentes.

Las dos ediciones se generan directamente de los Markdown canónicos, sin resumir capítulos ni ejemplos.
Se comprueba la existencia de los cinco capítulos, retos, contenido fundamental, diagramas vectoriales y páginas PDF sin texto vacío ni recortes horizontales detectables.

| Archivo | Palabras MD | Caracteres MD | Páginas PDF | Diagramas SVG |
|---|---:|---:|---:|---:|
| TEORIA | 35483 | 242162 | 84 | 6 |
| PRACTICAS | 28397 | 198117 | 75 | 0 |

## Autor procedente del Markdown

Los dos PDF presentan **AUTOR: JAIME GALLO** en portada y en la cabecera de cada página siguiente.
El texto repetido en la cabecera se toma de la línea canónica del Markdown correspondiente; no se introduce un autor independiente en el generador.

## Huellas de fuente canónica

| Documento | SHA-256 del MD que está incrustado en el PDF | Coincidencia byte por byte |
|---|---|---|
| TEORIA | `80d5b8b27c1050e2f03502833530b87eeb82282e3ea2781a4d42a0d640a8b582` | True |
| PRACTICAS | `16704ad6c64a3dc54b734867c095009e8a438a56d9aa6035835b8712f80d3cd2` | True |

## Alcance y límites

La validación calcula conteos, inspecciona texto extraído y cajas de texto mediante PyMuPDF, y comprueba que cada diagrama Mermaid tiene salida SVG. Este resultado **no implica** inspección visual manual de todas las páginas, navegación con lectores de pantalla o una clase piloto.
Las pruebas E2E del código se ejecutan mediante el workflow independiente \`m01-ci.yml\`.

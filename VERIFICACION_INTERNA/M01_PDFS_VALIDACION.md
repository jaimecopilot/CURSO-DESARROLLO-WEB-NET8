# M01 — Verificación automática de PDF y Markdown

**Carácter:** control técnico interno. No aparece en los PDF docentes.

Las dos ediciones se generan directamente de los Markdown canónicos, sin resumir capítulos ni ejemplos.
Se comprueba la existencia de los cinco capítulos, retos, contenido fundamental, diagramas vectoriales y páginas PDF sin texto vacío ni recortes horizontales detectables.

| Archivo | Palabras MD | Caracteres MD | Páginas PDF | Diagramas SVG |
|---|---:|---:|---:|---:|
| TEORIA | 33527 | 229167 | 81 | 7 |
| PRACTICAS | 29088 | 204954 | 81 | 0 |

## Autor procedente del Markdown

Los dos PDF presentan **AUTOR: JAIME GALLO** en portada y en la cabecera de cada página siguiente.
El texto repetido en la cabecera se toma de la línea canónica del Markdown correspondiente; no se introduce un autor independiente en el generador.

## Huellas de fuente canónica

| Documento | SHA-256 del MD que está incrustado en el PDF | Coincidencia byte por byte |
|---|---|---|
| TEORIA | `3a84d37c37dc17a66034daa6319b199b53de5ad03579ea3cb0109e4b5986b511` | True |
| PRACTICAS | `d24ade43805f9e36bdab4ba63ef824fd68bd0da950f243b8e81b74a444784405` | True |

## Alcance y límites

La validación calcula conteos, inspecciona texto extraído y cajas de texto mediante PyMuPDF, y comprueba que cada diagrama Mermaid tiene salida SVG. Este resultado **no implica** inspección visual manual de todas las páginas, navegación con lectores de pantalla o una clase piloto.
Las pruebas E2E del código se ejecutan mediante el workflow independiente \`m01-ci.yml\`.

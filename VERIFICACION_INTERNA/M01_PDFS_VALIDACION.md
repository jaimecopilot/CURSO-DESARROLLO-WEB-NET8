# M01 — Verificación automática de PDF y Markdown

**Carácter:** control técnico interno. No aparece en los PDF docentes.

Las dos ediciones se generan directamente de los Markdown canónicos, sin resumir capítulos ni ejemplos.
Se comprueba la existencia de los cinco capítulos, retos, contenido fundamental, diagramas vectoriales y páginas PDF sin texto vacío ni recortes horizontales detectables.

| Archivo | Palabras MD | Caracteres MD | Páginas PDF | Diagramas SVG |
|---|---:|---:|---:|---:|
| TEORIA | 33312 | 227779 | 80 | 7 |
| PRACTICAS | 21668 | 152978 | 61 | 0 |

## Autor procedente del Markdown

Los dos PDF presentan **AUTOR: JAIME GALLO** en portada y en la cabecera de cada página siguiente.
El texto repetido en la cabecera se toma de la línea canónica del Markdown correspondiente; no se introduce un autor independiente en el generador.

## Huellas de fuente canónica

| Documento | SHA-256 del MD que está incrustado en el PDF | Coincidencia byte por byte |
|---|---|---|
| TEORIA | `593f44e9c6d226fe8b0a5ce5a4b4e70c91fc4a098cea7668254ed3a15dbf2d99` | True |
| PRACTICAS | `f307bd4089200a0ee810fd84fc844f59c26d0fdce49c200c1a167b35cf20a5b9` | True |

## Alcance y límites

La validación calcula conteos, inspecciona texto extraído y cajas de texto mediante PyMuPDF, y comprueba que cada diagrama Mermaid tiene salida SVG. Este resultado **no implica** inspección visual manual de todas las páginas, navegación con lectores de pantalla o una clase piloto.
Las pruebas E2E del código se ejecutan mediante el workflow independiente \`m01-ci.yml\`.

# M01 — Verificación automática de PDF y Markdown

**Carácter:** control técnico interno. No aparece en los PDF docentes.

Las dos ediciones se generan directamente de los Markdown canónicos, sin resumir capítulos ni ejemplos.
Se comprueba la existencia de los cinco capítulos, retos, contenido fundamental, diagramas vectoriales y páginas PDF sin texto vacío ni recortes horizontales detectables.

| Archivo | Palabras MD | Caracteres MD | Páginas PDF | Diagramas SVG |
|---|---:|---:|---:|---:|
| TEORIA | 32626 | 222227 | 80 | 7 |
| PRACTICAS | 27864 | 193244 | 79 | 0 |

## Huellas de fuente canónica

| Documento | SHA-256 del MD que está incrustado en el PDF | Coincidencia byte por byte |
|---|---|---|
| TEORIA | `20a26e5e3f53519caec9a92ffda73c9b210326abd26d44d89f68e703877cef0d` | True |
| PRACTICAS | `6bb1f4771f52b680960c2d032f81fd4911352b0e6a96d1d20c87aa1028d91af7` | True |

## Alcance y límites

La validación calcula conteos, inspecciona texto extraído y cajas de texto mediante PyMuPDF, y comprueba que cada diagrama Mermaid tiene salida SVG. Este resultado **no implica** inspección visual manual de todas las páginas, navegación con lectores de pantalla o una clase piloto.
Las pruebas E2E del código se ejecutan mediante el workflow independiente \`m01-ci.yml\`.

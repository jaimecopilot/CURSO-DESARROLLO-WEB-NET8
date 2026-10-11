# M01 — Verificación automática de PDF y Markdown

**Carácter:** control técnico interno. No aparece en los PDF docentes.

Las dos ediciones se generan directamente de los Markdown canónicos, sin resumir capítulos ni ejemplos.
Se comprueba la existencia de los cinco capítulos, retos, contenido fundamental, diagramas vectoriales y páginas PDF sin texto vacío ni recortes horizontales detectables.

| Archivo | Palabras MD | Caracteres MD | Páginas PDF | Diagramas SVG |
|---|---:|---:|---:|---:|
| TEORIA | 29964 | 204741 | 74 | 7 |
| PRACTICAS | 14857 | 104848 | 45 | 0 |

## Huellas de fuente canónica

| Documento | SHA-256 del MD que está incrustado en el PDF | Coincidencia byte por byte |
|---|---|---|
| TEORIA | `7a7bd75df9bb16b03468f3ec7174dfd844f3bb3f4e573e37c6381963cade14b2` | True |
| PRACTICAS | `f55a70706fb106502616aa50b0873929403a0a8b76edd71c812046765a48bd33` | True |

## Alcance y límites

La validación calcula conteos, inspecciona texto extraído y cajas de texto mediante PyMuPDF, y comprueba que cada diagrama Mermaid tiene salida SVG. Este resultado **no implica** inspección visual manual de todas las páginas, navegación con lectores de pantalla o una clase piloto.
Las pruebas E2E del código se ejecutan mediante el workflow independiente \`m01-ci.yml\`.

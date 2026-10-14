# M05 — Informe técnico documental

Las fuentes de contenido son únicamente los dos Markdown canónicos.
Cada PDF incluye su Markdown completo, adjunto idéntico byte por byte.

| Documento | Palabras MD | Páginas PDF |
|---|---:|---:|
| TEORIA | 32603 | 75 |
| PRACTICAS | 28392 | 77 |

## Detalle de comprobaciones

Se verificaron portada, autor, cinco capítulos, paginación, integridad binaria de Markdown adjunto y límites de texto extraíble.
La inspección visual humana página a página no se sustituye por estas comprobaciones.

[
  {
    "tipo": "TEORIA",
    "paginas": 75,
    "palabras_md": 32603,
    "cobertura_palabras_visibles": 1.0,
    "palabras_faltantes_en_extraccion": [],
    "caracteres_md": 215595,
    "bytes_pdf": 624017,
    "sha256_md": "89081b5c3391f1a4df54a87ab80739f0f5c844b6336c502bbf268c8466a98f13",
    "fuente_md_incrustada_identica": true,
    "capitulos_inicio": {
      "1": 3,
      "2": 26,
      "3": 38,
      "4": 51,
      "5": 61
    }
  },
  {
    "tipo": "PRACTICAS",
    "paginas": 77,
    "palabras_md": 28392,
    "cobertura_palabras_visibles": 0.999832,
    "palabras_faltantes_en_extraccion": [
      [
        "razor",
        5
      ]
    ],
    "caracteres_md": 201086,
    "bytes_pdf": 603936,
    "sha256_md": "5fccd198f73a3e54d003180cb36df7a774674fda885cff51594d80e7334da1b0",
    "fuente_md_incrustada_identica": true,
    "capitulos_inicio": {
      "1": 3,
      "2": 22,
      "3": 37,
      "4": 46,
      "5": 59
    }
  }
]
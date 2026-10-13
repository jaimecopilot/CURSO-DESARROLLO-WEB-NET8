# M05 — Informe técnico documental

Las fuentes de contenido son únicamente los dos Markdown canónicos.
Cada PDF incluye su Markdown completo, adjunto idéntico byte por byte.

| Documento | Palabras MD | Páginas PDF |
|---|---:|---:|
| TEORIA | 32607 | 75 |
| PRACTICAS | 28118 | 76 |

## Detalle de comprobaciones

Se verificaron portada, autor, cinco capítulos, paginación, integridad binaria de Markdown adjunto y límites de texto extraíble.
La inspección visual humana página a página no se sustituye por estas comprobaciones.

[
  {
    "tipo": "TEORIA",
    "paginas": 75,
    "palabras_md": 32607,
    "cobertura_palabras_visibles": 1.0,
    "palabras_faltantes_en_extraccion": [],
    "caracteres_md": 215601,
    "bytes_pdf": 624028,
    "sha256_md": "4fdedb47347a8111cf09284cb4483cd0067d2405fc05864d8e57d710fb1d5504",
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
    "paginas": 76,
    "palabras_md": 28118,
    "cobertura_palabras_visibles": 0.999898,
    "palabras_faltantes_en_extraccion": [
      [
        "razor",
        3
      ]
    ],
    "caracteres_md": 198759,
    "bytes_pdf": 597214,
    "sha256_md": "a6b975b347787bccfe1d2adaa82344aa81d07ca08b78ddfcec6833132d37f46a",
    "fuente_md_incrustada_identica": true,
    "capitulos_inicio": {
      "1": 3,
      "2": 21,
      "3": 36,
      "4": 45,
      "5": 58
    }
  }
]
# M05 — Informe técnico documental

Las fuentes de contenido son únicamente los dos Markdown canónicos.
Cada PDF incluye su Markdown completo, adjunto idéntico byte por byte.

| Documento | Palabras MD | Páginas PDF |
|---|---:|---:|
| TEORIA | 32607 | 75 |
| PRACTICAS | 28387 | 78 |

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
    "bytes_pdf": 624033,
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
    "paginas": 78,
    "palabras_md": 28387,
    "cobertura_palabras_visibles": 0.999832,
    "palabras_faltantes_en_extraccion": [
      [
        "razor",
        5
      ]
    ],
    "caracteres_md": 200886,
    "bytes_pdf": 603575,
    "sha256_md": "20984ccad4d3f178d7731cfc219b39cd7b37af7ae856d7506a81d92608354b09",
    "fuente_md_incrustada_identica": true,
    "capitulos_inicio": {
      "1": 4,
      "2": 23,
      "3": 37,
      "4": 46,
      "5": 60
    }
  }
]
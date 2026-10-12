# Fidelidad de M02: Markdown canónico frente a texto visible PDF

Informe interno. El PDF se generó del MD y contiene su fuente adjunta idéntica byte a byte.
Se compararon por capítulo las palabras visibles representadas desde Markdown y extraídas del cuerpo PDF,
excluyendo las cabeceras y pies repetidos y los bloques Mermaid transformados en diagrama.

| Documento | Capítulo | Páginas | Cobertura tokens MD → PDF | Tokens no encontrados |
|---|---|---|---:|---:|
| TEORIA | 2.1 | 3-14 | 100.00% | 0 |
| TEORIA | 2.2 | 15-29 | 100.00% | 0 |
| TEORIA | 2.3 | 30-45 | 100.00% | 0 |
| TEORIA | 2.4 | 46-65 | 99.98% | 1 |
| TEORIA | 2.5 | 66-75 | 100.00% | 0 |
| PRACTICAS | P2.1 | 4-17 | 100.00% | 0 |
| PRACTICAS | P2.2 | 18-30 | 100.00% | 0 |
| PRACTICAS | P2.3 | 31-48 | 99.98% | 1 |
| PRACTICAS | P2.4 | 49-69 | 99.97% | 2 |
| PRACTICAS | P2.5 | 70-78 | 99.96% | 1 |

Los contadores de tokens son un diagnóstico de extracción textual: no prueban idéntica maquetación,
igualdad visual de los diagramas ni ausencia de errores de lectura humana.

## Datos

[
  {
    "tipo": "TEORIA",
    "paginas": 75,
    "fuente_original_incrustada_identica": true,
    "capitulos": [
      {
        "punto": "2.1",
        "desde": 3,
        "hasta": 14,
        "palabras_visibles_md": 3622,
        "palabras_extraidas_pdf": 3656,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": [
          [
            "formulario",
            2
          ],
          [
            "producto",
            2
          ],
          [
            "datos",
            2
          ],
          [
            "confirmacion",
            2
          ],
          [
            "2",
            1
          ],
          [
            "1",
            1
          ],
          [
            "html",
            1
          ],
          [
            "y",
            1
          ],
          [
            "post",
            1
          ],
          [
            "model",
            1
          ]
        ]
      },
      {
        "punto": "2.2",
        "desde": 15,
        "hasta": 29,
        "palabras_visibles_md": 4931,
        "palabras_extraidas_pdf": 4931,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      },
      {
        "punto": "2.3",
        "desde": 30,
        "hasta": 45,
        "palabras_visibles_md": 5150,
        "palabras_extraidas_pdf": 5150,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      },
      {
        "punto": "2.4",
        "desde": 46,
        "hasta": 65,
        "palabras_visibles_md": 6044,
        "palabras_extraidas_pdf": 6045,
        "cobertura": 0.999835,
        "tokens_no_encontrados": 1,
        "ejemplos_missing": [
          [
            "trustservercertificate",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "trustservercertifica",
            1
          ],
          [
            "te",
            1
          ]
        ]
      },
      {
        "punto": "2.5",
        "desde": 66,
        "hasta": 75,
        "palabras_visibles_md": 2902,
        "palabras_extraidas_pdf": 2902,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      }
    ]
  },
  {
    "tipo": "PRACTICAS",
    "paginas": 78,
    "fuente_original_incrustada_identica": true,
    "capitulos": [
      {
        "punto": "P2.1",
        "desde": 4,
        "hasta": 17,
        "palabras_visibles_md": 4209,
        "palabras_extraidas_pdf": 4216,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": [
          [
            "del",
            1
          ],
          [
            "paso",
            1
          ],
          [
            "archivo",
            1
          ],
          [
            "acción",
            1
          ],
          [
            "alumno",
            1
          ],
          [
            "evidencia",
            1
          ],
          [
            "observable",
            1
          ]
        ]
      },
      {
        "punto": "P2.2",
        "desde": 18,
        "hasta": 30,
        "palabras_visibles_md": 4162,
        "palabras_extraidas_pdf": 4162,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      },
      {
        "punto": "P2.3",
        "desde": 31,
        "hasta": 48,
        "palabras_visibles_md": 5417,
        "palabras_extraidas_pdf": 5418,
        "cobertura": 0.999815,
        "tokens_no_encontrados": 1,
        "ejemplos_missing": [
          [
            "cshtml",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "cshtm",
            1
          ],
          [
            "l",
            1
          ]
        ]
      },
      {
        "punto": "P2.4",
        "desde": 49,
        "hasta": 69,
        "palabras_visibles_md": 6275,
        "palabras_extraidas_pdf": 6277,
        "cobertura": 0.999681,
        "tokens_no_encontrados": 2,
        "ejemplos_missing": [
          [
            "aplicación",
            1
          ],
          [
            "trustservercertificate",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "aplicació",
            1
          ],
          [
            "n",
            1
          ],
          [
            "trustservercer",
            1
          ],
          [
            "tificate",
            1
          ]
        ]
      },
      {
        "punto": "P2.5",
        "desde": 70,
        "hasta": 78,
        "palabras_visibles_md": 2352,
        "palabras_extraidas_pdf": 2353,
        "cobertura": 0.999575,
        "tokens_no_encontrados": 1,
        "ejemplos_missing": [
          [
            "trustservercertificate",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "trustservercertifica",
            1
          ],
          [
            "te",
            1
          ]
        ]
      }
    ]
  }
]
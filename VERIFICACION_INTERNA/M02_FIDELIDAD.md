# Fidelidad de M02: Markdown canónico frente a texto visible PDF

Informe interno. El PDF se generó del MD y contiene su fuente adjunta idéntica byte a byte.
Se compararon por capítulo las palabras visibles representadas desde Markdown y extraídas del cuerpo PDF,
excluyendo las cabeceras y pies repetidos y los bloques Mermaid transformados en diagrama.

| Documento | Capítulo | Páginas | Cobertura tokens MD → PDF | Tokens no encontrados |
|---|---|---|---:|---:|
| TEORIA | 2.1 | 3-15 | 100.00% | 0 |
| TEORIA | 2.2 | 16-31 | 100.00% | 0 |
| TEORIA | 2.3 | 32-48 | 100.00% | 0 |
| TEORIA | 2.4 | 49-72 | 99.99% | 1 |
| TEORIA | 2.5 | 73-84 | 100.00% | 0 |
| PRACTICAS | P2.1 | 3-23 | 100.00% | 0 |
| PRACTICAS | P2.2 | 24-42 | 100.00% | 0 |
| PRACTICAS | P2.3 | 43-69 | 99.99% | 1 |
| PRACTICAS | P2.4 | 70-104 | 99.98% | 2 |
| PRACTICAS | P2.5 | 105-125 | 100.00% | 0 |

Los contadores de tokens son un diagnóstico de extracción textual: no prueban idéntica maquetación,
igualdad visual de los diagramas ni ausencia de errores de lectura humana.

## Datos

[
  {
    "tipo": "TEORIA",
    "paginas": 84,
    "fuente_original_incrustada_identica": true,
    "capitulos": [
      {
        "punto": "2.1",
        "desde": 3,
        "hasta": 15,
        "palabras_visibles_md": 3878,
        "palabras_extraidas_pdf": 3912,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": [
          [
            "formulario",
            2
          ],
          [
            "datos",
            2
          ],
          [
            "producto",
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
        "desde": 16,
        "hasta": 31,
        "palabras_visibles_md": 5348,
        "palabras_extraidas_pdf": 5348,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      },
      {
        "punto": "2.3",
        "desde": 32,
        "hasta": 48,
        "palabras_visibles_md": 5503,
        "palabras_extraidas_pdf": 5503,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      },
      {
        "punto": "2.4",
        "desde": 49,
        "hasta": 72,
        "palabras_visibles_md": 6945,
        "palabras_extraidas_pdf": 6946,
        "cobertura": 0.999856,
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
        "desde": 73,
        "hasta": 84,
        "palabras_visibles_md": 3363,
        "palabras_extraidas_pdf": 3363,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      }
    ]
  },
  {
    "tipo": "PRACTICAS",
    "paginas": 125,
    "fuente_original_incrustada_identica": true,
    "capitulos": [
      {
        "punto": "P2.1",
        "desde": 3,
        "hasta": 23,
        "palabras_visibles_md": 5937,
        "palabras_extraidas_pdf": 5944,
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
        "desde": 24,
        "hasta": 42,
        "palabras_visibles_md": 5637,
        "palabras_extraidas_pdf": 5637,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      },
      {
        "punto": "P2.3",
        "desde": 43,
        "hasta": 69,
        "palabras_visibles_md": 7656,
        "palabras_extraidas_pdf": 7657,
        "cobertura": 0.999869,
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
        "desde": 70,
        "hasta": 104,
        "palabras_visibles_md": 9986,
        "palabras_extraidas_pdf": 9988,
        "cobertura": 0.9998,
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
            "te",
            1
          ],
          [
            "trustservercertifica",
            1
          ]
        ]
      },
      {
        "punto": "P2.5",
        "desde": 105,
        "hasta": 125,
        "palabras_visibles_md": 5184,
        "palabras_extraidas_pdf": 5184,
        "cobertura": 1.0,
        "tokens_no_encontrados": 0,
        "ejemplos_missing": [],
        "ejemplos_extra": []
      }
    ]
  }
]
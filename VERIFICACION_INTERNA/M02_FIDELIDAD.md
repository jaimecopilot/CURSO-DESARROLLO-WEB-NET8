# Fidelidad de M02: Markdown canónico frente a texto visible PDF

Informe interno. El PDF se generó del MD y contiene su fuente adjunta idéntica byte a byte.
Se compararon por capítulo las palabras visibles representadas desde Markdown y extraídas del cuerpo PDF,
excluyendo las cabeceras y pies repetidos y los bloques Mermaid transformados en diagrama.

| Documento | Capítulo | Páginas | Cobertura tokens MD → PDF | Tokens no encontrados |
|---|---|---|---:|---:|
| TEORIA | 2.1 | 3-14 | 99.61% | 14 |
| TEORIA | 2.2 | 15-29 | 99.31% | 34 |
| TEORIA | 2.3 | 30-45 | 99.48% | 27 |
| TEORIA | 2.4 | 46-65 | 99.52% | 29 |
| TEORIA | 2.5 | 66-75 | 99.38% | 18 |
| PRACTICAS | P2.1 | 3-15 | 99.33% | 28 |
| PRACTICAS | P2.2 | 16-28 | 99.42% | 24 |
| PRACTICAS | P2.3 | 29-44 | 99.58% | 23 |
| PRACTICAS | P2.4 | 45-63 | 99.36% | 40 |
| PRACTICAS | P2.5 | 64-72 | 99.96% | 1 |

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
        "palabras_extraidas_pdf": 3640,
        "cobertura": 0.996135,
        "tokens_no_encontrados": 14,
        "ejemplos_missing": [
          [
            "el",
            2
          ],
          [
            "h1",
            2
          ],
          [
            "que",
            1
          ],
          [
            "producto",
            1
          ],
          [
            "también",
            1
          ],
          [
            "crear",
            1
          ],
          [
            "campo",
            1
          ],
          [
            "oculto",
            1
          ],
          [
            "p2",
            1
          ],
          [
            "envía",
            1
          ],
          [
            "public",
            1
          ],
          [
            "iactionresult",
            1
          ]
        ],
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
            "confirmacion",
            2
          ],
          [
            "2",
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
          ],
          [
            "antiforgery",
            1
          ],
          [
            "de",
            1
          ]
        ]
      },
      {
        "punto": "2.2",
        "desde": 15,
        "hasta": 29,
        "palabras_visibles_md": 4931,
        "palabras_extraidas_pdf": 4937,
        "cobertura": 0.993105,
        "tokens_no_encontrados": 34,
        "ejemplos_missing": [
          [
            "tag",
            2
          ],
          [
            "la",
            2
          ],
          [
            "helper",
            2
          ],
          [
            "cambio",
            2
          ],
          [
            "qué",
            2
          ],
          [
            "podemos",
            2
          ],
          [
            "el",
            1
          ],
          [
            "nombre",
            1
          ],
          [
            "precio",
            1
          ],
          [
            "una",
            1
          ],
          [
            "token",
            1
          ],
          [
            "antiforgery",
            1
          ],
          [
            "destino",
            1
          ],
          [
            "no",
            1
          ],
          [
            "del",
            1
          ],
          [
            "generación",
            1
          ],
          [
            "input",
            1
          ],
          [
            "id",
            1
          ],
          [
            "continuidad",
            1
          ],
          [
            "importante",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "e",
            6
          ],
          [
            "o",
            5
          ],
          [
            "p",
            5
          ],
          [
            "b",
            3
          ],
          [
            "ca",
            2
          ],
          [
            "ag",
            2
          ],
          [
            "pe",
            2
          ],
          [
            "d",
            2
          ],
          [
            "ó",
            2
          ],
          [
            "q",
            2
          ]
        ]
      },
      {
        "punto": "2.3",
        "desde": 30,
        "hasta": 45,
        "palabras_visibles_md": 5150,
        "palabras_extraidas_pdf": 5169,
        "cobertura": 0.994757,
        "tokens_no_encontrados": 27,
        "ejemplos_missing": [
          [
            "p2",
            2
          ],
          [
            "con",
            1
          ],
          [
            "dataannotations",
            1
          ],
          [
            "no",
            1
          ],
          [
            "al",
            1
          ],
          [
            "el",
            1
          ],
          [
            "un",
            1
          ],
          [
            "que",
            1
          ],
          [
            "precio",
            1
          ],
          [
            "negativo",
            1
          ],
          [
            "nombre",
            1
          ],
          [
            "reglas",
            1
          ],
          [
            "contrato",
            1
          ],
          [
            "junto",
            1
          ],
          [
            "crud",
            1
          ],
          [
            "4",
            1
          ],
          [
            "lo",
            1
          ],
          [
            "mismo",
            1
          ],
          [
            "declaradas",
            1
          ],
          [
            "required",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "o",
            9
          ],
          [
            "a",
            6
          ],
          [
            "co",
            4
          ],
          [
            "e",
            4
          ],
          [
            "p",
            3
          ],
          [
            "q",
            2
          ],
          [
            "g",
            2
          ],
          [
            "u",
            2
          ],
          [
            "c",
            1
          ],
          [
            "s",
            1
          ]
        ]
      },
      {
        "punto": "2.4",
        "desde": 46,
        "hasta": 65,
        "palabras_visibles_md": 6044,
        "palabras_extraidas_pdf": 6046,
        "cobertura": 0.995202,
        "tokens_no_encontrados": 29,
        "ejemplos_missing": [
          [
            "productos",
            3
          ],
          [
            "_db",
            3
          ],
          [
            "una",
            2
          ],
          [
            "producto",
            2
          ],
          [
            "var",
            2
          ],
          [
            "asnotracking",
            2
          ],
          [
            "localdb",
            1
          ],
          [
            "aplicación",
            1
          ],
          [
            "detalle",
            1
          ],
          [
            "read",
            1
          ],
          [
            "sola",
            1
          ],
          [
            "deliberadamente",
            1
          ],
          [
            "trustservercertificate",
            1
          ],
          [
            "consulta",
            1
          ],
          [
            "consultas",
            1
          ],
          [
            "sobre",
            1
          ],
          [
            "reutilizar",
            1
          ],
          [
            "index",
            1
          ],
          [
            "reales",
            1
          ],
          [
            "await",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "a",
            5
          ],
          [
            "e",
            5
          ],
          [
            "de",
            2
          ],
          [
            "u",
            2
          ],
          [
            "su",
            1
          ],
          [
            "so",
            1
          ],
          [
            "ap",
            1
          ],
          [
            "cac",
            1
          ],
          [
            "ó",
            1
          ],
          [
            "oca",
            1
          ]
        ]
      },
      {
        "punto": "2.5",
        "desde": 66,
        "hasta": 75,
        "palabras_visibles_md": 2902,
        "palabras_extraidas_pdf": 2925,
        "cobertura": 0.993797,
        "tokens_no_encontrados": 18,
        "ejemplos_missing": [
          [
            "mismo",
            2
          ],
          [
            "razor",
            1
          ],
          [
            "pages",
            1
          ],
          [
            "el",
            1
          ],
          [
            "del",
            1
          ],
          [
            "mvc",
            1
          ],
          [
            "modelstate",
            1
          ],
          [
            "host",
            1
          ],
          [
            "registra",
            1
          ],
          [
            "lo",
            1
          ],
          [
            "dataannotations",
            1
          ],
          [
            "siguen",
            1
          ],
          [
            "significando",
            1
          ],
          [
            "cierre",
            1
          ],
          [
            "módulo",
            1
          ],
          [
            "lecturas",
            1
          ],
          [
            "recomendadas",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "o",
            7
          ],
          [
            "s",
            7
          ],
          [
            "a",
            6
          ],
          [
            "e",
            4
          ],
          [
            "c",
            2
          ],
          [
            "de",
            1
          ],
          [
            "os",
            1
          ],
          [
            "eg",
            1
          ],
          [
            "ages",
            1
          ],
          [
            "ode",
            1
          ]
        ]
      }
    ]
  },
  {
    "tipo": "PRACTICAS",
    "paginas": 72,
    "fuente_original_incrustada_identica": true,
    "capitulos": [
      {
        "punto": "P2.1",
        "desde": 3,
        "hasta": 15,
        "palabras_visibles_md": 4209,
        "palabras_extraidas_pdf": 4217,
        "cobertura": 0.993348,
        "tokens_no_encontrados": 28,
        "ejemplos_missing": [
          [
            "un",
            3
          ],
          [
            "1",
            2
          ],
          [
            "2",
            2
          ],
          [
            "post",
            1
          ],
          [
            "el",
            1
          ],
          [
            "visual",
            1
          ],
          [
            "aplicación",
            1
          ],
          [
            "400",
            1
          ],
          [
            "escribir",
            1
          ],
          [
            "razor",
            1
          ],
          [
            "reto",
            1
          ],
          [
            "recibe",
            1
          ],
          [
            "pero",
            1
          ],
          [
            "según",
            1
          ],
          [
            "endpoint",
            1
          ],
          [
            "dato",
            1
          ],
          [
            "autónoma",
            1
          ],
          [
            "segundo",
            1
          ],
          [
            "criterio",
            1
          ],
          [
            "independiente",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "o",
            5
          ],
          [
            "e",
            4
          ],
          [
            "p",
            3
          ],
          [
            "a",
            2
          ],
          [
            "ó",
            2
          ],
          [
            "u",
            2
          ],
          [
            "del",
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
          ]
        ]
      },
      {
        "punto": "P2.2",
        "desde": 16,
        "hasta": 28,
        "palabras_visibles_md": 4162,
        "palabras_extraidas_pdf": 4171,
        "cobertura": 0.994234,
        "tokens_no_encontrados": 24,
        "ejemplos_missing": [
          [
            "2",
            4
          ],
          [
            "p2",
            2
          ],
          [
            "continuidad",
            2
          ],
          [
            "tag",
            1
          ],
          [
            "una",
            1
          ],
          [
            "el",
            1
          ],
          [
            "antiforgery",
            1
          ],
          [
            "form",
            1
          ],
          [
            "helper",
            1
          ],
          [
            "final",
            1
          ],
          [
            "diagnóstico",
            1
          ],
          [
            "preparar",
            1
          ],
          [
            "entorno",
            1
          ],
          [
            "paso",
            1
          ],
          [
            "interfaz",
            1
          ],
          [
            "investigar",
            1
          ],
          [
            "hacia",
            1
          ],
          [
            "guiada",
            1
          ],
          [
            "resolución",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "a",
            5
          ],
          [
            "co",
            3
          ],
          [
            "u",
            3
          ],
          [
            "o",
            2
          ],
          [
            "e",
            2
          ],
          [
            "ag",
            2
          ],
          [
            "dad",
            2
          ],
          [
            "y",
            1
          ],
          [
            "es",
            1
          ],
          [
            "p",
            1
          ]
        ]
      },
      {
        "punto": "P2.3",
        "desde": 29,
        "hasta": 44,
        "palabras_visibles_md": 5416,
        "palabras_extraidas_pdf": 5423,
        "cobertura": 0.995753,
        "tokens_no_encontrados": 23,
        "ejemplos_missing": [
          [
            "validación",
            2
          ],
          [
            "los",
            1
          ],
          [
            "2",
            1
          ],
          [
            "servidor",
            1
          ],
          [
            "mensajes",
            1
          ],
          [
            "dotnet",
            1
          ],
          [
            "build",
            1
          ],
          [
            "dos",
            1
          ],
          [
            "una",
            1
          ],
          [
            "paso",
            1
          ],
          [
            "cshtml",
            1
          ],
          [
            "diagnóstico",
            1
          ],
          [
            "comparar",
            1
          ],
          [
            "más",
            1
          ],
          [
            "distintos",
            1
          ],
          [
            "div",
            1
          ],
          [
            "produce",
            1
          ],
          [
            "problemas",
            1
          ],
          [
            "habituales",
            1
          ],
          [
            "operación",
            1
          ]
        ],
        "ejemplos_extra": [
          [
            "p",
            4
          ],
          [
            "a",
            3
          ],
          [
            "co",
            2
          ],
          [
            "dac",
            2
          ],
          [
            "ó",
            2
          ],
          [
            "es",
            1
          ],
          [
            "se",
            1
          ],
          [
            "cshtm",
            1
          ],
          [
            "l",
            1
          ],
          [
            "aso",
            1
          ]
        ]
      },
      {
        "punto": "P2.4",
        "desde": 45,
        "hasta": 63,
        "palabras_visibles_md": 6275,
        "palabras_extraidas_pdf": 6241,
        "cobertura": 0.993625,
        "tokens_no_encontrados": 40,
        "ejemplos_missing": [
          [
            "la",
            2
          ],
          [
            "nombre",
            2
          ],
          [
            "consulta",
            2
          ],
          [
            "incidencia",
            2
          ],
          [
            "editar",
            1
          ],
          [
            "productos",
            1
          ],
          [
            "inicial",
            1
          ],
          [
            "el",
            1
          ],
          [
            "de",
            1
          ],
          [
            "los",
            1
          ],
          [
            "no",
            1
          ],
          [
            "su",
            1
          ],
          [
            "aplicación",
            1
          ],
          [
            "existe",
            1
          ],
          [
            "semilla",
            1
          ],
          [
            "index",
            1
          ],
          [
            "dotnet",
            1
          ],
          [
            "build",
            1
          ],
          [
            "dato",
            1
          ],
          [
            "cuando",
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
            "p",
            1
          ],
          [
            "trustservercer",
            1
          ],
          [
            "tificate",
            1
          ],
          [
            "g",
            1
          ]
        ]
      },
      {
        "punto": "P2.5",
        "desde": 64,
        "hasta": 72,
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
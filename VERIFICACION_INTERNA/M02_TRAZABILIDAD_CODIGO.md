# M02 — Trazabilidad entre práctica, código y pruebas

Informe técnico interno. No forma parte del material destinado al alumno.

## Evolución de las instantáneas

| Punto | Archivos del estado | Archivos nuevos o modificados explicados en la práctica | Retiradas explícitas |
|---|---:|---:|---|
| P2.1 | 21 | 7 | `README.md` de P1.5, documento local de aquella instantánea |
| P2.2 | 21 | 5 | Ninguna |
| P2.3 | 23 | 7 | Ninguna |
| P2.4 | 24 | 12 | `Views/Productos/Confirmacion.cshtml` y `Views/Shared/_ValidationScriptsPartial.cshtml` |
| P2.5 | 28 | 10 | Ninguna |

La retirada del README se explica en el punto de partida de P2.1. Las dos retiradas de P2.4 están explicadas en la propia práctica: el alta persistente redirige a la ficha del registro creado y la validación obligatoria sigue ejecutándose en servidor aunque la demostración de scripts cliente no forme parte de esa instantánea.

La comprobación literal global M01-M02 sigue estando documentada en `M01_M02_TRAZABILIDAD_FUENTES.md`: las secciones de construcción transcriben los archivos nuevos o modificados de cada estado. Esta revisión añade el criterio pedagógico que la comparación literal no podía acreditar.

## Correspondencia pedagógica revisada

Tras la revisión, cada archivo transcrito de P2.1-P2.5 dispone de una explicación específica de su responsabilidad:

- P2.1 distingue controlador GET/POST, formulario HTML, antiforgery, confirmación sin persistencia y regresiones del catálogo.
- P2.2 explica qué HTML genera cada Tag Helper y por qué el contrato HTTP del controlador no cambia.
- P2.3 relaciona `ProductoFormulario`, DataAnnotations, model binding, `ModelState`, mensajes de campo, scripts cliente opcionales y validación de servidor.
- P2.4 explica proveedor EF Core, entidad, modelo de entrada, `AppDbContext`, registro/configuración, LocalDB, Create/Read/Update/Delete y persistencia.
- P2.5 explica el registro y mapeo de Razor Pages, `@page`, `PageModel`, handlers, imports, layout compartido y continuidad del CRUD MVC.

Se eliminaron las explicaciones genéricas repetidas que aparecían después de archivos diferentes. El código transcrito no se modificó durante esa corrección editorial.

## Pruebas versionadas

| Punto | Script | Cobertura funcional |
|---|---|---|
| P2.1 | `M02_FORMULARIOS_RAZOR/TESTS/2.1_e2e.sh` | GET formulario, POST inicialmente no habilitado, antiforgery 400, model binding, respuesta con token, aplicación autónoma, reto y ausencia de persistencia |
| P2.2 | `M02_FORMULARIOS_RAZOR/TESTS/2.2_e2e.sh` | Transformación a Tag Helpers, un único formulario/token, POST protegido, rutas generadas y regresión del catálogo |
| P2.3 | `M02_FORMULARIOS_RAZOR/TESTS/2.3_e2e.sh` | Required, StringLength, Range, errores de conversión, conservación de valores, reto de ModelState y scripts cliente |
| P2.4 | `M02_FORMULARIOS_RAZOR/TESTS/2.4_e2e.ps1` | Windows/LocalDB aislada, Read, Create, errores, Edit, Delete, antiforgery, PRG y persistencia después de reiniciar |
| P2.5 | `M02_FORMULARIOS_RAZOR/TESTS/2.5_e2e.ps1` | Razor Pages GET/POST, antiforgery, DataAnnotations, navegación MVC-Pages, aplicación autónoma, segundo handler y catálogo MVC conservado |

El workflow `.github/workflows/m02-ci.yml` ejecuta P2.1-P2.3 en Ubuntu y P2.4-P2.5 en Windows, donde se comprueba la presencia de SQL Server Express LocalDB.

## Límites del estado actual

Este informe describe la correspondencia de fuentes y el alcance de los scripts versionados. La creación del workflow no equivale por sí sola a afirmar que el run asociado al HEAD actual haya terminado con éxito; ese resultado debe comprobarse en GitHub Actions.

Los PDF existentes fueron generados antes de las últimas correcciones pedagógicas: el informe documental anterior registra 32.982 palabras para prácticas, mientras el Markdown actual contiene más contenido específico. Por tanto deben regenerarse desde los Markdown actuales y someterse de nuevo a la comprobación visual página a página antes del cierre definitivo de M02.

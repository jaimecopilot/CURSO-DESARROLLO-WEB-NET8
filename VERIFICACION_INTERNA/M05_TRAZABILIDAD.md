# M05 — Trazabilidad técnica interna

Este archivo **no forma parte de los manuales del alumno**. Documenta la correspondencia entre los puntos del temario, sus ejemplos, los ejercicios, los archivos efectivamente existentes y las pruebas que se deben ejecutar.

| Punto | Conocimiento explicado en teoría | Construcción guiada en prácticas | Archivos / elementos | Observaciones exigidas | Automatización |
|---|---|---|---|---|---|
| 5.1 | Interactive Server, servicios tipados, DTO, GET/POST, fallo de red/HTTP/JSON, memoria vs estado | P5.1.1–P5.1.7: compilar API/Blazor, ejecutar, añadir botón, crear, invalidar, refrescar, recuperar | `PROYECTO/BLAZOR/CursoWeb.Blazor/Components/Pages/CatalogoRemoto.razor`; `Services/ProductosApiService.cs`; `PROYECTO/API/CursoWeb.ProductosApi/Program.cs`; `PROYECTO/VARIANTES/P5.1_ANTES/...` | GET 200, detalle 404, POST 201/400, UI interactiva, actualización explícita, error tras detener API | `m05-integracion.yml` API HTTP; `m05-blazor-browser.yml` para navegador |
| 5.2 | Build vs run vs publish; dependencias; runtimeconfig; artefactos; entorno | P5.2: compilar, ejecutar, publicar a `.work/M05/publicacion-mvc`, inspeccionar artefactos | `PROYECTO/MVC/CursoWeb.Mvc/CursoWeb.Mvc.csproj`, `Program.cs`, `appsettings.json`, `wwwroot` | build/publish OK, DLL + assets, no sustitución de SqlServer por SQLite | `m05-integracion.yml` |
| 5.3 | Kestrel, dirección de escucha, routing, puertos ocupados, diferencia entre CRUD y rutas sin base | P5.3: arrancar DLL, comprobar HTML/estado/CSS/503, detener proceso | Misma salida MVC P5.2 y variable `Despliegue__SinLocalDb` | HTTP 200/200/200 y 503 documentado | `m05-integracion.yml` |
| 5.4 | ANCM, Hosting Bundle, pool No Managed Code, sitio/binding/identidad, dependencia LocalDB | P5.4: publicar MVC A a IIS, configurar pool/sitio, aislar DB en modo Production, verificar rutas | MVC A publicado; archivo de configuración solo en carpeta de despliegue | `http://localhost:8091/`, `.../Productos/Estado`, CSS; `Productos` devuelve 503 en modo sin base | IIS Windows real **SUCCESS**, ejecución 38456317027: instalación IIS/Hosting Bundle, publicación de MVC y HTTP 200 en inicio/Estado/CSS; 503 esperado en ruta dependiente de LocalDB. |
| 5.5 | Imagen vs contenedor, build multietapa, puertos host/contenedor, límites de LocalDB Linux | P5.5: build, run real, GET, logs, stop, cleanup | `PROYECTO/MVC/CursoWeb.Mvc/Dockerfile`, `.dockerignore`, `Program.cs` con modo explícito | Docker host 8081 → contenedor 8080; HTTP 200/200/200/503; logs y limpieza | `m05-integracion.yml` |

## Estados iniciales versionados

Se conserva el código Blazor anterior a la incorporación del botón de recarga en `PROYECTO/VARIANTES/P5.1_ANTES/Components/Pages/CatalogoRemoto.razor`. Se conserva el `Program.cs` MVC proveniente de M02 antes de introducir el modo de despliegue en `PROYECTO/VARIANTES/P5.2_ANTES/Program.cs`. Ambos están **fuera de las carpetas que compila cada proyecto** para impedir tipos duplicados.

Las variantes son referencias didácticas, no proyectos alternativos para desplegar. El alumno puede comparar las diferencias con el estado acumulativo de M05 sin recibir una segunda solución empresarial.

## Limitaciones que no pueden deducirse de SUCCESS

1. Compilar Blazor y obtener HTTP 200 del host no demuestra por sí mismo que funcionen los eventos de una página interactiva. Se requiere el workflow browser específico.
2. Comprobar API GET/POST no demuestra la totalidad de errores de navegación ni el tratamiento visual de una desconexión; deben ejecutarse por separado.
3. Publicar MVC y comprobar 200 de rutas independientes de SQL no demuestra el CRUD en LocalDB. Su validación corresponde al módulo de origen o a un ensayo Windows adicional.
4. Docker HTTP 200 no demuestra IIS. Son procesos y mecanismos distintos.
5. Los tiempos de 60/270/30 minutos no han sido medidos en una clase piloto y son estimaciones docentes.
6. El número de palabras, el número de páginas y la compilación no sustituyen la auditoría de comprensión conceptual ni la revisión visual completa.

## Estado editorial y pruebas verificadas a 14/10/2026

Los dos Markdown son las fuentes canónicas; sus PDF homónimos están publicados exclusivamente en `desarrollo/m05-consolidacion-despliegue`, sin integración en `main`.

| Documento | Palabras del MD | Páginas del PDF | Integridad |
|---|---:|---:|---|
| M05_TEORIA | 32.607 | 75 | MD íntegro adjunto al PDF y cobertura visible 100 % |
| M05_PRACTICAS | 28.118 | 76 | MD íntegro adjunto al PDF y cobertura visible 99,9832 % |

La publicación se realizó con la tipografía del M01: texto 9,8 pt y código 8,2 pt. Los controles automatizados confirmaron los cinco capítulos, los enlaces del índice, la presencia de texto en todas las páginas, la ausencia de desbordamientos simples y la identidad binaria entre la fuente Markdown y la incorporada a cada PDF. Véase `VERIFICACION_INTERNA/M05_PDFS_VALIDACION.md`.

**Evidencias GitHub Actions verificadas:**

- IIS Windows real: `38456317027`, SUCCESS, con ANCM, servidor HTTP y restricciones explícitas de LocalDB.
- Blazor en navegador Chromium: `38458993456`, SUCCESS para catálogo normal, vacío y respuesta JSON inválida. Ejecuciones posteriores también validaron el comportamiento del componente.
- Integración de Blazor/API, publicación Kestrel y contenedor Docker Linux real: `38517424599`, SUCCESS.
- Publicación PDF canónica y puertas documentales: `38516974252`, SUCCESS.
- Medición de PDF y renderizado de cada página a imagen: `38516974256`, SUCCESS.

**Límite de la evidencia:** la revisión visual se efectuó sobre mosaicos de todas las páginas renderizadas, complementados con comprobaciones automatizadas individuales de texto y límites de cada página. Existe una revisión pedagógica documental y de trazabilidad; estos controles no sustituyen una clase piloto real con alumnos ni garantizan que toda la infraestructura esté disponible. La descripción detallada está en `M05_CIERRE_VISUAL_PEDAGOGICO_2026-10-14.md`.

## Variantes del alumno y correspondencia añadida

- P5.1: `PROYECTO/VARIANTES/P5.1_ANTES/Components/Pages/CatalogoRemoto.razor` sirve como estado anterior al botón de consulta.
- P5.1: `PROYECTO/VARIANTES/P5.1_DIAGNOSTICO/Program.cs` incorpora escenarios reversibles de catálogo vacío, JSON inválido, 404 y 500; se describen copia de seguridad y restauración.
- P5.2: `PROYECTO/VARIANTES/P5.2_CAMBIO_VISTA/Views/Home/Index.cshtml` permite contrastar publicaciones A y B de la misma aplicación.
- P5.2: `PROYECTO/VARIANTES/P5.2_ANTES/Program.cs` recoge el estado previo al modo sin LocalDB.
- P5.5: el alumno reconstruye gradualmente el Dockerfile con referencia y restauración; el proyecto acumulativo conserva su versión compilable.

**Criterio de interpretación:** 75/77 páginas entra en el intervalo técnico aprobado de 75–100 para una extensión aproximada de 80, pero el cumplimiento cuantitativo y las pruebas automáticas no garantizan por sí solos la ausencia de redundancia ni una calidad didáctica ya revisada visualmente. Estas son comprobaciones independientes.

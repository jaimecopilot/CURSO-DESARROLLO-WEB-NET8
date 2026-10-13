# M05 — Trazabilidad técnica interna

Este archivo **no forma parte de los manuales del alumno**. Documenta la correspondencia entre los puntos del temario, sus ejemplos, los ejercicios, los archivos efectivamente existentes y las pruebas que se deben ejecutar.

| Punto | Conocimiento explicado en teoría | Construcción guiada en prácticas | Archivos / elementos | Observaciones exigidas | Automatización |
|---|---|---|---|---|---|
| 5.1 | Interactive Server, servicios tipados, DTO, GET/POST, fallo de red/HTTP/JSON, memoria vs estado | P5.1.1–P5.1.7: compilar API/Blazor, ejecutar, añadir botón, crear, invalidar, refrescar, recuperar | `PROYECTO/BLAZOR/CursoWeb.Blazor/Components/Pages/CatalogoRemoto.razor`; `Services/ProductosApiService.cs`; `PROYECTO/API/CursoWeb.ProductosApi/Program.cs`; `PROYECTO/VARIANTES/P5.1_ANTES/...` | GET 200, detalle 404, POST 201/400, UI interactiva, actualización explícita, error tras detener API | `m05-integracion.yml` API HTTP; `m05-blazor-browser.yml` para navegador |
| 5.2 | Build vs run vs publish; dependencias; runtimeconfig; artefactos; entorno | P5.2: compilar, ejecutar, publicar a `.work/M05/publicacion-mvc`, inspeccionar artefactos | `PROYECTO/MVC/CursoWeb.Mvc/CursoWeb.Mvc.csproj`, `Program.cs`, `appsettings.json`, `wwwroot` | build/publish OK, DLL + assets, no sustitución de SqlServer por SQLite | `m05-integracion.yml` |
| 5.3 | Kestrel, dirección de escucha, routing, puertos ocupados, diferencia entre CRUD y rutas sin base | P5.3: arrancar DLL, comprobar HTML/estado/CSS/503, detener proceso | Misma salida MVC P5.2 y variable `Despliegue__SinLocalDb` | HTTP 200/200/200 y 503 documentado | `m05-integracion.yml` |
| 5.4 | ANCM, Hosting Bundle, pool No Managed Code, sitio/binding/identidad, dependencia LocalDB | P5.4: publicar MVC A a IIS, configurar pool/sitio, aislar DB en modo Production, verificar rutas | MVC A publicado; archivo de configuración solo en carpeta de despliegue | `http://localhost:8091/`, `.../Productos/Estado`, CSS; `Productos` devuelve 503 en modo sin base | **Pendiente prueba IIS Windows real**. Kestrel no se acepta como sustituto. |
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

## Estado editorial

Los Markdown de teoría y prácticas de M05 están en **fase de desarrollo**, no cerrados. No publicar PDF definitivo hasta completar la extensión pedagógica útil, comparar código/pasos, ejecutar pruebas de navegador y plataformas disponibles, y cerrar editorialmente ambas fuentes con la tipografía M01 de 9,8/8,2 pt.

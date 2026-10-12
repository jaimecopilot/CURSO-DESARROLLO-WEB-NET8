# M01 — Contrato de reconstrucción didáctica de los cinco puntos

**Carácter:** organización interna, no se incorpora a los manuales del alumno.  
**Estado:** reconstrucción editorial en curso.  
**Decisión esencial del autor:** mejorar la narración de **teoría primero**; después acondicionar **prácticas y proyectos reales**. La meta editorial de aproximadamente 80 páginas de teoría y 80 de prácticas representa profundidad de referencia, no autorización para duplicar contenido.

## Diagnóstico editorial frente a la versión publicada

- La edición anterior acumuló ampliaciones que rompían el hilo de aprendizaje.
- La reducción posterior afectó principalmente al manual de prácticas, no a la homogeneización completa de la teoría: el diff de prácticas perdió más de mil líneas, mientras la teoría quedó casi intacta.
- Las pruebas E2E existentes acreditan los escenarios programados, **no** la progresión didáctica entre teoría, instrucciones y código.
- **Ningún PDF actual debe presentarse como la edición definitiva del M01:** el Markdown vuelve a modificarse mientras se reconstruye el contenido.

## Método obligatorio de reescritura

Para cada capítulo:
1. **Planteamiento del problema real** a resolver sobre el mismo catálogo MVC.
2. **Conceptos nuevos y explicación continua**, aprovechando C#, Web API, HTTP y EF Core ya aprendidos. No acumular tablas o epígrafes equivalentes.
3. **Ejemplo mínimo auténtico** que coincida con el estado real del proyecto del punto.
4. **Interpretación de ejecución y errores frecuentes**, sin confundir teoría con scripts internos de validación.
5. **Práctica guiada conectada conceptualmente**, que evolucione hacia una actividad de escritura o decisión propia.
6. **Reto autónomo antes de mostrar solución**, con referencia técnicamente verificable.
7. **Ampliaciones de consulta integradas en lugares lógicos**, no concatenadas tras una bibliografía o tras el cierre del capítulo.
8. **Revisión vertical concepto → ejercicio → archivo → edición → resultado**, antes de reescribir el siguiente punto.

No retirar texto por longitud; conservar el aprendizaje único. No reintroducir repeticiones para perseguir páginas. No regenerar PDF hasta cerrar Markdown, proyectos y comprobaciones.

## Correspondencia pedagógica canónica

| Teoría | Práctica y actividad principal | Código real del estado correspondiente | Resultado observable | Revisión didáctica |
|---|---|---|---|---|
| 1.1 HTTP y diferencia MVC/API | P1.1.1–1.1.3: crear plantilla, arrancar y recorrer solicitud | `1.1/CursoWeb.Mvc/Program.cs`, `HomeController.cs`, `Views/Home/Index.cshtml` | `GET /` y `GET /Home/Index`: HTML 200, CSS 200, ruta desconocida 404 | Unificar teoría sobre JSON/HTML; evitar volver a introducir el mismo concepto |
| 1.1 cabecera HTTP y Razor | P1.1.4, P1.1.5: activar cabecera y vista, y escribir un nuevo párrafo HTML autónomo | `1.1/CursoWeb.Mvc/Controllers/HomeController.cs`; `Views/Home/Index.cshtml` | Cabecera `X-Curso-Paso` y nuevo párrafo independiente en cuerpo; variante autónoma contrastable | **Iniciado**: teoría y práctica modificadas, comentario de trabajo en Razor y escenario E2E añadido |
| 1.1 razonamiento HTTP | P1.1.6 y reto: comparar recursos y cambiar dos zonas de la respuesta | `HomeController.cs`, `Views/Home/Index.cshtml`, `wwwroot/css/site.css` | Diferencia entre 200/404, CSS, cabeceras y HTML | Separar reto de solución |
| 1.2 responsabilidades MVC | P1.2.1–1.2.3: identificar y entregar `Producto` | `1.2/CursoWeb.Mvc/Models/Producto.cs`, `Controllers/ProductosController.cs` | `View(productos)`: contador con tres objetos | Reescribir teoría en progresión modelo → controlador → vista |
| 1.2 modelo de vista y layout | P1.2.4–1.2.6: mostrar elementos, navegar y explicar origen de datos | `Views/Productos/Index.cshtml`, `Views/Shared/_Layout.cshtml` | Tres productos y navegación; variante Bloc en reto | Sustituir activaciones mecánicas por decisiones justificadas |
| 1.3 proyecto, configuración y raíz web | P1.3.1–1.3.5: localizar, registrar, servir CSS y recursos | `1.3/CursoWeb.Mvc/Program.cs`, `appsettings.json`, `Views/Shared/_Layout.cshtml`, `wwwroot` | Log de configuración, CSS público, fichero de texto disponible | Distinguir ubicación, hospedaje y recurso sin recorrer dos veces los mismos archivos |
| 1.3 publicación de archivos | Reto 1.3: decidir qué es público y por qué | `wwwroot/recursos/aviso-laboratorio.txt`, `DOCUMENTACION/nota-interna.txt` | 200 en archivo público, 404 fuera de raíz web | Explicar por qué no debe confundirse con protección de secretos |
| 1.4 acciones y routing | P1.4.1–1.4.5: texto, detalles, ruta por atributos y enlaces | `1.4/CursoWeb.Mvc/Controllers/ProductosController.cs`, `Views/Productos/Detalle.cshtml`, `Index.cshtml` | 200 HTML/texto, 400/404 de detalle, ficha por ruta de atributo | Unificar razonamiento de selección, validación de id y `IActionResult` |
| 1.4 tipos de respuesta | Reto 1.4: elegir JSON sin nueva vista | `ProductosController.Resumen` preparado como variante | JSON con id/nombre o 404 | El alumno debe proponer la acción antes de leer el código resuelto |
| 1.5 composición Razor | P1.5.1–1.5.3: modelo tipado, condición y sección opcional | `1.5/CursoWeb.Mvc/Views/Productos/Index.cshtml`, `Detalle.cshtml`, `Shared/_Layout.cshtml` | Catálogo con mensaje condicional; nota de ficha | Diferenciar tipos de modelo y secciones sin repetición de MVC básico |
| 1.5 vistas parciales | P1.5.4–1.5.5 y reto: misma tarjeta desde lista y detalle | `Views/Shared/_TarjetaProducto.cshtml`, vistas de productos | Tarjetas reutilizadas; Lápiz con etiqueta económica | Escribir/razonar regla en la parcial antes de descubrir la variante preparada |

## Puertas de cierre

- Calidad de la **teoría completa** 1.1–1.5: un hilo narrativo continuo, sin epígrafes, diagramas o ejemplos redundantes, con ampliaciones útiles y bibliografía al final.
- Cada práctica 1.1–1.5 se ajusta a la teoría nueva, con ruta real de archivo, estado inicial, acción del alumno y resultados verificables.
- Cada requisito nuevo de un ejercicio tiene código o fragmento construido por el alumno y **solución reproducible**; todos los estados necesarios se compilan y ejecutan realmente.
- Se verifican progresión, continuidad y no dependencia de retos opcionales.
- Solo al terminar, se regeneran PDF desde Markdown, se inspeccionan visualmente y se verifica la extensión de los dos manuales sin añadir relleno.
- Sin aceptación humana no se fusiona `main`. M02 conserva su rama pero se actualizará desde el M01 definitivamente aceptado antes de cerrar M02.

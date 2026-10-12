# M01 — Inspección visual y pedagógica de teoría y prácticas

**Fecha:** 2026-10-12  
**Rama:** `revision-didactica/m01`  
**Versión de referencia auditada visualmente:** generación GitHub `38270179420`.  
**Alcance completo:** 84 páginas teoría + 75 páginas prácticas = **159 páginas**.

**Estado de aprobación:** **NO APROBADO para distribución final** mientras no se contraste la nueva versión posterior a esta inspección visual, no exista un paquete estable para el alumnado y no se haya completado una evaluación docente de tiempos y progresión.

## Metodología

Se renderizaron y examinaron las 159 páginas de los PDF originales; se agruparon en 40 paneles numerados y se revisaron las páginas sospechosas individualmente. La extracción estructurada de PDF aportó tamaño tipográfico, posición de cajas de texto, contenido, páginas y detección de recortes. La evaluación didáctica cruzó teoría, prácticas, proyectos y resultados del run E2E `38270086748` (SUCCESS).

Se distingue **integridad de PDF** de **calidad pedagógica**: páginas completas y código compilable no implican una buena secuencia de aprendizaje.

## Observaciones visuales de la edición de 159 páginas

| Documento | Páginas | Incidencia |
|---|---|---|
| Teoría | 19–20 | Bibliografía aislada en página 20, casi vacía |
| Teoría | 26–27, 38–39 | Gráficos desplazados respecto de su texto introductorio |
| Teoría | 3–4, 57–58 | Bloques fuente partidos en salto de página |
| Teoría | 14, 37, 41, 51, 63, 72, 75, 78, 81, otras | **15** marcadores de «Se reutiliza el fragmento…», incluida repetición inmediata |
| Teoría | 54–59 | Recorrido repetido de `Detalle(int id)` con riesgo de exceso de explicación |
| Teoría | 33, 48, 68, 84 | Cierres con desequilibrio de contenido y blancos excesivos |
| Prácticas | 3 | Clonación de rama editorial `revision-didactica/m01` en un manual destinado a estudiantes |
| Prácticas | 19–20, 56–57 | Código partido entre páginas consecutivas |
| Prácticas | 14, 27, 57, 75 | Finales de capítulo muy poco ocupados |
| Prácticas | 8–14 | Diagnósticos HTTP parcialmente repetidos |
| Prácticas | 34–37 | Aplicación autónoma más exigente que el reto guiado siguiente |
| Prácticas | 65–69 | Dos condiciones de precio similares sin transferencia claramente graduada |
| Prácticas | 48–49, 72–75 | Falta de evidencia inicial del resultado acumulado con todas las variantes |

En ambos: sin páginas completamente ilegibles ni bloques fuera de los márgenes detectados; caracteres y diagramas presentes. **Cuerpo 9,3 pt**, código aproximadamente 7,75 pt, sin metadatos de autor/título ni hipervínculos bibliográficos; hay margen de mejora para lectura impresa y accesibilidad.

## Evaluación de progresión docente

1. **Objetivos:** definidos de forma clara, conectados con un proyecto MVC.
2. **Arquitectura del curso:** orden HTTP → MVC → archivos/configuración → routing → Razor apropiado para alumnado que conoce C#, Web API y EF Core.
3. **Activación de conocimientos:** casos controlables mediante Kestrel y rutas reales; los resultados explican estados 200/400/404, modelo, vista y recursos estáticos.
4. **Autonomía:** descomentar bloques es útil para demostraciones, pero no basta como evaluación; los ejercicios autónomos de escritura de HTML, Razor, enrutamiento y parciales aportan transferencia.
5. **Secuencia de dificultad:** era inconsistente en P1.3 y P1.5: había ejercicios autónomos avanzados **antes** del reto guiado más simple.
6. **Continuidad:** las carpetas `PROYECTO/1.x` son instantáneas de la **línea troncal**, no acumulaciones automáticas de todas las variantes opcionales. Esto debe comunicarse y probarse.
7. **Carga temporal:** los 159 folios son manuales de referencia. La jornada docente de seis horas NO permite ejecutar todas las ampliaciones; se necesitan indicaciones de obligatoriedad/opcionalidad, especialmente P1.4 y P1.5.
8. **Soluciones:** mostrar soluciones tras los enunciados en un único manual es válido como material de autoestudio, pero debe indicarse que el alumno intenta primero. El profesor no debe utilizar la presencia del resultado resuelto como evidencia de aprendizaje.
9. **Punto por cerrar:** la maquetación y el contenido renovados necesitan una segunda inspección visual y una comprobación final de las instrucciones desde la distribución congelada del curso; la versión antigua no debe presentarse como definitiva.

## Cambios realizados a partir de la inspección

- Eliminados y sustituidos los **15** marcadores genéricos de la teoría por referencias concretas o fragmentos explicativos.
- Retirada del comando de clonación de la rama editorial; indicado el uso del repositorio/paquete estable distribuido por el docente. **El starter definitivo continúa pendiente**.
- Reordenadas las ampliaciones autónomas de P1.3 y P1.5 para que sigan **después** de los retos guiados; identificadas como opcionales.
- Incorporada la búsqueda de P1.4 al código de P1.5 como variante comentada y explicada la diferencia entre estado troncal y ampliaciones.
- Añadido un estado de test acumulativo que combina búsqueda por nombre, las dos etiquetas de precio, parciales, sección y Anchor Tag Helper.
- Ajustado el generador para aumentar legibilidad del texto, completar metadatos PDF y transformar URLs de referencias en vínculos activos, sujetos a revalidación posterior.

## Condiciones de cierre

- GitHub Actions E2E y PDF **SUCCESS** sobre el commit final de todas las modificaciones.
- Informe de edición PDF nueva: recuento, enlaces, metadatos, fuentes y ausencia de recortes, huecos injustificados y código roto por paginación.
- Revisión de contenido por el autor o piloto docente que confirme tiempos y claridad.
- Repositorio de estudiante/starter publicado y clonado desde cero con todos los pasos y rutas reales; sin referencias a ramas internas.
- Sin merge a `main` hasta autorización expresa del autor.

El detalle de las 159 páginas de la primera edición auditada está en la matriz CSV local generada durante esta sesión; la numeración de la nueva edición variará al modificar el diseño y no debe reutilizarse sin volver a mapear las páginas.

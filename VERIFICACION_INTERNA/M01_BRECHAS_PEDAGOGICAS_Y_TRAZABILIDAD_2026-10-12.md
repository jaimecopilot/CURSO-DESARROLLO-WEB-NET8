# M01 — Brechas pedagógicas y de trazabilidad detectadas

**Fecha:** 12/10/2026  
**Repositorio:** `jaimecopilot/CURSO-DESARROLLO-WEB-NET8`  
**Rama:** `revision-didactica/m01`  
**Estado:** REABIERTO POR CALIDAD PEDAGÓGICA. **No fusionar en main ni declarar M01 definitivamente cerrado.**  
**Carácter:** informe interno; no incluir en materiales del alumno.

## Motivo de la reapertura

El compromiso formativo expresado por el autor requiere profundidad equivalente a **aproximadamente 80 páginas de teoría y 80 de prácticas**, sin incorporar texto de relleno ni recuperar duplicaciones. La revisión produjo teoría de 80 páginas y prácticas de solo **61**, después de eliminar grandes bloques que no se evaluaron individualmente en cuanto a su aporte al aprendizaje.

La generación PDF se configuró para permitir menos de 80 páginas: esa corrección técnica no sustituye la decisión editorial del autor sobre profundidad y ejercicios. No puede utilizarse el PDF de 61 páginas como prueba de cierre docente.

## Comparación con la rama anterior

GitHub compare: `desarrollo/m01-mvc...revision-didactica/m01`.

| Magnitud | Resultado |
|---|---:|
| Páginas teoría: anterior → revisada | 80 → 80 |
| Páginas prácticas: anterior → revisada | 81 → 61 |
| Diff prácticas | 1.045 líneas eliminadas, 100 incorporadas |
| Palabras prácticas edición revisada (fidelidad interna) | 21.668 |
| Palabras teoría edición revisada (fidelidad interna) | 33.312 |

Análisis de secciones, mediante recuento uniforme de palabras en la extracción literal del Markdown de cada rama; los valores pueden variar respecto al contador editorial:

| Capítulo | Palabras edición anterior | Palabras revisada | Reducción |
|---|---:|---:|---:|
| P1.1 | 5.267 | 3.574 | 32,1 % |
| P1.2 | 5.494 | 4.278 | 22,1 % |
| P1.3 | 5.644 | 4.203 | 25,5 % |
| P1.4 | 7.467 | 5.465 | 26,8 % |
| P1.5 | 6.770 | 5.061 | 25,2 % |

No es legítimo equiparar automáticamente texto eliminado con duplicaciones: verificar qué actividades, razonamientos y casos de error aportaban aprendizaje único en los fragmentos suprimidos.

## Alcance REAL de la validación existente

- El workflow `M01 - E2E puntos 1.1 a 1.5` terminó SUCCESS: compilación y comprobación HTTP de estados y retos previstos en los scripts existentes.
- La matriz `M01_TRAZABILIDAD_CODIGO.md` comprueba 36 relaciones **práctica → archivo/marca/fragmentos**, mediante cadenas concretas y tests de HTTP.
- El código del M01 bajo `M01_MVC/PROYECTO/1.1`–`1.5` no cambió en el diff entre las dos ramas.
- La verificación **NO** asegura que todas las explicaciones teóricas estén correctamente desarrolladas en las prácticas, que cada nuevo ejercicio o explicación se materialice exactamente en los estados activables, ni que el alumno pueda realizar cada paso sin una solución prematura.
- El verificador de teoría `auditar_trazabilidad_practicas.py` solo comprueba la presencia de los cinco títulos teóricos mediante `require(f"# {point}." in theoretical[point])` dentro de cada capítulo. **NO establece trazabilidad semántica teoría → práctica**.
- Los PDF incrustan fielmente sus Markdown y superaron verificaciones automáticas de integridad. Esto no prueba que el contenido elegido sea didácticamente completo ni sustituye la revisión visual humana página a página.

## Trabajo necesario antes de cerrar M01

1. Comparar el texto retirado de cada punto P1.1–P1.5 con la edición revisada, clasificando cada bloque en **duplicado / útil y ya integrado / único perdido / interrupción del recorrido / ampliación opcional útil**.
2. Restaurar o reescribir únicamente el contenido útil que falte, **dentro del capítulo adecuado**, sin copiar nuevamente un bloque completo ni añadir un «collage» de anexos.
3. Mantener el recorrido fundamental realizable en seis horas, pero recuperar diagnósticos, ejemplos alternativos relevantes, casos negativos y actividades de razonamiento para el material de consulta.
4. Construir una matriz distinta de la verificación estática actual: **concepto teórico → explicación aplicada → paso/reto exacto → archivos involucrados → estado inicial → edición que realiza el alumno → compilación → comportamiento HTTP/HTML → continuidad → solución de referencia**.
5. Evaluar la calidad de cada reto como tarea autónoma, no solo su presencia textual y la ejecución del código entregado.
6. Repetir E2E reales del código después de cualquier modificación funcional, regenerar los 2 PDF desde los Markdown corregidos e inspeccionar visualmente todas las páginas.
7. Comparar la extensión con el objetivo de aproximadamente **80 páginas en cada manual**, y justificar cualquier desviación por razones pedagógicas, no por topes técnicos ni relleno.
8. Dejar M02 sin declarar finalizado: ya existe una rama derivada del M01 anterior a esta reapertura y deberá incorporar las correcciones de M01 antes de su publicación.

## Publicación

Este documento no modifica los manuales del alumno, no desactiva los tests ni fusiona ramas. La edición PDF de 61 páginas es un artefacto técnicamente íntegro **pero pendiente de recuperar la profundidad formativa acordada**.

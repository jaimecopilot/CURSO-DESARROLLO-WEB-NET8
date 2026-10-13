# Generación de PDF canónicos M04

El generador `generar_m04_pdf.py` toma exclusivamente los archivos canónicos
`TEORIA/M04_TEORIA.md` y `PRACTICAS/M04_PRACTICAS.md`. Utiliza el estilo
del curso y no inventa ni parafrasea contenido. Adjunta el Markdown original
en cada PDF y compara el texto visible para detectar omisiones.

Los resultados experimentales permanecen en GitHub Actions hasta que ambos
documentos cumplan el objetivo de extensión y se haya completado la revisión
pedagógica, funcional y visual. Los informes técnicos se escriben fuera de los
documentos destinados al alumnado, en VERIFICACION_INTERNA.

Comando de ensayo: `python M04_APIS_SEGURIDAD/DOCS/generar_m04_pdf.py`.

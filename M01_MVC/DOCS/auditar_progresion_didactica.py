#!/usr/bin/env python3
"""Correspondencia de competencias: teoría, práctica, código inicial y ejecución.

El informe es de uso interno y no se incrusta en los manuales.
Este control analiza presencia y secuencia; los cinco TESTS/*.sh comprueban
de forma independiente compilación, activación y resultados HTTP reales.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
M = ROOT / "M01_MVC"
T = (M / "TEORIA/M01_TEORIA.md").read_text(encoding="utf-8")
P = (M / "PRACTICAS/M01_PRACTICAS.md").read_text(encoding="utf-8")

REQUIREMENTS = [
    # punto, competencia, ancla teórica, ancla de práctica, archivos y anclas de código, ancla de test
    ("1.1", "Diferenciar cabecera HTTP y HTML", "cabecera HTTP", "Paso 1.1.4",
     [("PROYECTO/1.1/CursoWeb.Mvc/Controllers/HomeController.cs", "X-Curso-Paso"),
      ("PROYECTO/1.1/CursoWeb.Mvc/Views/Home/Index.cshtml", "PASO 1.1.5")],
     "X-Curso-Paso"),
    ("1.1", "Redactar HTML autónomo desde la vista", "la vista Razor", "Aplicación autónoma del paso 1.1.5",
     [("PROYECTO/1.1/CursoWeb.Mvc/Views/Home/Index.cshtml", "razonamiento-1-1")],
     "aplicacion-autonoma"),
    ("1.2", "Separar modelo, controlador y vista", "View(productos)", "Paso 1.2.3",
     [("PROYECTO/1.2/CursoWeb.Mvc/Models/Producto.cs", "class Producto"),
      ("PROYECTO/1.2/CursoWeb.Mvc/Controllers/ProductosController.cs", "View(productos)"),
      ("PROYECTO/1.2/CursoWeb.Mvc/Views/Productos/Index.cshtml", "@model")],
     "datos-vista"),
    ("1.2", "Escribir condición sobre el primer modelo", "Model.Count", "Aplicación autónoma P1.2",
     [("PROYECTO/1.2/CursoWeb.Mvc/Views/Productos/Index.cshtml", "APLICACION 1.2.4")],
     "aplicacion"),
    ("1.3", "Configurar MVC sin mezclar recursos públicos", "appsettings.json", "Paso 1.3.3",
     [("PROYECTO/1.3/CursoWeb.Mvc/Program.cs", "Curso:Nombre"),
      ("PROYECTO/1.3/CursoWeb.Mvc/wwwroot/css/catalogo.css", "main.container")],
     "configuracion"),
    ("1.3", "Publicar recurso propio de forma deliberada", "UseStaticFiles", "Aplicación autónoma P1.3",
     [("PROYECTO/1.3/CursoWeb.Mvc/DOCUMENTACION/ejercicio-publicacion.txt", "EJERCICIO DE PUBLICACIÓN"),
      ("PROYECTO/1.3/CursoWeb.Mvc/Views/Shared/_Layout.cshtml", "APLICACION 1.3.5")],
     "ejercicio-publicacion.txt"),
    ("1.4", "Distinguir rutas, parámetros y resultados HTTP", "NotFound()", "Paso 1.4.3",
     [("PROYECTO/1.4/CursoWeb.Mvc/Controllers/ProductosController.cs", "IActionResult Detalle(int id)"),
      ("PROYECTO/1.4/CursoWeb.Mvc/Views/Productos/Detalle.cshtml", "@model")],
     "detalle400"),
    ("1.4", "Programar búsqueda por nombre y reutilizar detalle", "StringComparison.OrdinalIgnoreCase", "Aplicación autónoma P1.4",
     [("PROYECTO/1.4/CursoWeb.Mvc/Controllers/ProductosController.cs", "APLICACION 1.4")],
     "/catalogo/buscar/Cuaderno"),
    ("1.5", "Reutilizar parcial tipada en dos páginas", "_TarjetaProducto.cshtml", "Paso 1.5.5",
     [("PROYECTO/1.5/CursoWeb.Mvc/Views/Shared/_TarjetaProducto.cshtml", "@model"),
      ("PROYECTO/1.5/CursoWeb.Mvc/Views/Productos/Detalle.cshtml", 'partial name="_TarjetaProducto"')],
     "detalle-parcial"),
    ("1.5", "Centralizar condición visual propia en parcial", "precio elevado o económico", "Aplicación autónoma P1.5",
     [("PROYECTO/1.5/CursoWeb.Mvc/Views/Shared/_TarjetaProducto.cshtml", "APLICACION 1.5")],
     "etiqueta-destacada"),
    ("1.5", "Generar enlaces MVC desde el modelo", "Anchor Tag Helper", "Integración final del M01",
     [("PROYECTO/1.5/CursoWeb.Mvc/Views/Shared/_TarjetaProducto.cshtml", "APLICACION 1.5.B"),
      ("PROYECTO/1.5/CursoWeb.Mvc/Views/_ViewImports.cshtml", "@addTagHelper")],
     "navegacion"),
]

def audit() -> None:
    lines = [
        "# M01 — Matriz semántica de competencias y correspondencias",
        "",
        "Informe técnico interno; las referencias remiten al material que trabaja el alumno.",
        "Este control verifica anclas explícitas y secuencias; el comportamiento lo verifican "
        "por separado los scripts de ejecución HTTP con compilación real.",
        "",
        "| Punto | Competencia | Teoría | Práctica | Código inicial | Escenario ejecutable |",
        "|---|---|---|---|---|---|",
    ]
    total=0
    for point, competence, theory, practice, files, test_anchor in REQUIREMENTS:
        title_t = f"# {point}."
        title_p = f"# P{point}."
        assert title_t in T, f"Falta capítulo {title_t}"
        assert title_p in P, f"Falta práctica {title_p}"
        tstart = T.index(title_t)
        tnext = re.search(r"(?m)^# 1\.[1-5]\.", T[tstart + len(title_t):])
        tsection = T[tstart:(tstart+len(title_t)+tnext.start()) if tnext else len(T)]
        pstart = P.index(title_p)
        pnext = re.search(r"(?m)^# P1\.[1-5]\.", P[pstart + len(title_p):])
        psection = P[pstart:(pstart+len(title_p)+pnext.start()) if pnext else len(P)]
        assert theory in tsection, f"{point}: teoría sin explicación de {competence}: {theory}"
        assert practice in psection, f"{point}: práctica sin actividad: {practice}"
        for rel, token in files:
            src = M / rel
            assert src.is_file(), f"Falta código: {rel}"
            assert token in src.read_text(encoding="utf-8"), f"No aparece {token} en {rel}"
        test = (M / "TESTS" / (point + "_e2e.sh")).read_text(encoding="utf-8")
        assert test_anchor in test, f"{point}: test no realiza {competence}: {test_anchor}"
        assert "run_scenario" in test, f"{point}: falta ejecución HTTP"
        lines.append(f"| {point} | {competence} | `{theory}` | `{practice}` | "
                     f"{len(files)} archivos | `{test_anchor}` |")
        total+=1

    # Las referencias no deben aparecer en mitad de una explicación.
    for name, body, prefix in [("Teoría",T,"# 1."),("Prácticas",P,"# P1.")]:
        chunks = re.split(rf"(?m)^(?={re.escape(prefix)}[1-5]\.\s)", body)
        assert len(chunks)>=6, f"{name}: faltan cinco capítulos"
        if name == "Teoría":
            for i, part in enumerate(chunks[1:],start=1):
                m = re.search(r"(?m)^\*\*(?:Referencias técnicas|Referencias de Microsoft Learn|Fuentes y referencias|Lecturas de referencia)\.\*\*",part)
                if m:
                    remaining=part[m.end():].strip()
                    assert remaining.count("\n\n")<8, f"Teoría 1.{i}: bibliografía interrumpe la explicación"

    combined=T+"\n"+P
    for marker in ["pruebas E2E", "GitHub Actions", "informe de auditoría", "workflow de pruebas"]:
        assert marker.lower() not in combined.lower(), f"Referencia interna en manuales: {marker}"
    lines += ["",f"**Competencias contrastadas: {total}.**","",
              "La matriz estática no sustituye la revisión pedagógica humana "
              "ni los escenarios HTTP reales de los cinco capítulos.",""]
    dst=ROOT/"VERIFICACION_INTERNA"/"M01_MATRIZ_COMPETENCIAS.md"
    dst.write_text("\n".join(lines),encoding="utf-8")
    print("\n".join(lines))

if __name__=="__main__":
    audit()

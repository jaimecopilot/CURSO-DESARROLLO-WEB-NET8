#!/usr/bin/env python3
"""Revisión automatizada de integridad de M01. No reemplaza una revisión visual."""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "M01_MVC"
THEORY = BASE / "TEORIA" / "M01_TEORIA.md"
PRACTICES = BASE / "PRACTICAS" / "M01_PRACTICAS.md"

def check(assertion: bool, message: str):
    if not assertion:
        raise AssertionError(message)

def check_document(file: Path, pattern: str) -> dict:
    text = file.read_text(encoding="utf-8")
    chapters = re.findall(pattern, text, re.M)
    expected = [str(n) for n in range(1, 6)]
    check(chapters == expected, f"{file.name}: se esperan capítulos 1.1 a 1.5; hallados {chapters}")
    fences = re.findall(r"^~~~", text, flags=re.M)
    check(len(fences) % 2 == 0, f"{file.name}: cercas Markdown sin cerrar")
    check(len(fences) >= 20, f"{file.name}: código demasiado reducido")
    check("La revisión final de M01 deberá" not in text, f"{file.name}: nota editorial en material docente")
    check("Los PDF se generarán tras cerrar" not in text, f"{file.name}: nota de producción en material docente")
    blocks = re.findall(r"^~~~mermaid\s*$", text, flags=re.M)
    return {
        "archivo": file.relative_to(ROOT).as_posix(),
        "palabras": len(text.split()),
        "caracteres": len(text),
        "lineas": len(text.splitlines()),
        "fragmentos_codigo": len(fences) // 2,
        "diagramas_mermaid": len(blocks),
        "capitulos": chapters
    }

def run() -> dict:
    theory = check_document(THEORY, r"^#\s+1\.([1-5])\.\s+")
    practice = check_document(PRACTICES, r"^#\s+P1\.([1-5])\.\s+")
    all_pract = PRACTICES.read_text(encoding="utf-8")
    all_theory = THEORY.read_text(encoding="utf-8")

    exercises = []
    for i in range(1, 6):
        key = f"1.{i}"
        check(f"# {key}." in all_theory, f"Teoría de {key} no localizada")
        check(f"# P{key}." in all_pract, f"Práctica P{key} no localizada")
        check(f"RETO {key}" in all_pract or f"Reto {key}" in all_pract,
              f"Reto {key} sin código ni explicación")
        project = BASE / "PROYECTO" / key / "CursoWeb.Mvc"
        check((project / "CursoWeb.Mvc.csproj").exists(), f"Proyecto {key} inexistente")
        check((project / "Controllers" / "HomeController.cs").exists(), f"HomeController {key} inexistente")
        sources = list(project.rglob("*.cs")) + list(project.rglob("*.cshtml"))
        check(sources, f"Archivos fuente {key} inexistentes")
        code = "\n".join(p.read_text(encoding="utf-8") for p in sources)
        check(f"RETO {key}" in code, f"El código del reto {key} no está en el proyecto")
        test = BASE / "TESTS" / f"{key}_e2e.sh"
        check(test.exists(), f"Script E2E {key} inexistente")
        test_text = test.read_text(encoding="utf-8")
        check("run_scenario" in test_text and "reto" in test_text,
              f"Falta prueba E2E del reto {key}")
        check(f"PROYECTO/{key}" in all_pract,
              f"La práctica P{key} no referencia su proyecto")
        exercises.append({
            "punto": key, "proyecto": project.relative_to(ROOT).as_posix(),
            "reto_en_proyecto": True, "e2e_definido": True
        })

    for name in ["Models/Producto.cs", "Controllers/ProductosController.cs",
                 "Views/Productos/Index.cshtml", "Views/Productos/Detalle.cshtml",
                 "Views/Shared/_Layout.cshtml", "Views/Shared/_TarjetaProducto.cshtml"]:
        check((BASE/"PROYECTO"/"1.5"/"CursoWeb.Mvc"/name).exists(),
              f"Archivo final de M01 inexistente: {name}")

    report={"estado":"PASS - integridad documental y de trazabilidad estática",
            "teoria":theory, "practicas":practice,"ejercicios":exercises,
            "alcance":"No sustituye compilación, E2E ni inspección visual de PDF"}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=="__main__":
    try: run()
    except Exception as e:
        print("ERROR DE INTEGRIDAD M01:", e, file=sys.stderr)
        raise

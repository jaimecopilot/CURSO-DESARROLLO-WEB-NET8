#!/usr/bin/env python3
"""Comprobación interna de fidelidad de fuentes M03 (no es material del alumno).

Cada bloque integral del cuaderno pertenece al capítulo adecuado y coincide,
carácter por carácter, con el archivo que recibirá el estudiante.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "M03_BLAZOR"
MANUAL = (BASE / "PRACTICAS" / "M03_PRACTICAS.md").read_text(encoding="utf-8")
TEORIA = (BASE / "TEORIA" / "M03_TEORIA.md").read_text(encoding="utf-8")

ARCHIVOS = {
    "3.1": [
        "CursoWeb.Blazor.csproj", "Program.cs",
        "Components/App.razor", "Components/Routes.razor",
        "Components/_Imports.razor", "Components/Layout/MainLayout.razor",
        "Components/Pages/Home.razor", "Components/Pages/Estatica.razor",
        "Components/Pages/Interactiva.razor", "wwwroot/app.css",
        "Properties/launchSettings.json",
    ],
    "3.2": [
        "Models/Producto.cs", "Components/Pages/Productos.razor",
        "Components/Layout/MainLayout.razor",
    ],
    "3.3": [
        "Components/TarjetaProducto.razor",
        "Components/Pages/Productos.razor",
    ],
    "3.4": [
        "Models/Producto.cs", "Components/TarjetaProducto.razor",
        "Components/Pages/Productos.razor",
    ],
    "3.5": [
        "Components/TarjetaProducto.razor",
        "Components/Pages/Productos.razor",
    ],
    "3.6": [
        "Program.cs", "Services/IProductosMemoriaService.cs",
        "Services/ProductosMemoriaService.cs",
        "Components/TarjetaProducto.razor",
        "Components/Pages/Productos.razor",
    ],
}

def chapter(md: str, point: str, manual: bool) -> str:
    prefix = "P" if manual else ""
    matches = list(re.finditer(
        r"(?m)^# " + prefix + re.escape(point) + r"\. ",
        md))
    if len(matches) != 1:
        raise AssertionError(f"{'PRÁCTICA' if manual else 'TEORÍA'} {point}: capítulo no único")
    following = re.search(r"(?m)^# " + prefix + r"3\.[1-6]\. ",
                          md[matches[0].end():])
    end = matches[0].end() + following.start() if following else len(md)
    return md[matches[0].start():end]

def language(file: str) -> str:
    if file.endswith(".razor"): return "razor"
    if file.endswith(".cs"): return "csharp"
    if file.endswith(".json"): return "json"
    if file.endswith(".css"): return "css"
    if file.endswith(".csproj"): return "xml"
    raise AssertionError(f"tipo inesperado: {file}")

total = 0
for number, paths in ARCHIVOS.items():
    sec = chapter(MANUAL, number, manual=True)
    theoretical = chapter(TEORIA, number, manual=False)
    assert re.search(r"(?m)^~~~(?:razor|csharp)", theoretical), \
        f"TEORÍA {number}: ningún ejemplo concreto C#/Razor"
    for rel in paths:
        f = BASE / "PROYECTO" / number / "CursoWeb.Blazor" / rel
        source = f.read_text(encoding="utf-8").rstrip("\r\n")
        exact = "~~~" + language(rel) + "\n" + source + "\n~~~"
        if exact not in sec:
            raise AssertionError(
                f"P{number}: archivo no reproducido íntegramente en su capítulo: {rel}"
            )
        total += 1
    print(f"P{number}: {len(paths)} archivos íntegros en prácticas + teoría con código", flush=True)

# Los dieciséis archivos del estado final son parte del itinerario completo.
final = BASE / "PROYECTO" / "3.6" / "CursoWeb.Blazor"
tracked = {
    x.relative_to(final).as_posix()
    for x in final.rglob("*")
    if x.is_file() and not any(part in {"bin", "obj", ".vs"} for part in x.parts)
}
covered = {x for group in ARCHIVOS.values() for x in group}
if not tracked.issubset(covered):
    raise AssertionError(f"Fuentes finales sin explicación: {sorted(tracked - covered)}")

print(f"M03: {total} transcripciones íntegramente fieles; "
      f"{len(tracked)} archivos finales trazados", flush=True)

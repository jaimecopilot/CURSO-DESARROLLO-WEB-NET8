#!/usr/bin/env python3
"""Comprueba fuentes completas dentro de los capítulos docentes M01 y M02.

No incluye resultados internos en los manuales. Las instantáneas se comparan
desde el estado 1.1 hasta el 2.5, con continuidad entre módulos.
"""
from __future__ import annotations
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    ("M01_MVC", "01", ["1.1", "1.2", "1.3", "1.4", "1.5"]),
    ("M02_FORMULARIOS_RAZOR", "02", ["2.1", "2.2", "2.3", "2.4", "2.5"]),
]
EXT = {".cs", ".cshtml", ".csproj", ".json", ".css", ".txt", ".md", ".xml"}
LANG = {".cs": "csharp", ".cshtml": "cshtml", ".csproj": "xml",
        ".json": "json", ".css": "css", ".txt": "text",
        ".md": "markdown", ".xml": "xml"}

def sources(prefix: Path) -> dict[str, str]:
    result = subprocess.run(["git", "ls-files", "--", str(prefix.relative_to(ROOT))],
                            cwd=ROOT, capture_output=True, text=True, check=True)
    out = {}
    for p in result.stdout.splitlines():
        f = ROOT / p
        if f.suffix in EXT:
            out[f.relative_to(prefix).as_posix()] = f.read_text(encoding="utf-8").rstrip("\r\n")
    return out

def section(md: str, title: str) -> str:
    matches = list(re.finditer("(?m)^# " + re.escape(title) + r"\.", md))
    if len(matches) != 1:
        raise AssertionError(f"Título no único: {title} ({len(matches)} coincidencias)")
    tail = md[matches[0].end():]
    following = re.search(r"(?m)^# (?:P)?[12]\.[1-5]\.", tail)
    return md[matches[0].start(): matches[0].end() + following.start() if following else len(md)]

lines = ["# Trazabilidad integral de fuentes M01–M02", "", 
         "Informe interno, no incluido en los manuales del alumno.", "",
         "| Punto | Archivos del estado | Archivos nuevos o cambiados comprobados | Eliminados |",
         "|---|---:|---:|---:|"]
prev = {}
total = 0
for module, num, points in MODULES:
    md = (ROOT / module / "PRACTICAS" / f"M{num}_PRACTICAS.md").read_text(encoding="utf-8")
    teo = (ROOT / module / "TEORIA" / f"M{num}_TEORIA.md").read_text(encoding="utf-8")
    for p in points:
        s = sources(ROOT / module / "PROYECTO" / p / "CursoWeb.Mvc")
        delta = {k:v for k,v in s.items() if k not in prev or v != prev[k]}
        removed = sorted(set(prev) - set(s))
        practical = section(md, f"P{p}")
        theoretical = section(teo, p)
        if not any(x in theoretical for x in ("~~~csharp", "~~~cshtml")):
            raise AssertionError(f"{p}: teoría sin ejemplos C#/Razor concretos")
        for rel, code in delta.items():
            literal = "~~~" + LANG[Path(rel).suffix] + "\n" + code + "\n~~~"
            if literal not in practical:
                raise AssertionError(f"P{p}: no coincide archivo completo {rel}")
            if f"P{p} — {rel}" not in practical and f"P{p} · {rel}" not in practical:
                raise AssertionError(f"P{p}: falta nombre y explicación para {rel}")
        total += len(delta)
        lines.append(f"| P{p} | {len(s)} | {len(delta)} | {len(removed)} |")
        if removed:
            lines.append(f"Archivos retirados de P{p}: {', '.join(removed)}.")
            lines.append("")
        prev = s
    lines.append("")
lines.extend([
    f"**Transcripciones exactas:** {total}.",
    f"**Archivos de código y recursos del proyecto final P2.5:** {len(prev)}.",
    "",
    "La comprobación es literal y estructural; no constituye por sí sola",
    "una evaluación humana de la redacción o una prueba E2E.",
])
dest = ROOT / "VERIFICACION_INTERNA" / "M01_M02_TRAZABILIDAD_FUENTES.md"
dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Verificados {total} archivos nuevos o modificados con cobertura íntegra; estado final {len(prev)} archivos.")

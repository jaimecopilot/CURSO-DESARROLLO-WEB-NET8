#!/usr/bin/env python3
"""Construye y prueba estados reales extraídos del Markdown de P4.3 (uso interno)."""
from pathlib import Path
import json
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "M04_APIS_SEGURIDAD/PRACTICAS/M04_PRACTICAS.md").read_text(encoding="utf-8")
start = source.index("### Construcción obligatoria — API REST a partir de una plantilla vacía")
end = source.index("### Ampliación P4.3 — comparar", start)
body = source[start:end]


def block_after(heading, nth=0):
    start = body.index(heading)
    match_start = start
    for _ in range(nth + 1):
        a = body.index("```csharp\n", match_start) + len("```csharp\n")
        b = body.index("\n```", a)
        match_start = b + len("\n```")
    return body[a:b].strip() + "\n"


step1 = block_after("**Etapa 1")
step2 = block_after("**Etapa 2")
step3 = block_after("**Etapa 3")
step4 = block_after("**Etapa 4")
dto = block_after("**Etapa 4", nth=1)

assert 'app.MapGet("/api/productos"' in step2
assert 'app.MapPost("/api/productos"' in step4
state3 = step2.replace("app.Run();", step3 + "\napp.Run();", 1)
state4 = state3.replace("app.Run();", step4 + "\napp.Run();", 1) + "\n" + dto

with tempfile.TemporaryDirectory(prefix="m04-practica-alumno-") as temporary:
    root = Path(temporary)
    for number, program in enumerate([step1, step2, state3, state4], start=1):
        project = root / f"etapa{number}"
        subprocess.run(
            ["dotnet", "new", "web", "-n", "CursoWeb.ProductosApi", "-f", "net8.0",
             "-o", str(project), "--no-restore"],
            check=True, capture_output=True, text=True,
        )
        (project / "Program.cs").write_text(program, encoding="utf-8")
        build = subprocess.run(
            ["dotnet", "build", str(project / "CursoWeb.ProductosApi.csproj"), "-c", "Release"],
            capture_output=True, text=True,
        )
        if build.returncode:
            raise AssertionError(f"Etapa {number} no compila:\n{build.stdout}\n{build.stderr}")
        print(f"P4.3 etapa {number}: compilación correcta", flush=True)

    port = 5087
    process = subprocess.Popen(
        ["dotnet", "run", "--no-build", "-c", "Release", "--project",
         str(root / "etapa4" / "CursoWeb.ProductosApi.csproj"), "--urls",
         f"http://127.0.0.1:{port}"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    try:
        base = f"http://127.0.0.1:{port}"
        for attempt in range(45):
            try:
                with urllib.request.urlopen(base + "/api/productos", timeout=2) as response:
                    products = json.load(response)
                    assert response.status == 200
                    break
            except (urllib.error.URLError, TimeoutError):
                if process.poll() is not None:
                    raise AssertionError("La API se detuvo antes de responder")
                time.sleep(1)
        else:
            raise AssertionError("La API no llegó a escuchar")
        assert [p["nombre"] for p in products] == ["Cuaderno", "Lápiz"], products

        with urllib.request.urlopen(base + "/api/productos/1") as response:
            detail = json.load(response)
            assert response.status == 200 and detail["nombre"] == "Cuaderno"
        try:
            urllib.request.urlopen(base + "/api/productos/999")
            raise AssertionError("Se esperaba HTTP 404")
        except urllib.error.HTTPError as error:
            assert error.code == 404

        valid = urllib.request.Request(
            base + "/api/productos",
            data=json.dumps({"nombre": "Regla", "precio": 1.75}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(valid) as response:
            created = json.load(response)
            assert response.status == 201
            assert response.headers["Location"] == "/api/productos/3"
            assert created["id"] == 3 and created["nombre"] == "Regla"

        invalid = urllib.request.Request(
            base + "/api/productos",
            data=json.dumps({"nombre": "", "precio": 0}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(invalid)
            raise AssertionError("Se esperaba HTTP 400")
        except urllib.error.HTTPError as error:
            assert error.code == 400

        print("P4.3: los estados y el contrato se han probado DESDE LOS BLOQUES DEL MD", flush=True)
    finally:
        process.terminate()
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()

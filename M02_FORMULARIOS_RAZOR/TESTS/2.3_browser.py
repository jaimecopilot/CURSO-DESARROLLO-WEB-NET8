#!/usr/bin/env python3
"""Prueba de navegador real P2.3, en copia temporal: validación cliente y servidor."""
from __future__ import annotations
import os, shutil, subprocess, tempfile, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "M02_FORMULARIOS_RAZOR" / "PROYECTO" / "2.3" / "CursoWeb.Mvc"
BASE = "http://127.0.0.1:5198"

def replace_exact(path: Path, old: str, new: str):
    content = path.read_text(encoding="utf-8")
    if content.count(old) != 1:
        raise RuntimeError(f"{path}: se esperaba un único marcador {old!r}, hallados {content.count(old)}")
    path.write_text(content.replace(old,new),encoding="utf-8")

with tempfile.TemporaryDirectory(prefix="m02-p23-browser-") as tmp:
    project = Path(tmp) / "CursoWeb.Mvc"
    shutil.copytree(SOURCE,project,ignore=shutil.ignore_patterns("bin","obj"))
    model=project/"Models"/"ProductoFormulario.cs"
    original=model.read_text(encoding="utf-8")
    for attribute in ("Required", "StringLength", "Range"):
        if f"// [{attribute}(" not in original:
            raise RuntimeError(f"Falta bloque de DataAnnotations {attribute}")
        original=original.replace(f"// [{attribute}(",f"[{attribute}(")
    model.write_text(original,encoding="utf-8")
    view=project/"Views"/"Productos"/"Crear.cshtml"
    original=view.read_text(encoding="utf-8")
    start=original.index("@* PASO 2.3.5 (ACTIVAR)")
    end=original.index("*@",start)+2
    selected='@section Scripts\n{\n    <partial name="_ValidationScriptsPartial" />\n}'
    if selected not in original[start:end]:
        raise RuntimeError("No se encontró la sección Scripts dentro del bloque preparado")
    view.write_text(original[:start]+selected+original[end:], encoding="utf-8")
    print("Estados activados: DataAnnotations y sección Scripts",flush=True)
    subprocess.run(["dotnet","build",str(project/"CursoWeb.Mvc.csproj"),"-c","Release","--nologo"],check=True,timeout=180)
    log=open(Path(tmp)/"kestrel.log","w",encoding="utf-8")
    proc=subprocess.Popen(["dotnet",str(project/"bin"/"Release"/"net8.0"/"CursoWeb.Mvc.dll"),"--urls",BASE],
        cwd=project,stdout=log,stderr=subprocess.STDOUT)
    try:
        for attempt in range(70):
            if proc.poll() is not None:
                raise RuntimeError("Kestrel terminó: "+(Path(tmp)/"kestrel.log").read_text())
            try:
                with urllib.request.urlopen(BASE+"/Productos/Crear",timeout=1) as resp:
                    if resp.status==200:break
            except Exception:time.sleep(.6)
        else:raise RuntimeError("Kestrel no respondió en /Productos/Crear")
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            page=browser.new_page(locale="es-ES")
            errors=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            posts=[]
            page.on("request",lambda req:posts.append(req.url) if req.method=="POST" else None)
            page.goto(BASE+"/Productos/Crear",wait_until="networkidle",timeout=40000)
            try:
                page.wait_for_function("Boolean(window.jQuery && window.jQuery.validator && window.jQuery.validator.unobtrusive)",timeout=12000)
            except Exception as e:
                raise RuntimeError("No se cargaron los tres scripts cliente desde CDN; imposible acreditar la validación de navegador") from e
            page.locator('input[name="Nombre"]').fill("X")
            page.locator('input[name="Precio"]').fill("7")
            page.locator('button[type="submit"]').click()
            page.wait_for_function('document.querySelector("[data-valmsg-for=Nombre]")?.textContent?.includes("entre 2 y 60")',timeout=10000)
            assert page.url.endswith("/Productos/Crear"),"Con entrada inválida se cambió de pantalla"
            assert not posts,"Un formulario inválido produjo POST pese a jQuery Validate"
            print("VALIDACIÓN CLIENTE OK: StringLength, mensaje visible sin enviar POST",flush=True)
            page.locator('input[name="Nombre"]').fill("Ana")
            page.locator('button[type="submit"]').click()
            page.locator("h1").first.wait_for(timeout=10000)
            page.wait_for_url("**/Productos/Crear",wait_until="load",timeout=10000)
            page.wait_for_function('document.body.textContent.includes("Datos recibidos del formulario")',timeout=10000)
            assert posts,"No se observó POST real con datos válidos"
            assert not errors,f"Excepciones JavaScript: {errors}"
            print("FORMULARIO VÁLIDO OK: POST real y página de confirmación; sin errores JS",flush=True)
            browser.close()
    finally:
        proc.terminate()
        try: proc.wait(timeout=8)
        except subprocess.TimeoutExpired:proc.kill()
        log.close()

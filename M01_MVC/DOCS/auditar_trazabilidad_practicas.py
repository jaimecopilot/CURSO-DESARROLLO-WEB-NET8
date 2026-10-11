#!/usr/bin/env python3
"""Verificación estática explícita de P1.1–P1.5: MD → bloque de proyecto → E2E.
La verificación de ejecución HTTP se realiza con los cinco scripts independientes.
No escribe sobre los documentos docentes ni sobre los proyectos del alumno.
"""
from __future__ import annotations
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[2]
M01=ROOT/"M01_MVC"
MD=(M01/"PRACTICAS"/"M01_PRACTICAS.md").read_text(encoding="utf-8")
THEORY=(M01/"TEORIA"/"M01_TEORIA.md").read_text(encoding="utf-8")

# Elemento: paso, archivo de código, delimitador identificable, fragmentos C# o Razor
# necesarios para ejecutar ese paso (pueden permanecer comentados).
SPECS={
"1.1":[
 ("1.1.4","Controllers/HomeController.cs","PASO 1.1.4",['Response.Headers["X-Curso-Paso"] = "1.1.4";']),
 ("1.1.5","Views/Home/Index.cshtml","PASO 1.1.5",['<section id="marca-paso-1-1-5">']),
 ("RETO 1.1","Controllers/HomeController.cs","RETO 1.1",['Response.Headers["X-Curso-Reto"] = "HTTP-y-HTML";']),
 ("RETO 1.1","Views/Home/Index.cshtml","RETO 1.1",['<p id="reto-1-1">']),
],
"1.2":[
 ("1.2.2","Models/Producto.cs","class Producto",["public int Id", "public string Nombre","public decimal Precio"]),
 ("1.2.3","Controllers/ProductosController.cs","PASO 1.2.3",["var productos = new List<Producto>","return View(productos);"]),
 ("1.2.4","Views/Productos/Index.cshtml","PASO 1.2.4",["@foreach (var producto in Model)","id=\"listado-productos\""]),
 ("1.2.5","Views/Shared/_Layout.cshtml","PASO 1.2.5",['href="/Productos"']),
 ("RETO 1.2","Controllers/ProductosController.cs","RETO 1.2",['Nombre = "Cuaderno"','Nombre = "Bloc"']),
],
"1.3":[
 ("1.3.1","CursoWeb.Mvc.csproj","Microsoft.NET.Sdk.Web",["<TargetFramework>net8.0</TargetFramework>"]),
 ("1.3.2","Program.cs","AddControllersWithViews",["app.UseStaticFiles();","app.UseRouting();","app.MapControllerRoute("]),
 ("1.3.3","Program.cs","PASO 1.3.3",['app.Configuration["Curso:Nombre"]','app.Logger.LogInformation(']),
 ("1.3.4","Views/Shared/_Layout.cshtml","PASO 1.3.4",['href="/css/catalogo.css"']),
 ("1.3.4","wwwroot/css/catalogo.css","PASO 1.3.4",["main.container"]),
 ("1.3.5","Views/Shared/_Layout.cshtml","PASO 1.3.5",['href="/recursos/guia-publica.txt"']),
 ("RETO 1.3","Views/Shared/_Layout.cshtml","RETO 1.3",['href="/recursos/aviso-laboratorio.txt"']),
],
"1.4":[
 ("1.4.1","Controllers/ProductosController.cs","PASO 1.4.1",["ObtenerProductosEjemplo()"]),
 ("1.4.2","Controllers/ProductosController.cs","PASO 1.4.2",['IActionResult Estado()','Content("Catalogo MVC disponible", "text/plain")']),
 ("1.4.3","Controllers/ProductosController.cs","PASO 1.4.3",["IActionResult Detalle(int id)","return BadRequest(","return NotFound();","return View(producto);"]),
 ("1.4.3","Views/Productos/Detalle.cshtml","@model",['@model CursoWeb.Mvc.Models.Producto','id="detalle-nombre"']),
 ("1.4.4","Controllers/ProductosController.cs","PASO 1.4.4",['"/catalogo/ficha/{id:int}"','return View("Detalle", producto);']),
 ("1.4.5","Views/Productos/Index.cshtml","PASO 1.4.5",['class="enlace-detalle"','/Productos/Detalle/@producto.Id']),
 ("RETO 1.4","Controllers/ProductosController.cs","RETO 1.4",['"/catalogo/resumen/{id:int}"','return Ok(new { producto.Id, producto.Nombre });']),
],
"1.5":[
 ("1.5.1","Views/Productos/Index.cshtml","@model",["@model IReadOnlyList<CursoWeb.Mvc.Models.Producto>?"]),
 ("1.5.1","Views/Productos/Detalle.cshtml","@model",["@model CursoWeb.Mvc.Models.Producto"]),
 ("1.5.2","Views/Productos/Index.cshtml","PASO 1.5.2",["Model.Count >= 3",'id="catalogo-completo"']),
 ("1.5.3","Views/Shared/_Layout.cshtml","PASO 1.5.3",['RenderSectionAsync("NotasPagina", required: false)']),
 ("1.5.3","Views/Productos/Detalle.cshtml","PASO 1.5.3",["@section NotasPagina",'id="nota-pagina-detalle"']),
 ("1.5.4","Views/Shared/_TarjetaProducto.cshtml","PASO 1.5.4",["@model CursoWeb.Mvc.Models.Producto",'class="tarjeta-producto"']),
 ("1.5.4","Views/Productos/Index.cshtml","PASO 1.5.4",['<partial name="_TarjetaProducto" model="producto" />']),
 ("1.5.5","Views/Productos/Detalle.cshtml","PASO 1.5.5",['<partial name="_TarjetaProducto" model="Model" />']),
 ("RETO 1.5","Views/Shared/_TarjetaProducto.cshtml","RETO 1.5",["Model.Precio < 3m",'class="etiqueta-economico"']),
]
}
expected_counts={"1.1":6,"1.2":5,"1.3":5,"1.4":6,"1.5":6}

def require(test: bool, label: str):
    if not test: raise AssertionError(label)

def sections(source: str, prefix: str) -> dict[str,str]:
    matches=list(re.finditer(rf"(?m)^# {prefix}1\.([1-5])\.",source))
    require(len(matches)==5, f"Se esperaban cinco capítulos de {prefix}")
    return {"1."+m.group(1):source[m.start():(matches[i+1].start() if i+1<len(matches) else len(source))]
            for i,m in enumerate(matches)}

practical=sections(MD,"P")
theoretical=sections(THEORY,"")

def audit():
    lines=["# M01 — Trazabilidad real de prácticas y proyectos","",
           "Informe interno generado desde el código versionado. El PDF procede solo de los MD.",
           "La correspondencia estática verifica archivos, marcas de activación y fragmentos concretos; GitHub Actions valida su compilación y ejecución HTTP por separado.",
           "",
           "| Punto | Pasos y reto en MD | Correspondencias de código | E2E |",
           "|---|---|---:|---|"]
    total=0
    for point,specs in SPECS.items():
        base=M01/"PROYECTO"/point/"CursoWeb.Mvc"
        ptext=practical[point]
        require(f"# {point}." in theoretical[point],f"Teoría {point} no localizada")
        script=M01/"TESTS"/(point+"_e2e.sh")
        test=script.read_text(encoding="utf-8")
        require("run_scenario" in test,f"{point}: script sin ejecución de escenarios")
        require("reto" in test.lower(),f"{point}: script sin reto")
        require(expected_counts[point]>=5,f"{point}: recuento E2E")
        require(f"RETO {point}" in ptext or f"Reto {point}" in ptext, f"{point}: reto ausente del MD")
        seen={}
        for label,relpath,marker,fragments in specs:
            source_path=base/relpath
            require(source_path.is_file(),f"{point}: archivo inexistente {relpath}")
            source=source_path.read_text(encoding="utf-8")
            require(marker in source,f"{point}: marca no existe en {relpath}: {marker}")
            for fragment in fragments:
                require(fragment in source,f"{point}: fragmento no existe en {relpath}: {fragment}")
            require(label in ptext or (label=="1.5.1" and "Paso 1.5.1" in ptext),
                    f"{point}: {label} no explicado en MD")
            seen.setdefault(label,0)
            seen[label]+=1
        # Requisitos que se explican en prácticas aunque no se activen por comentario.
        if point=="1.3":
            for name in ["appsettings.json","wwwroot/recursos/guia-publica.txt",
                         "wwwroot/recursos/aviso-laboratorio.txt","DOCUMENTACION/nota-interna.txt"]:
                require((base/name).is_file(), f"P1.3: falta el archivo de laboratorio {name}")
        # Marcadores de pasos activables que usan scripts; no basta con ver nombres en README.
        markers=[m for m in seen if m.startswith("RETO ") or (m[0].isdigit() and m not in ["1.2.2","1.3.1","1.3.2","1.4.1","1.5.1"])]
        for marker in markers:
            if marker.startswith("RETO ") or marker not in ("1.1.4",):
                require(marker in test or (marker=="1.3.3" and "configuracion 1.3.3" in test),
                        f"{point}: test no localiza marcador activable {marker}")
        require("PASO" in ptext or "Paso" in ptext,
                f"{point}: ausencia de pasos guiados en el MD")
        entries=len(specs)
        total+=entries
        lines.append(f"| P{point} | {len(seen)} etapas distintas, incluido reto | {entries} | {expected_counts[point]} escenarios |")
    lines+=["",f"**Total: {total} correspondencias de código comprobadas.**","",
            "**Límite:** los fragmentos conceptuales de teoría que no se presentan como ejercicios ejecutables no generan código nuevo. "
            "Las pruebas E2E de cada punto verifican las activaciones de los ejercicios, incluida la regresión del catálogo. "
            "Esta auditoría no acredita observación visual de los PDF ni la ejecución manual en Visual Studio.",""]
    report=ROOT/"VERIFICACION_INTERNA"/"M01_TRAZABILIDAD_CODIGO.md"
    report.write_text("\n".join(lines),encoding="utf-8")
    print("\n".join(lines))
if __name__=="__main__": audit()

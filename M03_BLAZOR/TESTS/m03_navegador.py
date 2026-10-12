#!/usr/bin/env python3
"""Prueba interna en Chromium: evolución de los seis puntos de M03.
Activa los comentarios didácticos sobre copias temporales, nunca sobre fuentes.
"""
from __future__ import annotations
import contextlib, os, re, shutil, subprocess, tempfile, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/"M03_BLAZOR"/"PROYECTO"
PORT=5197
BASE=f"http://127.0.0.1:{PORT}"

def edit(project, rel, source, dest):
    file=project/rel
    current=file.read_text(encoding="utf-8")
    if current.count(source)!=1:
        raise RuntimeError(f"{file}: marcador {source!r}, apariciones {current.count(source)}")
    file.write_text(current.replace(source,dest),encoding="utf-8")

def enable_block(project,rel,id):
    file=project/rel
    s=file.read_text(encoding="utf-8")
    start=f"/* {id} INICIO"
    end=f"{id} FIN */"
    if s.count(start)!=1 or s.count(end)!=1:
        raise RuntimeError(f"{file}: bloque {id} no único")
    s=s.replace(start,"").replace(end,"")
    file.write_text(s,encoding="utf-8")

def build_run(browser,point,transform=None,verify=None):
    with tempfile.TemporaryDirectory(prefix="m03-"+point+"-") as temp:
        project=Path(temp)/"CursoWeb.Blazor"
        shutil.copytree(SRC/point/"CursoWeb.Blazor",project,ignore=shutil.ignore_patterns("bin","obj"))
        if transform:transform(project)
        p=subprocess.run(["dotnet","build",str(project/"CursoWeb.Blazor.csproj"),"-c","Release","--nologo","--warnaserror"],capture_output=True,text=True,timeout=180)
        if p.returncode:
            raise RuntimeError(f"P{point} no compila después de activar:\n{p.stdout}\n{p.stderr}")
        log=open(Path(temp)/"kestrel.log","w")
        process=subprocess.Popen(["dotnet",str(project/"bin/Release/net8.0/CursoWeb.Blazor.dll"),"--urls",BASE],cwd=project,stdout=log,stderr=subprocess.STDOUT)
        try:
            import urllib.request
            for _ in range(90):
                if process.poll() is not None:break
                try:
                    with urllib.request.urlopen(BASE+"/",timeout=1) as res:
                        if res.status==200:break
                except Exception:time.sleep(.35)
            else: raise RuntimeError(f"P{point} no arrancó, log: "+Path(temp,"kestrel.log").read_text())
            if process.poll() is not None:raise RuntimeError(f"P{point}: Kestrel terminó"+Path(temp,"kestrel.log").read_text())
            context=browser.new_context()
            page=context.new_page()
            errors=[]
            page.on("pageerror",lambda err:errors.append(str(err)))
            verify(page)
            if errors:raise AssertionError(f"P{point}, JavaScript: {errors}")
            context.close()
            print(f"P{point}: compilación y navegador correctos",flush=True)
        finally:
            process.terminate()
            try:process.wait(timeout=8)
            except subprocess.TimeoutExpired:process.kill()
            log.close()

def verify31(page):
    page.goto(BASE+"/estatica",wait_until="networkidle")
    page.locator("#boton-estatico").click()
    assert page.locator("#contador-estatico").inner_text()=="Pulsaciones: 0"
    page.goto(BASE+"/interactiva",wait_until="networkidle")
    page.locator("#boton-interactivo").click()
    page.get_by_text("Pulsaciones: 1").wait_for(timeout=12000)
def t32(p):
    edit(p,"Components/Layout/MainLayout.razor",'@* <NavLink href="/productos">Productos</NavLink> *@','<NavLink href="/productos">Productos</NavLink>')
def verify32(page):
    page.goto(BASE+"/")
    page.get_by_role("link",name="Productos").click()
    page.wait_for_url("**/productos")
    page.locator("#lista-productos li").nth(2).wait_for(timeout=15000)
    assert page.locator("#lista-productos li").count()==3
def t33(p):
    f=p/"Components/Pages/Productos.razor"
    s=f.read_text(encoding="utf-8")
    start=s.index('<ul id="lista-productos">')
    end=s.index('</ul>',start)+len("</ul>")
    s=s[:start]+s[end:]
    edit_string='''@*
<div class="tarjetas" id="tarjetas-productos">
    @foreach (var producto in productos)
    {
        <TarjetaProducto Producto="producto" />
    }
</div>
*@'''
    assert s.count(edit_string)==1
    s=s.replace(edit_string,edit_string.removeprefix("@*\n").removesuffix("\n*@"))
    f.write_text(s,encoding="utf-8")
def verify33(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    page.locator(".tarjeta").nth(2).wait_for(timeout=15000)
    assert page.locator(".tarjeta").count()==3
    assert page.locator('[data-producto-id="2"]').inner_text().find("Lápiz")>=0
def t34(p):
    f="Components/Pages/Productos.razor"
    for id in ("PASO 3.4.2","PASO 3.4.3","PASO 3.4.4","RETO 3.4"):enable_block(p,f,id)
    for src,dst in [
        ('@* <button @onclick="() => Seleccionar(producto.Id)">Seleccionar</button> *@','<button @onclick="() => Seleccionar(producto.Id)">Seleccionar</button>'),
        ('@* <label>Nombre nuevo: <input id="nombre-nuevo" @bind="nuevoNombre" /></label> *@','<label>Nombre nuevo: <input id="nombre-nuevo" @bind="nuevoNombre" /></label>'),
        ('@* <button id="agregar" @onclick="Agregar">Añadir producto</button> *@','<button id="agregar" @onclick="Agregar">Añadir producto</button>'),
        ('@* <button id="limpiar" @onclick="Limpiar">Limpiar selección</button> *@','<button id="limpiar" @onclick="Limpiar">Limpiar selección</button>')]:
        edit(p,f,src,dst)
def verify34(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    page.locator('[data-producto-id="2"] button').click()
    page.get_by_text("Seleccionado: Lápiz").wait_for(timeout=12000)
    page.locator("#limpiar").click()
    page.get_by_text("Seleccionado: ninguno").wait_for(timeout=12000)
    page.locator("#nombre-nuevo").fill("Regla")
    page.locator("#agregar").click()
    page.locator(".tarjeta").nth(3).wait_for(timeout=12000)
    assert page.locator(".tarjeta").count()==4
    assert "Regla" in page.locator(".tarjeta").last.inner_text()
def t35(p):
    child="Components/TarjetaProducto.razor"
    parent="Components/Pages/Productos.razor"
    for id in ("PASO 3.5.2","RETO 3.5"):
        enable_block(p,child,id);enable_block(p,parent,id)
    for src,dst in [
        ('@* <button @onclick="NotificarSeleccion">Seleccionar</button> *@','<button @onclick="NotificarSeleccion">Seleccionar</button>'),
        ('@* <button @onclick="NotificarQuitar">Quitar</button> *@','<button @onclick="NotificarQuitar">Quitar</button>')
    ]: edit(p,child,src,dst)
    a=(p/parent).read_text(encoding="utf-8")
    original='<TarjetaProducto Producto="producto" />'
    replacement='<TarjetaProducto Producto="producto" AlSeleccionar="Seleccionar" AlQuitar="Quitar" />'
    assert a.count(original)==1
    a=a.replace(original,replacement)
    # Eliminar las dos variantes comentadas, que ya no hacen falta.
    a=re.sub(r'^\s*@\* <TarjetaProducto Producto="producto".*?\*@\s*\n','',a,flags=re.M)
    (p/parent).write_text(a,encoding="utf-8")
def verify35(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Seleccionar").click()
    page.get_by_text("Seleccionado: Lápiz").wait_for(timeout=12000)
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Quitar").click()
    page.get_by_text("Total: 2").wait_for(timeout=12000)
    assert page.locator('[data-producto-id="2"]').count()==0
def t36(p):
    enable_block(p,"Components/Pages/Productos.razor","PASO 3.6.2")
    edit(p,"Components/Pages/Productos.razor",
         '@* @if (!cargando && productos.Count == 0) { <p id="sin-productos">No hay productos para mostrar.</p> } *@',
         '@if (!cargando && productos.Count == 0) { <p id="sin-productos">No hay productos para mostrar.</p> }')
def verify36(page):
    page.goto(BASE+"/productos")
    page.get_by_text("Lista preparada").wait_for(timeout=18000)
    assert page.locator(".tarjeta").count()==3
    assert page.locator("#estado-carga").inner_text()=="Lista preparada"


def t31reto(p):
    edit(p,"Components/Pages/Interactiva.razor",
         "private void Incrementar() => contador++;",
         "private void Incrementar() => contador += 2;")
def v31reto(page):
    page.goto(BASE+"/interactiva",wait_until="networkidle")
    page.locator("#boton-interactivo").click()
    page.get_by_text("Pulsaciones: 2").wait_for(timeout=12000)
    page.locator("#boton-interactivo").click()
    page.get_by_text("Pulsaciones: 4").wait_for(timeout=12000)
def t32extra(p):
    t32(p)
    edit(p,"Components/Pages/Productos.razor",
        'new(3, "Carpeta", 3.75m)\n',
        'new(3, "Carpeta", 3.75m),\n        new(4, "Regla", 2.50m)\n')
def v32extra(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    page.locator("#lista-productos li").nth(3).wait_for(timeout=12000)
    assert page.locator("#lista-productos li").count()==4
    assert "Regla" in page.locator("#lista-productos").inner_text()
def t33reto(p):
    t33(p)
    file=p/"Components/TarjetaProducto.razor"
    s=file.read_text(encoding="utf-8")
    needle='''@*
    @if (Producto.Precio > 4m)
    {
        <p class="mensaje">Precio superior a 4 euros</p>
    }
    *@'''
    assert s.count(needle)==1
    s=s.replace(needle,needle.removeprefix("@*\n").removesuffix("\n    *@"))
    file.write_text(s,encoding="utf-8")
def v33reto(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    page.locator(".tarjeta").nth(2).wait_for(timeout=12000)
    assert page.locator(".mensaje").count()==1
    assert "Cuaderno" in page.locator(".mensaje").locator("..").inner_text()
def t36vacio(p):
    t36(p)
    file=p/"Services/ProductosMemoriaService.cs"
    s=file.read_text(encoding="utf-8")
    begin=s.index("        return\n        [")
    end=s.index("        ];",begin)+len("        ];")
    s=s[:begin]+"        return Array.Empty<Producto>();"+s[end:]
    file.write_text(s,encoding="utf-8")
def v36vacio(page):
    page.goto(BASE+"/productos")
    page.get_by_text("Lista preparada").wait_for(timeout=18000)
    page.locator("#sin-productos").wait_for(timeout=12000)
    assert page.locator(".tarjeta").count()==0

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    build_run(browser,"3.1",verify=verify31)
    build_run(browser,"3.2",t32,verify32)
    build_run(browser,"3.3",t33,verify33)
    build_run(browser,"3.4",t34,verify34)
    build_run(browser,"3.5",t35,verify35)
    build_run(browser,"3.6",t36,verify36)
    build_run(browser,"3.1",t31reto,v31reto)
    build_run(browser,"3.2",t32extra,v32extra)
    build_run(browser,"3.3",t33reto,v33reto)
    build_run(browser,"3.6",t36vacio,v36vacio)
    browser.close()
print("M03: seis escenarios de navegación e interactividad comprobados",flush=True)

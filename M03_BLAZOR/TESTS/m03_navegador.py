#!/usr/bin/env python3
"""Prueba interna en Chromium: evolución de los seis puntos de M03.
Activa los comentarios didácticos sobre copias temporales, nunca sobre fuentes.
"""
from __future__ import annotations
import contextlib, os, re, shutil, subprocess, tempfile, time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

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
    page.locator('[data-elemento-id="2"] button').click()
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
        enable_block(p,child,id)
    enable_block(p,parent,"RETO 3.5")
    for src,dst in [
        ('@* <button @onclick="NotificarSeleccion">Seleccionar</button> *@','<button @onclick="NotificarSeleccion">Seleccionar</button>'),
        ('@* <button @onclick="NotificarQuitar">Quitar</button> *@','<button @onclick="NotificarQuitar">Quitar</button>')
    ]: edit(p,child,src,dst)
    a=(p/parent).read_text(encoding="utf-8")
    original='<TarjetaProducto Producto="producto" />'
    replacement='<TarjetaProducto Producto="producto" AlSeleccionar="SeleccionarParaEditar" AlQuitar="Quitar" />'
    assert a.count(original)==1
    a=a.replace(original,replacement)
    a=re.sub(r'^\s*@\* <TarjetaProducto Producto="producto".*?\*@\s*\n','',a,flags=re.M)
    a=a.replace('<button class="seleccionar-padre" @onclick="() => SeleccionarParaEditar(producto.Id)">Seleccionar</button>','')
    (p/parent).write_text(a,encoding="utf-8")
def verify35(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Seleccionar").click()
    page.get_by_text("Seleccionado: Lápiz").wait_for(timeout=12000)
    page.locator("#editar-nombre").fill("Lápiz integrado")
    page.locator("#guardar-cambio").click()
    page.get_by_text("Seleccionado: Lápiz integrado").wait_for(timeout=12000)
    expect(page.locator('[data-producto-id="2"]')).to_contain_text("Lápiz integrado")
    page.locator("#nombre-nuevo").fill("Regla")
    page.locator("#agregar").click()
    page.get_by_text("Total: 4").wait_for(timeout=12000)
    page.locator("#buscar").fill("regla")
    page.get_by_text("Mostrando 1 de 4 productos").wait_for(timeout=12000)
    page.locator("#buscar").fill("")
    page.get_by_text("Mostrando 4 de 4 productos").wait_for(timeout=12000)
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Quitar").click()
    page.get_by_text("Total: 3").wait_for(timeout=12000)
    assert page.locator('[data-producto-id="2"]').count()==0
def t36(p):
    enable_block(p,"Components/Pages/Productos.razor","PASO 3.6.2")
    edit(p,"Components/Pages/Productos.razor",
         '@* @if (productos.Count == 0 && estado == "Lista preparada") { <p id="sin-productos">No hay productos para mostrar.</p> } *@',
         '@if (productos.Count == 0 && estado == "Lista preparada") { <p id="sin-productos">No hay productos para mostrar.</p> }')
def verify36(page):
    page.goto(BASE+"/productos")
    page.get_by_text("Lista preparada").wait_for(timeout=18000)
    assert page.locator(".tarjeta").count()==3
    assert page.locator("#estado-carga").inner_text()=="Lista preparada"
    # Continuidad completa: el servicio no elimina lo construido en P3.4/P3.5.
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Seleccionar").click()
    page.get_by_text("Seleccionado: Lápiz").wait_for(timeout=12000)
    page.locator("#editar-nombre").fill("Lápiz recuperado")
    page.locator("#guardar-cambio").click()
    page.get_by_text("Seleccionado: Lápiz recuperado").wait_for(timeout=12000)
    expect(page.locator('[data-producto-id="2"]')).to_contain_text("Lápiz recuperado")
    page.locator("#nombre-nuevo").fill("Regla")
    page.locator("#agregar").click()
    page.get_by_text("Total: 4").wait_for(timeout=12000)
    page.locator("#buscar").fill("regla")
    page.get_by_text("Mostrando 1 de 4 productos").wait_for(timeout=12000)
    page.locator("#buscar").fill("")
    page.get_by_text("Mostrando 4 de 4 productos").wait_for(timeout=12000)
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Quitar").click()
    page.get_by_text("Total: 3").wait_for(timeout=12000)
    page.locator("#deshacer").click()
    page.get_by_text("Total: 4").wait_for(timeout=12000)
    expect(page.locator('[data-producto-id="2"]')).to_contain_text("Lápiz recuperado")
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


def t34editor(p):
    t34(p)
    f="Components/Pages/Productos.razor"
    enable_block(p,f,"PASO 3.4.5")
    edit(p,f,
       '<button @onclick="() => Seleccionar(producto.Id)">Seleccionar</button>',
       '@* <button @onclick="() => Seleccionar(producto.Id)">Seleccionar</button> *@')
    edit(p,f,
       '@* <button @onclick="() => SeleccionarParaEditar(producto.Id)">Seleccionar</button> *@',
       '<button @onclick="() => SeleccionarParaEditar(producto.Id)">Seleccionar</button>')
    edit(p,f,
       '@* <label>Editar nombre: <input id="editar-nombre" @bind="nombreEditado" /></label> *@',
       '<label>Editar nombre: <input id="editar-nombre" @bind="nombreEditado" /></label>')
    edit(p,f,
       '@* <button id="guardar-cambio" @onclick="GuardarCambio">Guardar nombre</button> *@',
       '<button id="guardar-cambio" @onclick="GuardarCambio">Guardar nombre</button>')
def v34editor(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    page.locator('[data-elemento-id="2"] button').click()
    page.get_by_text("Seleccionado: Lápiz").wait_for(timeout=12000)
    assert page.locator("#editar-nombre").input_value()=="Lápiz"
    page.locator("#editar-nombre").fill("Lápiz rojo")
    page.locator("#guardar-cambio").click()
    page.get_by_text("Seleccionado: Lápiz rojo").wait_for(timeout=12000)
    assert "Lápiz rojo" in page.locator('[data-producto-id="2"]').inner_text()
    assert page.locator(".tarjeta").count()==3
    page.locator("#editar-nombre").fill("  ")
    page.locator("#guardar-cambio").click()
    assert "Lápiz rojo" in page.locator('[data-producto-id="2"]').inner_text()


def t34filtros(p):
    t34editor(p)
    rel="Components/Pages/Productos.razor"
    enable_block(p,rel,"RETO INTEGRADOR 3.4.6")
    for src,dst in [
        ('@* <label>Buscar por nombre: <input id="buscar" @bind="busqueda" @bind:event="oninput" /></label> *@',
         '<label>Buscar por nombre: <input id="buscar" @bind="busqueda" @bind:event="oninput" /></label>'),
        ('@* <label>Precio máximo: <input id="precio-maximo" type="number" min="0" step="0.5" @bind="precioMaximo" /></label> *@',
         '<label>Precio máximo: <input id="precio-maximo" type="number" min="0" step="0.5" @bind="precioMaximo" /></label>'),
        ('@* <button id="alternar-orden" @onclick="AlternarOrden">Invertir orden por precio</button> *@',
         '<button id="alternar-orden" @onclick="AlternarOrden">Invertir orden por precio</button>'),
        ('@* <p id="resumen-filtrado">Mostrando @ProductosVisibles.Count() de @productos.Count productos</p> *@',
         '<p id="resumen-filtrado">Mostrando @ProductosVisibles.Count() de @productos.Count productos</p>')]:
        edit(p,rel,src,dst)
    edit(p,rel,"@foreach (var producto in productos)",
         "@foreach (var producto in ProductosVisibles)")
def v34filtros(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    page.get_by_text("Mostrando 3 de 3 productos").wait_for(timeout=12000)
    assert page.locator(".tarjeta").count()==3
    assert page.locator(".tarjeta").first.get_attribute("data-producto-id")=="2"
    page.locator("#alternar-orden").click()
    expect(page.locator(".tarjeta").first).to_have_attribute("data-producto-id","1",timeout=12000)
    page.locator("#buscar").fill("láp")
    page.get_by_text("Mostrando 1 de 3 productos").wait_for(timeout=12000)
    assert page.locator(".tarjeta").count()==1
    expect(page.locator(".tarjeta").first).to_have_attribute("data-producto-id","2",timeout=12000)
    page.locator("#precio-maximo").fill("1")
    page.locator("#precio-maximo").blur()
    page.get_by_text("Mostrando 0 de 3 productos").wait_for(timeout=12000)
    page.locator("#precio-maximo").fill("2")
    page.locator("#precio-maximo").blur()
    page.get_by_text("Mostrando 1 de 3 productos").wait_for(timeout=12000)
    page.locator("#buscar").fill("")
    page.get_by_text("Mostrando 1 de 3 productos").wait_for(timeout=12000)
    assert page.locator(".tarjeta").first.get_attribute("data-producto-id")=="2"

def t35deshacer(p):
    t35(p)
    rel="Components/Pages/Productos.razor"
    enable_block(p,rel,"RETO INTEGRADOR 3.5.5")
    edit(p,rel,'<TarjetaProducto Producto="producto" AlSeleccionar="SeleccionarParaEditar" AlQuitar="Quitar" />',
         '<TarjetaProducto Producto="producto" AlSeleccionar="SeleccionarParaEditar" AlQuitar="QuitarConDeshacer" />')
    edit(p,rel,'@* <button id="deshacer" disabled="@(eliminacionPendiente is null)" @onclick="DeshacerEliminacion">Deshacer última eliminación</button> *@',
         '<button id="deshacer" disabled="@(eliminacionPendiente is null)" @onclick="DeshacerEliminacion">Deshacer última eliminación</button>')
    edit(p,rel,'@* <p id="estado-deshacer">@TextoDeshacer</p> *@',
         '<p id="estado-deshacer">@TextoDeshacer</p>')
def v35deshacer(page):
    page.goto(BASE+"/productos",wait_until="networkidle")
    assert page.locator("#deshacer").is_disabled()
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Quitar").click()
    page.get_by_text("Total: 2").wait_for(timeout=12000)
    assert page.locator("#deshacer").is_enabled()
    assert "Lápiz" in page.locator("#estado-deshacer").inner_text()
    page.locator("#deshacer").click()
    page.get_by_text("Total: 3").wait_for(timeout=12000)
    assert page.locator("#deshacer").is_disabled()
    assert [e.get_attribute("data-producto-id") for e in page.locator(".tarjeta").all()]==["2","3","1"]
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Seleccionar").click()
    page.get_by_text("Seleccionado: Lápiz").wait_for(timeout=12000)

def t36reintento(p):
    t36(p)
    file="Components/Pages/Productos.razor"
    for rel in ["Services/IProductosMemoriaService.cs",
                "Services/ProductosMemoriaService.cs",file]:
        enable_block(p,rel,"RETO INTEGRADOR 3.6.7")
    original='''    protected override async Task OnInitializedAsync()
    {
        estado = "Cargando productos...";
        productos = (await Catalogo.ObtenerAsync()).ToList();
        cargando = false;
        estado = "Lista preparada";
    }
'''
    edit(p,file,original,"")
    for src,dst in [
        ('@* <label>Simular fallo: <input id="simular-error" type="checkbox" @bind="simularError" /></label> *@',
         '<label>Simular fallo: <input id="simular-error" type="checkbox" @bind="simularError" /></label>'),
        ('@* <button id="recargar-productos" disabled="@cargando" @onclick="RecargarAsync">Recargar catálogo</button> *@',
         '<button id="recargar-productos" disabled="@cargando" @onclick="RecargarAsync">Recargar catálogo</button>'),
        ('@* @if (!string.IsNullOrEmpty(errorCarga)) { <p role="alert" id="error-carga">@errorCarga</p> } *@',
         '@if (!string.IsNullOrEmpty(errorCarga)) { <p role="alert" id="error-carga">@errorCarga</p> }')]:
        edit(p,file,src,dst)
def v36reintento(page):
    page.goto(BASE+"/productos")
    page.get_by_text("Lista preparada").wait_for(timeout=18000)
    assert page.locator(".tarjeta").count()==3
    page.locator('[data-producto-id="2"]').get_by_role("button",name="Quitar").click()
    page.get_by_text("Total: 2").wait_for(timeout=12000)
    assert page.locator("#deshacer").is_enabled()
    page.locator("#simular-error").check()
    page.locator("#recargar-productos").click()
    page.get_by_text("Carga fallida").wait_for(timeout=18000)
    assert "No se pudo cargar" in page.locator("#error-carga").inner_text()
    assert page.locator(".tarjeta").count()==0
    page.locator("#simular-error").uncheck()
    page.locator("#recargar-productos").click()
    page.get_by_text("Lista preparada").wait_for(timeout=18000)
    assert page.locator(".tarjeta").count()==3
    assert page.locator("#error-carga").count()==0
    assert page.locator("#deshacer").is_disabled()

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    build_run(browser,"3.1",verify=verify31)
    build_run(browser,"3.2",t32,verify32)
    build_run(browser,"3.3",t33,verify33)
    build_run(browser,"3.4",t34,verify34)
    build_run(browser,"3.4",t34editor,v34editor)
    build_run(browser,"3.5",t35,verify35)
    build_run(browser,"3.6",t36,verify36)
    build_run(browser,"3.1",t31reto,v31reto)
    build_run(browser,"3.2",t32extra,v32extra)
    build_run(browser,"3.3",t33reto,v33reto)
    build_run(browser,"3.6",t36vacio,v36vacio)
    build_run(browser,"3.4",t34filtros,v34filtros)
    build_run(browser,"3.5",t35deshacer,v35deshacer)
    build_run(browser,"3.6",t36reintento,v36reintento)
    browser.close()
print("M03: seis escenarios de navegación e interactividad comprobados",flush=True)

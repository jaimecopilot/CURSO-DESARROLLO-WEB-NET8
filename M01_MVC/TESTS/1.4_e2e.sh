#!/usr/bin/env bash
# P1.4: recorridos HTTP reales en seis estados, con reto y regresión del catálogo.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/M01_MVC/PROYECTO/1.4/CursoWeb.Mvc"
TMP="$(mktemp -d)"
PID=""
BASE="http://127.0.0.1:5091"

cleanup() {
    if [[ -n "$PID" ]]; then kill "$PID" 2>/dev/null || true; wait "$PID" 2>/dev/null || true; fi
    rm -rf "$TMP"
}
trap cleanup EXIT

get() {
    local state="$1" path="$2" expected="$3" name="$4" code
    code=$(curl -sS -D "$TMP/$state-$name.headers" -o "$TMP/$state-$name.body" -w "%{http_code}" "$BASE$path")
    if [[ "$code" != "$expected" ]]; then
        echo "FALLO [$state]: GET $path devolvió $code, se esperaba $expected" >&2
        cat "$TMP/$state-$name.body" >&2
        exit 1
    fi
}

run_scenario() {
    local project="$1" state="$2" ready
    echo "P1.4: compilando $state"
    dotnet build "$project/CursoWeb.Mvc.csproj" -c Release --nologo
    pushd "$project" >/dev/null
    dotnet bin/Release/net8.0/CursoWeb.Mvc.dll --urls "$BASE" >"$TMP/$state.log" 2>&1 &
    PID=$!
    popd >/dev/null
    ready=0
    for i in {1..40}; do
        if curl -fsS -o /dev/null "$BASE/" 2>/dev/null; then ready=1; break; fi
        if ! kill -0 "$PID" 2>/dev/null; then break; fi
        sleep 1
    done
    if [[ "$ready" != 1 ]]; then echo "FALLO: no arranca el servidor ($state)" >&2; cat "$TMP/$state.log"; exit 1; fi

    get "$state" "/" 200 home
    grep -Fq '1.1 | Primer recorrido MVC' "$TMP/$state-home.body"
    get "$state" "/Productos" 200 index
    grep -Fq 'El controlador ha enviado <strong>3</strong> productos' "$TMP/$state-index.body"
    grep -Fq 'href="/Productos">Productos</a>' "$TMP/$state-index.body"
    grep -Fq 'href="/recursos/guia-publica.txt"' "$TMP/$state-index.body"
    grep -Fq 'href="/css/catalogo.css"' "$TMP/$state-index.body"
    get "$state" "/recursos/guia-publica.txt" 200 guia
    get "$state" "/css/catalogo.css" 200 css
    get "$state" "/no-existe" 404 inexistente

    if [[ "$state" == "base" ]]; then
        get "$state" "/Productos/Estado" 404 estado
        get "$state" "/Productos/Detalle/2" 404 detalle
    else
        get "$state" "/Productos/Estado" 200 estado
        grep -iq '^Content-Type: text/plain' "$TMP/$state-estado.headers"
        grep -Fxq 'Catalogo MVC disponible' "$TMP/$state-estado.body"
    fi

    if [[ "$state" == "detalle" || "$state" == "atributo" || "$state" == "enlaces" || "$state" == "aplicacion" || "$state" == "reto" ]]; then
        get "$state" "/Productos/Detalle/2" 200 detalle
        grep -iq '^Content-Type: text/html' "$TMP/$state-detalle.headers"
        grep -Fq 'id="titulo-detalle"' "$TMP/$state-detalle.body"
        python3 - "$TMP/$state-detalle.body" <<'PY'
from pathlib import Path
from html import unescape
import sys
html=unescape(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert 'id="detalle-nombre">Lápiz</dd>' in html, html
assert 'id="detalle-id">2</dd>' in html, html
PY
        get "$state" "/Productos/Detalle/99" 404 detalle404
        get "$state" "/Productos/Detalle/0" 400 detalle400
        get "$state" "/Productos/Detalle" 400 sinid
    else
        get "$state" "/Productos/Detalle/2" 404 detalle
    fi

    if [[ "$state" == "atributo" || "$state" == "enlaces" || "$state" == "aplicacion" || "$state" == "reto" ]]; then
        get "$state" "/catalogo/ficha/2" 200 ficha
        grep -Fq 'id="detalle-producto"' "$TMP/$state-ficha.body"
        get "$state" "/catalogo/ficha/99" 404 ficha404
        get "$state" "/catalogo/ficha/no-numero" 404 fichaTexto
        get "$state" "/Productos/Ficha/2" 404 fichaConventional
    else
        get "$state" "/catalogo/ficha/2" 404 ficha
    fi

    if [[ "$state" == "enlaces" || "$state" == "aplicacion" || "$state" == "reto" ]]; then
        python3 - "$TMP/$state-index.body" <<'PY'
from pathlib import Path
import sys
h=Path(sys.argv[1]).read_text(encoding="utf-8")
assert h.count('class="enlace-detalle"') == 3, "Deben existir 3 enlaces de detalle"
for i in (1,2,3): assert f'href="/Productos/Detalle/{i}"' in h
PY
    else
        ! grep -Fq 'class="enlace-detalle"' "$TMP/$state-index.body"
    fi

    if [[ "$state" == "reto" ]]; then
        get "$state" "/catalogo/resumen/2" 200 resumen
        grep -iq '^Content-Type: application/json' "$TMP/$state-resumen.headers"
        python3 - "$TMP/$state-resumen.body" <<'PY'
from pathlib import Path
import json, sys
record=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert record["id"] == 2 and record["nombre"] == "Lápiz", record
PY
        get "$state" "/catalogo/resumen/99" 404 resumen404
        get "$state" "/catalogo/resumen/no-numero" 404 resumenTexto
    else
        get "$state" "/catalogo/resumen/2" 404 resumen
    fi
    if [[ "$state" == "aplicacion" ]]; then
        get "$state" "/catalogo/buscar/Cuaderno" 200 buscar
        grep -Fq 'id="detalle-nombre"' "$TMP/$state-buscar.body"
        grep -Fq 'Cuaderno' "$TMP/$state-buscar.body"
        get "$state" "/catalogo/buscar/cuaderno" 200 buscarMin
        get "$state" "/catalogo/buscar/NoExiste" 404 buscar404
        grep -iq '^Content-Type: text/html' "$TMP/$state-buscar.headers"
    else
        get "$state" "/catalogo/buscar/Cuaderno" 404 buscar
    fi
    echo "E2E OK: P1.4 $state (MVC, rutas convencionales/atributos y respuestas)"
    kill "$PID" 2>/dev/null || true
    wait "$PID" 2>/dev/null || true
    PID=""
}

run_scenario "$SRC" base

python3 - "$SRC" "$TMP" <<'PY'
from pathlib import Path
from shutil import copytree, ignore_patterns
import sys
source, tmp=map(Path, sys.argv[1:])
states=[
    ("estado",True,False,False,False,False),
    ("detalle",True,True,False,False,False),
    ("atributo",True,True,True,False,False),
    ("enlaces",True,True,True,True,False),
    ("aplicacion",True,True,True,True,False),
    ("reto",True,True,True,True,True)
]
blocks=[
    ("1.4.2","PASO",True),
    ("1.4.3","PASO",True),
    ("1.4.4","PASO",True),
    ("1.4","RETO",True)
]
for name, estado, detalle, atributo, enlaces, reto in states:
    dest=tmp/name
    copytree(source,dest,ignore=ignore_patterns("bin","obj"))
    ctl=dest/"Controllers"/"ProductosController.cs"
    text=ctl.read_text(encoding="utf-8")
    for enabled, marker in [(estado,"PASO 1.4.2"),(detalle,"PASO 1.4.3"),(atributo,"PASO 1.4.4"),(reto,"RETO 1.4")]:
        start=f"    /* {marker} INICIO\n"
        end=f"    {marker} FIN */"
        assert text.count(start)==1 and text.count(end)==1, f"Bloque {marker} ausente"
        if enabled: text=text.replace(start,"").replace(end,"")
    if name == "aplicacion":
        marker = '    // APLICACION 1.4 — Escribe aquí una acción propia BuscarPorNombre(string nombre).'
        assert text.count(marker) == 1
        answer = '''    [HttpGet("/catalogo/buscar/{nombre}")]
    public IActionResult BuscarPorNombre(string nombre)
    {
        var producto = ObtenerProductosEjemplo().FirstOrDefault(
            p => string.Equals(p.Nombre, nombre, StringComparison.OrdinalIgnoreCase));
        if (producto is null)
        {
            return NotFound();
        }
        return View("Detalle", producto);
    }

'''
        text = text.replace(marker, answer + marker)
    ctl.write_text(text,encoding="utf-8")
    v=dest/"Views"/"Productos"/"Index.cshtml"
    h=v.read_text(encoding="utf-8")
    start='            @* PASO 1.4.5 (inicio)\n'
    end='            PASO 1.4.5 (fin) *@'
    assert h.count(start)==1 and h.count(end)==1
    if enlaces: h=h.replace(start,"").replace(end,"")
    v.write_text(h,encoding="utf-8")
PY
for state in estado detalle atributo enlaces aplicacion reto; do
    run_scenario "$TMP/$state" "$state"
done
echo "P1.4: siete escenarios E2E reales, incluida búsqueda por nombre y reto."

#!/usr/bin/env bash
# P1.5: seis estados HTTP reales y la regresión del catálogo.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/M01_MVC/PROYECTO/1.5/CursoWeb.Mvc"
TMP="$(mktemp -d)"
PID=""
BASE="http://127.0.0.1:5091"

cleanup() {
  if [[ -n "$PID" ]]; then kill "$PID" 2>/dev/null || true; wait "$PID" 2>/dev/null || true; fi
  rm -rf "$TMP"
}
trap cleanup EXIT

get() {
  local state="$1" route="$2" expected="$3" tag="$4" result
  result="$(curl -sS -D "$TMP/$state-$tag.headers" -o "$TMP/$state-$tag.html" -w '%{http_code}' "$BASE$route")"
  if [[ "$result" != "$expected" ]]; then
    echo "P1.5 [$state] GET $route: obtenido $result, esperado $expected" >&2
    cat "$TMP/$state-$tag.html" >&2
    exit 1
  fi
}

run_scenario() {
  local path="$1" state="$2" ready=0
  echo "P1.5: compilación estado $state"
  dotnet build "$path/CursoWeb.Mvc.csproj" -c Release --nologo
  pushd "$path" >/dev/null
  dotnet bin/Release/net8.0/CursoWeb.Mvc.dll --urls "$BASE" >"$TMP/$state.log" 2>&1 &
  PID=$!
  popd >/dev/null
  for i in {1..40}; do
    if curl -fsS -o /dev/null "$BASE/Productos" 2>/dev/null; then ready=1; break; fi
    if ! kill -0 "$PID" 2>/dev/null; then break; fi
    sleep 1
  done
  if [[ "$ready" != 1 ]]; then echo "Kestrel no inicia para $state" >&2; cat "$TMP/$state.log"; exit 1; fi

  get "$state" "/" 200 home
  grep -Fq '1.1 | Primer recorrido MVC' "$TMP/$state-home.html"
  get "$state" "/Productos" 200 index
  grep -Fq '1.5 | Razor y presentación de productos' "$TMP/$state-index.html"
  grep -Fq 'ha enviado <strong>3</strong> productos' "$TMP/$state-index.html"
  get "$state" "/Productos/Detalle/2" 200 detalle
  grep -Fq 'id="detalle-id">2</dd>' "$TMP/$state-detalle.html"
  get "$state" "/Productos/Detalle/1" 200 detalle1
  get "$state" "/Productos/Detalle/99" 404 detalle404
  get "$state" "/Productos/Detalle/0" 400 detalle400
  get "$state" "/catalogo/ficha/2" 200 ficha
  get "$state" "/Productos/Estado" 200 estado
  get "$state" "/recursos/guia-publica.txt" 200 guia
  get "$state" "/css/catalogo.css" 200 css
  get "$state" "/no-existe" 404 noexistente
  python3 - "$TMP/$state-index.html" "$TMP/$state-detalle.html" "$TMP/$state-ficha.html" <<'PY'
from pathlib import Path
from html import unescape
import sys
idx, detail, ficha = (unescape(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:])
for producto in ("Cuaderno","Lápiz","Carpeta"):
    assert producto in idx, f"No se localiza {producto} en listado"
assert 'id="detalle-nombre">Lápiz' in detail
assert 'id="detalle-nombre">Lápiz' in ficha
assert idx.count('class="enlace-detalle"') == 3
PY

  if [[ "$state" == "base" ]]; then
    ! grep -Fq 'id="catalogo-completo"' "$TMP/$state-index.html"
  else
    grep -Fq 'id="catalogo-completo"' "$TMP/$state-index.html"
  fi

  if [[ "$state" == "base" || "$state" == "condicion" ]]; then
    ! grep -Fq 'id="nota-pagina-detalle"' "$TMP/$state-detalle.html"
  else
    grep -Fq 'id="nota-pagina-detalle"' "$TMP/$state-detalle.html"
    ! grep -Fq 'id="nota-pagina-detalle"' "$TMP/$state-index.html"
  fi

  if [[ "$state" == "base" || "$state" == "condicion" || "$state" == "seccion" ]]; then
    ! grep -Fq 'id="tarjetas-catalogo"' "$TMP/$state-index.html"
    ! grep -Fq 'class="tarjeta-producto"' "$TMP/$state-index.html"
  else
    grep -Fq 'id="tarjetas-catalogo"' "$TMP/$state-index.html"
    python3 - "$TMP/$state-index.html" <<'PY'
from pathlib import Path
import sys
html=Path(sys.argv[1]).read_text(encoding="utf-8")
assert html.count('class="tarjeta-producto"')==3, "El listado debe contener tres parciales"
for i in (1,2,3): assert f'data-producto-id="{i}"' in html
PY
  fi

  if [[ "$state" == "detalle-parcial" || "$state" == "aplicacion" || "$state" == "navegacion" || "$state" == "reto" ]]; then
    grep -Fq 'id="tarjeta-detalle"' "$TMP/$state-detalle.html"
    grep -Fq 'data-producto-id="2"' "$TMP/$state-detalle.html"
    grep -Fq 'data-producto-id="1"' "$TMP/$state-detalle1.html"
    [[ $(grep -c 'class="tarjeta-producto"' "$TMP/$state-detalle.html") -eq 1 ]]
  else
    ! grep -Fq 'id="tarjeta-detalle"' "$TMP/$state-detalle.html"
  fi

  if [[ "$state" == "reto" ]]; then
    python3 - "$TMP/$state-index.html" "$TMP/$state-detalle.html" "$TMP/$state-detalle1.html" <<'PY'
from pathlib import Path
from html import unescape
import sys
idx, detail_lapiz, detail_cuaderno=(unescape(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:])
assert idx.count('class="etiqueta-economico"')==1
assert "Precio económico" in idx
assert detail_lapiz.count('class="etiqueta-economico"')==1
assert detail_cuaderno.count('class="etiqueta-economico"')==0
PY
  else
    ! grep -Fq 'class="etiqueta-economico"' "$TMP/$state-index.html"
    ! grep -Fq 'class="etiqueta-economico"' "$TMP/$state-detalle.html"
  fi

  if [[ "$state" == "aplicacion" ]]; then
    python3 - "$TMP/$state-index.html" "$TMP/$state-detalle.html" "$TMP/$state-detalle1.html" <<'PY'
from pathlib import Path
from html import unescape
import sys
index, lapiz, cuaderno=(unescape(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:])
assert index.count('class="etiqueta-destacada"') == 1
assert cuaderno.count('class="etiqueta-destacada"') == 1
assert lapiz.count('class="etiqueta-destacada"') == 0
assert 'Producto destacado' in index
PY
  else
    ! grep -Fq 'class="etiqueta-destacada"' "$TMP/$state-index.html"
    ! grep -Fq 'class="etiqueta-destacada"' "$TMP/$state-detalle1.html"
  fi
  if [[ "$state" == "navegacion" ]]; then
    python3 - "$TMP/$state-index.html" "$TMP/$state-detalle.html" <<'PY'
from pathlib import Path
import re
import sys
index, detalle=(Path(p).read_text(encoding="utf-8") for p in sys.argv[1:])
assert 'asp-controller=' not in index and 'asp-action=' not in index, "Los Tag Helpers no se ejecutaron"
for id in (1, 2, 3):
    assert f'href="/Productos/Detalle/{id}"' in index, f"Falta el enlace al producto {id}"
assert 'href="/Productos/Detalle/2"' in detalle, "La misma parcial debe producir enlace en el detalle"
PY
  fi
  echo "E2E OK: P1.5 $state, vistas tipadas, layout, secciones y parciales"
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  PID=""
}

run_scenario "$SRC" base

python3 - "$SRC" "$TMP" <<'PY'
from pathlib import Path
from shutil import copytree,ignore_patterns
import sys

src,tmp=map(Path,sys.argv[1:])
for name,condition,section,cards,detail_card,reto in [
    ("condicion",True,False,False,False,False),
    ("seccion",True,True,False,False,False),
    ("tarjetas",True,True,True,False,False),
    ("detalle-parcial",True,True,True,True,False),
    ("aplicacion",True,True,True,True,False),
    ("navegacion",True,True,True,True,False),
    ("reto",True,True,True,True,True),
]:
    target=tmp/name
    copytree(src,target,ignore=ignore_patterns("bin","obj"))

    blocks=[
        (target/"Views"/"Productos"/"Index.cshtml",condition,"    @* PASO 1.5.2 (inicio)\n","    PASO 1.5.2 (fin) *@"),
        (target/"Views"/"Shared"/"_Layout.cshtml",section,"    @* PASO 1.5.3 (inicio)\n","    PASO 1.5.3 (fin) *@"),
        (target/"Views"/"Productos"/"Detalle.cshtml",section,"@* PASO 1.5.3 (inicio)\n","PASO 1.5.3 (fin) *@"),
        (target/"Views"/"Productos"/"Index.cshtml",cards,"    @* PASO 1.5.4 (inicio)\n","    PASO 1.5.4 (fin) *@"),
        (target/"Views"/"Productos"/"Detalle.cshtml",detail_card,"@* PASO 1.5.5 (inicio)\n","PASO 1.5.5 (fin) *@"),
        (target/"Views"/"Shared"/"_TarjetaProducto.cshtml",reto,"    @* RETO 1.5 (inicio)\n","    RETO 1.5 (fin) *@"),
    ]
    for path,enabled,start,end in blocks:
        content=path.read_text(encoding="utf-8")
        assert content.count(start)==1 and content.count(end)==1, f"Bloque ausente: {path}: {start}"
        if enabled: content=content.replace(start,"").replace(end,"")
        if name == "navegacion" and path.name == "_TarjetaProducto.cshtml":
            old_link = '<a href="/Productos/Detalle/@Model.Id">Ver detalle de @Model.Nombre</a>'
            new_link = '<a asp-controller="Productos" asp-action="Detalle" asp-route-id="@Model.Id">Ver detalle de @Model.Nombre</a>'
            assert content.count(old_link) == 1
            content = content.replace(old_link, new_link)
        if name == "aplicacion" and path.name == "_TarjetaProducto.cshtml":
            marker = '    @* APLICACION 1.5 — Escribe aquí una condición Razor propia: si Model.Precio >= 4m, representa <strong class="etiqueta-destacada">Producto destacado</strong>. La misma parcial se reutiliza en listado y detalle. *@'
            answer = '    @if (Model.Precio >= 4m)\n    {\n        <strong class="etiqueta-destacada">Producto destacado</strong>\n    }'
            assert content.count(marker) == 1
            content = content.replace(marker, answer)
        path.write_text(content,encoding="utf-8")
PY

for state in condicion seccion tarjetas detalle-parcial aplicacion navegacion reto; do
    run_scenario "$TMP/$state" "$state"
done
echo "P1.5: ocho escenarios E2E reales, incluidas regla autónoma, navegación Tag Helper y reto."

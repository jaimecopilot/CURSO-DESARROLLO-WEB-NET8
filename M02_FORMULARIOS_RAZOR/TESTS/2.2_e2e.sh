#!/usr/bin/env bash
# Comprobación HTTP del estado inicial y de la transformación guiada de P2.2.
# Control interno: no forma parte de los documentos del estudiante.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SOURCE="$ROOT/M02_FORMULARIOS_RAZOR/PROYECTO/2.2/CursoWeb.Mvc"
TMP="$(mktemp -d)"
BASE="http://127.0.0.1:5192"
PID=""
cleanup() {
  if [[ -n "$PID" ]]; then kill "$PID" 2>/dev/null || true; wait "$PID" 2>/dev/null || true; fi
  rm -rf "$TMP"
}
trap cleanup EXIT
start() {
  local dir="$1" label="$2" ready=0
  dotnet build "$dir/CursoWeb.Mvc.csproj" -c Release --nologo
  (cd "$dir" && dotnet bin/Release/net8.0/CursoWeb.Mvc.dll --urls "$BASE") >"$TMP/$label.log" 2>&1 &
  PID=$!
  for i in {1..40}; do
    if curl -fsS -o /dev/null "$BASE/Productos/Crear" 2>/dev/null; then ready=1; break; fi
    if ! kill -0 "$PID" 2>/dev/null; then break; fi
    sleep 1
  done
  [[ "$ready" -eq 1 ]] || { cat "$TMP/$label.log"; exit 1; }
}
stop() {
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  PID=""
  sleep 1
}
check() {
  local state="$1" result
  curl -fsS -o "$TMP/$state.index" "$BASE/Productos"
  curl -fsS -o "$TMP/$state.detalle" "$BASE/Productos/Detalle/2"
  curl -fsS -b "$TMP/$state.cookies" -c "$TMP/$state.cookies" \
      "$BASE/Productos/Crear" >"$TMP/$state.form"
  for product in Cuaderno Lápiz Carpeta; do grep -Fq "$product" "$TMP/$state.index"; done

  result="$(curl -sS -o "$TMP/$state.nocookie" -w '%{http_code}' \
      --data "Nombre=Rotulador&Precio=7" "$BASE/Productos/Crear")"
  [[ "$result" == 400 ]] || { echo "$state: sin token devolvió $result, esperado 400"; exit 1; }

  python3 - "$TMP/$state.form" >"$TMP/$state.token" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys
class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms=[]
        self.tokens=[]
        self.fields={}
        self.labels=[]
        self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="form": self.forms.append(a)
        if tag=="label": self.labels.append(a.get("for"))
        if tag=="input":
            self.fields[a.get("name")]=a
            if a.get("name")=="__RequestVerificationToken":
                self.tokens.append(a.get("value"))
        if tag=="a": self.links.append(a.get("href"))
c=Check()
c.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert len(c.forms)==1, "Debe haber un solo formulario"
assert c.forms[0].get("method","").lower()=="post"
assert c.forms[0].get("action","").lower().endswith("/productos/crear")
assert len(c.tokens)==1 and c.tokens[0], "Falta o se repite el token antiforgery"
assert "Nombre" in c.fields and "Precio" in c.fields
assert "Nombre" in c.labels and "Precio" in c.labels
assert any((h or "").lower().rstrip("/") in ("/productos", "/productos/index") for h in c.links)
print(c.tokens[0])
PY
  result="$(curl -sS -o "$TMP/$state.confirmacion" -w '%{http_code}' \
      -b "$TMP/$state.cookies" -c "$TMP/$state.cookies" \
      --data-urlencode "Nombre=Rotulador" --data-urlencode "Precio=7" \
      --data-urlencode "__RequestVerificationToken=$(cat "$TMP/$state.token")" \
      "$BASE/Productos/Crear")"
  [[ "$result" == 200 ]] || { echo "$state: POST protegido devolvió $result"; exit 1; }
  grep -Fq "Rotulador" "$TMP/$state.confirmacion"

  if [[ "$state" == final ]]; then
    python3 - "$TMP/$state.form" "$TMP/$state.index" "$TMP/$state.detalle" <<'PY'
from pathlib import Path
import sys
form,index,detail=(Path(x).read_text(encoding="utf-8") for x in sys.argv[1:])
for tag in ("asp-for=","asp-action=","asp-controller="):
    assert tag not in form, f"Tag Helper sin procesar: {tag}"
for id in (1,2,3):
    assert f"/Productos/Detalle/{id}" in index, f"Falta el enlace de producto {id}"
assert "/Productos/Detalle/2" in detail
PY
  fi
}
start "$SOURCE" base
check base
stop

cp -a "$SOURCE" "$TMP/final"
rm -rf "$TMP/final/bin" "$TMP/final/obj"
python3 - "$TMP/final" <<'PY'
from pathlib import Path
import sys
d=Path(sys.argv[1])
f=d/"Views/Productos/Crear.cshtml"
s=f.read_text(encoding="utf-8")
changes=[
('<form method="post" action="/Productos/Crear">','<form asp-controller="Productos" asp-action="Crear" method="post">'),
('    @Html.AntiForgeryToken()\n',''),
('<label for="Nombre">Nombre</label>','<label asp-for="Nombre"></label>'),
('<label for="Precio">Precio</label>','<label asp-for="Precio"></label>'),
('<input id="Nombre" name="Nombre" value="@Model.Nombre" />','<input asp-for="Nombre" />'),
('<input id="Precio" name="Precio" type="number" step="0.01" value="@Model.Precio.ToString(System.Globalization.CultureInfo.InvariantCulture)" />',
 '<input asp-for="Precio" type="number" step="0.01" />'),
('<a href="/Productos">Volver al catálogo</a>','<a asp-controller="Productos" asp-action="Index">Volver al catálogo</a>')]
for old,new in changes:
    assert s.count(old)==1, f"Fragmento no único: {old}"
    s=s.replace(old,new)
f.write_text(s,encoding="utf-8")
f=d/"Views/Shared/_TarjetaProducto.cshtml"
s=f.read_text(encoding="utf-8")
a='<a href="/Productos/Detalle/@Model.Id">Ver detalle de @Model.Nombre</a>'
b='<a asp-controller="Productos" asp-action="Detalle" asp-route-id="@Model.Id">Ver detalle de @Model.Nombre</a>'
assert s.count(a)==1
f.write_text(s.replace(a,b),encoding="utf-8")
f=d/"Views/Productos/Index.cshtml"
s=f.read_text(encoding="utf-8")
a='<a class="enlace-detalle" href="/Productos/Detalle/@producto.Id">Ver detalle</a>'
b='<a class="enlace-detalle" asp-controller="Productos" asp-action="Detalle" asp-route-id="@producto.Id">Ver detalle</a>'
assert s.count(a)==1
f.write_text(s.replace(a,b),encoding="utf-8")
PY
start "$TMP/final" final
check final
stop
echo "P2.2 completado: 2 estados, 400 sin token, 200 con token, ruta MVC, etiquetas y enlaces."

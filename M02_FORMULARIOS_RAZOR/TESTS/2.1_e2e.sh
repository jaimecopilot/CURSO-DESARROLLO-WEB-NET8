#!/usr/bin/env bash
# Validación técnica interna del itinerario P2.1, fuera del manual del alumno.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/M02_FORMULARIOS_RAZOR/PROYECTO/2.1/CursoWeb.Mvc"
TMP="$(mktemp -d)"
PORT=5186
BASE="http://127.0.0.1:$PORT"
PID=""
cleanup() {
  if [[ -n "$PID" ]]; then kill "$PID" 2>/dev/null || true; wait "$PID" 2>/dev/null || true; fi
  rm -rf "$TMP"
}
trap cleanup EXIT

start_app() {
  local dir="$1" label="$2"
  dotnet build "$dir/CursoWeb.Mvc.csproj" -c Release --nologo
  (cd "$dir" && exec dotnet bin/Release/net8.0/CursoWeb.Mvc.dll --urls "$BASE" >"$TMP/$label.log" 2>&1) &
  PID=$!
  for i in {1..60}; do
    if curl -fsS -o /dev/null "$BASE/Productos/Crear" 2>/dev/null; then
      return
    fi
    if ! kill -0 "$PID" 2>/dev/null; then
      cat "$TMP/$label.log" >&2; exit 1
    fi
    sleep 1
  done
  cat "$TMP/$label.log" >&2
  echo "No arrancó Kestrel en estado $label" >&2
  exit 1
}
stop_app() {
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  PID=""
  sleep 1
}
status() {
  curl -sS -o "$TMP/$1.body" -w '%{http_code}' -X "$2" "$BASE$3"
}

# Estado inicial: GET permitido y POST sin acción habilitada.
start_app "$SRC" base
[[ "$(status inicio GET /Productos)" == 200 ]]
grep -Fq "Cuaderno" "$TMP/inicio.body"
[[ "$(status formulario GET /Productos/Crear)" == 200 ]]
grep -Fq "__RequestVerificationToken" "$TMP/formulario.body"
[[ "$(status sin_post POST /Productos/Crear)" == 405 ]]
stop_app

# Activación real de la acción tal como la indica P2.1.
cp -a "$SRC" "$TMP/activado"
rm -rf "$TMP/activado/bin" "$TMP/activado/obj"
python3 - "$TMP/activado" <<'PY'
from pathlib import Path
import sys
base=Path(sys.argv[1])
path=base/"Controllers/ProductosController.cs"
s=path.read_text(encoding="utf-8")
start="    /* PASO 2.1.3 INICIO\n"
end="    PASO 2.1.3 FIN */"
assert s.count(start)==1 and s.count(end)==1
s=s.replace(start,"").replace(end,"")
path.write_text(s,encoding="utf-8")
PY

start_app "$TMP/activado" activado
# No tener token sigue dando 400 incluso cuando POST está activo.
[[ "$(status sin_token POST /Productos/Crear)" == 400 ]]
# La sesión y el token se obtienen del GET real del servidor; no hay tokens inventados.
curl -fsS -c "$TMP/cookiejar" -b "$TMP/cookiejar" "$BASE/Productos/Crear" >"$TMP/form.html"
python3 - "$TMP/form.html" >"$TMP/token" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys
class Inputs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens=[]
    def handle_starttag(self,tag,attrs):
        if tag=="input":
            a=dict(attrs)
            if a.get("name")=="__RequestVerificationToken":
                self.tokens.append(a.get("value",""))
reader=Inputs()
reader.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert len(reader.tokens)==1 and reader.tokens[0]
print(reader.tokens[0])
PY
token="$(cat "$TMP/token")"
code="$(curl -sS -b "$TMP/cookiejar" -c "$TMP/cookiejar" -o "$TMP/confirmacion.html" -w '%{http_code}' \
  --data-urlencode "Nombre=Rotulador" --data-urlencode "Precio=7" \
  --data-urlencode "__RequestVerificationToken=$token" "$BASE/Productos/Crear")"
[[ "$code" == 200 ]] || { echo "El POST protegido respondió $code"; exit 1; }
grep -Fq "Rotulador" "$TMP/confirmacion.html"
grep -Fq "precio-recibido" "$TMP/confirmacion.html"
grep -Fq "7" "$TMP/confirmacion.html"
curl -fsS "$BASE/Productos" >"$TMP/catalogo.html"
for producto in Cuaderno Lápiz Carpeta; do python3 -c 'import html,pathlib,sys; assert sys.argv[2] in html.unescape(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))' "$TMP/catalogo.html" "$producto"; done
! grep -Fq "Rotulador" "$TMP/catalogo.html"
stop_app

# Escribir la aplicación autónoma y activar el reto sobre otra copia.
cp -a "$TMP/activado" "$TMP/ampliado"
rm -rf "$TMP/ampliado/bin" "$TMP/ampliado/obj"
python3 - "$TMP/ampliado" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])/"Views/Productos/Confirmacion.cshtml"
s=p.read_text(encoding="utf-8")
a=s.index("@* APLICACION 2.1.5")
b=s.index("*@",a)+2
assert b>a
s=s[:a]+'''@if (Model.Precio >= 4m)
{
    <strong id="precio-elevado">Importe elevado para el ejemplo</strong>
}
'''+s[b:]
s=s.replace("@* RETO 2.1 INICIO\n","").replace("RETO 2.1 FIN *@","")
p.write_text(s,encoding="utf-8")
PY
start_app "$TMP/ampliado" ampliado
curl -fsS -b "$TMP/cookiejar2" -c "$TMP/cookiejar2" "$BASE/Productos/Crear" >"$TMP/form2.html"
python3 - "$TMP/form2.html" >"$TMP/token2" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys
class Parser(HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag=="input":
            values=dict(attrs)
            if values.get("name")=="__RequestVerificationToken":
                print(values["value"])
p=Parser()
p.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
PY
token="$(cat "$TMP/token2")"
for row in "Rotulador:7:yes:yes" "Goma:2:no:no"; do
  IFS=: read -r nombre precio elevado extenso <<<"$row"
  code="$(curl -sS -b "$TMP/cookiejar2" -c "$TMP/cookiejar2" -o "$TMP/resultado.html" -w '%{http_code}' \
      --data-urlencode "Nombre=$nombre" --data-urlencode "Precio=$precio" \
      --data-urlencode "__RequestVerificationToken=$token" "$BASE/Productos/Crear")"
  [[ "$code" == 200 ]]
  if [[ "$elevado" == yes ]]; then grep -Fq 'id="precio-elevado"' "$TMP/resultado.html"; else ! grep -Fq 'id="precio-elevado"' "$TMP/resultado.html"; fi
  if [[ "$extenso" == yes ]]; then grep -Fq 'id="nombre-extenso"' "$TMP/resultado.html"; else ! grep -Fq 'id="nombre-extenso"' "$TMP/resultado.html"; fi
done
stop_app
echo "P2.1 OK: GET, 405 sin POST, 400 sin antiforgery, 200 con token, binder, no persistencia y Razor."

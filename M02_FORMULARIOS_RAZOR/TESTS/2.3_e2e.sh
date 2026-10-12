#!/usr/bin/env bash
# Comprobación interna HTTP del aprendizaje P2.3: estado inicial y reglas activadas.
# No aparece ni se ejecuta desde el cuaderno del alumno.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SOURCE="$ROOT/M02_FORMULARIOS_RAZOR/PROYECTO/2.3/CursoWeb.Mvc"
TMP="$(mktemp -d)"
BASE="http://127.0.0.1:5193"
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
  for i in {1..45}; do
    if curl -fsS -o /dev/null "$BASE/Productos/Crear" 2>/dev/null; then ready=1; break; fi
    if ! kill -0 "$PID" 2>/dev/null; then break; fi
    sleep 1
  done
  [[ "$ready" -eq 1 ]] || { cat "$TMP/$label.log" >&2; exit 1; }
}
stop() {
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  PID=""
  sleep 1
}
token() {
  local label="$1"
  curl -fsS -b "$TMP/$label.cookies" -c "$TMP/$label.cookies" \
    "$BASE/Productos/Crear" > "$TMP/$label.html"
  python3 - "$TMP/$label.html" > "$TMP/$label.token" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys
class Inputs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens=[]
    def handle_starttag(self, tag, attrs):
        if tag == "input":
            d=dict(attrs)
            if d.get("name")=="__RequestVerificationToken":
                self.tokens.append(d.get("value"))
p=Inputs()
p.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert len(p.tokens)==1 and p.tokens[0], p.tokens
print(p.tokens[0])
PY
}
post() {
  local state="$1" label="$2" name="$3" price="$4"
  curl -sS -o "$TMP/$label.body" -w '%{http_code}' \
    -b "$TMP/$state.cookies" -c "$TMP/$state.cookies" \
    --data-urlencode "Nombre=$name" --data-urlencode "Precio=$price" \
    --data-urlencode "__RequestVerificationToken=$(cat "$TMP/$state.token")" \
    "$BASE/Productos/Crear"
}
assert_html() {
  local label="$1" text="$2"
  grep -Fq "$text" "$TMP/$label.body" || { echo "Ausente en $label: $text"; exit 1; }
}

# Antes de activar las anotaciones, un nombre de un carácter se admite.
start "$SOURCE" base
token base
[[ "$(post base x_inicial X 7)" == 200 ]]
assert_html x_inicial "Datos recibidos del formulario"
stop

# Simula descomentar las cuatro anotaciones PASO 2.3.2.
cp -a "$SOURCE" "$TMP/validado"
rm -rf "$TMP/validado/bin" "$TMP/validado/obj"
python3 - "$TMP/validado" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])/"Models/ProductoFormulario.cs"
s=p.read_text(encoding="utf-8")
for attr in ("Required", "StringLength", "Range"):
    old="// ["+attr+"("
    assert s.count(old)>=1, old
    s=s.replace(old,"["+attr+"(")
assert s.count("[Required(")==2
assert s.count("[StringLength(")==1
assert s.count("[Range(")==1
p.write_text(s,encoding="utf-8")
PY

start "$TMP/validado" validado
token validado
[[ "$(post validado nombre_corto X 7)" == 200 ]]
assert_html nombre_corto "El nombre debe tener entre 2 y 60 caracteres."
assert_html nombre_corto "Crear producto"
[[ "$(post validado nombre_ausente "" 7)" == 200 ]]
assert_html nombre_ausente "Indica el nombre."
[[ "$(post validado precio_cero Rotulador 0)" == 200 ]]
assert_html precio_cero "El precio debe estar entre 0,01 y 9999,99."
assert_html precio_cero "Rotulador"
[[ "$(post validado precio_ausente Rotulador "" )" == 200 ]]
assert_html precio_ausente "Indica el precio."
[[ "$(post validado precio_inconvertible Rotulador abc)" == 200 ]]
assert_html precio_inconvertible "Crear producto"
! grep -Fq "Datos recibidos del formulario" "$TMP/precio_inconvertible.body"
[[ "$(post validado entrada_correcta Rotulador 7)" == 200 ]]
assert_html entrada_correcta "Datos recibidos del formulario"
curl -fsS "$BASE/Productos" >"$TMP/catalogo.html"
for x in Cuaderno Lápiz Carpeta; do grep -Fq "$x" "$TMP/catalogo.html"; done
! grep -Fq "Rotulador" "$TMP/catalogo.html"
stop

# Comprueba también el bloque opcional RETO 2.3, no solo las anotaciones.
cp -a "$TMP/validado" "$TMP/reto"
rm -rf "$TMP/reto/bin" "$TMP/reto/obj"
python3 - "$TMP/reto" <<'PY'
from pathlib import Path
import sys
controller=Path(sys.argv[1])/"Controllers/ProductosController.cs"
s=controller.read_text(encoding="utf-8")
s=s.replace("        /* RETO 2.3 INICIO\n", "")
s=s.replace("        RETO 2.3 FIN */", "")
controller.write_text(s,encoding="utf-8")
PY
start "$TMP/reto" reto
token reto
[[ "$(post reto prohibido TESTProducto 7)" == 200 ]]
assert_html prohibido "El nombre no puede comenzar por TEST en este ejemplo."
[[ "$(post reto permitido Rotulador 7)" == 200 ]]
assert_html permitido "Datos recibidos del formulario"
stop

# Simula también activar la sección Scripts en una copia con reglas.
cp -a "$TMP/validado" "$TMP/cliente"
rm -rf "$TMP/cliente/bin" "$TMP/cliente/obj"
python3 - "$TMP/cliente" <<'PY'
from pathlib import Path
import sys
view=Path(sys.argv[1])/"Views/Productos/Crear.cshtml"
s=view.read_text(encoding="utf-8")
needle='@section Scripts\n{\n    <partial name="_ValidationScriptsPartial" />\n}'
assert needle in s
a=s.index('@* PASO 2.3.5 (ACTIVAR)')
z=s.index('*@',a)+2
s=s[:a]+needle+s[z:]
view.write_text(s,encoding="utf-8")
PY
start "$TMP/cliente" cliente
curl -fsS "$BASE/Productos/Crear" >"$TMP/cliente.html"
grep -Fq "jquery.min.js" "$TMP/cliente.html"
grep -Fq "jquery.validate.min.js" "$TMP/cliente.html"
grep -Fq "jquery.validate.unobtrusive.min.js" "$TMP/cliente.html"
stop
echo "P2.3 OK: estado sin anotaciones, Required/StringLength/Range, errores, conservación, reto y scripts renderizados."

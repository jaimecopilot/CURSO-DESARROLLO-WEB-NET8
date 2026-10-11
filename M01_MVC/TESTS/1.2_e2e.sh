#!/usr/bin/env bash
# P1.2: E2E HTTP de cada estado que la práctica pide ejecutar.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/M01_MVC/PROYECTO/1.2/CursoWeb.Mvc"
TMP="$(mktemp -d)"
PID=""
BASE="http://127.0.0.1:5091"

cleanup() {
  if [[ -n "$PID" ]]; then
    kill "$PID" 2>/dev/null || true
    wait "$PID" 2>/dev/null || true
  fi
  rm -rf "$TMP"
}
trap cleanup EXIT

run_scenario() {
  local project="$1" state="$2"
  echo "P1.2: compilando estado $state"
  dotnet build "$project/CursoWeb.Mvc.csproj" -c Release --nologo
  pushd "$project" >/dev/null
  dotnet "bin/Release/net8.0/CursoWeb.Mvc.dll" --urls "$BASE" >"$TMP/$state.log" 2>&1 &
  PID=$!
  popd >/dev/null

  local ready=0
  for i in {1..45}; do
    if curl -fsS -o /dev/null "$BASE/Productos" 2>/dev/null; then ready=1; break; fi
    if ! kill -0 "$PID" 2>/dev/null; then break; fi
    sleep 1
  done
  if [[ "$ready" != 1 ]]; then cat "$TMP/$state.log"; echo "El servidor no arranca" >&2; exit 1; fi

  local code
  code=$(curl -sS -D "$TMP/headers-$state" -o "$TMP/body-$state" -w "%{http_code}" "$BASE/Productos")
  if [[ "$code" != "200" ]]; then
    echo "Error: GET /Productos devolvió HTTP $code en $state" >&2
    cat "$TMP/$state.log" >&2
    cat "$TMP/body-$state" >&2
    exit 1
  fi
  grep -iq '^Content-Type: text/html' "$TMP/headers-$state"
  grep -Fq '1.2 | Modelo, Vista y Controlador' "$TMP/body-$state"
  grep -Fq 'proposito-vista' "$TMP/body-$state"

  code=$(curl -sS -o "$TMP/alias-$state" -w "%{http_code}" "$BASE/Productos/Index")
  [[ "$code" == "200" ]]
  grep -Fq '1.2 | Modelo, Vista y Controlador' "$TMP/alias-$state"

  code=$(curl -sS -o "$TMP/home-$state" -w "%{http_code}" "$BASE/")
  [[ "$code" == "200" ]]
  grep -Fq '1.1 | Primer recorrido MVC' "$TMP/home-$state"

  code=$(curl -sS -D "$TMP/cssheaders-$state" -o /dev/null -w "%{http_code}" "$BASE/css/site.css")
  [[ "$code" == "200" ]]
  grep -iq '^Content-Type: text/css' "$TMP/cssheaders-$state"

  code=$(curl -sS -o /dev/null -w "%{http_code}" "$BASE/no-existe")
  [[ "$code" == "404" ]]

  if [[ "$state" == "datos-vista" || "$state" == "completo" || "$state" == "reto" ]]; then
    echo "Verificación de HTML renderizado en $state:"
    grep -nE 'numero-productos|listado-productos|data-id|Cuaderno|Lápiz|Carpeta' "$TMP/body-$state" || true
  fi
  if [[ "$state" == "base" ]]; then
    grep -Fq 'id="sin-modelo"' "$TMP/body-$state"
    ! grep -Fq 'id="numero-productos"' "$TMP/body-$state"
  else
    ! grep -Fq 'id="sin-modelo"' "$TMP/body-$state"
    grep -Eq 'ha enviado <strong>3</strong> productos' "$TMP/body-$state"
    grep -Fq 'id="numero-productos"' "$TMP/body-$state"
  fi
  if [[ "$state" == "datos-vista" || "$state" == "completo" || "$state" == "reto" ]]; then
    grep -Fq 'id="listado-productos"' "$TMP/body-$state"
    # Razor codifica caracteres acentuados en HTML: comprobar texto decodificado.
    python3 - "$TMP/body-$state" "$state" <<'PY'
from html import unescape
from pathlib import Path
import sys
html = unescape(Path(sys.argv[1]).read_text(encoding="utf-8"))
expected_first = "Bloc" if sys.argv[2] == "reto" else "Cuaderno"
for product in (expected_first, "Lápiz", "Carpeta"):
    assert product in html, f"No se muestra el producto {product}"
assert html.count('data-id="') == 3, "El listado no tiene exactamente tres elementos"
if expected_first == "Bloc":
    assert "Cuaderno" not in html, "El reto debe reemplazar y no duplicar Cuaderno"
PY
  else
    ! grep -Fq 'id="listado-productos"' "$TMP/body-$state"
  fi
  if [[ "$state" == "completo" || "$state" == "reto" ]]; then
    grep -Fq 'href="/Productos">Productos</a>' "$TMP/body-$state"
  else
    ! grep -Fq 'href="/Productos">Productos</a>' "$TMP/body-$state"
  fi
  echo "E2E OK: P1.2 $state; GET, estado MVC, datos, vista, navegación y CSS"
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  PID=""
}

run_scenario "$SRC" base

python3 - "$SRC" "$TMP" <<'PY'
from pathlib import Path
from shutil import copytree, ignore_patterns
import sys

source, tmp = map(Path, sys.argv[1:])
for name, data, view, nav in [
    ("datos", True, False, False),
    ("datos-vista", True, True, False),
    ("completo", True, True, True),
    ("reto", True, True, True),
]:
    dest = tmp / name
    copytree(source, dest, ignore=ignore_patterns("bin", "obj"))
    ctl = dest / "Controllers" / "ProductosController.cs"
    code = ctl.read_text(encoding="utf-8")
    start, end = "        /* PASO 1.2.3 INICIO\n", "        PASO 1.2.3 FIN */\n"
    ret = "        return View(); // PASO 1.2.3: comentar al activar el envío de datos."
    assert code.count(start) == 1 and code.count(end) == 1 and code.count(ret) == 1
    if data:
        code = code.replace(start, "").replace(end, "").replace(ret, "        // " + ret.strip())
    if name == "reto":
        original = '            new() { Id = 1, Nombre = "Cuaderno", Precio = 4.50m },'
        variant = '            // new() { Id = 1, Nombre = "Bloc", Precio = 4.50m },'
        assert code.count(original) == 1 and code.count(variant) == 1, "Falta código comentado del RETO 1.2"
        code = code.replace(original, "            // " + original.strip())
        code = code.replace(variant, '            new() { Id = 1, Nombre = "Bloc", Precio = 4.50m },')
    ctl.write_text(code, encoding="utf-8")

    v = dest / "Views" / "Productos" / "Index.cshtml"
    code = v.read_text(encoding="utf-8")
    start, end = "    @* PASO 1.2.4 (inicio)\n", "    PASO 1.2.4 (fin) *@\n"
    assert code.count(start) == 1 and code.count(end) == 1
    if view:
        code = code.replace(start, "").replace(end, "")
    v.write_text(code, encoding="utf-8")

    layout = dest / "Views" / "Shared" / "_Layout.cshtml"
    code = layout.read_text(encoding="utf-8")
    start, end = '            @* PASO 1.2.5 (inicio)\n', '            PASO 1.2.5 (fin) *@\n'
    assert code.count(start) == 1 and code.count(end) == 1
    if nav:
        code = code.replace(start, "").replace(end, "")
    layout.write_text(code, encoding="utf-8")
PY

run_scenario "$TMP/datos" datos
run_scenario "$TMP/datos-vista" datos-vista
run_scenario "$TMP/completo" completo
run_scenario "$TMP/reto" reto

echo "P1.2: cinco escenarios E2E reales superados, incluido el reto."

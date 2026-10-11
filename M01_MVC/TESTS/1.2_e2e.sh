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

  if [[ "$state" == "datos-vista" || "$state" == "completo" ]]; then
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
  if [[ "$state" == "datos-vista" || "$state" == "completo" ]]; then
    grep -Fq 'id="listado-productos"' "$TMP/body-$state"
    for product in Cuaderno Lápiz Carpeta; do grep -Fq "$product" "$TMP/body-$state"; done
    [[ $(grep -c 'data-id="' "$TMP/body-$state") == 3 ]]
  else
    ! grep -Fq 'id="listado-productos"' "$TMP/body-$state"
  fi
  if [[ "$state" == "completo" ]]; then
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

echo "P1.2: cuatro escenarios E2E reales superados."

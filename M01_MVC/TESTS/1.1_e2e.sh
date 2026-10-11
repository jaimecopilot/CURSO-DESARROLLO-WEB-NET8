#!/usr/bin/env bash
# E2E HTTP del punto 1.1; prueba estado base y dos pasos optativos activados.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/M01_MVC/PROYECTO/1.1/CursoWeb.Mvc"
TMP="$(mktemp -d)"
PID=""
PORT=5091
BASE="http://127.0.0.1:$PORT"

cleanup() {
  if [[ -n "$PID" ]]; then
    kill "$PID" 2>/dev/null || true
    wait "$PID" 2>/dev/null || true
  fi
  rm -rf "$TMP"
}
trap cleanup EXIT

run_scenario() {
  local project="$1"
  local state="$2"
  echo "Compilando escenario: $state"
  dotnet build "$project/CursoWeb.Mvc.csproj" -c Release --nologo
  echo "Arrancando Kestrel: $state"
  dotnet "$project/bin/Release/net8.0/CursoWeb.Mvc.dll" --urls "$BASE" >"$TMP/server-$state.log" 2>&1 &
  PID=$!

  local ready=0
  for i in {1..40}; do
    if curl --silent --output /dev/null "$BASE/"; then ready=1; break; fi
    if ! kill -0 "$PID" 2>/dev/null; then break; fi
    sleep 1
  done
  if [[ "$ready" != 1 ]]; then
    cat "$TMP/server-$state.log"
    echo "Error: servidor no inicia" >&2
    exit 1
  fi

  local status
  status=$(curl --silent --show-error -D "$TMP/headers-$state.txt" -o "$TMP/body-$state.html" -w "%{http_code}" "$BASE/")
  [[ "$status" == 200 ]] || { echo "GET / devolvió $status en $state" >&2; exit 1; }
  grep -iq '^Content-Type: text/html' "$TMP/headers-$state.txt"
  grep -Fq '1.1 | Primer recorrido MVC' "$TMP/body-$state.html"
  grep -Fq 'resultado-inicial' "$TMP/body-$state.html"
  grep -Fq 'Navegación principal' "$TMP/body-$state.html"

  status=$(curl --silent --show-error --output /dev/null --write-out "%{http_code}" "$BASE/ruta-inexistente")
  [[ "$status" == 404 ]] || { echo "Ruta inexistente: $status; se esperaba 404" >&2; exit 1; }

  if [[ "$state" == "base" ]]; then
    ! grep -iq '^X-Curso-Paso:' "$TMP/headers-$state.txt"
    ! grep -Fq 'id="marca-paso-1-1-5"' "$TMP/body-$state.html"
  else
    grep -iq '^X-Curso-Paso: 1.1.4' "$TMP/headers-$state.txt"
    grep -Fq 'id="marca-paso-1-1-5"' "$TMP/body-$state.html"
  fi
  echo "E2E OK: $state (HTTP 200/404, vista Razor, layout y variantes)"

  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  PID=""
}

run_scenario "$SRC" "base"

# La activación se hace en un duplicado temporal del proyecto del alumno.
mkdir -p "$TMP/activado"
cp -a "$SRC/." "$TMP/activado/"
rm -rf "$TMP/activado/bin" "$TMP/activado/obj"
python3 - "$TMP/activado" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
controller = root / "Controllers" / "HomeController.cs"
content = controller.read_text(encoding="utf-8")
before = '// Response.Headers["X-Curso-Paso"] = "1.1.4";'
assert content.count(before) == 1, "No existe un bloque activable 1.1.4 único"
controller.write_text(content.replace(before, 'Response.Headers["X-Curso-Paso"] = "1.1.4";'), encoding="utf-8")

view = root / "Views" / "Home" / "Index.cshtml"
content = view.read_text(encoding="utf-8")
start, end = '@* PASO 1.1.5 (inicio)\n', '\nPASO 1.1.5 (fin) *@'
assert content.count(start) == 1 and content.count(end) == 1, "No existe un bloque Razor 1.1.5 único"
view.write_text(content.replace(start, "").replace(end, ""), encoding="utf-8")
PY

run_scenario "$TMP/activado" "activado"
echo "Punto 1.1: los dos escenarios E2E han superado las comprobaciones."

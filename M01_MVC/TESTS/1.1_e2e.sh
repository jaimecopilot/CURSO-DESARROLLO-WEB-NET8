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
  # El directorio de trabajo debe coincidir con el proyecto para localizar wwwroot.
  pushd "$project" >/dev/null
  dotnet "bin/Release/net8.0/CursoWeb.Mvc.dll" --urls "$BASE" >"$TMP/server-$state.log" 2>&1 &
  PID=$!
  popd >/dev/null

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

  status=$(curl --silent --show-error -o "$TMP/alternative-$state.html" --write-out "%{http_code}" "$BASE/Home/Index")
  [[ "$status" == 200 ]] || { echo "GET /Home/Index devolvió $status" >&2; exit 1; }
  grep -Fq '1.1 | Primer recorrido MVC' "$TMP/alternative-$state.html"

  status=$(curl --silent --show-error -D "$TMP/cssheaders-$state.txt" -o "$TMP/css-$state.txt" --write-out "%{http_code}" "$BASE/css/site.css")
  [[ "$status" == 200 ]] || { echo "GET /css/site.css devolvió $status" >&2; exit 1; }
  grep -iq '^Content-Type: text/css' "$TMP/cssheaders-$state.txt"
  ! grep -iq '^X-Curso-Paso:' "$TMP/cssheaders-$state.txt"

  status=$(curl --silent --show-error --output /dev/null --write-out "%{http_code}" "$BASE/ruta-inexistente")
  [[ "$status" == 404 ]] || { echo "Ruta inexistente: $status; se esperaba 404" >&2; exit 1; }

  if [[ "$state" == "base" || "$state" == "solo-vista" ]]; then
    ! grep -iq '^X-Curso-Paso:' "$TMP/headers-$state.txt"
  else
    grep -iq '^X-Curso-Paso: 1.1.4' "$TMP/headers-$state.txt"
  fi

  if [[ "$state" == "base" || "$state" == "solo-cabecera" ]]; then
    ! grep -Fq 'id="marca-paso-1-1-5"' "$TMP/body-$state.html"
  else
    grep -Fq 'id="marca-paso-1-1-5"' "$TMP/body-$state.html"
  fi
  echo "E2E OK: $state (HTTP 200/404, vista Razor, layout y variantes)"

  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  PID=""
}

run_scenario "$SRC" "base"

# Las tres variantes se generan sin modificar el código original del alumno.
python3 - "$SRC" "$TMP" <<'PY'
from pathlib import Path
from shutil import copytree, ignore_patterns
import sys

source, temporary = map(Path, sys.argv[1:])
header_line = '// Response.Headers["X-Curso-Paso"] = "1.1.4";'
razor_start, razor_end = '@* PASO 1.1.5 (inicio)\n', '\nPASO 1.1.5 (fin) *@'

for name, enable_header, enable_view in [
    ("solo-cabecera", True, False),
    ("solo-vista", False, True),
    ("activado", True, True),
]:
    target = temporary / name
    copytree(source, target, ignore=ignore_patterns("obj", "bin"))

    controller = target / "Controllers" / "HomeController.cs"
    c = controller.read_text(encoding="utf-8")
    assert c.count(header_line) == 1, "No se encuentra el paso 1.1.4"
    if enable_header:
        c = c.replace(header_line, header_line[3:])
    controller.write_text(c, encoding="utf-8")

    view = target / "Views" / "Home" / "Index.cshtml"
    v = view.read_text(encoding="utf-8")
    assert v.count(razor_start) == 1 and v.count(razor_end) == 1, "No se encuentra el paso 1.1.5"
    if enable_view:
        v = v.replace(razor_start, "").replace(razor_end, "")
    view.write_text(v, encoding="utf-8")
PY

run_scenario "$TMP/solo-cabecera" "solo-cabecera"
run_scenario "$TMP/solo-vista" "solo-vista"
run_scenario "$TMP/activado" "activado"

# La práctica también crea una aplicación desde la plantilla incluida en el SDK.
echo "Verificando la plantilla oficial MVC de .NET 8"
dotnet new mvc -f net8.0 --no-https -n PlantillaMvc -o "$TMP/PlantillaMvc" --no-restore
dotnet build "$TMP/PlantillaMvc/PlantillaMvc.csproj" -c Release --nologo
pushd "$TMP/PlantillaMvc" >/dev/null
dotnet "bin/Release/net8.0/PlantillaMvc.dll" --urls http://127.0.0.1:5095 >"$TMP/template.log" 2>&1 &
PID=$!
popd >/dev/null
ready=0
for i in {1..40}; do
  if curl --silent --output /dev/null http://127.0.0.1:5095/; then ready=1; break; fi
  if ! kill -0 "$PID" 2>/dev/null; then break; fi
  sleep 1
done
if [[ "$ready" != 1 ]]; then cat "$TMP/template.log"; echo "Falló la plantilla MVC" >&2; exit 1; fi
status=$(curl --silent --show-error -o "$TMP/template.html" --write-out "%{http_code}" http://127.0.0.1:5095/)
[[ "$status" == 200 ]]
grep -iq '<html' "$TMP/template.html"
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
PID=""
echo "E2E OK: plantilla MVC creada, compilada y ejecutada."
echo "Punto 1.1: cinco escenarios E2E reales superados."

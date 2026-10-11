#!/usr/bin/env bash
# P1.3: cada modificación de configuración, CSS, recurso público y reto es un estado ejecutable.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/M01_MVC/PROYECTO/1.3/CursoWeb.Mvc"
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
  local project="$1" state="$2" status ready
  echo "P1.3: compilando estado $state"
  dotnet build "$project/CursoWeb.Mvc.csproj" -c Release --nologo
  pushd "$project" >/dev/null
  dotnet "bin/Release/net8.0/CursoWeb.Mvc.dll" --urls "$BASE" >"$TMP/log-$state.txt" 2>&1 &
  PID=$!
  popd >/dev/null

  ready=0
  for _ in {1..45}; do
    if curl -fsS -o /dev/null "$BASE/Productos" 2>/dev/null; then ready=1; break; fi
    if ! kill -0 "$PID" 2>/dev/null; then break; fi
    sleep 1
  done
  if [[ "$ready" != 1 ]]; then cat "$TMP/log-$state.txt"; echo "No arranca Kestrel en $state" >&2; exit 1; fi

  status=$(curl -sS -o "$TMP/home-$state.html" -w "%{http_code}" "$BASE/")
  [[ "$status" == 200 ]]
  grep -Fq '1.1 | Primer recorrido MVC' "$TMP/home-$state.html"

  status=$(curl -sS -o "$TMP/prod-$state.html" -w "%{http_code}" "$BASE/Productos")
  [[ "$status" == 200 ]]
  grep -Fq 'El controlador ha enviado <strong>3</strong> productos' "$TMP/prod-$state.html"
  python3 - "$TMP/prod-$state.html" <<'PY'
from pathlib import Path
from html import unescape
import sys
html = unescape(Path(sys.argv[1]).read_text(encoding="utf-8"))
for nombre in ("Cuaderno", "Lápiz", "Carpeta"):
    assert nombre in html, f"Falta {nombre}"
assert html.count('data-id="') == 3
PY
  grep -Fq 'href="/Productos">Productos</a>' "$TMP/prod-$state.html"

  # Los recursos de wwwroot son públicos incluso antes de ponerles un enlace.
  status=$(curl -sS -D "$TMP/cssheaders-$state" -o "$TMP/css-$state.txt" -w "%{http_code}" "$BASE/css/catalogo.css")
  [[ "$status" == 200 ]]
  grep -iq '^Content-Type: text/css' "$TMP/cssheaders-$state"
  grep -Fq 'main.container' "$TMP/css-$state.txt"

  status=$(curl -sS -o "$TMP/guide-$state.txt" -w "%{http_code}" "$BASE/recursos/guia-publica.txt")
  [[ "$status" == 200 ]]
  grep -Fq 'PASO 1.3.5' "$TMP/guide-$state.txt"

  status=$(curl -sS -o "$TMP/aviso-$state.txt" -w "%{http_code}" "$BASE/recursos/aviso-laboratorio.txt")
  [[ "$status" == 200 ]]
  grep -Fq 'RETO 1.3' "$TMP/aviso-$state.txt"

  status=$(curl -sS -o /dev/null -w "%{http_code}" "$BASE/DOCUMENTACION/nota-interna.txt")
  [[ "$status" == 404 ]] || { echo "Un archivo fuera de wwwroot se publicó inesperadamente" >&2; exit 1; }

  status=$(curl -sS -o /dev/null -w "%{http_code}" "$BASE/no-existe")
  [[ "$status" == 404 ]]

  if [[ "$state" == "base" ]]; then
    ! grep -Fq "P1.3 configuracion: Curso MVC de productos" "$TMP/log-$state.txt"
  else
    grep -Fq "P1.3 configuracion: Curso MVC de productos" "$TMP/log-$state.txt"
  fi

  if [[ "$state" == "base" || "$state" == "log" ]]; then
    ! grep -Fq 'href="/css/catalogo.css"' "$TMP/prod-$state.html"
  else
    grep -Fq 'href="/css/catalogo.css"' "$TMP/prod-$state.html"
  fi

  if [[ "$state" == "base" || "$state" == "log" || "$state" == "css" ]]; then
    ! grep -Fq 'href="/recursos/guia-publica.txt"' "$TMP/prod-$state.html"
  else
    grep -Fq 'href="/recursos/guia-publica.txt"' "$TMP/prod-$state.html"
  fi

  if [[ "$state" == "reto" ]]; then
    grep -Fq 'href="/recursos/aviso-laboratorio.txt"' "$TMP/prod-$state.html"
  else
    ! grep -Fq 'href="/recursos/aviso-laboratorio.txt"' "$TMP/prod-$state.html"
  fi

  echo "E2E OK: P1.3 $state; 200 MVC/estáticos, 404 fuera de wwwroot, configuración y enlaces"
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  PID=""
}

run_scenario "$SRC" "base"

python3 - "$SRC" "$TMP" <<'PY'
from pathlib import Path
from shutil import copytree, ignore_patterns
import sys
src, temp = map(Path, sys.argv[1:])
for state, enable_log, enable_css, enable_guide, enable_reto in [
    ("log", True, False, False, False),
    ("css", True, True, False, False),
    ("guia", True, True, True, False),
    ("reto", True, True, True, True),
]:
    dest = temp / state
    copytree(src, dest, ignore=ignore_patterns("bin", "obj"))

    program = dest / "Program.cs"
    content = program.read_text(encoding="utf-8")
    commented = '// app.Logger.LogInformation("P1.3 configuracion: {Nombre}", app.Configuration["Curso:Nombre"]);'
    assert content.count(commented) == 1, "Falta bloque de configuración 1.3.3"
    if enable_log:
        content = content.replace(commented, commented[3:])
    program.write_text(content, encoding="utf-8")

    layout = dest / "Views" / "Shared" / "_Layout.cshtml"
    content = layout.read_text(encoding="utf-8")
    for enabled, start, end in [
        (enable_css, '    @* PASO 1.3.4 (inicio)\n', '    PASO 1.3.4 (fin) *@\n'),
        (enable_guide, '            @* PASO 1.3.5 (inicio)\n', '            PASO 1.3.5 (fin) *@\n'),
        (enable_reto, '            @* RETO 1.3 (inicio)\n', '            RETO 1.3 (fin) *@\n'),
    ]:
        assert content.count(start) == 1 and content.count(end) == 1, f"Falta bloque {start}"
        if enabled:
            content = content.replace(start, "").replace(end, "")
    layout.write_text(content, encoding="utf-8")
PY

for state in log css guia reto; do
  run_scenario "$TMP/$state" "$state"
done

echo "P1.3: cinco escenarios E2E superados, reto incluido."

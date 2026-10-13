#!/usr/bin/env python3
"""Compara TODOS los bloques de código de prácticas con el proyecto del punto."""
from pathlib import Path
from collections import Counter
import re
ROOT=Path(__file__).resolve().parents[2]
PRACT=(ROOT/"M01_MVC/PRACTICAS/M01_PRACTICAS.md").read_text(encoding="utf-8")
BASE=ROOT/"M01_MVC/PROYECTO"
DEST=ROOT/"VERIFICACION_INTERNA/M01_CODIGO_TODOS_LOS_EJEMPLOS.md"
EXT={"csharp":{".cs"},"cshtml":{".cshtml"},"json":{".json"},
     "css":{".css"},"xml":{".csproj",".xml"}}
def norm(s): return re.sub(r"\s+","",s)
def meaningful(line):
    v=line.strip()
    return (len(v)>3 and not v.startswith(("// ","/* PASO","PASO ","/* RETO","RETO ","@* "))
            and v not in ("{","}","};"))
def main():
    heads=list(re.finditer(r"(?m)^# P1\.([1-5])\.",PRACT))
    results=[]
    for i,h in enumerate(heads):
        point="1."+h.group(1)
        body=PRACT[h.start():(heads[i+1].start() if i+1<len(heads) else len(PRACT))]
        project=BASE/point/"CursoWeb.Mvc"
        source=[(p.relative_to(project).as_posix(),p.read_text(encoding="utf-8"))
                for p in project.rglob("*") if p.is_file()
                and p.suffix in {".cs",".cshtml",".css",".json",".csproj",".xml"}
                and "obj" not in p.parts and "bin" not in p.parts]
        for m in re.finditer(r"(?m)^~~~([A-Za-z0-9+.-]+)\s*\n([\s\S]*?)^~~~\s*$",body):
            lang=m.group(1).lower()
            if lang not in EXT: continue
            code=m.group(2)
            files=[(name,txt) for name,txt in source if Path(name).suffix in EXT[lang]]
            literal=[name for name,txt in files if norm(code) in norm(txt)]
            lines=[norm(line) for line in code.splitlines() if meaningful(line)]
            measured=[]
            for name,txt in files:
                compact=norm(txt)
                covered=sum(line in compact for line in lines)
                measured.append((covered,name))
            covered,name=max(measured,default=(0,""))
            coverage=covered/max(1,len(lines))
            status=("LITERAL" if literal else
                    "VARIANTE" if coverage>=.95 else
                    "PARCIAL" if coverage>=.60 else "NO_ACREDITADO")
            row={"punto":point,"linea":PRACT[:h.start()+m.start()].count("\n")+1,
                 "lenguaje":lang,"estado":status,"archivo":literal[0] if literal else name,
                 "cubiertas":len(lines) if literal else covered,"lineas":len(lines),
                 "extracto":next((z.strip()[:80] for z in code.splitlines() if z.strip()),"")}
            results.append(row)
    counts=Counter(x["estado"] for x in results)
    report=["# Auditoría completa de fragmentos de práctica contra código de M01","",
      "Es un diagnóstico de cobertura estática, NO una demostración de ejecución ni una equivalencia semántica completa.",
      "Coincidencia LITERAL significa igualdad del bloque tras normalizar espacios. VARIANTE significa 95% o más de líneas reconocibles en el archivo fuente y requiere verificar la activación.",
      "PARCIAL o NO_ACREDITADO deben revisarse individualmente. Un ejemplo abreviado puede ser legítimo si se identifica claramente como tal.",
      "",f"Total: {len(results)} bloques. "+", ".join(f"{name}: {count}" for name,count in sorted(counts.items())),
      "","| Punto | Línea del MD | Lenguaje | Clasificación | Archivo probable | Líneas identificadas | Primer contenido |",
      "|---|---:|---|---|---|---:|---|"]
    for item in results:
        report.append("| {punto} | {linea} | {lenguaje} | {estado} | {archivo} | {cubiertas}/{lineas} | {extracto} |".format(
            **{k:str(v).replace("|","/") for k,v in item.items()}))
    report+=["","## Elementos que requieren revisión editorial",""]
    for item in results:
        if item["estado"] in ("PARCIAL","NO_ACREDITADO"):
            report.append("- P{punto} línea {linea}, {estado}, archivo {archivo}, {cubiertas}/{lineas}: {extracto}".format(**item))
    report+=["","## Interpretación","",
        "Los fragmentos mostrados en su forma activa pueden no coincidir literalmente con el proyecto que los conserva comentados. La revisión de esos casos exige comprobar el script E2E y la documentación de activación.",
        "No declarar 100% de trazabilidad solo por las etiquetas PASO y RETO o por una prueba HTTP genérica.", ""]
    DEST.write_text("\n".join(report),encoding="utf-8")
    if counts.get("PARCIAL",0) or counts.get("NO_ACREDITADO",0):
        for row in results:
            if row["estado"] in ("PARCIAL", "NO_ACREDITADO"):
                print("REVISAR BLOQUE", row, flush=True)
        raise AssertionError("Existen fragmentos sin cobertura suficientemente acreditada en proyectos; ver matriz.")
    print("BLOQUES ANALIZADOS",len(results),"ESTADOS",dict(counts))
    for x in results:
        if x["estado"] != "LITERAL": print("REVISAR",x)
if __name__=="__main__": main()

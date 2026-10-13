#!/usr/bin/env python3
"""Verifica los estados J3-J6 compilando código EXTRÁIDO del MD del alumno.

Ningún Program.cs terminado preentregado se utiliza para construir estas etapas.
El mismo test usa el proveedor SqlServer; el workflow Windows comprueba además
el recorrido E2E de usuarios reales en LocalDB.
"""
from pathlib import Path
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
MD=(ROOT/"M04_APIS_SEGURIDAD/PRACTICAS/M04_PRACTICAS.md").read_text(encoding="utf-8")
START=MD.index("#### Paso J3. Construir Identity y comprobar las tablas LocalDB")
END=MD.index("#### Paso J7. Construir el estado final sin saltarse los anteriores", START)
section=MD[START:END]
PROJECT=ROOT/"M04_APIS_SEGURIDAD/PROYECTO/4.5/CursoWeb.IdentityJwtApi/CursoWeb.IdentityJwtApi.csproj"
csproj=PROJECT.read_text(encoding="utf-8")
assert "Microsoft.EntityFrameworkCore.SqlServer" in csproj
assert "Microsoft.EntityFrameworkCore.Sqlite" not in csproj

def blocks(marker):
    i=section.index(marker)
    nxt=section.find("#### Paso J", i+len(marker))
    part=section[i:nxt if nxt!=-1 else len(section)]
    return re.findall(r"~~~csharp\s*\n(.*?)\n~~~",part,re.S)

j3=blocks("#### Paso J3.")
j4=blocks("#### Paso J4.")
j5=blocks("#### Paso J5.")
j6=blocks("#### Paso J6.")
assert [len(x) for x in (j3,j4,j5,j6)]==[4,2,4,5], [len(x) for x in (j3,j4,j5,j6)]
program3="\n\n".join(j3) + "\n"
assert program3.count("var app = builder.Build();")==1
assert program3.count("app.Run();")==1
assert "UseSqlServer(conexion)" in program3

def before_run(program,code):
    assert program.count("app.Run();")==1
    return program.replace("app.Run();",code+"\n\napp.Run();",1)

program4=before_run(program3,j4[0])+"\n"+j4[1]+"\n"
program5=(j5[0]+"\n\n"+program4)
program5=program5.replace("var builder = WebApplication.CreateBuilder(args);",
    "var builder = WebApplication.CreateBuilder(args);\n\n"+j5[1],1)
program5=before_run(program5,j5[2])+"\n"+j5[3]+"\n"
program6=j6[0]+"\n"+program5
program6=program6.replace("var app = builder.Build();",
    j6[1]+"\n\nvar app = builder.Build();",1)
program6=program6.replace('app.MapGet("/",',j6[2]+'\n\napp.MapGet("/",',1)
program6=before_run(program6,j6[3])
assert "RequireRole(\"Formador\")" in program6
assert program6.count("builder.Build()")==1

with tempfile.TemporaryDirectory(prefix="m04-identity-desde-md-") as temp:
    root=Path(temp)
    for i,code in enumerate((program3,program4,program5,program6),start=3):
        p=root/f"J{i}"
        p.mkdir()
        (p/"CursoWeb.IdentityJwtApi.csproj").write_text(csproj,encoding="utf-8")
        (p/"Program.cs").write_text(code,encoding="utf-8")
        run=subprocess.run(["dotnet","build",str(p/"CursoWeb.IdentityJwtApi.csproj"),
                 "-c","Release"],capture_output=True,text=True)
        if run.returncode:
            raise AssertionError(f"J{i} NO COMPILA: {run.stdout[-12000:]} {run.stderr[-3000:]}")
        print(f"J{i}: COMPILA extraído literalmente de prácticas",flush=True)
print("J3-J6: etapas acumulativas compiladas desde el Markdown, sin solución final",flush=True)

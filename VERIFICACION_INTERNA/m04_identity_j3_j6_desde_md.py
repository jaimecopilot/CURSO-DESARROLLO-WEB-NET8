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
import os
import time
import json
import urllib.request
import urllib.error

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

    # El servidor del alumno se ejecuta DE VERDAD sobre LocalDB Windows
    # y no comparte base con la implementación de referencia.
    p=root/"J6"
    (p/"appsettings.json").write_text((ROOT/"M04_APIS_SEGURIDAD/PROYECTO/4.5/CursoWeb.IdentityJwtApi/appsettings.json").read_text(encoding="utf-8"),encoding="utf-8")
    db=os.environ.get("ConnectionStrings__IdentityDb","")
    if "(localdb)" not in db:
        raise AssertionError("Esta prueba requiere SQL Server Express LocalDB real.")
    own=re.sub(r"Database=[^;]+",lambda m:m.group(0)+"_ALUMNO",db,count=1)
    env=os.environ.copy()
    env["ConnectionStrings__IdentityDb"]=own
    port=5090
    dll=p/"bin"/"Release"/"net8.0"/"CursoWeb.IdentityJwtApi.dll"
    proc=subprocess.Popen(["dotnet",str(dll),"--urls",f"http://127.0.0.1:{port}"],
        cwd=p,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    base=f"http://127.0.0.1:{port}"
    def request(path,method="GET",body=None,token=None):
        headers={"Content-Type":"application/json"}
        if token: headers["Authorization"]="Bearer "+token
        req=urllib.request.Request(base+path,method=method,headers=headers,
            data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(req,timeout=10) as resp:
                return resp.status,json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as err:
            return err.code,{}
    try:
        for _ in range(75):
            if proc.poll() is not None:
                raise AssertionError("El servidor J6 dejó de ejecutarse")
            try:
                if request("/")[0]==200: break
            except (urllib.error.URLError, TimeoutError):
                time.sleep(2)
        else: raise AssertionError("J6 no inició en LocalDB")
        assert request("/api/identidad/yo")[0]==401
        creds={"email":"j6_alumno@example.test","password":"ClaveAlumnoSegura-2026!"}
        assert request("/auth/registro","POST",creds)[0]==201
        code,data=request("/auth/login","POST",creds)
        assert code==200 and data.get("accessToken"),(code,data)
        jwt=data["accessToken"]
        assert request("/api/identidad/yo",token=jwt)[0]==200
        assert request("/api/identidad/formador",token=jwt)[0]==403
        print("J6 EJECUTADO sobre LocalDB real: 201, 200 login, 401, 200 perfil y 403 Alumno",flush=True)
    finally:
        proc.terminate()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired: proc.kill()
print("J3-J6: estados compilados y API final ejecutada DESDE EL MARKDOWN",flush=True)

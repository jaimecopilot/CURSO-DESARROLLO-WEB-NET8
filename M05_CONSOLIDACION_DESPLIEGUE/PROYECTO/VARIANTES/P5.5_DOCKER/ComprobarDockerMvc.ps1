
# P5.5 — Variante autónoma: ciclo completo sobre la MISMA aplicación MVC A.
# Desde la raíz del repositorio, en PowerShell y con Docker Linux disponible.
param(
    [string]$CarpetaMvc = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc",
    [string]$Imagen = "cursoweb-mvc:m05-verificada",
    [string]$Contenedor = "cursoweb-m05-verificada",
    [int]$PuertoHost = 8083
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path (Join-Path $CarpetaMvc "CursoWeb.Mvc.csproj"))) {
    throw "No existe el proyecto MVC en $CarpetaMvc"
}
$tipo = (docker info --format "{{.OSType}}").Trim()
if ($LASTEXITCODE -ne 0 -or $tipo -ne "linux") {
    throw "La práctica exige Docker operativo en modo Linux"
}
$yaExiste = docker ps -a --filter "name=^/$Contenedor$" --format "{{.Names}}"
if ($yaExiste) {
    throw "Ya existe un contenedor llamado $Contenedor. No se elimina automáticamente."
}
Push-Location $CarpetaMvc
try {
    docker build -t $Imagen .
    if ($LASTEXITCODE -ne 0) { throw "Falló docker build" }
} finally {
    Pop-Location
}
$creado = $false
try {
    docker run -d --name $Contenedor -p "${PuertoHost}:8080" `
        -e Despliegue__SinLocalDb=true $Imagen | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Falló docker run" }
    $creado = $true
    $base = "http://127.0.0.1:$PuertoHost"
    $listo = $false
    for ($i = 0; $i -lt 40; $i++) {
        Start-Sleep -Seconds 1
        try {
            $respuesta = Invoke-WebRequest "$base/Productos/Estado" -UseBasicParsing -TimeoutSec 3
            if ($respuesta.StatusCode -eq 200) { $listo = $true; break }
        } catch {
            Write-Host "Esperando respuesta del contenedor..."
        }
    }
    if (-not $listo) {
        docker logs $Contenedor
        throw "El contenedor no devolvió 200 desde /Productos/Estado"
    }
    foreach ($ruta in @("/", "/Productos/Estado", "/css/site.css")) {
        $r = Invoke-WebRequest "$base$ruta" -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -ne 200) { throw "Se esperaba 200 en $ruta" }
        Write-Host "$ruta: 200"
    }
    try {
        Invoke-WebRequest "$base/Productos" -UseBasicParsing -TimeoutSec 5 | Out-Null
        throw "No es correcto obtener 200 del CRUD sin LocalDB"
    } catch [System.Net.WebException] {
        $estado = [int]$_.Exception.Response.StatusCode
        if ($estado -ne 503) { throw "Productos devolvió $estado en lugar de 503" }
        Write-Host "Productos: 503 previsto; LocalDB no existe en Linux"
    }
} finally {
    if ($creado) {
        docker logs $Contenedor
        docker stop $Contenedor | Out-Null
        docker rm -f $Contenedor | Out-Null
    }
}
Write-Host "Imagen conservada: $Imagen"
Write-Host "No se afirma funcionamiento del CRUD persistente."

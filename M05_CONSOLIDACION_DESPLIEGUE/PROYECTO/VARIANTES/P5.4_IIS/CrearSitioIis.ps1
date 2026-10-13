
# P5.4 — Variante autónoma. Ejecutar como administrador SOLO en host Windows
# con IIS y ASP.NET Core Hosting Bundle 8 previamente instalados.
# No modifica proyectos ni elimina sitios existentes.
param(
    [string]$Proyecto = ".\M05_CONSOLIDACION_DESPLIEGUE\PROYECTO\MVC\CursoWeb.Mvc\CursoWeb.Mvc.csproj",
    [string]$Destino = "C:\CursoWeb\M05\IIS",
    [int]$Puerto = 8091,
    [string]$Sitio = "CursoWeb-M05",
    [string]$Pool = "CursoWeb-M05-Pool"
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $Proyecto)) { throw "Falta el proyecto MVC: $Proyecto" }
Import-Module WebAdministration -ErrorAction Stop
if (Get-Website -Name $Sitio -ErrorAction SilentlyContinue) {
    throw "El sitio $Sitio ya existe; no se sobrescribe"
}
if (Test-Path "IIS:\AppPools\$Pool") {
    throw "El pool $Pool ya existe; no se sobrescribe"
}
$bindings = @(Get-WebBinding -Protocol http | Where-Object {
    $_.bindingInformation -like "*:$($Puerto):*"
})
if ($bindings.Count -gt 0) {
    throw "El puerto HTTP $Puerto ya está reservado por otro binding IIS"
}
New-Item -ItemType Directory -Path $Destino -Force | Out-Null
dotnet publish $Proyecto -c Release -o $Destino
if ($LASTEXITCODE -ne 0) { throw "No se pudo publicar MVC" }
foreach ($nombre in @("CursoWeb.Mvc.dll", "web.config", "wwwroot\css\site.css")) {
    if (-not (Test-Path (Join-Path $Destino $nombre))) {
        throw "La publicación no contiene $nombre"
    }
}
# Se modifica solo el directorio publicado, no el appsettings del proyecto.
$ajustes = @{ Despliegue = @{ SinLocalDb = $true } }
$ajustes | ConvertTo-Json -Depth 4 |
    Set-Content -Path (Join-Path $Destino "appsettings.Production.json") -Encoding UTF8
New-WebAppPool -Name $Pool | Out-Null
Set-ItemProperty "IIS:\AppPools\$Pool" -Name managedRuntimeVersion -Value ""
$identidad = "IIS AppPool\$Pool"
& icacls.exe $Destino /grant "${identidad}:(OI)(CI)RX" /T | Out-Null
if ($LASTEXITCODE -ne 0) { throw "No se pudieron asignar permisos de lectura" }
New-Website -Name $Sitio -PhysicalPath $Destino -Port $Puerto -ApplicationPool $Pool | Out-Null
Start-Website -Name $Sitio
Write-Host "Sitio $Sitio preparado: http://localhost:$Puerto/"
Write-Host "Comprobar GET /, /Productos/Estado, /css/site.css y el 503 de /Productos."
Write-Host "No se ha comprobado CRUD con LocalDB bajo la identidad IIS."

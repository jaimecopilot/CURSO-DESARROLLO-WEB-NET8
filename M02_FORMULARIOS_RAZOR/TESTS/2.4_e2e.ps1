# Prueba técnica de P2.4, ejecutable en Windows con .NET 8 y SQL Server Express LocalDB.
# Aísla la base usando un nombre único. No es un ejercicio del cuaderno del alumno.
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$source = Join-Path $repo "M02_FORMULARIOS_RAZOR/PROYECTO/2.4/CursoWeb.Mvc"
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("p24-e2e-" + [guid]::NewGuid().ToString("N"))
$project = Join-Path $tmp "CursoWeb.Mvc"
$database = "CursoWebP24_" + [guid]::NewGuid().ToString("N").Substring(0,16)
$env:ConnectionStrings__Productos = "Server=(localdb)\MSSQLLocalDB;Database=$database;Trusted_Connection=True;TrustServerCertificate=True"
$base = "http://127.0.0.1:5194"
$server = $null
$client = $null
$handler = $null

function Assert([bool]$ok,[string]$message) {
    if (-not $ok) { throw $message }
}
function Compile {
    & dotnet build (Join-Path $project "CursoWeb.Mvc.csproj") -c Release --nologo
    Assert ($LASTEXITCODE -eq 0) "No compila el proyecto de P2.4."
}
function Start-App {
    param([string]$tag)
    $script:server = Start-Process -FilePath "dotnet" -ArgumentList @("bin/Release/net8.0/CursoWeb.Mvc.dll","--urls",$base) -WorkingDirectory $project -NoNewWindow -PassThru -RedirectStandardOutput (Join-Path $tmp "$tag.out.log") -RedirectStandardError (Join-Path $tmp "$tag.err.log")
    $ready=$false
    for($i=0; $i -lt 50; $i++) {
        Start-Sleep -Milliseconds 900
        if($script:server.HasExited) {
            $e=Get-Content -Raw -ErrorAction SilentlyContinue (Join-Path $tmp "$tag.err.log")
            throw "Kestrel ha terminado al iniciar $tag. $e"
        }
        try {
            $test=[System.Net.Http.HttpClient]::new()
            $probe=$test.GetAsync("$base/Productos/Crear").GetAwaiter().GetResult()
            $test.Dispose()
            if([int]$probe.StatusCode -eq 200) { $ready=$true; break }
        } catch {}
    }
    Assert $ready "Kestrel no responde en $tag."
    $script:handler=[System.Net.Http.HttpClientHandler]::new()
    $script:handler.AllowAutoRedirect=$false
    $script:handler.UseCookies=$true
    $script:handler.CookieContainer=[System.Net.CookieContainer]::new()
    $script:client=[System.Net.Http.HttpClient]::new($script:handler)
}
function Stop-App {
    if($null -ne $script:client) { $script:client.Dispose(); $script:client=$null }
    if($null -ne $script:handler) { $script:handler.Dispose(); $script:handler=$null }
    if($null -ne $script:server -and -not $script:server.HasExited) {
        Stop-Process -Id $script:server.Id -Force -ErrorAction SilentlyContinue
        $script:server.WaitForExit(5000) | Out-Null
    }
    $script:server=$null
    Start-Sleep -Milliseconds 600
}
function Get-Page([string]$url) {
    $response=$script:client.GetAsync("$base$url").GetAwaiter().GetResult()
    $body=$response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    return @{ Code=[int]$response.StatusCode; Text=$body; Location=($response.Headers.Location) }
}
function Token([string]$page) {
    $html=(Get-Page $page)
    Assert ($html.Code -eq 200) "No se obtuvo formulario $page."
    $hidden=[regex]::Match($html.Text,'<input\b(?=[^>]*\bname="__RequestVerificationToken")[^>]*>')
    Assert $hidden.Success "No hay token antiforgery en $page."
    $value=[regex]::Match($hidden.Value,'\bvalue="([^"]+)"')
    Assert $value.Success "No tiene valor el token en $page."
    return [System.Net.WebUtility]::HtmlDecode($value.Groups[1].Value)
}
function Send-Post([string]$page,[hashtable]$fields,[string]$antiToken="") {
    $values=[System.Collections.Generic.Dictionary[string,string]]::new()
    foreach($key in $fields.Keys) { $values.Add([string]$key,[string]$fields[$key]) }
    if($antiToken) { $values.Add("__RequestVerificationToken",$antiToken) }
    $content=[System.Net.Http.FormUrlEncodedContent]::new($values)
    $response=$script:client.PostAsync("$base$page",$content).GetAwaiter().GetResult()
    $body=$response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    $location=if($response.Headers.Location){$response.Headers.Location.ToString()}else{""}
    return @{ Code=[int]$response.StatusCode; Text=$body; Location=$location }
}
function Activate([string]$point) {
    $path=Join-Path $project "Controllers/ProductosController.cs"
    $sourceCode=Get-Content -Raw -Encoding utf8 $path
    $prefix=[regex]::Escape("PASO $point INICIO")
    $suffix=[regex]::Escape("PASO $point FIN")
    Assert (($sourceCode -match $prefix) -and ($sourceCode -match $suffix)) "Marcas incompletas $point"
    $sourceCode=[regex]::Replace($sourceCode,"(?m)^\s*/\*\s*$prefix\r?\n","")
    $sourceCode=[regex]::Replace($sourceCode,"(?m)^\s*$suffix\s*\*/","")
    [System.IO.File]::WriteAllText($path,$sourceCode,[System.Text.UTF8Encoding]::new($false))
}
function Activate-Index([string]$point) {
    $path=Join-Path $project "Views/Productos/Index.cshtml"
    $sourceCode=Get-Content -Raw -Encoding utf8 $path
    $start="@* PASO $point (ACTIVAR):"
    $i=$sourceCode.IndexOf($start)
    Assert ($i -ge 0) "Falta marcador de enlace $point"
    $end=$sourceCode.IndexOf("*@",$i)
    Assert ($end -gt $i) "Falta cierre de comentario para $point"
    $block=$sourceCode.Substring($i,($end+2)-$i)
    $link=[regex]::Match($block,'<a asp-action="[^"]+" asp-route-id="@producto.Id">[^<]+</a>')
    Assert $link.Success "Falta enlace dentro de $point"
    $sourceCode=$sourceCode.Replace($block,$link.Value)
    [System.IO.File]::WriteAllText($path,$sourceCode,[System.Text.UTF8Encoding]::new($false))
}
function Check-Redirect([hashtable]$response,[string]$operation) {
    Assert ($response.Code -eq 302) "$operation debería redirigir con 302 (obtenido $($response.Code))."
    Assert ([bool]$response.Location) "$operation no indicó Location."
}
try {
    Assert ([bool](Get-Command sqllocaldb -ErrorAction SilentlyContinue)) "La prueba requiere LocalDB en Windows."
    & sqllocaldb start MSSQLLocalDB | Out-Host
    Copy-Item -Path $source -Destination $project -Recurse
    foreach($name in @("bin","obj")) {
        $folder=Join-Path $project $name
        if(Test-Path $folder) { Remove-Item $folder -Recurse -Force }
    }

    # 2.4.1 y 2.4.2: lectura de registros reales de la base creada.
    Compile
    Start-App "lectura"
    $index=Get-Page "/Productos"
    Assert ($index.Code -eq 200 -and $index.Text.Contains("Cuaderno") -and $index.Text.Contains("Lápiz") -and $index.Text.Contains("Carpeta")) "La semilla inicial no aparece en SQL."
    $detail=Get-Page "/Productos/Detalle/2"
    Assert ($detail.Code -eq 200) "No existe detalle 2 en base recién sembrada."
    Assert ((Get-Page "/Productos/Detalle/999999").Code -eq 404) "Id ausente no devuelve 404."
    $early=Send-Post "/Productos/Crear" @{ Nombre="Rotulador"; Precio="7" }
    Assert ($early.Code -eq 400) "Sin token se debería rechazar la solicitud incluso antes de habilitar el POST."
    Stop-App

    # 2.4.3: creación activable y protección de entradas inválidas.
    Activate "2.4.3"
    Compile
    Start-App "crear"
    $token=Token "/Productos/Crear"
    $bad=Send-Post "/Productos/Crear" @{ Nombre="X"; Precio="7" } $token
    Assert ($bad.Code -eq 200 -and $bad.Text.Contains("entre 2 y 60 caracteres")) "Create inválido no devuelve el formulario."
    $created=Send-Post "/Productos/Crear" @{ Nombre="Rotulador"; Precio="7" } $token
    Check-Redirect $created "Crear"
    Assert ($created.Location -match 'Detalle/([0-9]+)') "No se redirigió al Id recién creado."
    $id=[int]$Matches[1]
    $createdDetail=Get-Page "/Productos/Detalle/$id"
    Assert ($createdDetail.Code -eq 200 -and $createdDetail.Text.Contains("Rotulador")) "Create no insertó producto."
    Stop-App

    # 2.4.4: edición del mismo Id, con errores de formulario preservados.
    Activate "2.4.4"
    Activate-Index "2.4.4"
    Compile
    Start-App "editar"
    $editGet=Get-Page "/Productos/Editar/$id"
    Assert ($editGet.Code -eq 200 -and $editGet.Text.Contains("Rotulador")) "Edit GET no recuperó la entidad."
    $token=Token "/Productos/Editar/$id"
    $bad=Send-Post "/Productos/Editar/$id" @{ Nombre="X"; Precio="8" } $token
    Assert ($bad.Code -eq 200 -and $bad.Text.Contains("entre 2 y 60 caracteres")) "Edit inválido no conserva el formulario."
    $edited=Send-Post "/Productos/Editar/$id" @{ Nombre="Rotulador azul"; Precio="8" } $token
    Check-Redirect $edited "Editar"
    $after=Get-Page "/Productos/Detalle/$id"
    Assert ($after.Code -eq 200 -and $after.Text.Contains("Rotulador azul")) "Edit no actualizó la entidad."
    Stop-App

    # 2.4.5: GET no borra, POST con token sí borra.
    Activate "2.4.5"
    Activate-Index "2.4.5"
    Compile
    Start-App "eliminar"
    $confirmation=Get-Page "/Productos/Eliminar/$id"
    Assert ($confirmation.Code -eq 200 -and $confirmation.Text.Contains("Rotulador azul")) "Delete GET no muestra confirmación."
    Assert ((Get-Page "/Productos/Detalle/$id").Code -eq 200) "Delete GET eliminó inesperadamente un producto."
    $forged=Send-Post "/Productos/Eliminar/$id" @{}
    Assert ($forged.Code -eq 400) "Delete POST sin token no se bloqueó."
    $token=Token "/Productos/Eliminar/$id"
    $deleted=Send-Post "/Productos/Eliminar/$id" @{} $token
    Check-Redirect $deleted "Eliminar"
    Assert ((Get-Page "/Productos/Detalle/$id").Code -eq 404) "La entidad eliminada aún existe."
    $token=Token "/Productos/Crear"
    $new=Send-Post "/Productos/Crear" @{ Nombre="Bloc de dibujo"; Precio="12" } $token
    Check-Redirect $new "Crear de persistencia"
    Assert ($new.Location -match 'Detalle/([0-9]+)') "Falta Id del producto nuevo."
    $persistentId=[int]$Matches[1]
    $token=Token "/Productos/Editar/$persistentId"
    $save=Send-Post "/Productos/Editar/$persistentId" @{ Nombre="Bloc de dibujo"; Precio="14" } $token
    Check-Redirect $save "Edición para persistencia"
    Stop-App

    # 2.4.6: el reinicio conserva tanto la edición como el borrado.
    Start-App "reinicio"
    $persisted=Get-Page "/Productos/Detalle/$persistentId"
    Assert ($persisted.Code -eq 200 -and $persisted.Text.Contains("Bloc de dibujo")) "El registro no sobrevive al reinicio."
    Assert ($persisted.Text.Contains("14")) "El precio editado no sobrevive al reinicio."
    Assert ((Get-Page "/Productos/Detalle/$id").Code -eq 404) "El producto borrado reapareció."
    $index=Get-Page "/Productos"
    Assert ($index.Code -eq 200) "No se puede consultar tras reiniciar."
    Write-Host "P2.4 E2E OK: semilla, Read, Create, ModelState, Edit, Delete, antiforgery, PRG y persistencia tras reinicio."
} finally {
    Stop-App
    if(Test-Path $tmp) { Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue }
    Remove-Item Env:ConnectionStrings__Productos -ErrorAction SilentlyContinue
}

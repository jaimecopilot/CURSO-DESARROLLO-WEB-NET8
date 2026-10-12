# Prueba interna P2.5: estados reales de Razor Pages y navegación con LocalDB aislada.
# No forma parte del material del alumno; los bloques se activan en copia temporal.
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$source = Join-Path $repo "M02_FORMULARIOS_RAZOR/PROYECTO/2.5/CursoWeb.Mvc"
$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ("P25_" + [guid]::NewGuid().ToString("N"))
$project = Join-Path $tempRoot "CursoWeb.Mvc"
$dbName = "CursoWebP25_" + [guid]::NewGuid().ToString("N").Substring(0, 15)
$env:ConnectionStrings__Productos = "Server=(localdb)\MSSQLLocalDB;Database=$dbName;Trusted_Connection=True;TrustServerCertificate=True"
$baseUrl = "http://127.0.0.1:5195"
$server = $null; $client = $null; $handler = $null
function Assert([bool]$check, [string]$message) { if (-not $check) { throw $message } }
function Build-Project {
  & dotnet build (Join-Path $project "CursoWeb.Mvc.csproj") -c Release --nologo
  Assert ($LASTEXITCODE -eq 0) "No compiló una evolución de P2.5."
}
function Start-Web([string]$label) {
  $script:server = Start-Process -FilePath "dotnet" -ArgumentList @("bin/Release/net8.0/CursoWeb.Mvc.dll", "--urls", $baseUrl) -WorkingDirectory $project -PassThru -NoNewWindow -RedirectStandardOutput (Join-Path $tempRoot "$label.out.log") -RedirectStandardError (Join-Path $tempRoot "$label.err.log")
  $ready = $false
  for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Milliseconds 800
    if ($script:server.HasExited) { break }
    try {
      $probe = [Net.Http.HttpClient]::new()
      $response = $probe.GetAsync("$baseUrl/Comparacion").GetAwaiter().GetResult()
      $probe.Dispose()
      if ([int]$response.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
  }
  if (-not $ready) {
    Get-Content -Raw -ErrorAction SilentlyContinue (Join-Path $tempRoot "$label.err.log") | Write-Host
    Get-Content -Raw -ErrorAction SilentlyContinue (Join-Path $tempRoot "$label.out.log") | Write-Host
    throw "No arranca P2.5 en el estado $label"
  }
  $script:handler = [Net.Http.HttpClientHandler]::new()
  $script:handler.AllowAutoRedirect = $false
  $script:handler.UseCookies = $true
  $script:handler.CookieContainer = [Net.CookieContainer]::new()
  $script:client = [Net.Http.HttpClient]::new($script:handler)
}
function Stop-Web {
  if ($null -ne $script:client) { $script:client.Dispose(); $script:client = $null }
  if ($null -ne $script:handler) { $script:handler.Dispose(); $script:handler = $null }
  if ($null -ne $script:server -and -not $script:server.HasExited) {
    Stop-Process -Id $script:server.Id -Force -ErrorAction SilentlyContinue
    $script:server.WaitForExit(5000) | Out-Null
  }
  $script:server = $null
  Start-Sleep -Milliseconds 500
}
function Get-Response([string]$url) {
  $response = $script:client.GetAsync("$baseUrl$url").GetAwaiter().GetResult()
  return @{ Code=[int]$response.StatusCode; Html=($response.Content.ReadAsStringAsync().GetAwaiter().GetResult()) }
}
function Get-Token {
  $page = Get-Response "/Comparacion"
  Assert ($page.Code -eq 200) "GET /Comparacion no respondió HTTP 200."
  $field = [regex]::Match($page.Html, '<input\b(?=[^>]*\bname="__RequestVerificationToken")[^>]*>')
  Assert $field.Success "La Razor Page no generó un token antiforgery."
  $value = [regex]::Match($field.Value, '\bvalue="([^"]+)"')
  Assert $value.Success "Token antiforgery sin valor."
  return [Net.WebUtility]::HtmlDecode($value.Groups[1].Value)
}
function Post-Form([string]$url, [string]$name, [string]$token="") {
  $data = [Collections.Generic.Dictionary[string,string]]::new()
  $data.Add("Nombre", $name)
  if ($token) { $data.Add("__RequestVerificationToken", $token) }
  $body = [Net.Http.FormUrlEncodedContent]::new($data)
  $response = $script:client.PostAsync("$baseUrl$url", $body).GetAwaiter().GetResult()
  $html = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
  return @{ Code=[int]$response.StatusCode; Html=[Net.WebUtility]::HtmlDecode($html) }
}
function Alter([string]$relative, [scriptblock]$fn) {
  $p = Join-Path $project $relative
  $code = [IO.File]::ReadAllText($p)
  $new = & $fn $code
  Assert ($new -ne $code) "No hay cambio en $relative."
  [IO.File]::WriteAllText($p, $new, [Text.UTF8Encoding]::new($false))
}
function Activate-Code([string]$start, [string]$finish) {
  Alter "Pages/Comparacion.cshtml.cs" {
    param($s)
    $s = $s.Replace("    /* $start" + [Environment]::NewLine, "")
    $s = $s.Replace("    $finish */", "")
    return $s
  }
}
try {
  Assert ([bool](Get-Command sqllocaldb -ErrorAction SilentlyContinue)) "La comprobación P2.5 necesita Windows con LocalDB."
  & sqllocaldb start MSSQLLocalDB | Out-Host
  New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
  Copy-Item -Path $source -Destination $project -Recurse
  Remove-Item (Join-Path $project "bin"), (Join-Path $project "obj") -Recurse -Force -ErrorAction SilentlyContinue

  # Estado inicial: coexistencia y GET activos; OnPost todavía no se ejecuta.
  Build-Project; Start-Web "get"
  $page = Get-Response "/Comparacion"
  Assert ($page.Html.Contains("OnGet prepara la página")) "El GET no ha ejecutado OnGet."
  $catalog = Get-Response "/Productos"
  Assert ($catalog.Code -eq 200) "Se rompió el listado MVC al registrar Razor Pages."
  $before = Get-Response "/Productos/Estado"
  Assert ($before.Code -eq 200 -and $before.Html.Contains("Catalogo MVC disponible")) "MVC no está disponible."
  $token = Get-Token
  $postBefore = Post-Form "/Comparacion" "Ana" $token
  Assert (-not $postBefore.Html.Contains("OnPost ha recibido: Ana")) "El estado inicial ejecuta inesperadamente OnPost."
  Stop-Web

  # Paso 2.5.3: activar el handler preparado.
  Activate-Code "PASO 2.5.3 INICIO" "PASO 2.5.3 FIN"
  Build-Project; Start-Web "post"
  $token = Get-Token
  $success = Post-Form "/Comparacion" "Ana" $token
  Assert ($success.Code -eq 200 -and $success.Html.Contains("OnPost ha recibido: Ana")) "El binder o OnPost no produjo el resultado."
  $forged = Post-Form "/Comparacion" "Ana"
  Assert ($forged.Code -eq 400) "Un POST sin token no se rechazó con HTTP 400."
  $empty = Post-Form "/Comparacion" "" $token
  Assert ($empty.Code -eq 200 -and $empty.Html.Contains("Introduce un nombre.")) "El nombre vacío no se rechazó."
  Stop-Web

  # Paso 2.5.4: activar exactamente las dos anotaciones de la práctica.
  Alter "Pages/Comparacion.cshtml.cs" {
    param($s)
    $s = $s.Replace("    // [Required(", "    [Required(")
    $s = $s.Replace("    // [StringLength(", "    [StringLength(")
    $s = $s.Replace("    //     ErrorMessage =", "        ErrorMessage =")
    return $s
  }
  Build-Project; Start-Web "validacion"
  $token = Get-Token
  $short = Post-Form "/Comparacion" "X" $token
  Assert ($short.Code -eq 200 -and $short.Html.Contains("El nombre debe tener entre 2 y 60 caracteres.")) "No se aplicó StringLength."
  $long = Post-Form "/Comparacion" ("A" * 61) $token
  Assert ($long.Code -eq 200 -and $long.Html.Contains("El nombre debe tener entre 2 y 60 caracteres.")) "No se rechazaron 61 caracteres."
  $valid = Post-Form "/Comparacion" "Marta" $token
  Assert ($valid.Code -eq 200 -and $valid.Html.Contains("OnPost ha recibido: Marta")) "La validación rechazó entrada correcta."
  Stop-Web

  # Pasos 2.5.5 y 2.5.6: menú, navegación y condición Razor.
  Alter "Views/Shared/_Layout.cshtml" {
    param($s)
    return $s.Replace('@* <a asp-page="/Comparacion">Comparar Razor Pages</a> *@', '<a asp-page="/Comparacion">Comparar Razor Pages</a>')
  }
  Alter "Pages/Comparacion.cshtml" {
    param($s)
    return $s.Replace('<p id="mensaje-page">@Model.Mensaje</p>', '<p id="mensaje-page">@Model.Mensaje</p>' + [Environment]::NewLine + '@if (Model.Mensaje.Length > 40) { <p id="respuesta-larga">La respuesta supera los 40 caracteres.</p> }')
  }
  Build-Project; Start-Web "navegacion"
  $catalog = Get-Response "/Productos"
  Assert ($catalog.Code -eq 200 -and $catalog.Html.Contains('href="/Comparacion"')) "No existe navegación MVC a Razor Pages."
  $page = Get-Response "/Comparacion"
  Assert ($page.Html.Contains('href="/Productos"') -or $page.Html.Contains('href="/Productos/Index"')) "No existe enlace de regreso a MVC."
  Assert (-not $page.Html.Contains('id="respuesta-larga"')) "La condición Razor se activa con un mensaje corto."
  $token=Get-Token
  $longName = "Nombre que provoca un mensaje de más de cuarenta caracteres"
  $longResult = Post-Form "/Comparacion" $longName $token
  Assert ($longResult.Html.Contains('id="respuesta-larga"')) "No se ejecuta condición Razor del paso 2.5.6."
  Stop-Web

  # Reto: un segundo handler real con el botón asp-page-handler.
  Activate-Code "RETO 2.5 INICIO" "RETO 2.5 FIN"
  Alter "Pages/Comparacion.cshtml" {
    param($s)
    return $s.Replace('@* <button type="submit" asp-page-handler="Mayusculas">Mostrar en mayúsculas</button> *@', '<button type="submit" asp-page-handler="Mayusculas">Mostrar en mayúsculas</button>')
  }
  Build-Project; Start-Web "reto"
  $page = Get-Response "/Comparacion"
  Assert ($page.Html.Contains("handler=Mayusculas")) "El botón no genera el destino al handler."
  $token=Get-Token
  $second=Post-Form "/Comparacion?handler=Mayusculas" "Ana" $token
  Assert ($second.Code -eq 200 -and $second.Html.Contains("Nombre en mayúsculas: ANA")) "El segundo handler no funciona."
  $invalid=Post-Form "/Comparacion?handler=Mayusculas" "X" $token
  Assert ($invalid.Code -eq 200 -and $invalid.Html.Contains("El nombre debe tener entre 2 y 60 caracteres.")) "El reto no hereda validación."
  $forged=Post-Form "/Comparacion?handler=Mayusculas" "Ana"
  Assert ($forged.Code -eq 400) "El segundo handler no protege antiforgery."
  $catalog = Get-Response "/Productos"
  Assert ($catalog.Code -eq 200 -and (-not $catalog.Html.Contains("Nombre en mayúsculas: ANA"))) "La página modificó el catálogo."
  Write-Host "P2.5 OK: 5 builds, GET y POST reales, antiforgery, validación, Razor, navegación, reto y catálogo conservado."
} finally {
  Stop-Web
  if (Test-Path $tempRoot) { Remove-Item $tempRoot -Recurse -Force -ErrorAction SilentlyContinue }
  Remove-Item Env:ConnectionStrings__Productos -ErrorAction SilentlyContinue
}

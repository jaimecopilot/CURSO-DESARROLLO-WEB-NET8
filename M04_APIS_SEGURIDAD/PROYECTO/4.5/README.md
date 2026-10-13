# P4.4.6 · ASP.NET Core Identity + JWT Bearer en .NET 8

**Ampliación autónoma** del M04. No sustituye los proyectos 4.1–4.4 ni añade
actividades al recorrido presencial obligatorio de 6 horas.

## Qué construye el alumno

Una Minimal API independiente que registra usuarios con `UserManager`,
verifica contraseñas con `SignInManager`, almacena cuentas y roles en SQLite
mediante `IdentityDbContext`, emite JWT firmados de 15 minutos y protege rutas
con `AddJwtBearer` y políticas de autorización.

El componente `/perfil-jwt` de
`PROYECTO/4.4/CursoWeb.Blazor/Components/Pages/PerfilJwt.razor`
es el cliente de ensayo.

## Iniciar en un entorno local controlado

En PowerShell:

```powershell
$env:ASPNETCORE_ENVIRONMENT = "Development"
$env:Jwt__SigningKey = [Convert]::ToBase64String(
  [System.Security.Cryptography.RandomNumberGenerator]::GetBytes(48))
dotnet run --project .\CursoWeb.IdentityJwtApi\CursoWeb.IdentityJwtApi.csproj --urls http://localhost:5086
```

Para probar una identidad con rol Formador, antes del arranque y en un entorno
de ensayo limpio, añadir `DemoFormador__Email` y
`DemoFormador__Password` con valores nuevos del docente. No guardarlos en Git.

Usar otra terminal para arrancar el host Blazor 4.4 y abrir
`http://localhost:5094/perfil-jwt`. El cliente tiene configurada una URL base
por defecto de `http://localhost:5086/`.

## Rutas

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | /auth/registro | Registro Identity, siempre rol Alumno |
| POST | /auth/login | Contraseña Identity y emisión JWT |
| GET | /api/identidad/yo | JWT válido obligatorio |
| GET | /api/identidad/formador | JWT válido más rol Formador |

El workflow `.github/workflows/m04-identity-jwt-ci.yml` ejecuta pruebas
HTTP reales (registro, 400, 401, 403, firma alterada y 200 con rol).

## Límites de seguridad

**Solo Development**. Se usa `EnsureCreatedAsync` para el esquema SQLite
de prácticas; en producción corresponden migraciones y una arquitectura de
identidad adecuada. La clave de firma se genera fuera del repositorio. Los JWT
no están cifrados, no se imprimen y no se almacenan en el navegador. La acción
de la página que olvida el token **no lo revoca**. No existen refresh tokens,
MFA, recuperación de cuenta ni proveedor OIDC.

**Importante:** los bearer tokens integrados de `MapIdentityApi` no tienen
por qué ser JWT. Este proyecto genera JWT explícitos y usa `JwtBearer` para
validarlos.

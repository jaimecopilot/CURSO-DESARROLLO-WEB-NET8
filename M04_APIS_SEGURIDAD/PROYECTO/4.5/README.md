# P4.4.6 · ASP.NET Core Identity + JWT Bearer en .NET 8

**Ampliación autónoma** del M04. No sustituye los proyectos 4.1–4.4 ni añade
actividades al recorrido presencial obligatorio de 6 horas.

## Qué construye el alumno

Una Minimal API independiente que registra usuarios con `UserManager`,
verifica contraseñas con `SignInManager`, almacena cuentas y roles en SQL Server Express LocalDB
mediante `IdentityDbContext`, emite JWT firmados de 15 minutos y protege rutas
con `AddJwtBearer` y políticas de autorización.

El componente `/perfil-jwt` de
`PROYECTO/4.4/CursoWeb.Blazor/Components/Pages/PerfilJwt.razor`
es el cliente de ensayo.

## Iniciar en un entorno local controlado

Requisito: **Windows con SQL Server Express LocalDB instalado desde Visual Studio**. Comprueba la instancia mediante `sqllocaldb info MSSQLLocalDB` o el Explorador de objetos de SQL Server de Visual Studio. La base `CursoWeb_M04_IdentityJwt` se crea en esa instancia con autenticación integrada de Windows, no en un fichero SQLite. Se puede cambiar `ConnectionStrings:IdentityDb` sin modificar código fuente.

En PowerShell:

```powershell
$env:ASPNETCORE_ENVIRONMENT = "Development"
$env:Jwt__SigningKey = [Convert]::ToBase64String(
  [System.Security.Cryptography.RandomNumberGenerator]::GetBytes(48))
dotnet run --project .\CursoWeb.IdentityJwtApi\CursoWeb.IdentityJwtApi.csproj --urls http://localhost:5086
```

La cadena de conexión de desarrollo usa `Server=(localdb)\\MSSQLLocalDB;Database=CursoWeb_M04_IdentityJwt;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=true` (en JSON la barra invertida se escribe doble). Abre Visual Studio > Explorador de objetos de SQL Server > `(localdb)\\MSSQLLocalDB` para consultar las tablas `AspNetUsers`, `AspNetRoles` y `AspNetUserRoles` después del primer arranque.

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

Comprueba desde una terminal las respuestas del servidor para registro, entrada inválida (400), acceso sin token (401), rol insuficiente (403), firma alterada (401) y rol autorizado (200). Sigue los pasos del cuaderno de prácticas para preparar las peticiones.

## Límites de seguridad

**Solo Development**. Se usa `EnsureCreatedAsync` para el esquema SQL Server Express LocalDB
de prácticas; en producción corresponden migraciones y una arquitectura de
identidad adecuada. La clave de firma se genera fuera del repositorio. Los JWT
no están cifrados, no se imprimen y no se almacenan en el navegador. La acción
de la página que olvida el token **no lo revoca**. No existen refresh tokens,
MFA, recuperación de cuenta ni proveedor OIDC.

**Importante:** los bearer tokens integrados de `MapIdentityApi` no tienen
por qué ser JWT. Este proyecto genera JWT explícitos y usa `JwtBearer` para
validarlos.

## Reiniciar el laboratorio

Para recomenzar desde cero, **detén la API** y elimina exclusivamente la base de prácticas `CursoWeb_M04_IdentityJwt` usando el Explorador de objetos SQL Server de Visual Studio o SSMS; no borres otras bases LocalDB. `EnsureCreatedAsync` permite iniciar el esquema docente, pero no reemplaza migraciones para cambios posteriores.

La ejecución del alumno requiere **Windows** con `MSSQLLocalDB`. SQL Server LocalDB no se sustituye por SQLite ni por InMemory.

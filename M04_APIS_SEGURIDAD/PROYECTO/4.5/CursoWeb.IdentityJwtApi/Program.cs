using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);

// P4.5.1: laboratorio local; no se abre en producción con credenciales de prueba.
if (!builder.Environment.IsDevelopment())
    throw new InvalidOperationException("La API Identity/JWT docente solo se ejecuta en Development.");

var firma = builder.Configuration["Jwt:SigningKey"]
    ?? throw new InvalidOperationException(
        "Define Jwt__SigningKey con un secreto aleatorio fuera del repositorio.");
var bytesFirma = Encoding.UTF8.GetBytes(firma);
if (bytesFirma.Length < 32)
    throw new InvalidOperationException("Jwt__SigningKey requiere al menos 32 bytes UTF-8.");

var emisor = builder.Configuration["Jwt:Issuer"]
    ?? throw new InvalidOperationException("Falta Jwt:Issuer.");
var audiencia = builder.Configuration["Jwt:Audience"]
    ?? throw new InvalidOperationException("Falta Jwt:Audience.");

// SQL Server Express LocalDB, instalado con Visual Studio en Windows.
// La cadena se lee de configuración; no se utiliza SQLite.
var conexion = builder.Configuration.GetConnectionString("IdentityDb")
    ?? throw new InvalidOperationException(
        "Configura ConnectionStrings:IdentityDb apuntando a SQL Server Express LocalDB.");

builder.Services.AddDbContext<IdentidadDbContext>(opciones =>
    opciones.UseSqlServer(conexion));

builder.Services.AddIdentityCore<IdentityUser>(opciones =>
{
    opciones.User.RequireUniqueEmail = true;
    opciones.Password.RequiredLength = 8;
    opciones.Password.RequireDigit = true;
    opciones.Password.RequireUppercase = true;
    opciones.Password.RequireLowercase = true;
    opciones.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    opciones.Lockout.MaxFailedAccessAttempts = 5;
    opciones.Lockout.AllowedForNewUsers = true;
})
.AddRoles<IdentityRole>()
.AddEntityFrameworkStores<IdentidadDbContext>()
.AddSignInManager()
.AddDefaultTokenProviders();

// P4.5.2: JWT de verdad, validando firma, emisor, audiencia y expiración.
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(opciones =>
    {
        opciones.MapInboundClaims = false;
        opciones.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = emisor,
            ValidateAudience = true,
            ValidAudience = audiencia,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(bytesFirma),
            ValidateLifetime = true,
            RequireExpirationTime = true,
            RequireSignedTokens = true,
            ClockSkew = TimeSpan.FromSeconds(5),
            NameClaimType = ClaimTypes.NameIdentifier,
            RoleClaimType = ClaimTypes.Role
        };
    });
builder.Services.AddAuthorization();

var app = builder.Build();

// P4.5.3: tablas reales de Identity en SQL Server Express LocalDB. EnsureCreated es SOLO docente.
using (var alcance = app.Services.CreateScope())
{
    var db = alcance.ServiceProvider.GetRequiredService<IdentidadDbContext>();
    await db.Database.EnsureCreatedAsync();

    var roles = alcance.ServiceProvider.GetRequiredService<RoleManager<IdentityRole>>();
    foreach (var nombre in new[] { "Alumno", "Formador" })
        if (!await roles.RoleExistsAsync(nombre))
            await roles.CreateAsync(new IdentityRole(nombre));

    // Cuenta docente opcional: email y clave SOLO de variables de entorno.
    var correoDocente = builder.Configuration["DemoFormador:Email"];
    var claveDocente = builder.Configuration["DemoFormador:Password"];
    if (!string.IsNullOrWhiteSpace(correoDocente) &&
        !string.IsNullOrWhiteSpace(claveDocente))
    {
        var usuarios = alcance.ServiceProvider.GetRequiredService<UserManager<IdentityUser>>();
        var existente = await usuarios.FindByEmailAsync(correoDocente);
        if (existente is null)
        {
            existente = new IdentityUser { UserName = correoDocente, Email = correoDocente };
            var creado = await usuarios.CreateAsync(existente, claveDocente);
            if (!creado.Succeeded)
                throw new InvalidOperationException("Cuenta docente inválida: " +
                    string.Join("; ", creado.Errors.Select(e => e.Description)));
        }
        else if (!await usuarios.IsInRoleAsync(existente, "Formador"))
        {
            // Nunca elevar a Formador una cuenta previamente registrada por el público.
            throw new InvalidOperationException(
                "El correo de Formador ya pertenece a otra cuenta. Usa una base de ensayo limpia.");
        }
        if (!await usuarios.IsInRoleAsync(existente, "Formador"))
        {
            var resultadoRol = await usuarios.AddToRoleAsync(existente, "Formador");
            if (!resultadoRol.Succeeded)
                throw new InvalidOperationException("No se pudo asignar Formador.");
        }
    }
}

app.UseAuthentication();
app.UseAuthorization();

app.MapGet("/", () => Results.Ok(new
{
    servicio = "M04 Identity + JWT (Development)",
    rutas = new[] { "/auth/registro", "/auth/login", "/api/identidad/yo",
                    "/api/identidad/formador" }
}));

// P4.5.4: Identity aplica hash de contraseñas; no las almacenamos manualmente.
app.MapPost("/auth/registro", async (RegistrarDto entrada,
    UserManager<IdentityUser> usuarios) =>
{
    if (string.IsNullOrWhiteSpace(entrada.Email) ||
        string.IsNullOrWhiteSpace(entrada.Password))
        return Results.BadRequest("Correo y contraseña obligatorios.");

    var nuevo = new IdentityUser
    {
        UserName = entrada.Email.Trim(),
        Email = entrada.Email.Trim()
    };
    var resultado = await usuarios.CreateAsync(nuevo, entrada.Password);
    if (!resultado.Succeeded)
        return Results.ValidationProblem(
            resultado.Errors.GroupBy(e => e.Code)
                .ToDictionary(g => g.Key, g => g.Select(e => e.Description).ToArray()));

    var asignacion = await usuarios.AddToRoleAsync(nuevo, "Alumno");
    if (!asignacion.Succeeded)
        return Results.Problem("No se pudo configurar el rol del usuario.");

    return Results.Created("/api/identidad/yo", new
    {
        id = nuevo.Id,
        email = nuevo.Email,
        rol = "Alumno"
    });
});

// P4.5.5: comprueba contraseñas y bloqueo mediante SignInManager.
app.MapPost("/auth/login", async (AccederDto entrada,
    UserManager<IdentityUser> usuarios,
    SignInManager<IdentityUser> acceso) =>
{
    var usuario = await usuarios.FindByEmailAsync(entrada.Email ?? "");
    if (usuario is null)
        return Results.Unauthorized();

    var resultado = await acceso.CheckPasswordSignInAsync(
        usuario, entrada.Password ?? "", lockoutOnFailure: true);
    if (!resultado.Succeeded)
        return Results.Unauthorized();

    var roles = await usuarios.GetRolesAsync(usuario);
    var ahora = DateTime.UtcNow;
    var caducidad = ahora.AddMinutes(15);
    var claims = new List<Claim>
    {
        new(JwtRegisteredClaimNames.Sub, usuario.Id),
        new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString("N")),
        new(JwtRegisteredClaimNames.Iat,
            DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString(),
            ClaimValueTypes.Integer64),
        new(ClaimTypes.NameIdentifier, usuario.Id),
        new(ClaimTypes.Email, usuario.Email ?? "")
    };
    claims.AddRange(roles.Select(rol => new Claim(ClaimTypes.Role, rol)));

    var token = new JwtSecurityToken(
        issuer: emisor,
        audience: audiencia,
        claims: claims,
        notBefore: ahora,
        expires: caducidad,
        signingCredentials: new SigningCredentials(
            new SymmetricSecurityKey(bytesFirma),
            SecurityAlgorithms.HmacSha256));

    return Results.Ok(new
    {
        accessToken = new JwtSecurityTokenHandler().WriteToken(token),
        tokenType = "Bearer",
        expiresAtUtc = caducidad
    });
});

// P4.5.6: sin Bearer válido devuelve 401.
app.MapGet("/api/identidad/yo", (ClaimsPrincipal principal) =>
    Results.Ok(new
    {
        id = principal.FindFirstValue(ClaimTypes.NameIdentifier),
        email = principal.FindFirstValue(ClaimTypes.Email),
        roles = principal.FindAll(ClaimTypes.Role).Select(c => c.Value).ToArray()
    }))
    .RequireAuthorization();

// P4.5.7: un token de Alumno es auténtico pero carece del rol => 403.
app.MapGet("/api/identidad/formador", () =>
    Results.Ok(new { mensaje = "Recurso reservado a Formador" }))
    .RequireAuthorization(p => p.RequireRole("Formador"));

app.Run();

record RegistrarDto(string Email, string Password);
record AccederDto(string Email, string Password);

sealed class IdentidadDbContext(DbContextOptions<IdentidadDbContext> opciones)
    : IdentityDbContext<IdentityUser>(opciones) { }
public partial class Program { }

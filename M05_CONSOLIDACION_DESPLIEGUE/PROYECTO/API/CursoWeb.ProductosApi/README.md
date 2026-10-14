# API de productos — consolidación P5.1 (.NET 8)

Ejecutar desde esta carpeta:

```powershell
dotnet run --urls http://localhost:5081
```

Esta es la API utilizada por la aplicación Blazor durante P5.1. Arráncala en una terminal y mantén ese proceso activo mientras abres el catálogo remoto de Blazor.

- GET `http://localhost:5081/api/productos`: respuesta 200 y lista JSON.
- GET `http://localhost:5081/api/productos/999`: respuesta 404.
- POST `http://localhost:5081/api/productos` con `{"nombre":"Regla","precio":1.75}`: respuesta 201.
- POST con nombre vacío o precio cero: respuesta 400.

Los datos permanecen en memoria y vuelven a los dos productos iniciales cuando reinicias el servidor. El CRUD de MVC con SQL Server Express LocalDB es un proyecto distinto.

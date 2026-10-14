# API de productos — práctica P4.3 (.NET 8)

Ejecutar desde esta carpeta:

```powershell
dotnet run --urls http://localhost:5081
```

Esta carpeta sirve para estudiar el contrato de productos y comparar los endpoints con la API que construirás paso a paso en P4.3. Sigue la práctica para saber qué bloques modificar o activar.

- GET `http://localhost:5081/api/productos`: respuesta 200 y lista JSON.
- GET `http://localhost:5081/api/productos/999`: respuesta 404.
- POST `http://localhost:5081/api/productos` con `{"nombre":"Regla","precio":1.75}`: respuesta 201.
- POST con nombre vacío o precio cero: respuesta 400.

Los datos permanecen en memoria y se reinician al volver a arrancar la API. La práctica no requiere SQL Server ni autenticación para estos endpoints.

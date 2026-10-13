# API auxiliar para P4.1 (NET 8)

Ejecutar desde esta carpeta:

```powershell
dotnet run --urls http://localhost:5081
```

Esta API de laboratorio está disponible **antes** de empezar P4.1; se estudia en detalle y se modifica en P4.3.

- GET `http://localhost:5081/api/productos`: 200 y lista JSON.
- GET `http://localhost:5081/api/productos/999`: 404.
- POST `http://localhost:5081/api/productos` con JSON `{"nombre":"Regla","precio":1.75}`: 201.
- POST sin nombre o con precio cero: 400.

Los datos son de memoria: reiniciar la API restaura los dos productos iniciales. No se utiliza base de datos ni autenticación en P4.1.

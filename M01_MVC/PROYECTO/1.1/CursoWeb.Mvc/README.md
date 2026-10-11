# Proyecto ejecutable del punto 1.1

Este es el estado inicial de la aplicación MVC A. Evolucionará durante M01 y M02. No requiere base de datos ni paquetes NuGet externos.

## Ejecutar

Desde esta carpeta:

~~~bash
dotnet restore
dotnet run --no-launch-profile --urls http://localhost:5091
~~~

Abrir http://localhost:5091. Detener con Ctrl+C.

## Activar bloques

- Paso 1.1.4 en Controllers/HomeController.cs: descomentar solo la línea que asigna la cabecera X-Curso-Paso.
- Paso 1.1.5 en Views/Home/Index.cshtml: quitar los dos delimitadores que envuelven el comentario Razor 1.1.5; mantener el HTML interior.
- Guardar y actualizar el navegador. Ambos pasos se pueden activar a la vez.
- **RETO 1.1:** en `Controllers/HomeController.cs` descomentar la asignación `X-Curso-Reto`. En `Views/Home/Index.cshtml` retirar los delimitadores del comentario `RETO 1.1` para hacer visible el párrafo `reto-1-1`. El reto dispone de código completo y explicación en P1.1, apartado G.

Las explicaciones y el recorrido completo se encuentran en la sección 1.1 de ../../../PRACTICAS/M01_PRACTICAS.md (subir tres niveles desde este directorio).

## Verificación automatizada

Desde la raíz del repositorio:

~~~bash
bash M01_MVC/TESTS/1.1_e2e.sh
~~~

El script compila y ejecuta HTTP real sobre Kestrel; verifica la vista, el layout, códigos 200 y 404 y los fragmentos y el reto activados en una copia temporal del proyecto. Requiere .NET SDK 8, Bash, Python 3 y curl. GitHub Actions permite ejecutar la prueba en una máquina con .NET 8.

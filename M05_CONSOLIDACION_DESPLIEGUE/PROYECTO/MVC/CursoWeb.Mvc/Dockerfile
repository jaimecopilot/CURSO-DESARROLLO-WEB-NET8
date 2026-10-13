# P5.5: imagen didáctica de la MISMA aplicación MVC A (P2.5).
# Construir desde la carpeta del proyecto MVC: docker build -t cursoweb-mvc:m05 .
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS compilacion
WORKDIR /src
COPY . .
RUN dotnet restore CursoWeb.Mvc.csproj
RUN dotnet publish CursoWeb.Mvc.csproj -c Release --no-restore -o /app/publicada

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS ejecucion
WORKDIR /app
COPY --from=compilacion /app/publicada .
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
# El contenedor NO configura ni instala SQL Server/LocalDB.
# Al ejecutar, añadir -e Despliegue__SinLocalDb=true.
ENTRYPOINT ["dotnet", "CursoWeb.Mvc.dll"]

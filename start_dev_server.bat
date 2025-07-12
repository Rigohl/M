@echo off
echo Buscando procesos en el puerto 9002...
FOR /F "tokens=5" %%i IN ('netstat -ano ^| findstr :9002') DO (
    SET PID=%%i
)

IF DEFINED PID (
    echo Se encontro un proceso en el puerto 9002 (PID: %PID%). Intentando terminarlo...
    taskkill /PID %PID% /F
    IF %ERRORLEVEL% NEQ 0 (
        echo Error al terminar el proceso. Es posible que necesites ejecutar este archivo como Administrador.
    ) ELSE (
        echo Proceso terminado exitosamente.
    )
) ELSE (
    echo No se encontraron procesos en el puerto 9002.
)

echo.
echo Iniciando el servidor de desarrollo de Next.js...
npm run dev

echo.
echo La pagina deberia estar disponible en http://localhost:9002
echo Presiona cualquier tecla para cerrar esta ventana.
pause > NUL
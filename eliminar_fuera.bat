@echo off
REM Eliminar carpetas y archivos duplicados fuera de mi-web-cancion
cd /d "%~dp0src"

REM Eliminar componentes duplicados
rd /s /q components
rd /s /q hooks
rd /s /q lib
rd /s /q config

cd ..
REM Eliminar src si ya no tiene nada útil
if exist src rmdir /s /q src

echo Limpieza completada.
pause

@echo off
REM Mover archivos de la subcarpeta interna a la principal y eliminar la subcarpeta

setlocal
set "SRC=%~dp0mi-web-cancion\mi-web-cancion"
set "DST=%~dp0mi-web-cancion"

REM Mover todos los archivos (no carpetas) y sobrescribir
for %%F in ("%SRC%\*") do (
    if not "%%~aF"=="d" move /Y "%%F" "%DST%"
)

REM Eliminar la subcarpeta interna si está vacía
rd /S /Q "%SRC%"

echo Proceso completado.
pause

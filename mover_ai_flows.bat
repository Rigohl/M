@echo off
REM Copiar archivos de src/ai/flows a mi-web-cancion/src/ai/flows y luego eliminar src/ai
set SRC=%~dp0src\ai\flows
set DST=%~dp0mi-web-cancion\src\ai\flows
if not exist "%DST%" mkdir "%DST%"
copy /Y "%SRC%\*.*" "%DST%\"
rd /s /q "%~dp0src\ai"
echo Flows movidos y src/ai eliminado.
pause

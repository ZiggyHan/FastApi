@echo off
REM Cargar variables de entorno desde .env
for /f "usebackq tokens=1,* delims==" %%A in (".env") do set %%A=%%B

REM Ejecutar el script
poetry run python main.py
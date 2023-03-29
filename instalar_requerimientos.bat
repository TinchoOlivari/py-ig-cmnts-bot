@ECHO OFF
:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

pip install -r requirements.txt

goto:eof
:errorNoPython

echo.
echo Error^: Python NO esta instalado! 
echo Descargar de: https://www.python.org/downloads/

PAUSE
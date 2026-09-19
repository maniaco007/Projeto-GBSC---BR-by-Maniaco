@echo off
rem Gera o GBSC-Updater.exe (precisa de Python 3 e: pip install pyinstaller esptool)
python -m PyInstaller --onefile --windowed --name GBSC-Updater --add-data "firmware;firmware" --collect-all esptool --collect-all serial gbsc_updater.py
echo.
echo Pronto: dist\GBSC-Updater.exe
pause

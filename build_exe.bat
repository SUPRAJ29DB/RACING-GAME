@echo off
setlocal
cd /d "%~dp0"
echo ============================================
echo       NEON RUSH - WINDOWS EXE BUILDER
echo ============================================
py -m pip install --upgrade pip
if errorlevel 1 goto error
py -m pip install -r requirements.txt
if errorlevel 1 goto error
py -m PyInstaller --noconfirm --clean --onefile --windowed --name NeonRush game.py
if errorlevel 1 goto error
echo.
echo Build complete! Your game is here:
echo %CD%\dist\NeonRush.exe
pause
exit /b 0
:error
echo.
echo Build failed. Check the error messages above.
pause
exit /b 1

@echo off
echo ========================================
echo    VEDA AI - EXE Builder with Logo
echo ========================================
echo.

echo Step 1: Converting logo to ICO format...
python convert_logo_to_ico.py
if errorlevel 1 (
    echo Error: Logo conversion failed!
    pause
    exit /b 1
)
echo.

echo Step 2: Installing PyInstaller...
pip install pyinstaller pillow
echo.

echo Step 3: Building EXE with VEDA logo...
pyinstaller --onefile ^
    --windowed ^
    --icon=veda-icon.ico ^
    --name="VEDA_AI" ^
    --add-data "python_frontend;python_frontend" ^
    --add-data "data;data" ^
    --add-data "python_backend;python_backend" ^
    --hidden-import=pyttsx3 ^
    --hidden-import=speech_recognition ^
    --hidden-import=fastapi ^
    --hidden-import=uvicorn ^
    run_veda_ai.py

if errorlevel 1 (
    echo Error: Build failed!
    pause
    exit /b 1
)
echo.

echo Step 4: Cleaning up build files...
rmdir /s /q build
del VEDA_AI.spec
echo.

echo ========================================
echo    Build Complete! 
echo ========================================
echo.
echo Your EXE file with VEDA logo:
echo    dist\VEDA_AI.exe
echo.
echo File size:
dir dist\VEDA_AI.exe | find "VEDA_AI.exe"
echo.
echo Test karne ke liye:
echo    cd dist
echo    VEDA_AI.exe
echo.
pause

@echo off
echo ========================================
echo    VEDA AI v5.0 - Launcher
echo ========================================
echo.

REM Kill any existing Python processes
echo Stopping any existing VEDA instances...
taskkill /F /IM python.exe >nul 2>&1

echo.
echo Starting VEDA AI...
echo.

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python run_veda_ai.py

pause

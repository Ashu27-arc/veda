@echo off
title VEDA AI v5.0
color 0A
echo ========================================
echo    VEDA AI v5.0 - Launcher
echo ========================================
echo.

REM Kill any existing Python processes running VEDA
echo [*] Stopping any existing VEDA instances...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 1 /nobreak >nul

echo.
echo [*] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run these commands first:
    echo   1. python -m venv venv
    echo   2. venv\Scripts\activate.bat
    echo   3. pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if uvicorn is installed
echo [*] Checking dependencies...
python -c "import uvicorn, fastapi, requests" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies missing!
    echo Installing required packages...
    pip install -q fastapi uvicorn requests websockets
)

echo.
echo ========================================
echo    Starting VEDA AI...
echo    Browser will open automatically!
echo ========================================
echo.

REM Run VEDA AI
python run_veda_ai.py

echo.
echo ========================================
echo    VEDA AI has stopped
echo ========================================
pause

@echo off
title VEDA AI - Starting...
color 0A
echo.
echo ========================================
echo    VEDA AI v5.0 - Smart Launcher
echo ========================================
echo.

REM Check if already running
echo [1/5] Checking for existing instances...
netstat -ano | findstr ":8000" >nul
if %errorlevel% equ 0 (
    echo WARNING: Port 8000 is already in use!
    echo VEDA AI might already be running.
    echo.
    choice /C YN /M "Do you want to stop existing instance and restart"
    if errorlevel 2 goto :skip_kill
    
    echo Stopping existing instance...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)
:skip_kill

REM Check virtual environment
echo.
echo [2/5] Checking virtual environment...
if not exist "venv\Scripts\python.exe" (
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

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check dependencies
echo [4/5] Checking dependencies...
python -c "import fastapi, uvicorn, requests" 2>nul
if errorlevel 1 (
    echo WARNING: Some dependencies are missing!
    echo Installing/updating dependencies...
    pip install -q fastapi uvicorn requests websockets
)

REM Start VEDA AI
echo.
echo [5/5] Starting VEDA AI...
echo.
echo ========================================
echo    VEDA AI is starting...
echo    Browser will open automatically
echo    when server is ready!
echo ========================================
echo.

python run_veda_ai.py

REM If script exits, show error
echo.
echo ========================================
echo    VEDA AI has stopped
echo ========================================
pause

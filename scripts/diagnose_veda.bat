@echo off
title VEDA AI - Diagnostics
color 0E
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           VEDA AI - System Diagnostics                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/8] Checking Python installation...
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python is NOT installed or not in PATH
    echo    Please install Python 3.8 or higher
    goto :end
) else (
    echo ✅ Python is installed
)

echo.
echo [2/8] Checking virtual environment...
if exist "venv\Scripts\python.exe" (
    echo ✅ Virtual environment exists
) else (
    echo ❌ Virtual environment NOT found
    echo    Run: python -m venv venv
    goto :end
)

echo.
echo [3/8] Checking port 8000 availability...
netstat -ano | findstr ":8000" >nul
if errorlevel 1 (
    echo ✅ Port 8000 is available
) else (
    echo ⚠️  Port 8000 is in use
    echo    VEDA AI might already be running
    echo    Or another application is using this port
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
        echo    Process ID: %%a
    )
)

echo.
echo [4/8] Checking required files...
set missing=0
if exist "run_veda_ai.py" (
    echo ✅ run_veda_ai.py found
) else (
    echo ❌ run_veda_ai.py NOT found
    set missing=1
)

if exist "python_backend\main.py" (
    echo ✅ python_backend\main.py found
) else (
    echo ❌ python_backend\main.py NOT found
    set missing=1
)

if exist "python_frontend\index.html" (
    echo ✅ python_frontend\index.html found
) else (
    echo ❌ python_frontend\index.html NOT found
    set missing=1
)

if exist "requirements.txt" (
    echo ✅ requirements.txt found
) else (
    echo ❌ requirements.txt NOT found
    set missing=1
)

if %missing%==1 (
    echo.
    echo ⚠️  Some required files are missing!
    goto :end
)

echo.
echo [5/8] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    goto :end
) else (
    echo ✅ Virtual environment activated
)

echo.
echo [6/8] Checking Python packages...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo ❌ fastapi not installed
    set missing=1
) else (
    echo ✅ fastapi installed
)

python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo ❌ uvicorn not installed
    set missing=1
) else (
    echo ✅ uvicorn installed
)

python -c "import requests" 2>nul
if errorlevel 1 (
    echo ❌ requests not installed
    set missing=1
) else (
    echo ✅ requests installed
)

python -c "import websockets" 2>nul
if errorlevel 1 (
    echo ❌ websockets not installed
    set missing=1
) else (
    echo ✅ websockets installed
)

if %missing%==1 (
    echo.
    echo ⚠️  Some packages are missing!
    echo    Run: pip install -r requirements.txt
    goto :end
)

echo.
echo [7/8] Checking log files...
if exist "logs\veda_ai.log" (
    echo ✅ Log file exists
    echo    Last 5 lines:
    echo    ─────────────────────────────────────────
    powershell -Command "Get-Content logs\veda_ai.log -Tail 5"
    echo    ─────────────────────────────────────────
) else (
    echo ⚠️  Log file not found (will be created on first run)
)

echo.
echo [8/8] Testing server connectivity...
echo    Attempting to connect to http://localhost:8000...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Server is not running
    echo    This is normal if you haven't started VEDA AI yet
) else (
    echo ✅ Server is running and responding!
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    Diagnostics Complete                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:end
echo.
echo Press any key to exit...
pause >nul

@echo off
title VEDA AI - Browser Launcher
color 0B
echo.
echo ========================================
echo    Opening VEDA AI in Browser...
echo ========================================
echo.

REM Check if server is running
echo [*] Checking if VEDA AI server is running...
netstat -ano | findstr ":8000" >nul
if errorlevel 1 (
    echo.
    echo ERROR: VEDA AI server is not running!
    echo.
    echo Please start VEDA AI first:
    echo   - Run: start_veda.bat
    echo   - OR: start_veda_fixed.bat
    echo.
    pause
    exit /b 1
)

echo [*] Server is running!
echo [*] Opening browser...
echo.

REM Wait a moment
timeout /t 1 /nobreak >nul

REM Open browser
start http://localhost:8000

echo.
echo ========================================
echo    Browser opened successfully!
echo ========================================
echo.
echo If page doesn't load:
echo   1. Wait 5 seconds and refresh (F5)
echo   2. Check if server is running
echo   3. Manually visit: http://localhost:8000
echo.
pause

@echo off
title VEDA AI - Open Browser
color 0B

echo.
echo ========================================
echo    Opening VEDA AI in Browser
echo ========================================
echo.

REM Check if server is running
netstat -ano | findstr ":8000" >nul
if errorlevel 1 (
    echo ❌ VEDA AI server is not running!
    echo.
    echo Please start VEDA AI first:
    echo   - Run: start_veda.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Server is running!
echo 🌐 Opening browser...
echo.

REM Wait a moment
timeout /t 1 /nobreak >nul

REM Open browser - this is the most reliable method on Windows
start http://localhost:8000

echo.
echo ✅ Browser opened!
echo.
echo If page doesn't load:
echo   1. Wait 2-3 seconds and refresh (F5)
echo   2. Check if server is running
echo   3. Try: python open_browser.py
echo.
timeout /t 3 /nobreak >nul

@echo off
echo Opening VEDA AI in browser...
timeout /t 2 /nobreak >nul
start http://localhost:8000
echo.
echo Browser opened!
echo If VEDA AI is not running, run: start_veda.bat
pause

@echo off
title VEDA AI - Fix Verification
color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         VEDA AI - Browser Fix Verification                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo Checking if all fix files are present...
echo.

set missing=0

echo [1/7] Checking new launcher...
if exist "start_veda_fixed.bat" (
    echo ✅ start_veda_fixed.bat found
) else (
    echo ❌ start_veda_fixed.bat NOT found
    set missing=1
)

echo [2/7] Checking diagnostics tool...
if exist "diagnose_veda.bat" (
    echo ✅ diagnose_veda.bat found
) else (
    echo ❌ diagnose_veda.bat NOT found
    set missing=1
)

echo [3/7] Checking updated run script...
if exist "run_veda_ai.py" (
    findstr /C:"wait_for_server" run_veda_ai.py >nul
    if errorlevel 1 (
        echo ❌ run_veda_ai.py not updated (missing wait_for_server)
        set missing=1
    ) else (
        echo ✅ run_veda_ai.py updated with health check
    )
) else (
    echo ❌ run_veda_ai.py NOT found
    set missing=1
)

echo [4/7] Checking documentation...
if exist "BROWSER_FIX_GUIDE.md" (
    echo ✅ BROWSER_FIX_GUIDE.md found
) else (
    echo ❌ BROWSER_FIX_GUIDE.md NOT found
    set missing=1
)

if exist "BROWSER_ISSUE_FIXED.md" (
    echo ✅ BROWSER_ISSUE_FIXED.md found
) else (
    echo ❌ BROWSER_ISSUE_FIXED.md NOT found
    set missing=1
)

echo [5/7] Checking quick reference...
if exist "START_HERE.txt" (
    echo ✅ START_HERE.txt found
) else (
    echo ❌ START_HERE.txt NOT found
    set missing=1
)

echo [6/7] Checking changelog...
if exist "WHATS_NEW_BROWSER_FIX.md" (
    echo ✅ WHATS_NEW_BROWSER_FIX.md found
) else (
    echo ❌ WHATS_NEW_BROWSER_FIX.md NOT found
    set missing=1
)

echo [7/7] Checking summary...
if exist "FIXED_SUMMARY.txt" (
    echo ✅ FIXED_SUMMARY.txt found
) else (
    echo ❌ FIXED_SUMMARY.txt NOT found
    set missing=1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.

if %missing%==0 (
    echo ✅✅✅ ALL FIX FILES PRESENT! ✅✅✅
    echo.
    echo Browser fix has been successfully applied!
    echo.
    echo Next steps:
    echo   1. Run: start_veda_fixed.bat
    echo   2. Wait for "Server is ready!" message
    echo   3. Browser will open automatically
    echo.
    echo For help, read:
    echo   - START_HERE.txt (Quick reference)
    echo   - BROWSER_ISSUE_FIXED.md (Hindi guide)
    echo   - BROWSER_FIX_GUIDE.md (English guide)
) else (
    echo ❌ SOME FILES ARE MISSING!
    echo.
    echo Please ensure all fix files are present.
    echo Re-run the fix process if needed.
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause

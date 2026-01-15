@echo off
echo ========================================
echo    VEDA AI - Quick Install
echo ========================================
echo.

REM Create installation directory
if not exist "C:\Program Files\VEDA AI" mkdir "C:\Program Files\VEDA AI"

REM Copy files
echo Copying VEDA AI files...
xcopy /E /I /Y "dist\VEDA_AI.exe" "C:\Program Files\VEDA AI\"
xcopy /E /I /Y "python_frontend" "C:\Program Files\VEDA AI\python_frontend\"
xcopy /E /I /Y "data" "C:\Program Files\VEDA AI\data\"
xcopy /E /I /Y "python_backend" "C:\Program Files\VEDA AI\python_backend\"
copy /Y ".env" "C:\Program Files\VEDA AI\"
copy /Y "veda-icon.ico" "C:\Program Files\VEDA AI\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\VEDA AI.lnk');$s.TargetPath='C:\Program Files\VEDA AI\VEDA_AI.exe';$s.IconLocation='C:\Program Files\VEDA AI\veda-icon.ico';$s.Save()"

REM Create start menu shortcut
echo Creating start menu shortcut...
if not exist "%appdata%\Microsoft\Windows\Start Menu\Programs\VEDA AI" mkdir "%appdata%\Microsoft\Windows\Start Menu\Programs\VEDA AI"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%appdata%\Microsoft\Windows\Start Menu\Programs\VEDA AI\VEDA AI.lnk');$s.TargetPath='C:\Program Files\VEDA AI\VEDA_AI.exe';$s.IconLocation='C:\Program Files\VEDA AI\veda-icon.ico';$s.Save()"

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo VEDA AI has been installed to:
echo C:\Program Files\VEDA AI
echo.
echo Shortcuts created on:
echo - Desktop
echo - Start Menu
echo.
echo Run VEDA AI from Desktop or Start Menu!
echo.
pause

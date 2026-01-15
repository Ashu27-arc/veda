@echo off
echo ========================================
echo VEDA AI - Microphone Calibration
echo ========================================
echo.
echo Yeh script aapke microphone ko calibrate karega
echo Calibration ke time chup raho (2 seconds)
echo.
pause

python scripts/calibrate_voice.py

echo.
echo ========================================
echo Calibration complete!
echo Ab VEDA start karo aur bolo!
echo ========================================
pause

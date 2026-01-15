@echo off
echo ========================================
echo VEDA AI - Microphone Test
echo ========================================
echo.
echo Yeh script aapke microphone ko test karega
echo Jab bole "Speak now", tab kuch bolo
echo.
pause

python -c "from python_backend.voice_advanced import test_voice_recognition; test_voice_recognition()"

echo.
pause

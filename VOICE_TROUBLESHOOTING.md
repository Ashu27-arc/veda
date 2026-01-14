# 🎤 VEDA AI - Voice Recognition Troubleshooting Guide

## Quick Fix (1 Minute)

```bash
# Run this command to automatically fix most issues
python fix_microphone.py
```

This will automatically:
- ✅ Detect your microphone
- ✅ Test access permissions
- ✅ Calibrate for your environment
- ✅ Test voice recognition
- ✅ Save optimal settings

---

## Common Issues & Solutions

### ❌ Issue 1: "No voice detected"

**Symptoms:**
- Clicking "Speak" button shows error
- "No voice detected" message appears
- Microphone not responding

**Solutions:**

1. **Run Diagnostic Test**
   ```bash
   python test_microphone.py
   ```
   This will tell you exactly what's wrong.

2. **Check Microphone Connection**
   - Ensure microphone is plugged in
   - Try a different USB port
   - Check if microphone LED is on (if applicable)

3. **Enable Microphone Permissions**
   - Press `Win + I` to open Settings
   - Go to **Privacy > Microphone**
   - Enable "Allow apps to access your microphone"
   - Enable "Allow desktop apps to access your microphone"
   - Scroll down and ensure Python is allowed

4. **Test in Windows Settings**
   - Press `Win + I` > **System > Sound**
   - Under "Input", select your microphone
   - Click "Test your microphone" and speak
   - If bar doesn't move, microphone isn't working

---

### ❌ Issue 2: "Could not understand audio"

**Symptoms:**
- Microphone works but VEDA can't understand
- "Could not understand audio" error
- Recognition fails repeatedly

**Solutions:**

1. **Calibrate Voice**
   ```bash
   python calibrate_voice.py
   ```
   OR click "🎯 Calibrate Voice" button in UI

2. **Improve Audio Quality**
   - Speak louder and clearer
   - Reduce background noise
   - Close windows, turn off fans
   - Move away from noisy areas

3. **Adjust Microphone Volume**
   - Right-click speaker icon in taskbar
   - Select "Sounds" > "Recording" tab
   - Double-click your microphone
   - Set "Levels" to 80-100%
   - Enable "Microphone Boost" if available

4. **Position Microphone Correctly**
   - Keep 6-12 inches from mouth
   - Point microphone at your mouth
   - Don't cover microphone with hand

---

### ❌ Issue 3: "Speech recognition service error"

**Symptoms:**
- "RequestError" or "Service error"
- Internet connection error
- API timeout

**Solutions:**

1. **Check Internet Connection**
   ```bash
   ping google.com
   ```
   If this fails, fix your internet first.

2. **Try Again**
   - Google Speech API might be temporarily down
   - Wait 30 seconds and try again

3. **Use Different Network**
   - Switch from WiFi to mobile hotspot
   - Check if firewall is blocking

---

### ❌ Issue 4: "Microphone access error"

**Symptoms:**
- "OSError" or "Cannot access microphone"
- Permission denied error
- Microphone in use by another app

**Solutions:**

1. **Close Other Apps**
   - Close Zoom, Teams, Discord, Skype
   - Close any video recording software
   - Close browser tabs using microphone

2. **Restart Audio Service**
   ```bash
   # Run as Administrator
   net stop audiosrv
   net start audiosrv
   ```

3. **Restart Computer**
   - Sometimes Windows audio service gets stuck
   - A restart usually fixes it

---

### ❌ Issue 5: Low Accuracy (Below 70%)

**Symptoms:**
- VEDA understands sometimes but not always
- Accuracy is inconsistent
- Wrong words recognized

**Solutions:**

1. **Calibrate in Your Environment**
   ```bash
   python fix_microphone.py
   ```
   Calibration adapts to your room's noise level.

2. **Improve Environment**
   - Close windows (reduce outside noise)
   - Turn off fans, AC
   - Use in quiet room
   - Avoid echo-prone rooms

3. **Speak Clearly**
   - Speak at normal pace (not too fast/slow)
   - Pronounce words clearly
   - Use simple commands first
   - Avoid mumbling

4. **Use Better Microphone**
   - Built-in laptop mics are often poor quality
   - Use external USB microphone
   - Use headset with boom mic
   - Gaming headsets work great

---

## Step-by-Step Diagnostic Process

### Step 1: Test Microphone Hardware
```bash
python test_microphone.py
```

**Expected Output:**
```
✅ Found 1 microphone(s)
✅ Microphone is accessible
✅ Energy threshold set to 4000
✅ Audio captured successfully
✅ Recognized: 'hello veda'
```

**If any test fails**, follow the error message instructions.

---

### Step 2: Fix & Calibrate
```bash
python fix_microphone.py
```

**Expected Output:**
```
✅ Found 1 microphone(s)
✅ Microphone is accessible
✅ Calibration complete!
✅ Audio recorded successfully!
✅ Recognized: 'hello veda'
🎉 SUCCESS! Your microphone is working perfectly!
```

---

### Step 3: Test in VEDA AI

1. Start VEDA AI:
   ```bash
   python run_veda_ai.py
   ```

2. Click "🎯 Calibrate Voice" button

3. Click "🎤 Speak" button

4. Say: "Hello VEDA"

5. Should see: "✅ You said: 'hello veda'"

---

## Advanced Troubleshooting

### Check Microphone in Device Manager

1. Press `Win + X` > Device Manager
2. Expand "Audio inputs and outputs"
3. Look for your microphone
4. If yellow warning icon:
   - Right-click > Update driver
   - Right-click > Uninstall device
   - Restart computer (Windows will reinstall)

### Check Windows Audio Service

1. Press `Win + R`
2. Type: `services.msc`
3. Find "Windows Audio"
4. Ensure Status is "Running"
5. If not, right-click > Start

### Reinstall Audio Drivers

1. Go to your PC manufacturer's website
2. Download latest audio drivers
3. Install and restart

### Check for Windows Updates

1. Press `Win + I` > Update & Security
2. Click "Check for updates"
3. Install all updates
4. Restart computer

---

## Microphone Recommendations

### Budget Options ($10-30)
- **Zalman ZM-Mic1** - Clip-on mic
- **Fifine K669B** - USB desktop mic
- **Any gaming headset** - Usually good quality

### Mid-Range ($30-80)
- **Blue Snowball** - Professional USB mic
- **HyperX Cloud II** - Gaming headset
- **Audio-Technica ATR2100x** - Dynamic mic

### Professional ($80+)
- **Blue Yeti** - Studio quality
- **Rode NT-USB** - Broadcast quality
- **Shure SM7B** - Professional studio

---

## Tips for Best Voice Recognition

### ✅ DO:
- Speak at normal conversational pace
- Use simple, clear commands
- Calibrate in the room you'll use VEDA
- Keep microphone 6-12 inches away
- Use in quiet environment
- Speak directly at microphone
- Use external microphone if possible

### ❌ DON'T:
- Don't speak too fast or too slow
- Don't whisper or shout
- Don't use in noisy environment
- Don't cover microphone
- Don't use with loud background music
- Don't use built-in laptop mic if possible
- Don't skip calibration

---

## Still Having Issues?

### 1. Check Logs
```bash
# View recent errors
type logs\veda_ai.log
```

### 2. Test with Simple Commands
Start with very simple commands:
- "hello"
- "time"
- "date"
- "weather"

### 3. Try Text Commands First
- Type commands instead of speaking
- Verify VEDA AI is working
- Then troubleshoot voice separately

### 4. Reinstall Dependencies
```bash
pip uninstall SpeechRecognition pyaudio
pip install SpeechRecognition pyaudio
```

### 5. Use Different Python Version
- Try Python 3.9 or 3.10
- Some audio libraries work better with specific versions

---

## Quick Reference Commands

```bash
# Test microphone
python test_microphone.py

# Fix and calibrate
python fix_microphone.py

# Manual calibration
python calibrate_voice.py

# Test advanced voice
python -m python_backend.voice_advanced

# View logs
type logs\veda_ai.log

# Start VEDA AI
python run_veda_ai.py
```

---

## Contact Support

If none of these solutions work:

1. **Check GitHub Issues**: [github.com/yourusername/veda-ai/issues](https://github.com/yourusername/veda-ai/issues)
2. **Create New Issue**: Include output from `python test_microphone.py`
3. **Email**: your.email@example.com

---

## Success Checklist

Before using VEDA AI voice commands, ensure:

- [ ] Microphone is connected and detected
- [ ] Windows microphone permissions enabled
- [ ] Microphone volume is 80-100%
- [ ] `python test_microphone.py` passes all tests
- [ ] `python fix_microphone.py` shows success
- [ ] Calibration completed (threshold 2000-6000 is good)
- [ ] Internet connection is active
- [ ] No other apps using microphone
- [ ] Quiet environment with minimal background noise

---

**Made with ❤️ for VEDA AI Users**

*Last Updated: January 2026*

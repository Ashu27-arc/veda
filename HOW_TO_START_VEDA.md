# VEDA AI - Complete Start Guide

## 🚀 Quick Start (Recommended)

### Option 1: Automatic Start (Best)
```bash
start_veda.bat
```
Yeh automatically:
- Virtual environment activate karega
- Server start karega
- Browser open karega (5 seconds mein)

### Option 2: Manual Browser Open
Agar browser automatically nahi khula:
```bash
# Terminal 1: Start VEDA AI
start_veda.bat

# Terminal 2: Open Browser
open_browser.bat
```

### Option 3: Python Script
```bash
python open_browser.py
```

## 📋 Step-by-Step Instructions

### First Time Setup
1. Virtual environment banao (agar nahi hai):
   ```bash
   python -m venv venv
   ```

2. Dependencies install karo:
   ```bash
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. VEDA AI start karo:
   ```bash
   start_veda.bat
   ```

### Daily Use
```bash
# Bas yeh command run karo
start_veda.bat
```

Browser automatically khul jayega `http://localhost:8000` par!

## 🔧 Troubleshooting

### Problem 1: Browser nahi khul raha
**Solution:**
```bash
# Method 1: Batch file use karo
open_browser.bat

# Method 2: Python script use karo
python open_browser.py

# Method 3: Manually browser mein jao
# Open: http://localhost:8000
```

### Problem 2: Server nahi chal raha
**Check karo:**
```bash
netstat -ano | findstr ":8000"
```

**Fix:**
```bash
# Purane processes kill karo
taskkill /F /IM python.exe

# Phir start karo
start_veda.bat
```

### Problem 3: Port already in use
```bash
# Port free karo
for /f "tokens=5" %a in ('netstat -ano ^| findstr ":8000"') do taskkill /F /PID %a

# Phir start karo
start_veda.bat
```

### Problem 4: Page load nahi ho raha
1. 5 seconds wait karo
2. Page refresh karo (F5)
3. Logs check karo: `type logs\veda_ai.log`

## 📁 Important Files

### Start Scripts
- `start_veda.bat` - Main launcher (auto-opens browser)
- `start_veda_fixed.bat` - Alternative launcher
- `run_veda_ai.py` - Python launcher

### Browser Scripts
- `open_browser.bat` - Opens browser (if not auto-opened)
- `open_browser.py` - Python script to open browser
- `open_veda_browser.bat` - Alternative browser opener

### Other
- `auto_start.py` - Auto-start on Windows boot
- `tray.py` - System tray icon

## ✅ Verification Steps

1. **Check if server is running:**
   ```bash
   netstat -ano | findstr ":8000"
   ```
   Output should show: `LISTENING` on port 8000

2. **Check server health:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy",...}`

3. **Check logs:**
   ```bash
   type logs\veda_ai.log
   ```
   Should show: "VEDA AI backend initialized"

## 🎯 What Happens When You Start

1. ✅ Virtual environment activates
2. ✅ Dependencies check hota hai
3. ✅ FastAPI server start hota hai (port 8000)
4. ✅ Wake word detection start hota hai
5. ✅ Automation engine start hota hai
6. ✅ Browser automatically khulta hai
7. ✅ VEDA AI UI load hota hai

## 🌐 Access URLs

- **Main UI:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **Settings:** http://localhost:8000/settings
- **API Docs:** http://localhost:8000/docs (FastAPI auto-docs)

## 🛑 How to Stop

### Method 1: Graceful Stop
Press `Ctrl+C` in the terminal where VEDA is running

### Method 2: Force Stop
```bash
taskkill /F /IM python.exe
```

### Method 3: Stop specific process
```bash
# Find PID
netstat -ano | findstr ":8000"

# Kill that PID
taskkill /F /PID <PID_NUMBER>
```

## 💡 Pro Tips

1. **Auto-start on boot:**
   ```bash
   python auto_start.py
   ```

2. **Run in background:**
   ```bash
   start /B start_veda.bat
   ```

3. **Check if running:**
   ```bash
   curl http://localhost:8000/health
   ```

4. **View real-time logs:**
   ```bash
   Get-Content logs\veda_ai.log -Wait -Tail 20
   ```

## 🆘 Still Having Issues?

1. Check `BROWSER_OPEN_FIX.md` for detailed browser fixes
2. Check `logs\veda_ai.log` for errors
3. Try `start_veda_fixed.bat` as alternative
4. Manually open browser: http://localhost:8000

## 📞 Quick Commands Reference

```bash
# Start VEDA AI
start_veda.bat

# Open browser
open_browser.bat

# Stop VEDA AI
taskkill /F /IM python.exe

# Check status
netstat -ano | findstr ":8000"

# View logs
type logs\veda_ai.log

# Health check
curl http://localhost:8000/health
```

---

**Happy VEDAing! 🚀**

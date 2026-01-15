# Browser Open Fix - VEDA AI

## Problem
Browser automatically nahi khul raha hai jab VEDA AI start hota hai.

## Solutions (Try in order)

### Method 1: Use Open Browser Script (Easiest)
```bash
# Pehle VEDA AI start karo
start_veda.bat

# Phir dusre terminal mein browser open karo
open_browser.bat
```

### Method 2: Use Python Script
```bash
python open_browser.py
```

### Method 3: Manual Browser Open
1. VEDA AI start karo: `start_veda.bat`
2. Browser mein manually jao: `http://localhost:8000`

### Method 4: Improved Start Script
Updated `start_veda.bat` ab automatically browser open karega:
```bash
start_veda.bat
```

## Verification
Check if server is running:
```bash
netstat -ano | findstr ":8000"
```

Agar output aata hai, toh server chal raha hai!

## Common Issues

### Issue 1: Server nahi chal raha
**Solution:** 
```bash
# Pehle purane processes kill karo
taskkill /F /IM python.exe

# Phir start karo
start_veda.bat
```

### Issue 2: Port already in use
**Solution:**
```bash
# Port 8000 ko free karo
for /f "tokens=5" %a in ('netstat -ano ^| findstr ":8000"') do taskkill /F /PID %a
```

### Issue 3: Browser khulta hai par page load nahi hota
**Solution:**
- 5 seconds wait karo
- Page refresh karo (F5)
- Check logs: `type logs\veda_ai.log`

## Files Created
- `open_browser.py` - Python script to open browser
- `open_browser.bat` - Batch file to open browser
- Updated `run_veda_ai.py` - Improved browser opening logic
- Updated `start_veda.bat` - Auto-opens browser

## Quick Commands

### Start VEDA AI
```bash
start_veda.bat
```

### Open Browser (if not opened automatically)
```bash
open_browser.bat
```

### Check Server Status
```bash
curl http://localhost:8000/health
```

### Stop VEDA AI
```bash
# Press Ctrl+C in the terminal
# OR
taskkill /F /IM python.exe
```

## Testing
1. Close all VEDA AI instances
2. Run: `start_veda.bat`
3. Browser should open automatically in 5 seconds
4. If not, run: `open_browser.bat`

## Success Indicators
✅ Server running on port 8000
✅ Browser opens automatically
✅ VEDA AI UI loads
✅ No errors in logs

## Need Help?
Check logs: `logs\veda_ai.log`

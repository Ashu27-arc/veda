# VEDA AI - Deployment Guide (Live Karne Ka Tarika)

## 📋 Prerequisites (Zaruri Cheezein)

### 1. System Requirements
- **Operating System**: Windows 10/11
- **Python**: Version 3.8 ya usse upar
- **RAM**: Minimum 4GB (8GB recommended)
- **Internet Connection**: API keys aur online features ke liye

### 2. Required Software
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Git (optional, for cloning)
- Node.js (agar frontend separately run karna ho)

---

## 🚀 Installation Steps

### Step 1: Project Setup
```bash
# Project folder mein jao
cd path/to/VEDA_AI

# Virtual environment banao (recommended)
python -m venv venv

# Virtual environment activate karo
# Windows:
venv\Scripts\activate
```

### Step 2: Dependencies Install Karo
```bash
# Saari required libraries install karo
pip install -r requirements.txt
```

### Step 3: Environment Variables Setup
`.env` file banao aur apni API keys add karo:

```env
# OpenAI API Key (agar online AI use kar rahe ho)
OPENAI_API_KEY=your_openai_api_key_here

# Groq API Key (alternative)
GROQ_API_KEY=your_groq_api_key_here

# Weather API Key
WEATHER_API_KEY=your_weather_api_key_here

# Other settings
AI_MODE=online  # ya 'local' for offline mode
```

---

## 🎯 Running VEDA AI (Live Karna)

### Method 1: Simple Run (Recommended)
```bash
# Main application run karo
python run_veda_ai.py
```

### Method 2: Auto Start
```bash
# System startup pe automatically run hoga
python auto_start.py
```

### Method 3: System Tray Mode
```bash
# Background mein system tray se run karo
python tray.py
```

### Method 4: Direct Backend Run
```bash
# Sirf backend run karna ho to
python python_backend/main.py
```

---

## ⚙️ Configuration (Settings)

### Voice Calibration
Pehli baar use karne se pehle voice calibrate karo:
```bash
python calibrate_voice.py
```

### Settings File
`data/settings.json` mein apni preferences set karo:
```json
{
  "ai_mode": "online",
  "voice_enabled": true,
  "wake_word": "Hey Veda",
  "language": "en",
  "theme": "dark"
}
```

---

## 🌐 Production Deployment (Server Pe Live Karna)

### Option 1: Local Network Pe Deploy
```bash
# Backend ko specific IP pe run karo
python python_backend/main.py --host 0.0.0.0 --port 5000
```

### Option 2: Windows Service Banao
1. **NSSM (Non-Sucking Service Manager) install karo**
   - Download: https://nssm.cc/download
   
2. **Service create karo**:
```bash
nssm install VEDA_AI "C:\path\to\venv\Scripts\python.exe" "C:\path\to\run_veda_ai.py"
nssm start VEDA_AI
```

### Option 3: Task Scheduler Use Karo
1. Task Scheduler kholo
2. "Create Basic Task" select karo
3. Trigger: "When the computer starts"
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `C:\path\to\run_veda_ai.py`

---

## 🔧 Troubleshooting (Common Issues)

### Issue 1: Module Not Found Error
```bash
# Solution: Dependencies dobara install karo
pip install -r requirements.txt --upgrade
```

### Issue 2: Microphone Access Denied
- Windows Settings → Privacy → Microphone → Allow apps to access microphone

### Issue 3: API Key Error
- `.env` file check karo
- API keys valid hain ya nahi verify karo

### Issue 4: Port Already in Use
```bash
# Different port use karo
python python_backend/main.py --port 5001
```

---

## 📦 Building Executable (EXE Banana)

### PyInstaller Use Karke
```bash
# PyInstaller install karo
pip install pyinstaller

# EXE build karo
pyinstaller --onefile --windowed --icon=icon.ico run_veda_ai.py

# EXE dist folder mein milega
```

### Setup Installer Banana
```bash
# Inno Setup ya NSIS use karo
# installer folder mein already ek setup file hai
```

---

## 🔐 Security Best Practices

1. **API Keys ko secure rakho**
   - `.env` file ko `.gitignore` mein add karo
   - Environment variables use karo production mein

2. **User Permissions**
   - Limited user permissions se run karo
   - Admin rights sirf zarurat hone pe do

3. **Network Security**
   - Firewall rules properly configure karo
   - HTTPS use karo agar remote access chahiye

---

## 📊 Monitoring & Logs

### Log Files Check Karo
```bash
# Application logs
type logs\veda_ai.log

# Error logs
type logs\jarvis.log
```

### Performance Monitoring
- Task Manager mein CPU/Memory usage check karo
- Logs regularly review karo

---

## 🔄 Updates & Maintenance

### Code Update Karna
```bash
# Latest code pull karo (agar Git use kar rahe ho)
git pull origin main

# Dependencies update karo
pip install -r requirements.txt --upgrade

# Application restart karo
```

### Backup
Regular backup lo:
- `data/` folder (settings aur history)
- `.env` file (API keys)
- Custom configurations

---

## 📞 Support & Help

### Documentation
- Main guide: `HOW_TO_USE_VEDA.md`
- Test commands: `tests/test_commands.py`

### Common Commands Test Karo
```bash
# Test suite run karo
python tests/test_commands.py
```

---

## ✅ Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with API keys
- [ ] Voice calibrated (`python calibrate_voice.py`)
- [ ] Microphone permissions granted
- [ ] Application running (`python run_veda_ai.py`)
- [ ] Wake word working ("Hey Veda")
- [ ] Basic commands tested

---

## 🎉 Success!

Agar sab kuch sahi se setup ho gaya hai, to ab aap VEDA AI ko use kar sakte ho!

**Wake word bolo**: "Hey Veda"  
**Command do**: "What's the weather?" ya "Open Chrome"

Happy coding! 🚀

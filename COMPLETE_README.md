# 🤖 VEDA AI - Complete Documentation

![VEDA AI](https://img.shields.io/badge/VEDA-AI%20Assistant-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/version-5.0-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)
![AI](https://img.shields.io/badge/AI-LM%20Studio-purple?style=for-the-badge)

**A powerful, JARVIS-inspired AI assistant with advanced automation and self-training capabilities**

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Features](#-features)
3. [Installation](#-installation)
4. [LM Studio Setup](#-lm-studio-setup)
5. [Browser Fix](#-browser-fix)
6. [Voice Setup](#-voice-setup)
7. [Automation](#-automation)
8. [Commands](#-commands)
9. [Troubleshooting](#-troubleshooting)
10. [Advanced](#-advanced)

---

## 🚀 Quick Start

### For Beginners (3 Steps):

```bash
# Step 1: Start VEDA AI
start_veda_fixed.bat

# Step 2: Wait for message
✅ Server is ready!

# Step 3: Browser opens automatically
http://localhost:8000
```

### For Advanced Users:

```bash
# Activate virtual environment
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run VEDA AI
python run_veda_ai.py
```

---

## ✨ Features

### 🎯 Core Features
- 🎤 **90-95% Voice Accuracy** - Advanced voice recognition
- 🌐 **Bilingual Support** - English + Hinglish
- 💻 **System Control** - Complete Windows automation
- 🌤️ **Real-time Weather** - Live weather updates
- 🤖 **Self-Training AI** - Learns from conversations
- 🔒 **Security Hardened** - Comprehensive protection
- 📚 **Offline Mode** - Works without internet

### 🤖 Automation Features (v5.0)
- ⚙️ **Task Scheduler** - Schedule tasks daily, weekly, or at intervals
- 💡 **Proactive Suggestions** - AI suggests actions based on context
- 🧠 **Context Awareness** - Learns your patterns and predicts needs
- 📊 **Usage Analytics** - Tracks app usage and command frequency
- 🚀 **Smart Shortcuts** - Create shortcuts for frequent commands
- 🔔 **System Monitoring** - Proactive alerts for disk, memory, CPU, battery

### 🎨 UI Features
- 🌌 **Cosmic Theme** - Beautiful space-themed interface
- ⚡ **Real-time Animations** - Smooth transitions and effects
- 📱 **Responsive Design** - Works on all screen sizes
- 🎭 **Dual Logo Display** - Symmetric design with glowing effects
- 🌊 **Voice Wave Indicator** - Visual feedback during voice input

---

## 📥 Installation

### Prerequisites:
- Windows 10/11
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection (for initial setup)

### Step-by-Step Installation:

#### 1. Clone or Download
```bash
# Clone repository
git clone https://github.com/yourusername/veda-ai.git
cd veda-ai

# Or download ZIP and extract
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
```

#### 3. Activate Virtual Environment
```bash
venv\Scripts\activate.bat
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Setup Automation (Optional)
```bash
python setup_automation.py
```

#### 6. Run VEDA AI
```bash
# Best method (recommended)
start_veda_fixed.bat

# Or standard method
python run_veda_ai.py
```

---

## 🤖 LM Studio Setup

### What is LM Studio?

LM Studio is a desktop application for running local AI models. It's:
- ✅ Free and Open Source
- ✅ Easy to Use (GUI interface)
- ✅ Fast and Optimized
- ✅ OpenAI Compatible
- ✅ 100% Private (offline)

### Installation:

#### Step 1: Download LM Studio
1. Visit: https://lmstudio.ai/
2. Download for Windows
3. Install and launch

#### Step 2: Download a Model

**Recommended Models:**

| Model | Size | Speed | Quality | RAM Required |
|-------|------|-------|---------|--------------|
| Phi-3 Mini | ~2GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 4GB |
| Llama 3.2 3B | ~2-4GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 8GB |
| Mistral 7B | ~4-8GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 8GB |

**How to Download:**
1. Open LM Studio
2. Click "Discover" tab
3. Search for "Phi-3" (recommended for beginners)
4. Select GGUF format
5. Choose Q4_K_M quantization
6. Click "Download"

#### Step 3: Start Server
1. Go to "Local Server" tab
2. Click "Select a model to load"
3. Choose your downloaded model
4. Click "Load Model"
5. Click "Start Server"
6. Verify: ✅ Server running on port 1234

#### Step 4: Configure VEDA AI

Your `.env` file is already configured:
```env
AI_MODE=self_training
LM_STUDIO_MODEL=local-model
LM_STUDIO_API_URL=http://localhost:1234
LM_STUDIO_TIMEOUT=60
LM_STUDIO_MAX_RETRIES=2
```

No changes needed!

#### Step 5: Test
```bash
# Start VEDA AI
start_veda_fixed.bat

# Try command
"Hello VEDA"

# Check logs
type logs\veda_ai.log
# Should see: "Using LM Studio model: local-model"
```

### LM Studio vs Ollama:

| Feature | LM Studio | Ollama |
|---------|-----------|--------|
| Interface | ✅ GUI | ❌ CLI only |
| Easy Setup | ✅ Very easy | ⚠️ Requires CLI |
| Model Browser | ✅ Built-in | ❌ Manual |
| Windows Support | ✅ Excellent | ⚠️ Limited |
| API Format | ✅ OpenAI | ❌ Custom |

**LM Studio is recommended for VEDA AI!**

---

## 🌐 Browser Fix

### Problem:
Browser not opening automatically or showing blank page.

### Solution Applied:

#### What Was Fixed:
- ✅ Server health check before opening browser
- ✅ Automatic port conflict detection
- ✅ Dependency verification
- ✅ Multiple browser opening methods
- ✅ Clear error messages

#### How to Use:

**Method 1: Fixed Launcher (Best)**
```bash
start_veda_fixed.bat
```

**Method 2: Standard Launcher**
```bash
start_veda.bat
```

**Method 3: Manual Browser**
```bash
# Start VEDA
start_veda.bat

# Then open browser
open_veda_browser.bat
```

**Method 4: Direct URL**
```bash
# Start VEDA
start_veda.bat

# Open browser manually
http://localhost:8000
```

#### Diagnostics:
```bash
# Check system health
diagnose_veda.bat

# Verify fix applied
verify_fix.bat
```

#### Common Issues:

**Issue 1: Port Already in Use**
```bash
# Automatically fixed by start_veda_fixed.bat
# Or manually:
netstat -ano | findstr ":8000"
taskkill /F /PID <PID>
```

**Issue 2: Browser Opens but Blank Page**
```
Solution:
1. Wait 5 seconds
2. Refresh (F5)
3. Check server is running
```

**Issue 3: Can't Connect**
```bash
# Run diagnostics
diagnose_veda.bat

# Check logs
type logs\veda_ai.log
```

---

## 🎤 Voice Setup

### Voice Recognition:

VEDA AI uses advanced voice recognition with 90-95% accuracy.

#### Features:
- ✅ Multi-language support (English, Hindi, Hinglish)
- ✅ Automatic calibration
- ✅ Noise cancellation
- ✅ Real-time feedback

#### Setup:

**Step 1: Test Microphone**
```bash
python fix_microphone.py
```

**Step 2: Calibrate Voice**
```bash
python calibrate_voice.py
```

**Step 3: Use in VEDA AI**
1. Click "VOICE INPUT" button
2. Speak clearly
3. Wait for response

#### Voice Commands:

**English:**
- "Hello VEDA"
- "Open Chrome"
- "What's the weather?"
- "Close Notepad"

**Hinglish:**
- "Namaste VEDA"
- "Chrome kholo"
- "Mausam kaisa hai?"
- "Notepad band karo"

#### Troubleshooting:

**Problem: Microphone not detected**
```bash
# Fix microphone
python fix_microphone.py

# Check Windows settings
Settings > Privacy > Microphone
```

**Problem: Low accuracy**
```bash
# Calibrate voice
python calibrate_voice.py

# Reduce background noise
# Speak more clearly
```

**Problem: No speech detected**
```
Solution:
1. Check microphone connection
2. Enable microphone in Windows
3. Close other apps using microphone
4. Calibrate voice
```

---

## ⚙️ Automation

### Task Scheduler:

Schedule tasks to run automatically.

#### Create Task:
1. Open VEDA AI
2. Click "⚙️ AUTO" button
3. Go to "Scheduled Tasks" tab
4. Fill in:
   - Task name
   - Command to execute
   - Schedule type (daily, weekly, interval)
   - Schedule value (time or interval)
5. Click "Add Task"

#### Schedule Types:
- **Daily:** Run at specific time every day
- **Weekly:** Run on specific day and time
- **Interval:** Run every X hours/minutes
- **Once:** Run once at specific time

#### Examples:
```
Task: Morning Greeting
Command: speak "Good morning!"
Schedule: daily
Value: 08:00

Task: Weather Update
Command: weather
Schedule: interval
Value: 3h

Task: System Cleanup
Command: cleanup temp files
Schedule: weekly
Value: Sunday 10:00
```

### Proactive Suggestions:

VEDA AI suggests actions based on context.

#### Features:
- 💡 Low disk space warnings
- 💡 High memory usage alerts
- 💡 Battery low notifications
- 💡 Frequent app suggestions
- 💡 Time-based reminders

#### How It Works:
1. VEDA monitors system
2. Detects patterns
3. Suggests actions
4. You can execute or dismiss

### Context Awareness:

VEDA learns your patterns.

#### What It Learns:
- 📊 Most used apps
- 📊 Command frequency
- 📊 Time-based patterns
- 📊 Daily routines

#### Benefits:
- Faster command execution
- Predictive suggestions
- Smart shortcuts
- Personalized experience

### Smart Shortcuts:

Create one-word commands.

#### Create Shortcut:
1. Click "⚙️ AUTO" button
2. Go to "Shortcuts" tab
3. Enter:
   - Shortcut name (e.g., "work")
   - Full command (e.g., "open chrome and open gmail")
4. Click "Create"

#### Use Shortcut:
```
Instead of: "open chrome and open gmail"
Just say: "work"
```

---

## 💬 Commands

### System Commands:

**Applications:**
```
"open chrome"
"open notepad"
"open calculator"
"close chrome"
"close all apps"
```

**System Control:**
```
"shutdown"
"restart"
"sleep"
"lock"
"volume up"
"volume down"
"mute"
```

**File Operations:**
```
"create file test.txt"
"delete file test.txt"
"open folder documents"
"search for python files"
```

### Weather Commands:

**English:**
```
"what's the weather?"
"weather in Delhi"
"weather in Mumbai and Delhi"
```

**Hinglish:**
```
"mausam kaisa hai?"
"Delhi mein mausam kaisa hai?"
"Mumbai aur Delhi ka mausam"
```

### AI Commands:

**Conversation:**
```
"hello"
"how are you?"
"tell me a joke"
"what can you do?"
```

**Questions:**
```
"what is Python?"
"explain AI"
"how to code?"
```

### Automation Commands:

**Tasks:**
```
"show tasks"
"create task"
"delete task"
"enable task"
```

**Suggestions:**
```
"show suggestions"
"execute suggestion"
```

**Context:**
```
"show context"
"show patterns"
"show analytics"
```

---

## 🐛 Troubleshooting

### Common Issues:

#### 1. Browser Not Opening
**Solution:**
```bash
# Use fixed launcher
start_veda_fixed.bat

# Or run diagnostics
diagnose_veda.bat
```

#### 2. Voice Not Working
**Solution:**
```bash
# Fix microphone
python fix_microphone.py

# Calibrate voice
python calibrate_voice.py
```

#### 3. LM Studio Not Connecting
**Solution:**
1. Open LM Studio
2. Load a model
3. Start server
4. Verify port 1234

#### 4. Port Already in Use
**Solution:**
```bash
# Find process
netstat -ano | findstr ":8000"

# Kill process
taskkill /F /PID <PID>
```

#### 5. Dependencies Missing
**Solution:**
```bash
# Activate venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

#### 6. Slow Performance
**Solution:**
1. Use smaller LM Studio model (Phi-3 Mini)
2. Close other applications
3. Increase timeout in .env
4. Restart computer

#### 7. Out of Memory
**Solution:**
1. Use smaller model
2. Close other apps
3. Restart computer
4. Upgrade RAM

### Diagnostic Tools:

**System Diagnostics:**
```bash
diagnose_veda.bat
```

**Fix Verification:**
```bash
verify_fix.bat
```

**Microphone Fix:**
```bash
python fix_microphone.py
```

**Voice Calibration:**
```bash
python calibrate_voice.py
```

### Log Files:

**Application Logs:**
```bash
type logs\veda_ai.log
```

**Error Logs:**
```bash
# Check last 50 lines
powershell -Command "Get-Content logs\veda_ai.log -Tail 50"
```

---

## 🔧 Advanced

### Building Executable:

```bash
# Build with logo
build_with_logo.bat

# Or manually
python build_with_logo.py
```

### Custom Training:

```bash
# Train with custom data
python train_veda.py

# Training data location
training_data.json
lm_studio_training_data.txt
```

### Configuration:

**Environment Variables (.env):**
```env
# AI Configuration
AI_MODE=self_training
LM_STUDIO_MODEL=local-model
LM_STUDIO_API_URL=http://localhost:1234
LM_STUDIO_TIMEOUT=60
LM_STUDIO_MAX_RETRIES=2

# Voice Configuration
PICOVOICE_ACCESS_KEY=your_key_here
```

**Settings (data/settings.json):**
```json
{
  "owner_name": "Sir",
  "voice_enabled": true,
  "wake_word_enabled": true,
  "automation_enabled": true
}
```

### API Endpoints:

**Health Check:**
```
GET http://localhost:8000/health
```

**Voice Command:**
```
GET http://localhost:8000/voice
```

**Settings:**
```
GET http://localhost:8000/settings
POST http://localhost:8000/settings/owner
```

**Automation:**
```
GET http://localhost:8000/automation/status
GET http://localhost:8000/automation/suggestions
POST http://localhost:8000/automation/execute-suggestion
```

**Tasks:**
```
GET http://localhost:8000/tasks
POST http://localhost:8000/tasks
DELETE http://localhost:8000/tasks/{task_id}
```

### Security:

**Features:**
- ✅ Input validation
- ✅ Command sanitization
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Secure WebSocket
- ✅ No external data sharing

**Best Practices:**
1. Keep dependencies updated
2. Use virtual environment
3. Don't expose to internet
4. Regular backups
5. Monitor logs

### Performance Optimization:

**Tips:**
1. Use Phi-3 Mini for speed
2. Enable GPU in LM Studio
3. Close unnecessary apps
4. Use SSD for better I/O
5. Increase RAM if possible

### Folder Structure:

```
veda-ai/
├── docs/                    # All documentation
│   ├── guides/             # Setup guides
│   ├── troubleshooting/    # Problem solutions
│   └── archive/            # Old documentation
├── python_backend/         # Backend code
├── python_frontend/        # Frontend code
├── data/                   # User data
├── logs/                   # Log files
├── scripts/                # Utility scripts
└── README.md              # Main readme
```

---

## 📚 Additional Resources

### Documentation Files:
- `COMPLETE_README.md` - This file (complete guide)
- `docs/guides/LM_STUDIO_SETUP.md` - LM Studio setup
- `docs/guides/BROWSER_FIX.md` - Browser fix guide
- `docs/guides/VOICE_SETUP.md` - Voice setup guide
- `docs/troubleshooting/COMMON_ISSUES.md` - Common problems

### Quick References:
- `START_HERE.txt` - Quick start guide
- `LM_STUDIO_QUICK_REFERENCE.txt` - LM Studio reference
- `FIXED_SUMMARY.txt` - Browser fix summary

### External Links:
- **LM Studio:** https://lmstudio.ai/
- **Python:** https://www.python.org/
- **FastAPI:** https://fastapi.tiangolo.com/

---

## 🎊 Credits

**VEDA AI** - Made with ❤️ in India 🇮🇳

**Technologies Used:**
- Python 3.8+
- FastAPI
- LM Studio
- WebSocket
- Speech Recognition
- pyttsx3

**Special Thanks:**
- LM Studio team
- FastAPI team
- Python community
- All contributors

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Support

**Need Help?**
- Read this documentation
- Check troubleshooting section
- Run diagnostic tools
- Check log files

**Found a Bug?**
- Check logs
- Run diagnostics
- Report with details

---

**Version:** 5.0  
**Date:** January 2026  
**Status:** ✅ Production Ready  
**Tested:** Windows 10/11

---

*"At your service, Sir."* - VEDA AI 🤖

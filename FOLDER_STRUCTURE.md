# 📁 VEDA AI - Folder Structure

## 🎯 Clean and Organized Structure

```
veda-ai/
│
├── 📄 README.md                    # Quick start guide (main file)
├── 📄 COMPLETE_README.md           # Complete documentation (all-in-one)
├── 📄 START_HERE.txt               # Quick reference card
├── 📄 FOLDER_STRUCTURE.md          # This file
│
├── 📁 docs/                        # All documentation
│   ├── 📄 DOCUMENTATION.md         # Main documentation
│   │
│   ├── 📁 guides/                  # Setup and how-to guides
│   │   ├── LM_STUDIO_SETUP.md      # LM Studio setup (English)
│   │   ├── LM_STUDIO_SETUP_HINDI.md # LM Studio setup (Hindi)
│   │   ├── LM_STUDIO_QUICK_REFERENCE.txt # Quick reference
│   │   ├── OLLAMA_TO_LM_STUDIO_MIGRATION.md # Migration guide
│   │   ├── OLLAMA_REPLACED_WITH_LM_STUDIO.md # Change summary
│   │   ├── COMPLETE_AUTOMATION_GUIDE.md # Automation guide
│   │   ├── VOICE_README.md         # Voice setup guide
│   │   └── QUICK_START.md          # Quick start guide
│   │
│   ├── 📁 troubleshooting/         # Problem solutions
│   │   ├── BROWSER_FIX_GUIDE.md    # Browser fix (English)
│   │   ├── BROWSER_ISSUE_FIXED.md  # Browser fix (Hindi)
│   │   ├── README_BROWSER_FIX.txt  # Browser fix (Quick)
│   │   ├── WHATS_NEW_BROWSER_FIX.md # Browser fix changelog
│   │   └── FIXED_SUMMARY.txt       # Browser fix summary
│   │
│   └── 📁 archive/                 # Old documentation
│       ├── DOCUMENTATION_ARCHIVE.md
│       ├── FILES_MERGED.md
│       ├── LAYOUT_CHANGED.md
│       ├── BOTH_SIDES_GLOW.md
│       └── UI_IMPROVEMENTS.md
│
├── 📁 scripts/                     # Utility scripts
│   ├── diagnose_veda.bat           # System diagnostics
│   ├── verify_fix.bat              # Verify fixes applied
│   ├── fix_microphone.py           # Fix microphone issues
│   ├── calibrate_voice.py          # Calibrate voice recognition
│   ├── setup_automation.py         # Setup automation system
│   └── train_veda.py               # Train custom AI model
│
├── 📁 python_backend/              # Backend code
│   ├── main.py                     # FastAPI server
│   ├── ai_engine.py                # AI processing
│   ├── lm_studio_ai.py             # LM Studio integration
│   ├── voice.py                    # Voice recognition
│   ├── voice_advanced.py           # Advanced voice features
│   ├── system_control.py           # System commands
│   ├── automation_engine.py        # Automation system
│   ├── proactive_assistant.py      # Proactive suggestions
│   ├── context_awareness.py        # Pattern learning
│   ├── task_scheduler.py           # Task scheduling
│   ├── jarvis_personality.py       # JARVIS personality
│   ├── self_learning.py            # Self-learning AI
│   ├── weather.py                  # Weather API
│   ├── config.py                   # Configuration
│   ├── logger.py                   # Logging system
│   └── utils.py                    # Utility functions
│
├── 📁 python_frontend/             # Frontend code
│   ├── index.html                  # Main UI
│   ├── app.js                      # JavaScript logic
│   ├── style.css                   # Styling
│   ├── 📁 assets/                  # Images and assets
│   │   ├── veda-logo.png
│   │   ├── veda-logo-bg.png
│   │   └── veda.png
│   └── 📁 sounds/                  # Sound files
│       └── Hey-Veda_en_windows_v4_0_0.ppn
│
├── 📁 data/                        # User data (auto-created)
│   ├── settings.json               # User settings
│   ├── conversation_history.json  # Chat history
│   ├── learning_data.json          # Learned responses
│   ├── automation_config.json      # Automation config
│   ├── scheduled_tasks.json        # Scheduled tasks
│   ├── user_patterns.json          # Usage patterns
│   ├── context_data.json           # Context data
│   ├── task_queue.json             # Task queue
│   └── voice_profile.json          # Voice settings
│
├── 📁 logs/                        # Log files (auto-created)
│   └── veda_ai.log                 # Application logs
│
├── 📁 venv/                        # Virtual environment
│   └── ...                         # Python packages
│
├── 📁 build/                       # Build files (auto-created)
│   └── ...                         # Compiled files
│
├── 📁 dist/                        # Distribution files (auto-created)
│   └── ...                         # Executable files
│
├── 📁 installer/                   # Installer files
│   └── VEDA_AI-Setup.exe           # Windows installer
│
├── 📄 .env                         # Environment variables
├── 📄 .gitignore                   # Git ignore rules
├── 📄 requirements.txt             # Python dependencies
├── 📄 VEDA_AI.spec                 # PyInstaller spec
├── 📄 installer_script.iss         # Inno Setup script
│
├── 🚀 start_veda_fixed.bat         # Best launcher (use this!)
├── 🚀 start_veda.bat               # Standard launcher
├── 🚀 open_veda_browser.bat        # Open browser only
├── 🚀 run_veda_ai.py               # Python launcher
│
├── 🔧 build_with_logo.bat          # Build executable
├── 🔧 build_with_logo.py           # Build script
├── 🔧 install_veda.bat             # Install script
│
└── 📄 training_data.json           # Training data
    📄 lm_studio_training_data.txt  # LM Studio training data
    📄 huggingface_training_data.json # Hugging Face data
    📄 Modelfile                    # Model configuration
```

---

## 📂 Folder Descriptions

### 📁 Root Level
- **README.md** - Quick start guide (read this first!)
- **COMPLETE_README.md** - Complete documentation (everything in one file)
- **START_HERE.txt** - Quick reference card
- **FOLDER_STRUCTURE.md** - This file

### 📁 docs/
All documentation organized by category:
- **guides/** - Setup and how-to guides
- **troubleshooting/** - Problem solutions
- **archive/** - Old documentation (for reference)

### 📁 scripts/
Utility scripts for maintenance and setup:
- **diagnose_veda.bat** - Check system health
- **verify_fix.bat** - Verify fixes applied
- **fix_microphone.py** - Fix microphone issues
- **calibrate_voice.py** - Calibrate voice
- **setup_automation.py** - Setup automation
- **train_veda.py** - Train AI model

### 📁 python_backend/
Backend Python code:
- **main.py** - FastAPI server (entry point)
- **ai_engine.py** - AI processing logic
- **lm_studio_ai.py** - LM Studio integration
- **automation_engine.py** - Automation system
- **voice.py** - Voice recognition
- **system_control.py** - System commands

### 📁 python_frontend/
Frontend HTML/CSS/JS:
- **index.html** - Main UI
- **app.js** - JavaScript logic
- **style.css** - Styling
- **assets/** - Images and logos
- **sounds/** - Wake word files

### 📁 data/
User data (auto-created on first run):
- **settings.json** - User preferences
- **conversation_history.json** - Chat history
- **learning_data.json** - Learned responses
- **automation_config.json** - Automation settings
- **scheduled_tasks.json** - Scheduled tasks

### 📁 logs/
Application logs (auto-created):
- **veda_ai.log** - All application logs

---

## 🎯 Important Files

### Must Read:
1. **README.md** - Start here!
2. **COMPLETE_README.md** - Complete guide
3. **START_HERE.txt** - Quick reference

### Setup Guides:
1. **docs/guides/LM_STUDIO_SETUP.md** - AI setup
2. **docs/guides/VOICE_README.md** - Voice setup
3. **docs/guides/COMPLETE_AUTOMATION_GUIDE.md** - Automation

### Troubleshooting:
1. **docs/troubleshooting/BROWSER_FIX_GUIDE.md** - Browser issues
2. **docs/troubleshooting/FIXED_SUMMARY.txt** - Quick fixes

### Scripts:
1. **scripts/diagnose_veda.bat** - Diagnostics
2. **scripts/fix_microphone.py** - Microphone fix
3. **scripts/calibrate_voice.py** - Voice calibration

---

## 🚀 Launchers

### Recommended:
- **start_veda_fixed.bat** - Best option (use this!)

### Alternative:
- **start_veda.bat** - Standard launcher
- **run_veda_ai.py** - Python launcher
- **open_veda_browser.bat** - Browser only

---

## 🔧 Build Files

### Build Executable:
- **build_with_logo.bat** - Build with logo
- **build_with_logo.py** - Build script
- **VEDA_AI.spec** - PyInstaller spec

### Installer:
- **installer_script.iss** - Inno Setup script
- **installer/VEDA_AI-Setup.exe** - Windows installer

---

## 📊 File Count Summary

```
Total Files: ~100+
├── Documentation: ~20 files
├── Python Code: ~25 files
├── Frontend: ~5 files
├── Scripts: ~10 files
├── Data: ~10 files (auto-created)
├── Logs: ~2 files (auto-created)
└── Other: ~30 files
```

---

## 🎯 Navigation Guide

### Want to...

**Start VEDA AI?**
→ Run `start_veda_fixed.bat`

**Read documentation?**
→ Open `COMPLETE_README.md`

**Setup LM Studio?**
→ Read `docs/guides/LM_STUDIO_SETUP.md`

**Fix browser issues?**
→ Read `docs/troubleshooting/BROWSER_FIX_GUIDE.md`

**Fix voice issues?**
→ Run `scripts/fix_microphone.py`

**Check system health?**
→ Run `scripts/diagnose_veda.bat`

**Setup automation?**
→ Run `scripts/setup_automation.py`

**Train AI model?**
→ Run `scripts/train_veda.py`

**View logs?**
→ Open `logs/veda_ai.log`

**Change settings?**
→ Edit `data/settings.json`

---

## 🧹 Clean Structure Benefits

### Before:
```
❌ 50+ files in root directory
❌ Hard to find documentation
❌ Mixed scripts and docs
❌ Confusing structure
```

### After:
```
✅ Organized folders
✅ Easy to find files
✅ Separated by purpose
✅ Clean root directory
```

---

## 📝 Notes

### Auto-Created Folders:
These folders are created automatically on first run:
- `data/` - User data
- `logs/` - Log files
- `build/` - Build files (when building)
- `dist/` - Distribution files (when building)

### Don't Delete:
- `python_backend/` - Backend code
- `python_frontend/` - Frontend code
- `venv/` - Virtual environment
- `.env` - Configuration
- `requirements.txt` - Dependencies

### Safe to Delete:
- `build/` - Can rebuild
- `dist/` - Can rebuild
- `logs/` - Will recreate
- `docs/archive/` - Old docs

---

**Version:** 1.0  
**Date:** January 2026  
**Status:** ✅ Clean and Organized

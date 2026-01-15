# 🤖 VEDA AI - Advanced Automated Intelligent Assistant

![VEDA AI](https://img.shields.io/badge/VEDA-AI%20Assistant-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/version-5.0-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-red?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Automated-purple?style=for-the-badge)

**A powerful, JARVIS-inspired AI assistant with advanced automation and self-training capabilities - No OpenAI required!**

---

## 🎯 What's New in v5.0 - AUTOMATION EDITION

### 🤖 Advanced Automation System
- **⚙️ Task Scheduler** - Schedule tasks daily, weekly, or at intervals
- **💡 Proactive Suggestions** - AI suggests actions based on context
- **🧠 Context Awareness** - Learns your patterns and predicts needs
- **📊 Usage Analytics** - Tracks app usage and command frequency
- **🚀 Smart Shortcuts** - Create shortcuts for frequent commands
- **⏰ Background Processing** - Tasks run automatically in background
- **🔔 System Monitoring** - Proactive alerts for disk, memory, CPU, battery

### ✅ Previous Features (v4.0)
- **Self-Training AI** - Learns from your conversations
- **100% Offline** - Works without internet
- **Completely Free** - No API costs
- **Full Privacy** - Your data stays local
- **3 AI Options** - Ollama, Hugging Face, or Local AI

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Activate virtual environment (IMPORTANT!)
.\venv\Scripts\activate

# 2. Install ALL dependencies
pip install -r requirements.txt

# 3. Install automation packages (REQUIRED for v5.0)
pip install schedule apscheduler

# 4. Setup automation system
python setup_automation.py

# 5. Run VEDA AI
python run_veda_ai.py

# Optional: Add Ollama for better AI
# Download from https://ollama.ai
ollama serve
ollama pull llama2
```

Browser automatically opens at `http://localhost:8000`

**⚠️ Important**: Make sure to install `schedule` and `apscheduler` packages for automation features to work!

---

## ✨ Key Features

### 🤖 Automation & Intelligence
- ⚙️ **Task Automation** - Schedule and automate repetitive tasks
- 💡 **Proactive Assistant** - Suggests actions before you ask
- 🧠 **Pattern Learning** - Learns your daily routines
- 📊 **Smart Analytics** - Tracks usage and provides insights
- 🚀 **Quick Shortcuts** - One-word commands for complex tasks
- 🔔 **System Monitoring** - Real-time health checks and alerts

### 🎯 Core Features
- 🎤 **90-95% Voice Accuracy** - Advanced voice calibration
- 🌐 **Bilingual Support** - English + Hinglish
- 💻 **System Control** - Complete Windows control
- 🌤️ **Real-time Weather** - Live weather updates
- 🤖 **Self-Training AI** - Learns from you automatically
- 🔒 **Security Hardened** - Comprehensive protection
- 📚 **Offline Mode** - Works without internet

---

## 🧠 Self-Training AI

### How It Works:
1. **Use VEDA normally** - Talk to it like usual
2. **Automatic Learning** - Saves successful conversations
3. **Gets Smarter** - Reuses learned responses
4. **Train Custom Model** - Optional advanced training

### AI Options (Priority Order):
1. **Learned Responses** - From previous conversations
2. **Ollama** - Local AI models (recommended)
3. **Hugging Face** - Transformer models
4. **Local AI** - Rule-based (always available)

### Quick Setup:
```bash
# Option 1: Use as-is (already working!)
python run_veda_ai.py

# Option 2: Add Ollama (recommended)
ollama serve
ollama pull llama2

# Option 3: Train custom model
python train_veda.py
```

**See:** `QUICK_SETUP_SELF_TRAINING.md` for detailed setup

---

## 📚 Documentation

### Quick Guides:
- 📖 **[QUICK_SETUP_SELF_TRAINING.md](QUICK_SETUP_SELF_TRAINING.md)** - 5-minute setup
- 🎓 **[SELF_TRAINING_GUIDE.md](SELF_TRAINING_GUIDE.md)** - Complete training guide
- ✅ **[OPENAI_REMOVED.md](OPENAI_REMOVED.md)** - What changed

### Complete Documentation:
- 📖 **[DOCUMENTATION.md](DOCUMENTATION.md)** - Full documentation
- System Commands
- Building Executable
- Deployment Guide
- Security Information
- Troubleshooting
- Fixes Applied

---

## 🐛 Bug Tracking

For security issues and bug reports, see:

### 🔒 [BUGS.md](BUGS.md)

---

## 💬 Example Commands

**English:**
- "Hello" / "Open Chrome" / "What's the weather?"

**Hinglish:**
- "Namaste" / "Chrome kholo" / "Mausam kaisa hai?"

---

## 🆘 Quick Help

**Voice not working?**
```bash
python fix_microphone.py
```

**Test everything:**
```bash
python test_fixes.py
```

**View logs:**
```bash
type logs\veda_ai.log
```

---

## 📞 Support

- **Documentation:** [DOCUMENTATION.md](DOCUMENTATION.md)
- **Bugs:** [BUGS.md](BUGS.md)
- **Issues:** [GitHub Issues](https://github.com/yourusername/veda-ai/issues)

---

**Made with ❤️ in India 🇮🇳**

*"At your service, Sir."* - VEDA AI

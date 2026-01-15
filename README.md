# 🤖 VEDA AI - Your Intelligent Bilingual Assistant

<div align="center">

![VEDA AI](https://img.shields.io/badge/VEDA-AI%20Assistant-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/version-3.1-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-red?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Hardened-brightgreen?style=for-the-badge)

**A powerful, JARVIS-inspired AI assistant that understands both English and Hinglish**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security) • [Documentation](#-documentation)

</div>

---

## 🌟 Overview

VEDA AI is an advanced personal AI assistant built with Python, featuring voice recognition, system control, weather updates, and intelligent conversation capabilities. Inspired by JARVIS from Iron Man, VEDA provides a professional yet friendly experience with support for both English and Hinglish (Hindi-English mix).

### ⚠️ IMPORTANT SECURITY NOTICE

**Version 3.1 includes critical security fixes. Please read [BUGS.md](BUGS.md) for details.**

### Why VEDA AI?

- 🎯 **90-95% Voice Accuracy** - Advanced voice calibration system
- 🌐 **Bilingual Support** - Seamlessly understands English and Hinglish
- 🎤 **Voice Control** - Natural voice commands with push-to-talk
- 💻 **System Control** - Complete control over your Windows system
- 🌤️ **Real-time Weather** - Live weather updates for any city
- 🤖 **AI-Powered** - Online (OpenAI) and offline AI modes
- 🎨 **Modern UI** - Beautiful web-based interface
- 🔒 **Privacy-Focused** - Works offline with local AI
- 🛡️ **Security Hardened** - Comprehensive input validation and protection

---

## ✨ Features

### 🎤 Voice Recognition & Control
- **Advanced Voice Calibration** - 3-second calibration for 90-95% accuracy
- **Push-to-Talk Interface** - Click and speak for better control
- **Bilingual Recognition** - Understands English, Hindi, and Hinglish
- **Real-time Processing** - Fast voice-to-text conversion
- **Ambient Noise Adjustment** - Automatic noise filtering

### 💬 AI Conversation
- **Dual AI Modes**:
  - **Online Mode**: OpenAI GPT-4 integration for intelligent responses
  - **Offline Mode**: Local AI with JARVIS-style personality
- **Context-Aware Responses** - Remembers conversation flow
- **Natural Language Processing** - Understands casual conversation
- **Personality System** - Professional JARVIS-inspired responses

### 🌤️ Weather Integration
- **Real-time Weather Data** - Live updates from multiple APIs
- **Multi-City Support** - Check weather for multiple cities at once
- **Bilingual Weather Reports** - English and Hinglish responses
- **Detailed Information**: Temperature, Humidity, Wind speed, Conditions

### 💻 System Control
- **Application Management**: Open 20+ popular apps
- **Volume Control**: Increase/decrease/mute
- **System Operations**: Lock, Restart, Shutdown, WiFi control
- **System Information**: Battery, Time, Date, Health

### 🔒 Security Features (NEW in v3.1)
- **Input Sanitization** - Protection against injection attacks
- **Command Validation** - Malicious pattern detection
- **Secure CORS** - Restricted origins only
- **Rate Limiting Ready** - Infrastructure for API protection
- **Comprehensive Logging** - Security event tracking

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11
- Microphone (for voice commands)
- Internet connection (for online features)

### Quick Install

1. **Clone or Download the Repository**
```bash
git clone https://github.com/yourusername/veda-ai.git
cd veda-ai
```

2. **Create Virtual Environment** (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables** (REQUIRED)

Create a `.env` file in the root directory:
```env
# OpenAI API Key (for better AI responses)
OPENAI_API_KEY=your_openai_api_key_here

# Picovoice Access Key (for wake word detection)
PICOVOICE_ACCESS_KEY=your_picovoice_access_key_here
```

⚠️ **SECURITY WARNING**: Never commit your `.env` file to version control!

5. **Run VEDA AI**
```bash
python run_veda_ai.py
```

The application will automatically open in your browser at `http://localhost:8000`

---

## 📖 Usage

### First Time Setup

1. **Voice Calibration** (Highly Recommended)
   - Click the "🎯 Calibrate Voice" button
   - Stay silent for 3 seconds
   - This improves accuracy from 70% to 90-95%

2. **Test Voice Recognition**
   - Click "🎤 Speak" button
   - Wait for "Listening..." message
   - Say a simple command like "Hello"

### Using Voice Commands

1. Click the "🎤 Speak" button
2. Wait for "Listening..." indicator
3. Speak your command clearly
4. Wait for response

### Using Text Commands

1. Type your command in the input box
2. Press Enter or click Send
3. Get instant response

---

## 🎯 Commands

### 🌐 Opening Apps & Websites

#### Applications
```
English:
- "open chrome" / "open notepad" / "open calculator"
- "open word" / "open excel" / "open powerpoint"

Hinglish:
- "chrome kholo" / "notepad kholo" / "calculator kholo"
```

#### Websites
```
English:
- "open youtube" / "open google" / "open gmail"
- "open whatsapp" / "open facebook"

Hinglish:
- "youtube kholo" / "google kholo" / "gmail kholo"
```

### 🌤️ Weather Commands

```
English:
- "what's the weather?"
- "weather in Delhi"
- "weather in Delhi and Mumbai"

Hinglish:
- "mausam kaisa hai?"
- "Delhi ka mausam batao"
- "Delhi aur Mumbai ka mausam"
```

### 🔊 Volume Control

```
English:
- "volume up" - Increase by 10%
- "volume down" - Decrease by 10%
- "mute volume" - Mute audio

Hinglish:
- "volume badhao"
- "volume kam karo"
- "volume mute karo"
```

### 💬 Conversation

```
English:
- "hello" / "hi" / "hey"
- "how are you?"
- "who are you?"
- "thank you"

Hinglish:
- "namaste" / "kaise ho?"
- "tum kaun ho?"
- "shukriya"
```

---

## 🔒 Security

### Version 3.1 Security Improvements

VEDA AI v3.1 includes comprehensive security hardening:

#### ✅ Fixed Vulnerabilities
- **Exposed API Keys** - Removed from repository
- **Command Injection** - Comprehensive input sanitization
- **CORS Misconfiguration** - Restricted to local origins only
- **WebSocket Validation** - Enhanced message validation
- **Deprecated APIs** - Updated to modern standards

#### 🛡️ Security Features
- **Input Sanitization** - Removes dangerous characters
- **Command Validation** - Blocks malicious patterns
- **Secure CORS** - Specific origins only
- **Comprehensive Logging** - All security events logged
- **Error Handling** - No sensitive information in errors

### Security Best Practices

1. **Never commit `.env` file**
   ```bash
   # Verify it's in .gitignore
   cat .gitignore | grep .env
   ```

2. **Use strong API keys**
   - Generate new keys from official dashboards
   - Rotate keys regularly
   - Never share keys publicly

3. **Keep dependencies updated**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Review logs regularly**
   ```bash
   type logs\veda_ai.log
   ```

### Reporting Security Issues

If you discover a security vulnerability:
1. **DO NOT** create a public issue
2. Email: security@veda-ai.com (if available)
3. Or create a private security advisory on GitHub

For detailed security information, see [BUGS.md](BUGS.md)

---

## 🐛 Troubleshooting

### Voice Not Working?

#### Quick Fix (Recommended)
```bash
python fix_microphone.py
```

#### Manual Steps
1. **Check Microphone Permissions**
   - Windows Settings > Privacy > Microphone
   - Enable "Allow apps to access your microphone"

2. **Calibrate Voice**
   - Click "🎯 Calibrate Voice" button
   - OR run: `python calibrate_voice.py`

3. **Test Microphone**
   ```bash
   python test_microphone.py
   ```

### Commands Not Recognized?

1. **Check Internet Connection** - Voice recognition requires internet
2. **Try Text Commands** - Verify VEDA is working
3. **Check Logs** - View `logs/veda_ai.log` for errors

### Application Won't Start?

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Check Python Version**
   ```bash
   python --version  # Should be 3.8+
   ```

3. **Port Already in Use**
   ```bash
   python run_veda_ai.py --port 8001
   ```

---

## 📚 Documentation

- **[BUGS.md](BUGS.md)** - Security audit and bug fixes (READ THIS FIRST!)
- **[HOW_TO_USE_VEDA.md](HOW_TO_USE_VEDA.md)** - Detailed usage guide (Hinglish)
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[SYSTEM_COMMANDS_REFERENCE.md](SYSTEM_COMMANDS_REFERENCE.md)** - Complete command list
- **[SYSTEM_CONTROL_GUIDE.md](SYSTEM_CONTROL_GUIDE.md)** - System control guide
- **[VEDA_AI_COMPLETE_GUIDE.md](VEDA_AI_COMPLETE_GUIDE.md)** - Complete documentation
- **API Documentation** - Available at `/docs` when running

---

## 🏗️ Architecture

### Technology Stack

#### Backend
- **FastAPI** - Modern web framework
- **Python 3.8+** - Core language
- **SpeechRecognition** - Voice input processing
- **pyttsx3** - Text-to-speech engine
- **OpenAI API** - Advanced AI responses

#### Frontend
- **HTML5/CSS3** - Modern UI
- **JavaScript** - Interactive features
- **WebSocket** - Real-time communication

#### Security
- **Input Sanitization** - Protection against injection
- **Command Validation** - Malicious pattern detection
- **Secure CORS** - Restricted origins
- **Comprehensive Logging** - Security event tracking

---

## 📊 Performance

### Voice Recognition
- **Accuracy**: 90-95% (after calibration)
- **Response Time**: 2-5 seconds
- **Languages**: English, Hindi, Hinglish

### System Requirements
- **CPU**: Minimal usage (<5%)
- **RAM**: ~200MB
- **Storage**: ~500MB (with dependencies)
- **Network**: Optional (for online features)

---

## 🛣️ Roadmap

### Upcoming Features
- [ ] Mobile app (Android/iOS)
- [ ] Multi-language support
- [ ] Smart home integration
- [ ] Calendar and reminder system
- [ ] Voice authentication
- [ ] Cloud sync

### Known Limitations
- **Gesture Control**: Experimental (basic functionality only)
- **Wake Word**: Requires Picovoice API key
- **Voice Recognition**: Requires internet for best accuracy
- **System Commands**: Windows-only (Linux/Mac support planned)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repo
git clone https://github.com/yourusername/veda-ai.git
cd veda-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python run_veda_ai.py --debug
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - For GPT-4 API
- **Google** - For Speech Recognition API
- **Picovoice** - For wake word detection
- **FastAPI** - For the amazing web framework
- **Iron Man** - For JARVIS inspiration

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/veda-ai/issues)
- **Security**: See [BUGS.md](BUGS.md) for security reporting
- **Documentation**: [Wiki](https://github.com/yourusername/veda-ai/wiki)

---

## ⚠️ Important Notes

### Security
- **NEVER** commit your `.env` file
- **ALWAYS** use environment variables for secrets
- **REVIEW** [BUGS.md](BUGS.md) for security information
- **UPDATE** dependencies regularly

### API Keys
- Get OpenAI API key from: https://platform.openai.com/api-keys
- Get Picovoice key from: https://console.picovoice.ai/

### System Commands
- Some commands require administrator privileges
- Shutdown/Restart commands have 5-second warnings
- WiFi control requires admin rights

---

<div align="center">

**Made with ❤️ in India 🇮🇳**

**VEDA AI - Your Intelligent Bilingual Assistant**

**Version 3.1 - Security Hardened**

[⬆ Back to Top](#-veda-ai---your-intelligent-bilingual-assistant)

</div>

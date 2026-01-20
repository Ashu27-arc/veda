# VEDA AI - Pending Tasks & Improvements (Kamiyan)

> Last Updated: January 2026  
> Version: 5.0

---

## 1. Backend Issues (Python)

### 1.1 Voice Recognition Issues
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| Voice recognition fails in noisy environment | `voice_advanced.py` | HIGH | Pending |
| No fallback to offline speech recognition | `voice_advanced.py` | MEDIUM | Pending |
| Google Speech API dependency (needs internet) | `voice_advanced.py` | HIGH | Pending |
| No Vosk/Whisper offline integration | `voice_advanced.py` | MEDIUM | Pending |
| Speech synthesis (`pyttsx3`) blocks main thread | `voice_advanced.py` | LOW | Pending |

**Suggested Fix:**
```python
# Add Vosk for offline recognition
# pip install vosk
from vosk import Model, KaldiRecognizer
# Use Whisper for better accuracy
# pip install openai-whisper
```

---

### 1.2 AI Engine Limitations
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| LM Studio dependency (external app required) | `ai_engine.py`, `lm_studio_ai.py` | HIGH | ✅ FIXED |
| No GPT/Claude API integration option | `ai_engine.py` | MEDIUM | ✅ FIXED |
| Self-learning is basic (exact/partial match only) | `self_learning.py` | MEDIUM | ✅ FIXED |
| No semantic similarity for learned responses | `self_learning.py` | MEDIUM | ✅ FIXED |
| Hugging Face models not pre-configured | `huggingface_ai.py` | LOW | Pending |
| No conversation context memory (multi-turn) | `ai_engine.py` | HIGH | ✅ FIXED |

**✅ IMPLEMENTED - New ML Features (v6.0):**
```python
# New files added:
# - ml_config.py           - ML configuration
# - ai_providers.py        - OpenAI, Claude, Groq integration
# - intent_classifier.py   - Intent classification
# - conversation_memory.py - Multi-turn context memory
# - semantic_search.py     - Semantic similarity search
# - sentiment_analyzer.py  - User mood detection
# - ai_engine_ml.py        - Enhanced AI engine
```

---

### 1.3 System Control Limitations
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| Only Windows supported (no Linux/Mac) | `system_control.py` | LOW | Pending |
| Volume control fails on some systems | `system_control.py` | MEDIUM | Pending |
| No brightness control implemented | `system_control.py` | MEDIUM | Pending |
| App finder misses some installed apps | `system_control.py` | LOW | Pending |
| No Bluetooth control | `system_control.py` | LOW | Pending |
| No display/monitor control | `system_control.py` | LOW | Pending |

---

### 1.4 Gesture Control Issues
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| Opens separate OpenCV window (not integrated in UI) | `gesture_control.py` | HIGH | Pending |
| MediaPipe version compatibility issues | `gesture_control.py` | MEDIUM | Pending |
| Limited gesture vocabulary (only 7 gestures) | `gesture_control.py` | LOW | Pending |
| No custom gesture training | `gesture_control.py` | LOW | Pending |
| High CPU usage during gesture detection | `gesture_control.py` | MEDIUM | Pending |

---

### 1.5 Weather Module
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| API key hardcoded or missing | `weather.py` | HIGH | Pending |
| No weather alerts/notifications | `weather.py` | LOW | Pending |
| Limited to current weather (no forecast) | `weather.py` | MEDIUM | Pending |

---

### 1.6 Security Issues
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| No authentication for API endpoints | `main.py` | HIGH | Pending |
| WebSocket has no rate limiting | `main.py` | MEDIUM | Pending |
| CORS allows localhost only (good but no production config) | `main.py` | LOW | Pending |
| No input sanitization for file paths | `system_control.py` | HIGH | Pending |
| Command injection possible via subprocess | `system_control.py` | HIGH | Pending |

---

## 2. Frontend Issues (JavaScript/HTML/CSS)

### 2.1 UI/UX Issues
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| Mobile responsive design incomplete | `style.css` | HIGH | Pending |
| No dark/light theme toggle | `style.css`, `app.js` | MEDIUM | Pending |
| Chat history not persistent (lost on refresh) | `app.js` | HIGH | Pending |
| No typing indicator while AI is thinking | `app.js` | MEDIUM | Pending |
| Suggestions panel UI incomplete | `app.js` | LOW | Pending |
| No keyboard shortcuts documentation | `index.html` | LOW | Pending |

---

### 2.2 Camera Integration
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| Camera preview in UI, but no actual gesture processing | `app.js`, `index.html` | HIGH | Pending |
| No camera permission error handling message | `app.js` | MEDIUM | Pending |
| Camera feed not connected to backend gesture control | `app.js` | HIGH | Pending |

---

### 2.3 WebSocket Issues
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| Max 5 reconnect attempts only | `app.js` | LOW | Pending |
| No exponential backoff for reconnection | `app.js` | LOW | Pending |
| Connection status not shown clearly | `app.js` | MEDIUM | Pending |

---

### 2.4 Automation Panel
| Issue | File | Priority | Status |
|-------|------|----------|--------|
| Shortcuts list not loading (`loadShortcuts` is placeholder) | `app.js` | MEDIUM | Pending |
| No task edit functionality (only add/delete) | `app.js` | LOW | Pending |
| No task execution history | `app.js` | LOW | Pending |

---

## 3. Missing Features

### 3.1 Core Features Missing
| Feature | Description | Priority |
|---------|-------------|----------|
| **Wake Word Detection** | "Hey VEDA" wake word (file exists but not integrated) | HIGH |
| **Conversation Memory** | Remember context across conversations | HIGH |
| **Multi-language TTS** | Hindi text-to-speech support | MEDIUM |
| **Email Integration** | Send/read emails | MEDIUM |
| **Calendar Integration** | Google/Outlook calendar | MEDIUM |
| **Reminder System** | Set reminders with notifications | HIGH |
| **Note Taking** | Voice notes, quick notes | MEDIUM |
| **Smart Home Control** | IoT device control (Alexa/Google Home) | LOW |

---

### 3.2 Automation Features Missing
| Feature | Description | Priority |
|---------|-------------|----------|
| **Workflow Automation** | Multi-step automated workflows | MEDIUM |
| **Conditional Actions** | If-then-else automation rules | MEDIUM |
| **Trigger-based Actions** | Time, location, app-based triggers | MEDIUM |
| **Macro Recording** | Record and replay mouse/keyboard actions | LOW |

---

### 3.3 AI/ML Features Missing
| Feature | Description | Priority | Status |
|---------|-------------|----------|--------|
| **Intent Classification** | Better command understanding | HIGH | ✅ DONE |
| **Named Entity Recognition** | Extract names, dates, locations | MEDIUM | ✅ PARTIAL |
| **Sentiment Analysis** | Understand user mood | LOW | ✅ DONE |
| **Voice Cloning** | Custom voice for TTS | LOW | Pending |
| **Face Recognition** | Identify users | LOW | Pending |
| **Conversation Memory** | Multi-turn context | HIGH | ✅ DONE |
| **Semantic Search** | Find similar responses | HIGH | ✅ DONE |
| **Multi-Provider AI** | OpenAI, Claude, Groq support | MEDIUM | ✅ DONE |

---

## 4. Code Quality Issues

### 4.1 General Issues
| Issue | Priority |
|-------|----------|
| No unit tests | HIGH |
| No integration tests | HIGH |
| No type hints (Python) | MEDIUM |
| Inconsistent error handling | MEDIUM |
| No API documentation (Swagger/OpenAPI) | MEDIUM |
| No logging levels configuration | LOW |
| Hardcoded values (should be in config) | MEDIUM |

---

### 4.2 Documentation Missing
| Document | Description | Priority |
|----------|-------------|----------|
| API Documentation | All endpoints with examples | HIGH |
| Architecture Diagram | System design overview | MEDIUM |
| Contribution Guide | How to contribute | LOW |
| Code Style Guide | Coding standards | LOW |
| Deployment Guide | Production deployment | MEDIUM |

---

## 5. Dependencies Issues

### 5.1 Version Conflicts
```txt
# requirements.txt - No versions specified
# Should be:
fastapi==0.109.0
uvicorn[standard]==0.27.0
speechrecognition==3.10.1
pyttsx3==2.90
pyaudio==0.2.14
# ... etc
```

### 5.2 Missing Optional Dependencies
```txt
# For offline voice recognition
vosk==0.3.45
openai-whisper==20231117

# For better AI
sentence-transformers==2.2.2
openai==1.10.0
anthropic==0.18.0

# For testing
pytest==7.4.0
pytest-asyncio==0.23.0
httpx==0.26.0
```

---

## 6. Deployment Issues

| Issue | Priority |
|-------|----------|
| No Docker configuration | MEDIUM |
| No CI/CD pipeline | MEDIUM |
| No production config (only localhost) | HIGH |
| No environment variables for secrets | HIGH |
| No logging to file/service | MEDIUM |
| No health monitoring/alerting | LOW |

---

## 7. Quick Win Improvements (Easy to Fix)

### Priority 1 - Can be fixed in 1 day:
1. Add `.env` support for API keys and secrets
2. Add version numbers to requirements.txt
3. Add basic unit tests for AI engine
4. Fix mobile responsive CSS
5. Add typing indicator in UI
6. Persist chat history in localStorage

### Priority 2 - Can be fixed in 1 week:
1. Add OpenAI/Claude API integration
2. Implement wake word detection
3. Add reminder system
4. Create Docker configuration
5. Add Vosk offline speech recognition

### Priority 3 - Long term:
1. Implement conversation memory
2. Add multi-language TTS
3. Create mobile app
4. Add smart home integration
5. Implement workflow automation

---

## 8. File-wise Summary

| File | Issues Count | Critical |
|------|-------------|----------|
| `ai_engine.py` | 6 | 2 |
| `voice_advanced.py` | 5 | 2 |
| `system_control.py` | 8 | 2 |
| `gesture_control.py` | 5 | 1 |
| `main.py` | 4 | 2 |
| `self_learning.py` | 3 | 0 |
| `app.js` | 8 | 2 |
| `style.css` | 3 | 1 |
| `index.html` | 2 | 1 |

---

## 9. How to Use This Document

1. **Pick issues by priority** - Start with HIGH priority items
2. **Update status** - Change "Pending" to "In Progress" or "Done"
3. **Add new issues** - Found a bug? Add it here
4. **Track progress** - Use this as your development roadmap

---

## 10. Contributors

*Add your name when you fix an issue!*

| Name | Issues Fixed | Date |
|------|-------------|------|
| - | - | - |

---

**Made with ❤️ for VEDA AI Development Team**

*"Every bug fixed is a step towards perfection."*

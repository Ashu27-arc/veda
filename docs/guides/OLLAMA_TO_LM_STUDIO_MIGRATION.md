# 🔄 Ollama to LM Studio Migration Guide

## 📋 Why Migrate?

VEDA AI has been updated to use **LM Studio** instead of Ollama for better:
- ✅ **Ease of Use** - GUI instead of CLI
- ✅ **Windows Support** - Better integration
- ✅ **Model Management** - Visual interface
- ✅ **OpenAI Compatibility** - Standard API format
- ✅ **Performance** - Optimized for Windows

---

## 🎯 What Changed?

### Files Renamed:
- `ollama_ai.py` → `lm_studio_ai.py`
- `ollama_training_data.txt` → `lm_studio_training_data.txt`

### Configuration Updated:
- `.env` file now uses `LM_STUDIO_*` variables
- `config.py` updated with LM Studio settings
- `ai_engine.py` imports updated

### Backward Compatibility:
- ✅ Old `ollama_response()` function still works
- ✅ Old config variables mapped to new ones
- ✅ No breaking changes to existing code

---

## 🚀 Migration Steps

### Step 1: Uninstall Ollama (Optional)

If you want to completely remove Ollama:

**Windows:**
```bash
# Stop Ollama service
taskkill /F /IM ollama.exe

# Uninstall from Control Panel
# Or delete Ollama folder
```

**Note:** You can keep Ollama installed if you want. VEDA AI will use LM Studio by default.

### Step 2: Install LM Studio

1. Download from: https://lmstudio.ai/
2. Run installer
3. Launch LM Studio

### Step 3: Download a Model

**Recommended for VEDA AI:**
- **Phi-3 Mini** (2GB) - Fast, good for low-end PCs
- **Llama 3.2 3B** (2-4GB) - Balanced
- **Mistral 7B** (4-8GB) - Best quality

**How to download:**
1. Open LM Studio
2. Go to "Discover" tab
3. Search for model (e.g., "Phi-3")
4. Download GGUF format, Q4_K_M quantization

### Step 4: Start LM Studio Server

1. Go to "Local Server" tab
2. Select and load your model
3. Click "Start Server"
4. Verify server is running on port 1234

### Step 5: Update VEDA AI Configuration

Your `.env` file is already updated! Just verify:

```env
# LM Studio Configuration
AI_MODE=self_training
LM_STUDIO_MODEL=local-model
LM_STUDIO_API_URL=http://localhost:1234
LM_STUDIO_TIMEOUT=60
LM_STUDIO_MAX_RETRIES=2
```

### Step 6: Test VEDA AI

```bash
# Start VEDA AI
start_veda_fixed.bat

# Try a command
"Hello VEDA"

# Check logs for:
"Using LM Studio model: local-model"
```

---

## 📊 Comparison: Before vs After

### Before (Ollama):
```bash
# Install Ollama
ollama serve

# Download model
ollama pull llama2

# Create custom model
ollama create veda-custom -f Modelfile

# Use in VEDA AI
# Requires CLI knowledge
```

### After (LM Studio):
```bash
# Install LM Studio (GUI)
# Download model (GUI)
# Load model (GUI)
# Start server (GUI)
# Use in VEDA AI
# No CLI knowledge needed!
```

---

## 🔧 Configuration Mapping

### Old (Ollama) → New (LM Studio)

| Ollama | LM Studio | Notes |
|--------|-----------|-------|
| `OLLAMA_MODEL` | `LM_STUDIO_MODEL` | Model name |
| `OLLAMA_API_URL` | `LM_STUDIO_API_URL` | API endpoint |
| `OLLAMA_TIMEOUT` | `LM_STUDIO_TIMEOUT` | Request timeout |
| `OLLAMA_MAX_RETRIES` | `LM_STUDIO_MAX_RETRIES` | Retry count |
| `http://localhost:11434` | `http://localhost:1234` | Default port |

### Backward Compatibility:

Old code still works! The system automatically maps:
```python
# Old code (still works)
from python_backend.ollama_ai import ollama_response
response = ollama_response("Hello")

# New code (recommended)
from python_backend.lm_studio_ai import lm_studio_response
response = lm_studio_response("Hello")
```

---

## 🎯 Model Equivalents

### Ollama Model → LM Studio Equivalent

| Ollama | LM Studio | Size | Notes |
|--------|-----------|------|-------|
| `llama2` | Llama 3.2 3B | ~2GB | Better, newer |
| `mistral` | Mistral 7B | ~4GB | Same quality |
| `codellama` | CodeLlama 7B | ~4GB | Same |
| `phi` | Phi-3 Mini | ~2GB | Faster |
| `tinyllama` | TinyLlama | ~1GB | Same |

---

## 🐛 Troubleshooting

### Problem 1: "Ollama not running" error

**Cause:** Old code trying to use Ollama

**Solution:**
1. Make sure LM Studio server is running
2. Check `.env` has `LM_STUDIO_API_URL=http://localhost:1234`
3. Restart VEDA AI

### Problem 2: Import errors

**Cause:** Old imports

**Solution:**
```python
# Change this:
from python_backend.ollama_ai import ollama_response

# To this:
from python_backend.lm_studio_ai import lm_studio_response
```

### Problem 3: Port conflict

**Cause:** Ollama still running on port 11434

**Solution:**
```bash
# Stop Ollama
taskkill /F /IM ollama.exe

# Or change LM Studio port in settings
```

### Problem 4: Model not found

**Cause:** Model name mismatch

**Solution:**
1. Check loaded model name in LM Studio
2. Update `LM_STUDIO_MODEL` in `.env`
3. Or use `local-model` (default)

---

## 💡 Benefits of Migration

### Performance:
- ✅ Faster startup
- ✅ Better Windows optimization
- ✅ GPU acceleration (if available)

### Usability:
- ✅ Visual model management
- ✅ No CLI commands needed
- ✅ Real-time monitoring
- ✅ Easy model switching

### Compatibility:
- ✅ OpenAI API format
- ✅ Better integration with VEDA AI
- ✅ Standard error handling

### Features:
- ✅ Built-in model browser
- ✅ Chat interface for testing
- ✅ Model comparison
- ✅ Performance metrics

---

## 📚 Additional Resources

### LM Studio:
- **Website:** https://lmstudio.ai/
- **Setup Guide:** See `LM_STUDIO_SETUP.md`
- **Hindi Guide:** See `LM_STUDIO_SETUP_HINDI.md`

### VEDA AI:
- **Documentation:** See `DOCUMENTATION.md`
- **Quick Start:** See `START_HERE.txt`
- **Browser Fix:** See `BROWSER_FIX_GUIDE.md`

---

## ✅ Migration Checklist

- [ ] Install LM Studio
- [ ] Download a model (Phi-3 Mini recommended)
- [ ] Load model in LM Studio
- [ ] Start LM Studio server (port 1234)
- [ ] Verify `.env` configuration
- [ ] Stop Ollama (optional)
- [ ] Test VEDA AI with `start_veda_fixed.bat`
- [ ] Verify logs show "Using LM Studio model"
- [ ] Test commands work properly
- [ ] Delete Ollama (optional)

---

## 🎊 Conclusion

Migration from Ollama to LM Studio is:
- ✅ **Easy** - Just install and run
- ✅ **Safe** - Backward compatible
- ✅ **Better** - Improved performance and usability
- ✅ **Free** - No cost

**Recommended:** Complete migration for best experience!

---

**Version:** 1.0  
**Date:** January 2026  
**Status:** ✅ Production Ready  
**Tested:** Windows 10/11

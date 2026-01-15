# 🚀 LM Studio Setup Guide for VEDA AI

## 📋 What is LM Studio?

LM Studio is a desktop application that lets you run local AI models (LLMs) on your computer. It's:
- ✅ **Free and Open Source**
- ✅ **Easy to Use** - GUI interface
- ✅ **Fast** - Optimized for local inference
- ✅ **OpenAI Compatible** - Works with OpenAI API format
- ✅ **No Internet Required** - Fully offline
- ✅ **Privacy Focused** - Your data stays on your computer

## 🎯 Why LM Studio over Ollama?

| Feature | LM Studio | Ollama |
|---------|-----------|--------|
| GUI Interface | ✅ Yes | ❌ No (CLI only) |
| Model Discovery | ✅ Built-in browser | ❌ Manual download |
| OpenAI API | ✅ Yes | ❌ Custom format |
| Easy Setup | ✅ Very easy | ⚠️ Requires CLI knowledge |
| Model Management | ✅ Visual | ❌ Command-line |
| Windows Support | ✅ Excellent | ⚠️ Limited |

---

## 📥 Installation

### Step 1: Download LM Studio

1. Visit: https://lmstudio.ai/
2. Click "Download for Windows"
3. Run the installer
4. Follow installation wizard

### Step 2: Launch LM Studio

1. Open LM Studio from Start Menu
2. You'll see the main interface with:
   - 🔍 **Discover** - Browse models
   - 💬 **Chat** - Test models
   - 🔌 **Local Server** - API server
   - ⚙️ **Settings** - Configuration

---

## 🤖 Downloading Models

### Recommended Models for VEDA AI:

#### 1. **Phi-3 Mini (Best for Speed)** ⭐⭐⭐⭐⭐
- **Size:** ~2GB
- **Speed:** Very Fast
- **Quality:** Good
- **RAM:** 4GB minimum
- **Search:** "microsoft/Phi-3-mini-4k-instruct-gguf"

#### 2. **Llama 3.2 (Best Balance)** ⭐⭐⭐⭐
- **Size:** ~2-4GB
- **Speed:** Fast
- **Quality:** Excellent
- **RAM:** 8GB recommended
- **Search:** "llama-3.2-3b-instruct"

#### 3. **Mistral 7B (Best Quality)** ⭐⭐⭐⭐⭐
- **Size:** ~4-8GB
- **Speed:** Medium
- **Quality:** Excellent
- **RAM:** 8GB minimum
- **Search:** "mistral-7b-instruct"

### How to Download:

1. Click **"Discover"** tab
2. Search for model name (e.g., "Phi-3")
3. Click on the model
4. Select **GGUF** format
5. Choose quantization:
   - **Q4_K_M** - Good balance (recommended)
   - **Q5_K_M** - Better quality, slower
   - **Q8_0** - Best quality, slowest
6. Click **"Download"**
7. Wait for download to complete

---

## 🔌 Starting the Local Server

### Step 1: Load a Model

1. Go to **"Local Server"** tab
2. Click **"Select a model to load"**
3. Choose your downloaded model
4. Click **"Load Model"**
5. Wait for model to load (shows "Model loaded" when ready)

### Step 2: Start Server

1. Click **"Start Server"** button
2. Server will start on `http://localhost:1234`
3. You'll see: ✅ **"Server running on port 1234"**

### Step 3: Verify Server

1. Server should show:
   ```
   ✅ Server running
   📡 http://localhost:1234
   🤖 Model: [your-model-name]
   ```

---

## ⚙️ VEDA AI Configuration

### Your `.env` file is already configured:

```env
# LM Studio Configuration
AI_MODE=self_training
LM_STUDIO_MODEL=local-model
LM_STUDIO_API_URL=http://localhost:1234
LM_STUDIO_TIMEOUT=60
LM_STUDIO_MAX_RETRIES=2
```

### No changes needed! Just:
1. Start LM Studio
2. Load a model
3. Start the server
4. Run VEDA AI

---

## 🧪 Testing

### Test 1: Check if LM Studio is Running

Open browser and visit:
```
http://localhost:1234/v1/models
```

You should see JSON response with model info.

### Test 2: Test with VEDA AI

1. Start LM Studio server
2. Run VEDA AI:
   ```bash
   start_veda_fixed.bat
   ```
3. Try a command:
   ```
   "Hello VEDA"
   ```
4. Check logs for:
   ```
   Using LM Studio model: local-model
   ```

---

## 🎯 Model Selection Guide

### For Low-End PCs (4GB RAM):
- ✅ Phi-3 Mini Q4_K_M (~2GB)
- ✅ TinyLlama Q4_K_M (~1GB)

### For Mid-Range PCs (8GB RAM):
- ✅ Llama 3.2 3B Q4_K_M (~2GB)
- ✅ Phi-3 Medium Q5_K_M (~3GB)
- ✅ Mistral 7B Q4_K_M (~4GB)

### For High-End PCs (16GB+ RAM):
- ✅ Llama 3.1 8B Q5_K_M (~6GB)
- ✅ Mistral 7B Q8_0 (~8GB)
- ✅ Mixtral 8x7B Q4_K_M (~26GB)

---

## 🔧 Troubleshooting

### Problem 1: "LM Studio not running"

**Solution:**
1. Open LM Studio
2. Go to "Local Server" tab
3. Load a model
4. Click "Start Server"
5. Verify server is running (green indicator)

### Problem 2: "Connection refused"

**Solution:**
1. Check if LM Studio server is running
2. Verify port 1234 is not blocked
3. Check firewall settings
4. Restart LM Studio

### Problem 3: "Model not loaded"

**Solution:**
1. Go to LM Studio "Local Server" tab
2. Click "Select a model to load"
3. Choose a downloaded model
4. Wait for "Model loaded" message

### Problem 4: "Slow responses"

**Solution:**
1. Use a smaller model (Phi-3 Mini)
2. Use lower quantization (Q4_K_M instead of Q8_0)
3. Close other applications
4. Increase `LM_STUDIO_TIMEOUT` in `.env`

### Problem 5: "Out of memory"

**Solution:**
1. Use a smaller model
2. Close other applications
3. Restart your computer
4. Use Q4_K_M quantization

---

## 💡 Pro Tips

### 1. Model Management
- Keep 2-3 models downloaded
- Use Phi-3 for speed, Mistral for quality
- Delete unused models to save space

### 2. Performance Optimization
- Use Q4_K_M for best speed/quality balance
- Enable GPU acceleration in LM Studio settings
- Close unnecessary applications

### 3. Server Settings
- Keep server running in background
- Set to auto-start with Windows (optional)
- Monitor RAM usage

### 4. VEDA AI Integration
- Test with simple commands first
- Check logs for errors
- Adjust timeout if needed

---

## 📊 Comparison: LM Studio vs Ollama

### LM Studio Advantages:
✅ Easy GUI interface  
✅ Built-in model browser  
✅ Visual model management  
✅ OpenAI-compatible API  
✅ Better Windows support  
✅ Real-time monitoring  

### Ollama Advantages:
✅ Lighter weight  
✅ Command-line control  
✅ Better for servers  
✅ Scriptable  

**For VEDA AI, LM Studio is recommended** because:
- Easier for beginners
- Better Windows integration
- Visual feedback
- OpenAI-compatible (easier to code)

---

## 🚀 Quick Start Checklist

- [ ] Download LM Studio from https://lmstudio.ai/
- [ ] Install LM Studio
- [ ] Download a model (Phi-3 Mini recommended)
- [ ] Load model in "Local Server" tab
- [ ] Start server (port 1234)
- [ ] Verify server at http://localhost:1234/v1/models
- [ ] Run VEDA AI with `start_veda_fixed.bat`
- [ ] Test with "Hello VEDA"
- [ ] Check logs for "Using LM Studio model"

---

## 📚 Additional Resources

- **LM Studio Website:** https://lmstudio.ai/
- **LM Studio Discord:** https://discord.gg/lmstudio
- **Model Hub:** https://huggingface.co/models?library=gguf
- **VEDA AI Docs:** See `DOCUMENTATION.md`

---

## 🎊 Benefits for VEDA AI

With LM Studio, VEDA AI gets:
- ✅ **100% Privacy** - No data sent to cloud
- ✅ **No API Costs** - Completely free
- ✅ **Offline Mode** - Works without internet
- ✅ **Fast Responses** - Local inference
- ✅ **Customizable** - Choose your own models
- ✅ **Hindi Support** - Works with multilingual models

---

**Version:** 1.0  
**Date:** January 2026  
**Status:** ✅ Production Ready  
**Tested:** Windows 10/11

# VEDA AI Free Hosting Guide

## Important Note
Voice features (microphone) will NOT work on cloud hosting because:
- Browser cannot stream audio to cloud server
- PyAudio requires local system access
- Speech recognition needs local microphone

**Cloud version will only have TEXT CHAT functionality.**

---

## Option 1: Railway.app (Recommended - Easiest)

### Steps:
1. **GitHub pe push karo:**
   ```bash
   git add .
   git commit -m "Add deployment files"
   git push origin master
   ```

2. **Railway signup:**
   - Go to https://railway.app
   - Sign up with GitHub

3. **Deploy:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your veda repository
   - Railway will auto-detect Python

4. **Environment Setup:**
   - Go to Settings > Variables
   - Add: `PORT=8000`

5. **Get your URL:**
   - Railway will give you: `https://veda-production-xxxx.up.railway.app`

### Cost: FREE (500 hours/month)

---

## Option 2: Render.com

### Steps:
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New" > "Web Service"
4. Connect your repo
5. Settings:
   - Build Command: `pip install -r requirements-cloud.txt`
   - Start Command: `uvicorn python_backend.main:app --host 0.0.0.0 --port $PORT`

### Cost: FREE (750 hours/month, sleeps after 15 min inactivity)

---

## Option 3: Fly.io

### Steps:
1. Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
2. Run:
   ```bash
   fly auth signup
   fly launch
   fly deploy
   ```

### Cost: FREE (3 shared VMs)

---

## Option 4: Vercel (Frontend Only)

Vercel is for static frontend only. You would need to separate frontend and backend.

---

## Option 5: Oracle Cloud (Always Free Forever)

### Steps:
1. Sign up at https://www.oracle.com/cloud/free/
2. Create a Compute instance (Always Free eligible)
3. SSH into instance
4. Install Python and clone repo
5. Run with: `uvicorn python_backend.main:app --host 0.0.0.0 --port 8000`

### Cost: ALWAYS FREE (2 VMs, 1GB RAM each)

---

## Quick Comparison

| Platform | Free Tier | Sleep? | Best For |
|----------|-----------|--------|----------|
| Railway | 500 hrs/month | No | Easy deployment |
| Render | 750 hrs/month | Yes (15 min) | Hobby projects |
| Fly.io | 3 VMs | No | Global reach |
| Oracle | Always free | No | Long-term hosting |

---

## Making Voice Work (Advanced)

To make voice work on cloud, you would need:
1. Use Web Speech API (browser-based recognition)
2. Send text commands to server
3. This requires frontend changes

### Web Speech API Changes (frontend):
```javascript
// In app.js - Browser-based speech recognition
const recognition = new webkitSpeechRecognition();
recognition.lang = 'hi-IN'; // Hindi
recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    // Send text to server via WebSocket
    ws.send(text);
};
recognition.start();
```

This way, speech recognition happens in browser (free) and only text goes to server.

---

## Recommended: Railway.app

Railway is the easiest and most reliable for beginners:
1. Connect GitHub
2. Auto-deploy on push
3. Free SSL certificate
4. Custom domain support
5. No sleep time

Go to: https://railway.app

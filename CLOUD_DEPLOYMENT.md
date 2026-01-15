# VEDA AI - Cloud Deployment Guide

## ⚠️ Important Notice

VEDA AI ek desktop application hai. Cloud pe deploy karne se:
- ❌ Voice recognition kaam nahi karega (microphone local machine pe hai)
- ❌ System commands kaam nahi karenge (apps user ke machine pe khulne chahiye)
- ✅ Sirf AI chat functionality kaam karegi

## 🌐 Cloud Deployment Options

### Option 1: Heroku Deployment

1. **Heroku Account Banao**: https://heroku.com

2. **Heroku CLI Install Karo**:
```bash
# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

3. **Project Setup**:
```bash
# Procfile banao
echo "web: uvicorn python_backend.main:app --host 0.0.0.0 --port $PORT" > Procfile

# runtime.txt banao
echo "python-3.11.0" > runtime.txt
```

4. **Deploy Karo**:
```bash
heroku login
heroku create veda-ai-app
git push heroku main
```

### Option 2: AWS EC2 Deployment

1. **EC2 Instance Launch Karo**:
   - Ubuntu 22.04 LTS
   - t2.micro (free tier)
   - Security Group: Port 80, 443, 5000 open

2. **Server Setup**:
```bash
# SSH se connect karo
ssh -i your-key.pem ubuntu@your-ec2-ip

# Dependencies install karo
sudo apt update
sudo apt install python3-pip python3-venv nginx -y

# Project upload karo (Git ya SCP se)
git clone your-repo-url
cd veda-ai

# Virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env file banao
nano .env
# API keys add karo
```

3. **Nginx Configuration**:
```bash
sudo nano /etc/nginx/sites-available/veda-ai
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/veda-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. **Systemd Service Banao**:
```bash
sudo nano /etc/systemd/system/veda-ai.service
```

```ini
[Unit]
Description=VEDA AI Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/veda-ai
Environment="PATH=/home/ubuntu/veda-ai/venv/bin"
ExecStart=/home/ubuntu/veda-ai/venv/bin/python run_veda_ai.py

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable veda-ai
sudo systemctl start veda-ai
sudo systemctl status veda-ai
```

### Option 3: DigitalOcean Droplet

1. **Droplet Create Karo**:
   - Ubuntu 22.04
   - Basic plan ($6/month)
   - Choose datacenter region

2. **Same Steps as AWS EC2** (upar dekho)

### Option 4: Railway.app (Easiest)

1. **Railway Account**: https://railway.app

2. **GitHub Connect Karo**:
   - Repository select karo
   - Automatic deploy hoga

3. **Environment Variables Add Karo**:
   - Dashboard → Variables
   - OPENAI_API_KEY add karo

4. **Deploy!**
   - Automatic build aur deploy hoga
   - Public URL milega

### Option 5: Render.com (Free Tier Available)

1. **Render Account**: https://render.com

2. **New Web Service**:
   - GitHub repo connect karo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn python_backend.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**:
   - OPENAI_API_KEY add karo

4. **Deploy**:
   - Automatic deployment

## 🔧 Modified Code for Cloud Deployment

### Update `python_backend/main.py`:

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cloud deployment ke liye CORS update
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein specific domain use karo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Voice aur system control features disable karo cloud pe
CLOUD_MODE = os.getenv("CLOUD_MODE", "false").lower() == "true"

if CLOUD_MODE:
    print("⚠️ Running in CLOUD MODE - Voice and System features disabled")
```

### Create `Dockerfile` (Optional):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "python_backend.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

## 🚀 Quick Deploy Commands

### Using Docker:
```bash
docker build -t veda-ai .
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key veda-ai
```

### Using PM2 (Process Manager):
```bash
npm install -g pm2
pm2 start "python run_veda_ai.py" --name veda-ai
pm2 save
pm2 startup
```

## 🔒 Security Checklist for Cloud

- [ ] `.env` file ko `.gitignore` mein add karo
- [ ] Environment variables use karo (API keys)
- [ ] HTTPS enable karo (Let's Encrypt)
- [ ] Firewall configure karo
- [ ] Rate limiting add karo
- [ ] CORS properly configure karo
- [ ] Regular backups lo

## 📊 Monitoring

### Logs Check Karo:
```bash
# Systemd service logs
sudo journalctl -u veda-ai -f

# Application logs
tail -f logs/veda_ai.log
```

### Health Check Endpoint:
```python
@app.get("/health")
def health_check():
    return {"status": "healthy", "mode": "cloud"}
```

## 💡 Best Practice

**Recommendation**: VEDA AI ko cloud pe deploy karne ki bajaye:

1. **Local Network Pe Run Karo** - Sabse better option
2. **Desktop App Banao** - PyInstaller se EXE banao
3. **Mobile App Banao** - API expose karo, mobile app se connect karo

Cloud deployment sirf AI chat ke liye useful hai, full features ke liye local deployment best hai.

## 🆘 Support

Agar cloud deployment mein problem aaye to:
- Logs check karo
- Environment variables verify karo
- Port configuration check karo
- Firewall rules verify karo


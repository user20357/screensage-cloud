# 🌐 ScreenSage Architect - Complete Cloud Setup Guide

## 🎯 Perfect for Your Intel Pentium G2020 Setup!

Your hardware is **ideal** for this cloud setup:
- **Your PC**: Development, browser, basic tools
- **Cloud**: All heavy AI processing (YOLO, transformers, etc.)
- **Result**: Professional AI app with zero local GPU requirements!

---

## 📋 **Phase 1: Your Setup Tasks (30 minutes)**

### **1. Get API Keys & Accounts**

#### **OpenRouter.ai (Better than OpenAI)**
```bash
1. Go to: https://openrouter.ai/
2. Sign up with email
3. Go to "Keys" section  
4. Create API key
5. Copy key: sk-or-v1-xxxxx
6. Note: $5 free credit, access to GPT-4, Claude, Llama!
```

#### **GitHub (Code hosting)**
```bash
1. Go to: https://github.com
2. Create account
3. Create repository: "screensage-cloud"
4. Make it public
```

#### **Render (Backend - FREE 750 hours/month)**
```bash
1. Go to: https://render.com
2. Sign up with GitHub
3. No setup needed yet
```

#### **Vercel (Frontend - FREE)**
```bash
1. Go to: https://vercel.com  
2. Sign up with GitHub
3. Install CLI: npm install -g vercel
```

#### **Kaggle (GPU Processing - FREE 30 hours/week)**
```bash
1. Go to: https://kaggle.com
2. Create account
3. Verify phone number (required for GPU)
4. Go to Settings → API → Create New Token
5. Download kaggle.json file
```

#### **HuggingFace (AI Demo - FREE)**
```bash
1. Go to: https://huggingface.co
2. Create account
3. No setup needed yet
```

---

## 🚀 **Phase 2: Cloud Deployment**

### **Step 1: Prepare Your Code**

**On your Intel Pentium G2020 PC:**

```powershell
# 1. Clone the project
cd C:\
git clone https://github.com/yourusername/screensage-cloud.git
cd screensage-cloud

# 2. Copy our optimized code
# (The code is already prepared in w:\ai\website)
```

### **Step 2: Deploy Backend to Render**

```bash
# 1. Create GitHub repository
cd w:\ai\website
git init
git add .
git commit -m "ScreenSage Architect - Cloud Edition"
git remote add origin https://github.com/yourusername/screensage-cloud.git
git push -u origin main

# 2. Deploy on Render
# Go to render.com/dashboard
# Click "New +" → "Web Service"
# Connect GitHub repo
# Settings:
#   Name: screensage-backend
#   Root Directory: backend
#   Build Command: pip install -r requirements_cloud.txt
#   Start Command: python main.py
```

**Environment Variables in Render:**
```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
PORT=8000
CORS_ORIGINS=["https://screensage-frontend.vercel.app"]
DEBUG=false
KAGGLE_API_URL=https://your-kaggle-notebook-url
```

### **Step 3: Deploy Frontend to Vercel**

```powershell
# In your frontend directory
cd w:\ai\website\frontend

# Deploy to Vercel
vercel

# Follow prompts:
# Project name: screensage-frontend
# Directory: ./
# Override settings? N

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://screensage-backend.onrender.com

vercel env add NEXT_PUBLIC_WS_URL
# Enter: wss://screensage-backend.onrender.com/ws

# Deploy production
vercel --prod
```

### **Step 4: Setup Kaggle GPU Processing**

**Create Kaggle Notebook:**

1. **Go to kaggle.com/code**
2. **Create New Notebook**
3. **Settings:**
   - Title: "ScreenSage AI Processor"
   - Language: Python
   - Accelerator: GPU T4 x2 (FREE!)
   - Internet: On

4. **Copy this code to your Kaggle notebook:**

```python
# ScreenSage Architect - Kaggle GPU Processor
# Perfect for Intel Pentium G2020 + Cloud setup!

import torch
import torchvision.transforms as transforms
from transformers import BlipProcessor, BlipForConditionalGeneration
import cv2
import numpy as np
from PIL import Image
import base64
import io
import json
import requests
from typing import Dict, Any, List
import logging
import time
from flask import Flask, request, jsonify
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🚀 ScreenSage Architect - Kaggle GPU Processor")
print(f"GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

class KaggleGPUProcessor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        self.setup_models()
        
    def setup_models(self):
        """Load AI models on GPU"""
        try:
            logger.info("Loading BLIP model...")
            self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            self.blip_model.to(self.device)
            
            logger.info("Loading YOLO model...")
            self.yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            self.yolo_model.to(self.device)
            
            logger.info("✅ All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def process_screenshot(self, image_data: bytes) -> Dict[str, Any]:
        """Process screenshot with GPU acceleration"""
        start_time = time.time()
        
        try:
            image = Image.open(io.BytesIO(image_data))
            logger.info(f"Processing {image.size} image...")
            
            # Generate caption
            inputs = self.blip_processor(image, return_tensors="pt").to(self.device)
            with torch.no_grad():
                out = self.blip_model.generate(**inputs, max_length=50)
            caption = self.blip_processor.decode(out[0], skip_special_tokens=True)
            
            # Detect objects
            img_array = np.array(image)
            with torch.no_grad():
                yolo_results = self.yolo_model(img_array)
            
            objects = []
            for *box, conf, cls in yolo_results.xyxy[0].cpu().numpy():
                if conf > 0.3:
                    objects.append({
                        "class": self.yolo_model.names[int(cls)],
                        "confidence": float(conf),
                        "bbox": [float(x) for x in box]
                    })
            
            processing_time = time.time() - start_time
            
            return {
                "status": "success",
                "caption": caption,
                "objects": objects,
                "processing_time": processing_time,
                "gpu_used": torch.cuda.is_available(),
                "device": str(self.device),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "processing_time": time.time() - start_time
            }

# Initialize processor
processor = KaggleGPUProcessor()

# Flask API
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "gpu_available": torch.cuda.is_available(),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    })

@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        image_data = base64.b64decode(data.get("image", ""))
        result = processor.process_screenshot(image_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

# Start Flask server in background
def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False)

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

print("🎯 Kaggle GPU Processor is running!")
print("API available at: http://localhost:5000")
print("Perfect for your Intel Pentium G2020 setup!")

# Keep notebook running
import time
while True:
    time.sleep(60)
    print(f"✅ GPU Processor running... {time.strftime('%H:%M:%S')}")
```

5. **Run the notebook** - it will start your GPU API server!
6. **Make it public** so your backend can access it
7. **Copy the notebook URL** for your backend configuration

### **Step 5: Setup HuggingFace Demo**

1. **Go to huggingface.co/new-space**
2. **Settings:**
   - Space name: screensage-architect
   - SDK: Gradio
   - Hardware: CPU basic (free)
   - Visibility: Public

3. **Upload files:**
   - Copy `w:\ai\website\ai-models\huggingface_gradio.py` → `app.py`
   - Copy `w:\ai\website\ai-models\requirements.txt` → `requirements.txt`

4. **Your demo will be at:**
   `https://huggingface.co/spaces/yourusername/screensage-architect`

---

## 🎯 **Phase 3: Configuration & Testing**

### **Update Backend Configuration**

**In your Render dashboard, set these environment variables:**

```bash
# OpenRouter.ai API
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini

# Kaggle GPU endpoint
KAGGLE_API_URL=https://your-kaggle-notebook-url/process

# Basic settings
PORT=8000
DEBUG=false
CORS_ORIGINS=["https://screensage-frontend.vercel.app"]
```

### **Test Your Cloud Setup**

1. **Backend Health Check:**
   ```bash
   curl https://screensage-backend.onrender.com/health
   # Should return: {"status":"healthy"}
   ```

2. **Frontend Access:**
   ```bash
   # Open: https://screensage-frontend.vercel.app
   # Should show ScreenSage interface
   ```

3. **Kaggle GPU Test:**
   ```bash
   curl https://your-kaggle-notebook-url/health
   # Should return GPU status
   ```

4. **HuggingFace Demo:**
   ```bash
   # Open: https://huggingface.co/spaces/yourusername/screensage-architect
   # Should show Gradio interface
   ```

---

## 💰 **Cost Breakdown (All FREE!)**

| Service | Free Tier | What You Get |
|---------|-----------|--------------|
| **Render** | 750 hours/month | Backend API hosting |
| **Vercel** | 100GB bandwidth | Frontend hosting |
| **Kaggle** | 30 GPU hours/week | T4 GPU processing |
| **OpenRouter** | $5 free credit | GPT-4, Claude access |
| **HuggingFace** | CPU spaces free | AI demo hosting |

**Total Monthly Cost: $0** 🎉

---

## 🚀 **What You'll Have**

### **✅ Complete Cloud Architecture:**
- **Frontend**: Modern React app on Vercel
- **Backend**: FastAPI server on Render  
- **AI Processing**: GPU-powered Kaggle notebooks
- **Demo**: Public HuggingFace Spaces
- **API**: OpenRouter.ai for multiple AI models

### **✅ Perfect for Your Hardware:**
- **Your Intel Pentium G2020**: Just runs browser + development tools
- **Cloud GPUs**: Handle all heavy AI processing
- **Result**: Professional AI app with zero local requirements!

### **✅ Features Working:**
- Screenshot upload & analysis
- Browser screen capture
- OCR text extraction  
- AI-powered automation suggestions
- Real-time WebSocket communication
- Task creation & management
- Multi-model AI support (GPT-4, Claude, Llama)

---

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **Render deployment fails:**
   ```bash
   # Check build logs in Render dashboard
   # Ensure requirements_cloud.txt is correct
   # Verify Python version compatibility
   ```

2. **Vercel deployment fails:**
   ```bash
   # Check function logs in Vercel dashboard
   # Verify environment variables are set
   # Ensure API URLs are correct
   ```

3. **Kaggle notebook stops:**
   ```bash
   # Kaggle notebooks auto-stop after inactivity
   # Just restart the notebook
   # Consider upgrading to Kaggle Pro for longer sessions
   ```

4. **OpenRouter API errors:**
   ```bash
   # Check API key is correct
   # Verify you have credits remaining
   # Try different model (gpt-4o-mini is cheapest)
   ```

---

## 🎯 **Success Checklist**

- [ ] ✅ OpenRouter.ai API key obtained
- [ ] ✅ All cloud accounts created
- [ ] ✅ Backend deployed to Render
- [ ] ✅ Frontend deployed to Vercel
- [ ] ✅ Kaggle GPU notebook running
- [ ] ✅ HuggingFace demo working
- [ ] ✅ Can upload screenshots and get AI analysis
- [ ] ✅ Browser screen capture works
- [ ] ✅ WebSocket real-time features work

---

## 🎉 **Congratulations!**

You've successfully created a **professional AI-powered automation platform** using:

- **Your Intel Pentium G2020**: Perfect for development
- **Free cloud services**: $0/month operational cost
- **Enterprise-grade AI**: GPT-4, Claude, YOLO, BLIP
- **Modern architecture**: React, FastAPI, WebSockets
- **Global accessibility**: Available worldwide

**Your desktop app is now a cloud service! 🌍**

---

## 📞 **Need Help?**

**Priority debugging order:**
1. Test each service individually
2. Check environment variables
3. Verify API keys and quotas
4. Check cloud service logs
5. Test with simple requests first

**Your setup is perfect for this architecture - enjoy your new cloud AI platform!** 🚀
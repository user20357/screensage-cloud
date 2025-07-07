# 🚀 ScreenSage Architect - Setup Instructions

## 🎯 Your Action Items (What You Need to Do)

### 1. Get API Keys (5 minutes)
```bash
# Get OpenAI API Key (or skip for now - app works without it)
# 1. Go to https://platform.openai.com/api-keys
# 2. Create new API key
# 3. Copy the key (starts with sk-...)
```

### 2. Create GitHub Repository (2 minutes)
```bash
# 1. Go to github.com
# 2. Create new repository: "screensage-architect-cloud"
# 3. Make it public
# 4. Copy the repository URL
```

### 3. Sign Up for Cloud Platforms (10 minutes)
```bash
# All free - no credit card required for basic tiers:

# Render (Backend hosting)
# 1. Go to render.com
# 2. Sign up with GitHub
# 3. No setup needed yet

# Vercel (Frontend hosting)  
# 1. Go to vercel.com
# 2. Sign up with GitHub
# 3. No setup needed yet

# HuggingFace (AI demo)
# 1. Go to huggingface.co
# 2. Create account
# 3. No setup needed yet

# Kaggle (GPU processing)
# 1. Go to kaggle.com
# 2. Create account
# 3. Verify phone number for GPU access
```

---

## 🛠️ Local Development Setup

### Step 1: Clone and Setup Backend
```bash
# Navigate to your project
cd w:/ai/website/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Edit .env file and add your OpenAI key:
# OPENAI_API_KEY=sk-your-key-here
# (or leave as dummy_key for testing without AI)
```

### Step 2: Setup Frontend
```bash
# Open new terminal
cd w:/ai/website/frontend

# Install Node.js dependencies
npm install

# Create environment file
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
echo NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws >> .env.local
```

### Step 3: Test Locally
```bash
# Terminal 1 - Start Backend
cd w:/ai/website/backend
python main.py
# Should show: "Server running on http://0.0.0.0:8000"

# Terminal 2 - Start Frontend  
cd w:/ai/website/frontend
npm run dev
# Should show: "Ready - started server on 0.0.0.0:3000"

# Open browser: http://localhost:3000
# You should see the ScreenSage Architect interface!
```

---

## 🌐 Cloud Deployment (After Local Testing Works)

### Step 1: Deploy Backend to Render

```bash
# 1. Push backend to GitHub
cd w:/ai/website/backend
git init
git add .
git commit -m "Initial backend"
git remote add origin https://github.com/YOURUSERNAME/screensage-backend.git
git push -u origin main

# 2. Deploy on Render:
# - Go to render.com/dashboard
# - Click "New +" → "Web Service"
# - Connect your GitHub repo
# - Settings:
#   Name: screensage-backend
#   Build Command: pip install -r requirements.txt
#   Start Command: python main.py
#   
# - Environment Variables:
#   OPENAI_API_KEY = your-key-here
#   PORT = 8000
#   CORS_ORIGINS = ["*"]
#
# - Click "Create Web Service"
# - Wait for deployment (5-10 minutes)
# - Copy your backend URL: https://screensage-backend-xxx.onrender.com
```

### Step 2: Deploy Frontend to Vercel

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy frontend
cd w:/ai/website/frontend
vercel

# Follow prompts:
# - Link to existing project? N
# - Project name: screensage-frontend
# - Directory: ./
# - Override settings? N

# 3. Set environment variables:
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://your-backend-url.onrender.com

vercel env add NEXT_PUBLIC_WS_URL  
# Enter: wss://your-backend-url.onrender.com/ws

# 4. Redeploy with new env vars:
vercel --prod

# Your frontend URL: https://screensage-frontend-xxx.vercel.app
```

### Step 3: Create HuggingFace Demo

```bash
# 1. Go to huggingface.co/new-space
# 2. Settings:
#    Space name: screensage-architect
#    SDK: Gradio
#    Hardware: CPU basic (free)
#    Visibility: Public
#
# 3. Upload files:
#    - Copy w:/ai/website/ai-models/huggingface_gradio.py → app.py
#    - Copy w:/ai/website/ai-models/requirements.txt → requirements.txt
#
# 4. Your demo URL: https://huggingface.co/spaces/YOURUSERNAME/screensage-architect
```

---

## ✅ Testing Your Deployment

### 1. Test Backend
```bash
# Check health endpoint
curl https://your-backend.onrender.com/health

# Should return:
# {"status":"healthy","timestamp":"2024-..."}
```

### 2. Test Frontend
```bash
# 1. Open your Vercel URL in browser
# 2. Try uploading a screenshot
# 3. Check if OCR and analysis work
# 4. Look for any console errors (F12)
```

### 3. Test HuggingFace Demo
```bash
# 1. Open your HuggingFace Space URL
# 2. Upload a test image
# 3. Check if analysis works
# 4. Try the example images
```

---

## 🐛 Troubleshooting

### Backend Issues:
```bash
# Check Render logs:
# 1. Go to render.com/dashboard
# 2. Click your service
# 3. Check "Logs" tab

# Common fixes:
# - Ensure all dependencies in requirements.txt
# - Check environment variables are set
# - Verify Python version compatibility
```

### Frontend Issues:
```bash
# Check Vercel logs:
# 1. Go to vercel.com/dashboard  
# 2. Click your project
# 3. Check "Functions" tab for errors

# Common fixes:
# - Verify API URL is correct
# - Check CORS settings in backend
# - Ensure all npm packages installed
```

### Local Development Issues:
```bash
# Backend not starting:
pip install --upgrade pip
pip install -r requirements.txt

# Frontend not starting:
rm -rf node_modules package-lock.json
npm install

# Port conflicts:
# Change PORT in backend .env to 8001
# Update NEXT_PUBLIC_API_URL accordingly
```

---

## 🎯 Success Checklist

Your setup is complete when:

- [ ] ✅ Local backend runs on http://localhost:8000
- [ ] ✅ Local frontend runs on http://localhost:3000  
- [ ] ✅ Can upload screenshots locally
- [ ] ✅ OCR extracts text from images
- [ ] ✅ Backend deployed to Render
- [ ] ✅ Frontend deployed to Vercel
- [ ] ✅ HuggingFace demo works
- [ ] ✅ Cloud version can analyze screenshots

---

## 🚀 What's Next?

Once your prototype is working:

1. **Enhance AI Analysis**: Add more sophisticated models
2. **Real-time Features**: Improve WebSocket performance  
3. **User Authentication**: Add login system
4. **Database Integration**: Store tasks persistently
5. **Browser Extension**: For better screen access

---

## 📞 Need Help?

**Priority debugging order:**
1. Test locally first
2. Check all environment variables
3. Verify API keys and quotas
4. Check cloud platform logs
5. Test each component individually

**Common gotchas:**
- CORS errors → Update CORS_ORIGINS in backend
- WebSocket fails → Check WSS vs WS protocol
- OCR not working → Tesseract installation issue
- AI analysis empty → API key or quota issue

**Your prototype should work even without OpenAI API key** - it will use fallback analysis methods.

---

## 🎉 Congratulations!

You've successfully migrated ScreenSage Architect from desktop to cloud! 

**What you've built:**
- ✅ Modern React web interface
- ✅ FastAPI backend with OCR and AI
- ✅ Real-time WebSocket communication
- ✅ Browser-based screen capture
- ✅ Cloud deployment on free tiers
- ✅ AI-powered automation suggestions

**Total setup time: ~30 minutes**
**Monthly cost: $0 (free tiers)**

Your cloud-based ScreenSage Architect is ready for users worldwide! 🌍# 🚀 ScreenSage Architect - Setup Instructions

## 🎯 Your Action Items (What You Need to Do)

### 1. Get API Keys (5 minutes)
```bash
# Get OpenAI API Key (or skip for now - app works without it)
# 1. Go to https://platform.openai.com/api-keys
# 2. Create new API key
# 3. Copy the key (starts with sk-...)
```

### 2. Create GitHub Repository (2 minutes)
```bash
# 1. Go to github.com
# 2. Create new repository: "screensage-architect-cloud"
# 3. Make it public
# 4. Copy the repository URL
```

### 3. Sign Up for Cloud Platforms (10 minutes)
```bash
# All free - no credit card required for basic tiers:

# Render (Backend hosting)
# 1. Go to render.com
# 2. Sign up with GitHub
# 3. No setup needed yet

# Vercel (Frontend hosting)  
# 1. Go to vercel.com
# 2. Sign up with GitHub
# 3. No setup needed yet

# HuggingFace (AI demo)
# 1. Go to huggingface.co
# 2. Create account
# 3. No setup needed yet

# Kaggle (GPU processing)
# 1. Go to kaggle.com
# 2. Create account
# 3. Verify phone number for GPU access
```

---

## 🛠️ Local Development Setup

### Step 1: Clone and Setup Backend
```bash
# Navigate to your project
cd w:/ai/website/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Edit .env file and add your OpenAI key:
# OPENAI_API_KEY=sk-your-key-here
# (or leave as dummy_key for testing without AI)
```

### Step 2: Setup Frontend
```bash
# Open new terminal
cd w:/ai/website/frontend

# Install Node.js dependencies
npm install

# Create environment file
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
echo NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws >> .env.local
```

### Step 3: Test Locally
```bash
# Terminal 1 - Start Backend
cd w:/ai/website/backend
python main.py
# Should show: "Server running on http://0.0.0.0:8000"

# Terminal 2 - Start Frontend  
cd w:/ai/website/frontend
npm run dev
# Should show: "Ready - started server on 0.0.0.0:3000"

# Open browser: http://localhost:3000
# You should see the ScreenSage Architect interface!
```

---

## 🌐 Cloud Deployment (After Local Testing Works)

### Step 1: Deploy Backend to Render

```bash
# 1. Push backend to GitHub
cd w:/ai/website/backend
git init
git add .
git commit -m "Initial backend"
git remote add origin https://github.com/YOURUSERNAME/screensage-backend.git
git push -u origin main

# 2. Deploy on Render:
# - Go to render.com/dashboard
# - Click "New +" → "Web Service"
# - Connect your GitHub repo
# - Settings:
#   Name: screensage-backend
#   Build Command: pip install -r requirements.txt
#   Start Command: python main.py
#   
# - Environment Variables:
#   OPENAI_API_KEY = your-key-here
#   PORT = 8000
#   CORS_ORIGINS = ["*"]
#
# - Click "Create Web Service"
# - Wait for deployment (5-10 minutes)
# - Copy your backend URL: https://screensage-backend-xxx.onrender.com
```

### Step 2: Deploy Frontend to Vercel

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy frontend
cd w:/ai/website/frontend
vercel

# Follow prompts:
# - Link to existing project? N
# - Project name: screensage-frontend
# - Directory: ./
# - Override settings? N

# 3. Set environment variables:
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://your-backend-url.onrender.com

vercel env add NEXT_PUBLIC_WS_URL  
# Enter: wss://your-backend-url.onrender.com/ws

# 4. Redeploy with new env vars:
vercel --prod

# Your frontend URL: https://screensage-frontend-xxx.vercel.app
```

### Step 3: Create HuggingFace Demo

```bash
# 1. Go to huggingface.co/new-space
# 2. Settings:
#    Space name: screensage-architect
#    SDK: Gradio
#    Hardware: CPU basic (free)
#    Visibility: Public
#
# 3. Upload files:
#    - Copy w:/ai/website/ai-models/huggingface_gradio.py → app.py
#    - Copy w:/ai/website/ai-models/requirements.txt → requirements.txt
#
# 4. Your demo URL: https://huggingface.co/spaces/YOURUSERNAME/screensage-architect
```

---

## ✅ Testing Your Deployment

### 1. Test Backend
```bash
# Check health endpoint
curl https://your-backend.onrender.com/health

# Should return:
# {"status":"healthy","timestamp":"2024-..."}
```

### 2. Test Frontend
```bash
# 1. Open your Vercel URL in browser
# 2. Try uploading a screenshot
# 3. Check if OCR and analysis work
# 4. Look for any console errors (F12)
```

### 3. Test HuggingFace Demo
```bash
# 1. Open your HuggingFace Space URL
# 2. Upload a test image
# 3. Check if analysis works
# 4. Try the example images
```

---

## 🐛 Troubleshooting

### Backend Issues:
```bash
# Check Render logs:
# 1. Go to render.com/dashboard
# 2. Click your service
# 3. Check "Logs" tab

# Common fixes:
# - Ensure all dependencies in requirements.txt
# - Check environment variables are set
# - Verify Python version compatibility
```

### Frontend Issues:
```bash
# Check Vercel logs:
# 1. Go to vercel.com/dashboard  
# 2. Click your project
# 3. Check "Functions" tab for errors

# Common fixes:
# - Verify API URL is correct
# - Check CORS settings in backend
# - Ensure all npm packages installed
```

### Local Development Issues:
```bash
# Backend not starting:
pip install --upgrade pip
pip install -r requirements.txt

# Frontend not starting:
rm -rf node_modules package-lock.json
npm install

# Port conflicts:
# Change PORT in backend .env to 8001
# Update NEXT_PUBLIC_API_URL accordingly
```

---

## 🎯 Success Checklist

Your setup is complete when:

- [ ] ✅ Local backend runs on http://localhost:8000
- [ ] ✅ Local frontend runs on http://localhost:3000  
- [ ] ✅ Can upload screenshots locally
- [ ] ✅ OCR extracts text from images
- [ ] ✅ Backend deployed to Render
- [ ] ✅ Frontend deployed to Vercel
- [ ] ✅ HuggingFace demo works
- [ ] ✅ Cloud version can analyze screenshots

---

## 🚀 What's Next?

Once your prototype is working:

1. **Enhance AI Analysis**: Add more sophisticated models
2. **Real-time Features**: Improve WebSocket performance  
3. **User Authentication**: Add login system
4. **Database Integration**: Store tasks persistently
5. **Browser Extension**: For better screen access

---

## 📞 Need Help?

**Priority debugging order:**
1. Test locally first
2. Check all environment variables
3. Verify API keys and quotas
4. Check cloud platform logs
5. Test each component individually

**Common gotchas:**
- CORS errors → Update CORS_ORIGINS in backend
- WebSocket fails → Check WSS vs WS protocol
- OCR not working → Tesseract installation issue
- AI analysis empty → API key or quota issue

**Your prototype should work even without OpenAI API key** - it will use fallback analysis methods.

---

## 🎉 Congratulations!

You've successfully migrated ScreenSage Architect from desktop to cloud! 

**What you've built:**
- ✅ Modern React web interface
- ✅ FastAPI backend with OCR and AI
- ✅ Real-time WebSocket communication
- ✅ Browser-based screen capture
- ✅ Cloud deployment on free tiers
- ✅ AI-powered automation suggestions

**Total setup time: ~30 minutes**
**Monthly cost: $0 (free tiers)**

Your cloud-based ScreenSage Architect is ready for users worldwide! 🌍
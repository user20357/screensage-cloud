# 🚀 ScreenSage Architect - Cloud Deployment Guide

## 📋 Quick Setup Checklist

### Prerequisites (Your Setup Tasks)
- [ ] Get OpenAI API key (or use free alternatives)
- [ ] Create GitHub repository
- [ ] Sign up for cloud platforms (all free tiers)

### Cloud Platforms Setup
- [ ] **Render** account (Backend API)
- [ ] **Vercel** account (Frontend hosting)
- [ ] **HuggingFace** account (AI demo)
- [ ] **Kaggle** account (GPU processing)

---

## 🎯 Phase 1: Working Prototype (Priority)

### 1. Backend Deployment (Render - Free Tier)

```bash
# 1. Push backend code to GitHub
cd website/backend
git init
git add .
git commit -m "Initial backend setup"
git remote add origin https://github.com/yourusername/screensage-backend.git
git push -u origin main

# 2. Deploy on Render
# - Go to render.com
# - Connect GitHub repo
# - Choose "Web Service"
# - Build Command: pip install -r requirements.txt
# - Start Command: python main.py
```

**Environment Variables to set in Render:**
```
OPENAI_API_KEY=your_openai_key_here
PORT=8000
CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
DEBUG=false
```

### 2. Frontend Deployment (Vercel - Free Tier)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy frontend
cd website/frontend
npm install
vercel --prod

# 3. Set environment variables in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
# NEXT_PUBLIC_WS_URL=wss://your-backend.onrender.com/ws
```

### 3. HuggingFace Spaces Demo

```bash
# 1. Create new Space on huggingface.co
# - Choose "Gradio" as SDK
# - Upload ai-models/huggingface_gradio.py as app.py
# - Upload ai-models/requirements.txt

# 2. Your demo will be available at:
# https://huggingface.co/spaces/yourusername/screensage-architect
```

---

## 🔧 Local Development Setup

### 1. Backend Setup
```bash
cd website/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run backend
python main.py
# Backend runs on http://localhost:8000
```

### 2. Frontend Setup
```bash
cd website/frontend

# Install dependencies
npm install

# Set environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws" >> .env.local

# Run frontend
npm run dev
# Frontend runs on http://localhost:3000
```

### 3. Docker Setup (Optional)
```bash
cd website/deployment

# Run with Docker Compose
docker-compose up -d

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Redis: localhost:6379
```

---

## 🤖 AI Models Setup

### Option 1: Kaggle Notebooks (Free GPU)

1. **Create Kaggle Notebook:**
   - Go to kaggle.com/code
   - Create new notebook
   - Copy content from `ai-models/kaggle_processor.py`
   - Enable GPU in settings

2. **Setup API endpoint:**
   ```python
   # In your Kaggle notebook, add this at the end:
   from flask import Flask, request, jsonify
   
   app = Flask(__name__)
   
   @app.route('/analyze', methods=['POST'])
   def analyze_endpoint():
       data = request.json
       result = process_request(data)
       return jsonify(result)
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

3. **Make notebook public and get URL**

### Option 2: HuggingFace Spaces (Gradio UI)

1. **Create HuggingFace Space:**
   - Go to huggingface.co/new-space
   - Choose Gradio SDK
   - Upload `ai-models/huggingface_gradio.py` as `app.py`
   - Upload `ai-models/requirements.txt`

2. **Your demo will auto-deploy at:**
   `https://huggingface.co/spaces/yourusername/screensage-architect`

---

## 🌐 Screen Capture Strategy

### Browser Screen Capture API (Recommended for Prototype)

**Pros:**
- ✅ Works like Google Meet screen sharing
- ✅ No browser extension needed
- ✅ Cross-browser compatible
- ✅ User controls what to share

**Cons:**
- ❌ Requires user permission each time
- ❌ Limited to browser tabs/windows
- ❌ Can't capture full desktop automatically

**Implementation:** Already included in `frontend/src/components/ScreenCapture.tsx`

### Browser Extension (Future Enhancement)

**Pros:**
- ✅ Better desktop access
- ✅ More automation possibilities
- ✅ Persistent permissions

**Cons:**
- ❌ Requires installation
- ❌ More complex development
- ❌ Store approval process

---

## 📊 Testing Your Deployment

### 1. Backend Health Check
```bash
curl https://your-backend.onrender.com/health
# Should return: {"status": "healthy", "timestamp": "..."}
```

### 2. Frontend Access
- Visit your Vercel URL
- Try uploading a screenshot
- Check if analysis works

### 3. WebSocket Connection
- Open browser dev tools
- Go to Network tab
- Look for WebSocket connection to `/ws`

### 4. AI Processing
- Test with HuggingFace Spaces demo
- Upload sample screenshots
- Verify OCR and AI analysis work

---

## 🔍 Troubleshooting

### Common Issues:

1. **CORS Errors:**
   ```bash
   # Update CORS_ORIGINS in backend .env
   CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
   ```

2. **WebSocket Connection Failed:**
   ```bash
   # Check if backend WebSocket endpoint is accessible
   # Update NEXT_PUBLIC_WS_URL in frontend
   ```

3. **OCR Not Working:**
   ```bash
   # Ensure Tesseract is installed in Docker/Render
   # Check backend logs for OCR errors
   ```

4. **AI Analysis Failing:**
   ```bash
   # Verify OpenAI API key is set
   # Check API quota and billing
   # Fallback to pattern matching if needed
   ```

---

## 💰 Cost Breakdown (Free Tiers)

| Service | Free Tier Limits | Cost After |
|---------|------------------|------------|
| **Render** | 750 hours/month | $7/month |
| **Vercel** | 100GB bandwidth | $20/month |
| **HuggingFace** | CPU spaces free | GPU $0.60/hour |
| **Kaggle** | 30 hours GPU/week | N/A |
| **OpenAI** | $5 free credit | $0.01-0.03/1K tokens |

**Total Monthly Cost for Prototype: $0** (using free tiers)

---

## 🚀 Next Steps After Prototype

1. **Phase 2: Enhanced Features**
   - Real-time WebSocket optimization
   - Advanced AI model integration
   - User authentication system

2. **Phase 3: Production Ready**
   - Database integration (PostgreSQL)
   - Caching layer (Redis)
   - Monitoring and logging

3. **Phase 4: Scale Up**
   - Dedicated GPU instances
   - CDN optimization
   - Load balancing

---

## 📞 Support

If you encounter issues:

1. Check the logs in Render/Vercel dashboards
2. Test locally first with Docker Compose
3. Verify all environment variables are set
4. Check API quotas and limits

**Priority Order for Troubleshooting:**
1. Backend health endpoint
2. Frontend loading
3. Screenshot upload
4. OCR processing
5. AI analysis
6. WebSocket connection
7. Real-time features

---

## 🎯 Success Metrics

Your prototype is working when:
- ✅ Frontend loads without errors
- ✅ Screenshot upload works
- ✅ OCR extracts text from images
- ✅ AI provides basic analysis
- ✅ Suggested actions are generated
- ✅ Tasks can be created and viewed

**Minimum Viable Product (MVP) achieved!** 🎉# 🚀 ScreenSage Architect - Cloud Deployment Guide

## 📋 Quick Setup Checklist

### Prerequisites (Your Setup Tasks)
- [ ] Get OpenAI API key (or use free alternatives)
- [ ] Create GitHub repository
- [ ] Sign up for cloud platforms (all free tiers)

### Cloud Platforms Setup
- [ ] **Render** account (Backend API)
- [ ] **Vercel** account (Frontend hosting)
- [ ] **HuggingFace** account (AI demo)
- [ ] **Kaggle** account (GPU processing)

---

## 🎯 Phase 1: Working Prototype (Priority)

### 1. Backend Deployment (Render - Free Tier)

```bash
# 1. Push backend code to GitHub
cd website/backend
git init
git add .
git commit -m "Initial backend setup"
git remote add origin https://github.com/yourusername/screensage-backend.git
git push -u origin main

# 2. Deploy on Render
# - Go to render.com
# - Connect GitHub repo
# - Choose "Web Service"
# - Build Command: pip install -r requirements.txt
# - Start Command: python main.py
```

**Environment Variables to set in Render:**
```
OPENAI_API_KEY=your_openai_key_here
PORT=8000
CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
DEBUG=false
```

### 2. Frontend Deployment (Vercel - Free Tier)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy frontend
cd website/frontend
npm install
vercel --prod

# 3. Set environment variables in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
# NEXT_PUBLIC_WS_URL=wss://your-backend.onrender.com/ws
```

### 3. HuggingFace Spaces Demo

```bash
# 1. Create new Space on huggingface.co
# - Choose "Gradio" as SDK
# - Upload ai-models/huggingface_gradio.py as app.py
# - Upload ai-models/requirements.txt

# 2. Your demo will be available at:
# https://huggingface.co/spaces/yourusername/screensage-architect
```

---

## 🔧 Local Development Setup

### 1. Backend Setup
```bash
cd website/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run backend
python main.py
# Backend runs on http://localhost:8000
```

### 2. Frontend Setup
```bash
cd website/frontend

# Install dependencies
npm install

# Set environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws" >> .env.local

# Run frontend
npm run dev
# Frontend runs on http://localhost:3000
```

### 3. Docker Setup (Optional)
```bash
cd website/deployment

# Run with Docker Compose
docker-compose up -d

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Redis: localhost:6379
```

---

## 🤖 AI Models Setup

### Option 1: Kaggle Notebooks (Free GPU)

1. **Create Kaggle Notebook:**
   - Go to kaggle.com/code
   - Create new notebook
   - Copy content from `ai-models/kaggle_processor.py`
   - Enable GPU in settings

2. **Setup API endpoint:**
   ```python
   # In your Kaggle notebook, add this at the end:
   from flask import Flask, request, jsonify
   
   app = Flask(__name__)
   
   @app.route('/analyze', methods=['POST'])
   def analyze_endpoint():
       data = request.json
       result = process_request(data)
       return jsonify(result)
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

3. **Make notebook public and get URL**

### Option 2: HuggingFace Spaces (Gradio UI)

1. **Create HuggingFace Space:**
   - Go to huggingface.co/new-space
   - Choose Gradio SDK
   - Upload `ai-models/huggingface_gradio.py` as `app.py`
   - Upload `ai-models/requirements.txt`

2. **Your demo will auto-deploy at:**
   `https://huggingface.co/spaces/yourusername/screensage-architect`

---

## 🌐 Screen Capture Strategy

### Browser Screen Capture API (Recommended for Prototype)

**Pros:**
- ✅ Works like Google Meet screen sharing
- ✅ No browser extension needed
- ✅ Cross-browser compatible
- ✅ User controls what to share

**Cons:**
- ❌ Requires user permission each time
- ❌ Limited to browser tabs/windows
- ❌ Can't capture full desktop automatically

**Implementation:** Already included in `frontend/src/components/ScreenCapture.tsx`

### Browser Extension (Future Enhancement)

**Pros:**
- ✅ Better desktop access
- ✅ More automation possibilities
- ✅ Persistent permissions

**Cons:**
- ❌ Requires installation
- ❌ More complex development
- ❌ Store approval process

---

## 📊 Testing Your Deployment

### 1. Backend Health Check
```bash
curl https://your-backend.onrender.com/health
# Should return: {"status": "healthy", "timestamp": "..."}
```

### 2. Frontend Access
- Visit your Vercel URL
- Try uploading a screenshot
- Check if analysis works

### 3. WebSocket Connection
- Open browser dev tools
- Go to Network tab
- Look for WebSocket connection to `/ws`

### 4. AI Processing
- Test with HuggingFace Spaces demo
- Upload sample screenshots
- Verify OCR and AI analysis work

---

## 🔍 Troubleshooting

### Common Issues:

1. **CORS Errors:**
   ```bash
   # Update CORS_ORIGINS in backend .env
   CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
   ```

2. **WebSocket Connection Failed:**
   ```bash
   # Check if backend WebSocket endpoint is accessible
   # Update NEXT_PUBLIC_WS_URL in frontend
   ```

3. **OCR Not Working:**
   ```bash
   # Ensure Tesseract is installed in Docker/Render
   # Check backend logs for OCR errors
   ```

4. **AI Analysis Failing:**
   ```bash
   # Verify OpenAI API key is set
   # Check API quota and billing
   # Fallback to pattern matching if needed
   ```

---

## 💰 Cost Breakdown (Free Tiers)

| Service | Free Tier Limits | Cost After |
|---------|------------------|------------|
| **Render** | 750 hours/month | $7/month |
| **Vercel** | 100GB bandwidth | $20/month |
| **HuggingFace** | CPU spaces free | GPU $0.60/hour |
| **Kaggle** | 30 hours GPU/week | N/A |
| **OpenAI** | $5 free credit | $0.01-0.03/1K tokens |

**Total Monthly Cost for Prototype: $0** (using free tiers)

---

## 🚀 Next Steps After Prototype

1. **Phase 2: Enhanced Features**
   - Real-time WebSocket optimization
   - Advanced AI model integration
   - User authentication system

2. **Phase 3: Production Ready**
   - Database integration (PostgreSQL)
   - Caching layer (Redis)
   - Monitoring and logging

3. **Phase 4: Scale Up**
   - Dedicated GPU instances
   - CDN optimization
   - Load balancing

---

## 📞 Support

If you encounter issues:

1. Check the logs in Render/Vercel dashboards
2. Test locally first with Docker Compose
3. Verify all environment variables are set
4. Check API quotas and limits

**Priority Order for Troubleshooting:**
1. Backend health endpoint
2. Frontend loading
3. Screenshot upload
4. OCR processing
5. AI analysis
6. WebSocket connection
7. Real-time features

---

## 🎯 Success Metrics

Your prototype is working when:
- ✅ Frontend loads without errors
- ✅ Screenshot upload works
- ✅ OCR extracts text from images
- ✅ AI provides basic analysis
- ✅ Suggested actions are generated
- ✅ Tasks can be created and viewed

**Minimum Viable Product (MVP) achieved!** 🎉
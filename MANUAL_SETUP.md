# 🚀 Manual Setup Guide - ScreenSage Architect

## ⚡ Quick Manual Setup (5 minutes)

Since the automated scripts are taking time, here's a manual approach:

### Step 1: Backend Setup
```powershell
# Open PowerShell in w:\ai\website\backend
cd w:\ai\website\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install minimal dependencies
pip install fastapi uvicorn python-multipart python-dotenv pillow pytesseract requests

# Create .env file
echo "PORT=8000" > .env
echo "DEBUG=true" >> .env
echo "OPENAI_API_KEY=dummy_key" >> .env
echo 'CORS_ORIGINS=["http://localhost:3000"]' >> .env
```

### Step 2: Frontend Setup
```powershell
# Open NEW PowerShell in w:\ai\website\frontend
cd w:\ai\website\frontend

# Install Node dependencies (this may take a few minutes)
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws" >> .env.local
```

### Step 3: Start Services

**Terminal 1 - Backend:**
```powershell
cd w:\ai\website\backend
.\venv\Scripts\Activate.ps1
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd w:\ai\website\frontend
npm run dev
```

### Step 4: Test
Open browser: `http://localhost:3000`

---

## 🔧 If You Get Errors

### Backend Errors:
```powershell
# If module not found:
pip install --upgrade pip
pip install fastapi uvicorn python-multipart python-dotenv pillow pytesseract requests

# If permission errors:
# Run PowerShell as Administrator
```

### Frontend Errors:
```powershell
# If npm install fails:
npm cache clean --force
npm install

# If port 3000 is busy:
# Edit package.json, change "dev": "next dev" to "dev": "next dev -p 3001"
```

### PowerShell Execution Policy:
```powershell
# If you get execution policy errors:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎯 What Should Happen

### Backend (Terminal 1):
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Frontend (Terminal 2):
```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
- Network:      http://192.168.1.100:3000

✓ Ready in 2.3s
```

### Browser:
- Should show ScreenSage Architect interface
- Upload tab should work
- Live capture tab should work (with permission)

---

## 🚨 Troubleshooting

### 1. Backend won't start:
```powershell
# Check Python version
python --version  # Should be 3.8+

# Check if virtual environment is activated
# You should see (venv) in your prompt

# Try installing one by one:
pip install fastapi
pip install uvicorn
python main.py
```

### 2. Frontend won't start:
```powershell
# Check Node version
node --version  # Should be 16+
npm --version

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### 3. CORS errors in browser:
- Check backend .env file has correct CORS_ORIGINS
- Restart backend after changing .env

### 4. WebSocket connection failed:
- Check NEXT_PUBLIC_WS_URL in frontend .env.local
- Make sure backend is running first

---

## 🎉 Success Indicators

✅ **Backend working**: Visit `http://localhost:8000/health` shows `{"status":"healthy"}`

✅ **Frontend working**: `http://localhost:3000` shows ScreenSage interface

✅ **Full integration**: Can upload screenshot and see analysis

---

## 💡 Next Steps After Basic Setup

1. **Add OpenAI API key** (optional):
   ```
   # Edit backend/.env
   OPENAI_API_KEY=sk-your-real-key-here
   ```

2. **Install full AI dependencies** (optional):
   ```powershell
   pip install torch torchvision transformers easyocr
   ```

3. **Deploy to cloud** (optional):
   - Follow DEPLOYMENT_GUIDE.md

---

## 🔄 Alternative: Docker Setup

If manual setup is problematic:

```powershell
# Make sure Docker is installed
docker --version

# Run with Docker Compose
cd w:\ai\website\deployment
docker-compose up
```

This will:
- Start backend on http://localhost:8000
- Start frontend on http://localhost:3000
- Include Redis and PostgreSQL

---

## 📞 Still Having Issues?

1. **Check logs**: Look at terminal output for specific errors
2. **Test components separately**: Try backend health endpoint first
3. **Verify prerequisites**: Python 3.8+, Node 16+, npm
4. **Clean install**: Delete venv and node_modules, start over

**Most common issue**: Virtual environment not activated properly
**Solution**: Make sure you see `(venv)` in your terminal prompt

---

## 🎯 Minimal Working Version

If you just want to see it work quickly:

1. Skip AI dependencies for now
2. Use dummy API key
3. Focus on getting the interface up
4. Add features incrementally

The app will work with basic OCR and pattern matching even without OpenAI!
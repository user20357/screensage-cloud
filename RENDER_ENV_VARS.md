# 🔧 Render Environment Variables Setup

## ✅ **Required Environment Variables**

Set these in your Render dashboard:

### **1. OpenRouter API Key**
```
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```
**Get your key from**: https://openrouter.ai/keys

### **2. Basic Configuration**
```
PORT=8000
DEBUG=false
CORS_ORIGINS=["*"]
```

### **3. Optional (for later)**
```
OPENROUTER_MODEL=openai/gpt-4o-mini
KAGGLE_API_URL=https://your-kaggle-notebook-url
```

## 🎯 **How to Set in Render:**

1. Go to your Render dashboard
2. Click on your service
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Add each variable above

## ⚡ **Quick Test:**

After setting variables, your app should start successfully:
```
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 🔗 **Test Endpoints:**

```bash
# Health check
curl https://your-app.onrender.com/health

# Should return:
{"status":"healthy","timestamp":"2024-01-01T12:00:00Z"}
```

Your Intel Pentium G2020 setup will work perfectly with this! 🚀
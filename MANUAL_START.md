# Manual Startup Instructions for imgtoimg.ai

## 🚀 How to Start the Full AI-Powered Website

### Step 1: Start Backend (Terminal 1)
```bash
cd backend
python main.py
```

**Expected Output:**
```
Starting imgtoimg.ai Backend with AI Models
Backend: http://localhost:8005
API Docs: http://localhost:8005/docs
First model load may take 5-15 minutes...
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8005
```

**Note:** First run will download AI models (3-4GB). This may take 5-15 minutes depending on your internet speed.

### Step 2: Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 3: Access the Website
- **Main App**: http://localhost:3000
- **Backend API**: http://localhost:8005
- **API Documentation**: http://localhost:8005/docs

## 🔧 Troubleshooting

### If Backend Fails to Start:
1. **Model Download Issues:**
   ```bash
   # Set environment variable for better downloads
   set HF_HUB_DISABLE_SYMLINKS_WARNING=1
   cd backend
   python main.py
   ```

2. **Port Already in Use:**
   ```bash
   # Kill existing processes
   netstat -ano | findstr :8005
   taskkill /PID <PID_NUMBER> /F
   ```

3. **Dependencies Missing:**
   ```bash
   python fix_dependencies.py
   ```

### If Frontend Fails to Start:
1. **NPM Not Found:**
   - Install Node.js from https://nodejs.org/
   - Restart your terminal
   - Try again

2. **Dependencies Missing:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Port Already in Use:**
   ```bash
   # Frontend will automatically use next available port
   # Or manually specify port:
   npm run dev -- --port 3001
   ```

## 🎯 Quick Test

Once both servers are running:

1. Go to http://localhost:3000
2. Upload any image (JPG, PNG, WebP)
3. Enter a prompt like: "a beautiful landscape painting"
4. Click "Generate Image"
5. Wait for AI generation (first time may take longer)

## 💡 Performance Tips

- **GPU Recommended**: 10x faster than CPU
- **First Generation**: Takes longer as models load into memory
- **Subsequent Generations**: Much faster (30-60 seconds)
- **Internet Required**: Only for first-time model download

## 🆘 If Nothing Works

Try the simple demo mode:
```bash
cd backend
python simple_main.py
```

This runs without AI models for testing the interface.
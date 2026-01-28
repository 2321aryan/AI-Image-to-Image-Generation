#!/usr/bin/env python3
"""
Full startup script for imgtoimg.ai with real AI models
Handles model downloading and loading properly
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def check_requirements():
    """Check if requirements are met"""
    try:
        import torch
        import diffusers
        import fastapi
        print("✅ All dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: python fix_dependencies.py")
        return False

def set_environment():
    """Set environment variables for better model loading"""
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
    os.environ["TRANSFORMERS_CACHE"] = os.path.join(os.getcwd(), "models", "cache")
    os.environ["HF_HOME"] = os.path.join(os.getcwd(), "models", "huggingface")
    
    # Create cache directories
    os.makedirs("models/cache", exist_ok=True)
    os.makedirs("models/huggingface", exist_ok=True)
    os.makedirs("temp/uploads", exist_ok=True)
    os.makedirs("temp/results", exist_ok=True)
    
    print("✅ Environment configured")

def start_backend():
    """Start the backend with proper model handling"""
    print("\n🚀 Starting Full imgtoimg.ai Backend...")
    print("=" * 50)
    
    if not os.path.exists("backend/main.py"):
        print("❌ Please run from project root directory")
        return None
    
    print("🔄 Starting backend server...")
    print("⚠️  First run may take 5-15 minutes to download AI models")
    print("📊 Model download progress will be shown below...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd="backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor output
        def monitor_output():
            for line in iter(process.stdout.readline, ''):
                print(f"[Backend] {line.strip()}")
        
        monitor_thread = threading.Thread(target=monitor_output, daemon=True)
        monitor_thread.start()
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend"""
    print("\n🌐 Starting Frontend...")
    print("=" * 30)
    
    if not os.path.exists("frontend/package.json"):
        print("⚠️  Frontend not found, skipping")
        return None
    
    try:
        # Check if node_modules exists
        if not os.path.exists("frontend/node_modules"):
            print("📦 Installing frontend dependencies...")
            install_result = subprocess.run(
                ["npm", "install"],
                cwd="frontend",
                capture_output=True,
                text=True
            )
            if install_result.returncode != 0:
                print(f"❌ Failed to install: {install_result.stderr}")
                return None
        
        print("🔄 Starting frontend server...")
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd="frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor output
        def monitor_output():
            for line in iter(process.stdout.readline, ''):
                if "Local:" in line or "localhost" in line:
                    print(f"✅ {line.strip()}")
                elif "error" in line.lower():
                    print(f"❌ {line.strip()}")
        
        monitor_thread = threading.Thread(target=monitor_output, daemon=True)
        monitor_thread.start()
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def wait_for_backend():
    """Wait for backend to be ready"""
    import requests
    
    print("\n⏳ Waiting for backend to be ready...")
    for i in range(60):  # Wait up to 5 minutes
        try:
            response = requests.get("http://localhost:8005/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is ready!")
                return True
        except:
            pass
        
        if i % 10 == 0:
            print(f"   Still waiting... ({i//10 + 1}/6)")
        time.sleep(5)
    
    print("⚠️  Backend startup timeout, but continuing...")
    return False

def main():
    """Main startup function"""
    print("🎨 imgtoimg.ai - Full AI-Powered Startup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Set environment
    set_environment()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)
    
    # Wait for backend
    time.sleep(10)  # Give it time to start
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Wait for backend to be ready
    wait_for_backend()
    
    print("\n" + "=" * 60)
    print("🎉 imgtoimg.ai is starting up!")
    print("📱 Frontend: http://localhost:3000 (when ready)")
    print("🔧 Backend: http://localhost:8005")
    print("📚 API Docs: http://localhost:8005/docs")
    print("=" * 60)
    print("\n💡 Tips:")
    print("- First generation will be slower as models load")
    print("- Upload an image and enter a prompt to start")
    print("- Model download may take 5-15 minutes on first run")
    print("- Press Ctrl+C to stop all servers")
    
    # Setup signal handlers
    def signal_handler(signum, frame):
        print("\n🛑 Shutting down...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Keep running
    try:
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process and backend_process.poll() is not None:
                print("❌ Backend stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        pass
    finally:
        print("\n🛑 Stopping servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()

if __name__ == "__main__":
    main()
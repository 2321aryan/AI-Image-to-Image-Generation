#!/usr/bin/env python3
"""
Complete startup script for the Image Generator
"""
import subprocess
import os
import time
import sys
import requests
from threading import Thread

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_backend_running():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_frontend_running():
    """Check if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    
    if check_backend_running():
        print("✅ Backend is already running")
        return True
    
    try:
        # Start backend in background
        backend_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd="backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for startup
        for i in range(10):
            time.sleep(2)
            if check_backend_running():
                print("✅ Backend started successfully!")
                return True
            print(f"⏳ Waiting for backend startup... ({i+1}/10)")
        
        print("⚠️  Backend may still be starting up...")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the frontend server"""
    print("🌐 Starting frontend server...")
    
    if check_frontend_running():
        print("✅ Frontend is already running")
        return True
    
    try:
        # Install dependencies first
        print("📦 Installing frontend dependencies...")
        success, stdout, stderr = run_command("npm install", cwd="frontend")
        if not success:
            print(f"⚠️  npm install had issues: {stderr}")
        
        # Start frontend in background
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd="frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for startup
        for i in range(15):
            time.sleep(2)
            if check_frontend_running():
                print("✅ Frontend started successfully!")
                return True
            print(f"⏳ Waiting for frontend startup... ({i+1}/15)")
        
        print("⚠️  Frontend may still be starting up...")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def test_system():
    """Test the complete system"""
    print("\n🧪 Testing system...")
    
    # Test backend health
    if check_backend_running():
        print("✅ Backend health check passed")
    else:
        print("❌ Backend health check failed")
        return False
    
    # Test upload endpoint
    try:
        from PIL import Image
        
        # Create test image
        test_image = Image.new('RGB', (512, 512), (100, 150, 200))
        test_image.save("test_image.png")
        
        # Test upload
        with open("test_image.png", 'rb') as f:
            files = {'files': ("test_image.png", f, 'image/png')}
            response = requests.post("http://localhost:8005/api/upload", files=files, timeout=30)
        
        os.remove("test_image.png")
        
        if response.status_code == 200:
            print("✅ Upload endpoint working")
            
            # Test generation
            upload_data = response.json()
            generation_request = {
                "upload_id": upload_data["upload_id"],
                "prompt": "a beautiful landscape",
                "model": "stable-diffusion-1.5",
                "aspect_ratio": "1:1",
                "num_outputs": 1,
                "strength": 0.8,
                "guidance_scale": 7.5,
                "steps": 30
            }
            
            gen_response = requests.post(
                "http://localhost:8005/api/generate", 
                json=generation_request, 
                timeout=60
            )
            
            if gen_response.status_code == 200:
                print("✅ Generation endpoint working")
                return True
            else:
                print(f"❌ Generation endpoint failed: {gen_response.status_code}")
                return False
        else:
            print(f"❌ Upload endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    print("🎨 Image Generator Startup")
    print("=" * 40)
    
    # Create necessary directories
    directories = [
        "temp/uploads", "temp/results", "temp/analysis", "temp/cache"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Start backend
    backend_success = start_backend()
    
    # Start frontend
    frontend_success = start_frontend()
    
    # Test system
    if backend_success:
        system_working = test_system()
    else:
        system_working = False
    
    print("\n" + "=" * 40)
    print("🎉 Startup Complete!")
    print("=" * 40)
    
    if backend_success and frontend_success and system_working:
        print("✅ All systems are running successfully!")
        print("\n🔗 Access your Image Generator:")
        print("  Frontend: http://localhost:3000")
        print("  Backend:  http://localhost:8005")
        print("  API Docs: http://localhost:8005/docs")
        print("\n📝 Instructions:")
        print("  1. Open http://localhost:3000 in your browser")
        print("  2. Upload an image")
        print("  3. Enter a prompt describing what you want")
        print("  4. Click 'Generate Image'")
        print("  5. Wait for the AI to process your request")
        
    else:
        print("⚠️  Some services may not be fully ready")
        print("\n🔧 Manual startup:")
        if not backend_success:
            print("  Backend: cd backend && python main.py")
        if not frontend_success:
            print("  Frontend: cd frontend && npm run dev")
        
        print("\n🔗 URLs (try these manually):")
        print("  Frontend: http://localhost:3000")
        print("  Backend:  http://localhost:8005")
    
    print("\n💡 Tips:")
    print("  - First AI generation may take 5-15 minutes")
    print("  - Keep both terminal windows open")
    print("  - Check console for any errors")
    
    return True

if __name__ == "__main__":
    main()
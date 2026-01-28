#!/usr/bin/env python3
"""
Comprehensive fix for all image generator issues
"""
import subprocess
import os
import shutil
import time
import sys

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_backend_running():
    """Check if backend is running on port 8005"""
    try:
        import requests
        response = requests.get("http://localhost:8005/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🔧 Comprehensive Image Generator Fix")
    print("=" * 50)
    
    # 1. Fix frontend types issue
    print("\n1. 🧹 Cleaning frontend cache...")
    frontend_dir = "frontend"
    
    cache_dirs = [
        os.path.join(frontend_dir, "node_modules", ".vite"),
        os.path.join(frontend_dir, "dist"),
        os.path.join(frontend_dir, ".vite")
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"✅ Cleaned {cache_dir}")
            except Exception as e:
                print(f"⚠️  Could not clean {cache_dir}: {e}")
    
    # 2. Verify backend dependencies
    print("\n2. 📦 Checking backend dependencies...")
    backend_dir = "backend"
    
    # Check if requirements.txt exists
    requirements_path = os.path.join(backend_dir, "requirements.txt")
    if os.path.exists(requirements_path):
        print("✅ Requirements file found")
        
        # Install backend dependencies
        print("Installing backend dependencies...")
        success, stdout, stderr = run_command("pip install -r requirements.txt", cwd=backend_dir)
        if success:
            print("✅ Backend dependencies installed")
        else:
            print(f"⚠️  Backend dependency installation had issues: {stderr}")
    else:
        print("⚠️  Requirements file not found")
    
    # 3. Create necessary directories
    print("\n3. 📁 Creating necessary directories...")
    directories = [
        "temp/uploads", "temp/results", "temp/analysis", "temp/cache",
        "models/facial", "models/body", "models/style", "models/age",
        "models/clothing", "models/environment"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}")
    
    # 4. Start backend
    print("\n4. 🚀 Starting backend server...")
    if check_backend_running():
        print("✅ Backend is already running")
    else:
        print("Starting backend server...")
        # Start backend in background
        try:
            backend_process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a bit for startup
            time.sleep(3)
            
            if check_backend_running():
                print("✅ Backend started successfully on http://localhost:8005")
            else:
                print("⚠️  Backend may still be starting up...")
                print("Check manually: http://localhost:8005/health")
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
    
    # 5. Install frontend dependencies
    print("\n5. 📦 Installing frontend dependencies...")
    success, stdout, stderr = run_command("npm install", cwd=frontend_dir)
    if success:
        print("✅ Frontend dependencies installed")
    else:
        print(f"⚠️  Frontend dependency installation had issues: {stderr}")
    
    # 6. Start frontend
    print("\n6. 🌐 Starting frontend...")
    print("Starting frontend development server...")
    print("This will open in a new terminal window...")
    
    try:
        # Start frontend in background
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(2)
        print("✅ Frontend server starting...")
        print("Frontend should be available at: http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        print("Try manually: cd frontend && npm run dev")
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("🔗 URLs:")
    print("  Frontend: http://localhost:3000")
    print("  Backend:  http://localhost:8005")
    print("  API Docs: http://localhost:8005/docs")
    print("\n📝 Notes:")
    print("  - First AI model load may take 5-15 minutes")
    print("  - Check console for any remaining errors")
    print("  - Both servers should now be running")
    
    return True

if __name__ == "__main__":
    main()
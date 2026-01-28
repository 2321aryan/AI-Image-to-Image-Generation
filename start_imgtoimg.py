#!/usr/bin/env python3
"""
Startup script for imgtoimg.ai clone
Starts both backend and frontend servers
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class ServerManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
    
    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🚀 Starting backend server...")
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd="backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor backend output
            def monitor_backend():
                for line in iter(self.backend_process.stdout.readline, ''):
                    if self.running:
                        print(f"[Backend] {line.strip()}")
                    else:
                        break
            
            threading.Thread(target=monitor_backend, daemon=True).start()
            print("✅ Backend server started on http://localhost:8004")
            
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
        
        return True
    
    def start_frontend(self):
        """Start the React frontend server"""
        if not os.path.exists("frontend/package.json"):
            print("⚠️  Frontend not found - running backend only")
            return True
        
        print("🌐 Starting frontend server...")
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
                    print(f"❌ Failed to install frontend dependencies: {install_result.stderr}")
                    return False
            
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd="frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor frontend output
            def monitor_frontend():
                for line in iter(self.frontend_process.stdout.readline, ''):
                    if self.running:
                        print(f"[Frontend] {line.strip()}")
                    else:
                        break
            
            threading.Thread(target=monitor_frontend, daemon=True).start()
            print("✅ Frontend server started on http://localhost:3000")
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
        
        return True
    
    def wait_for_backend(self, timeout=30):
        """Wait for backend to be ready"""
        import requests
        
        print("⏳ Waiting for backend to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get("http://localhost:8004/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend is ready!")
                    return True
            except:
                pass
            time.sleep(1)
        
        print("⚠️  Backend startup timeout - continuing anyway")
        return False
    
    def stop_servers(self):
        """Stop both servers"""
        print("\n🛑 Stopping servers...")
        self.running = False
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend server stopped")
            except:
                self.frontend_process.kill()
                print("🔨 Frontend server force killed")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend server stopped")
            except:
                self.backend_process.kill()
                print("🔨 Backend server force killed")
    
    def run(self):
        """Run both servers"""
        try:
            # Start backend first
            if not self.start_backend():
                return False
            
            # Wait a bit for backend to start
            time.sleep(3)
            
            # Wait for backend to be ready
            self.wait_for_backend()
            
            # Start frontend
            if not self.start_frontend():
                return False
            
            print("\n" + "=" * 60)
            print("🎉 imgtoimg.ai is running!")
            print("📱 Frontend: http://localhost:3000")
            print("🔧 Backend API: http://localhost:8004")
            print("📚 API Docs: http://localhost:8004/docs")
            print("=" * 60)
            print("\n💡 Tips:")
            print("- Upload an image and enter a prompt to get started")
            print("- First generation may take longer as models are loaded")
            print("- Use Ctrl+C to stop the servers")
            print("\nPress Ctrl+C to stop...")
            
            # Keep running until interrupted
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            
        except Exception as e:
            print(f"❌ Error running servers: {e}")
            return False
        finally:
            self.stop_servers()
        
        return True

def check_requirements():
    """Check if basic requirements are met"""
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    # Check if backend exists
    if not os.path.exists("backend/main.py"):
        print("❌ Backend not found. Please run from the project root directory.")
        return False
    
    # Check if requirements are installed
    try:
        import fastapi
        import torch
        import diffusers
        print("✅ Core dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: python install_imgtoimg.py")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🚀 imgtoimg.ai Startup Script")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Create server manager
    manager = ServerManager()
    
    # Setup signal handlers
    def signal_handler(signum, frame):
        print("\n🛑 Received interrupt signal")
        manager.running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run servers
    success = manager.run()
    
    if success:
        print("\n👋 imgtoimg.ai stopped successfully")
    else:
        print("\n❌ imgtoimg.ai stopped with errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
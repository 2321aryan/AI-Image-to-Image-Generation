#!/usr/bin/env python3
"""
Quick start script for AI Image Generator
This script helps you get the application running quickly.
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("🎨 AI Image Generator - Quick Start")
    print("=" * 50)
    print("Local AI-powered image-to-image generation")
    print("Unlimited usage • Complete privacy • No restrictions")
    print("=" * 50)

def check_dependencies():
    """Check if basic dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
        return False
    
    # Check Python
    try:
        print(f"✅ Python: {sys.version.split()[0]}")
    except:
        print("❌ Python not found")
        return False
    
    return True

def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    try:
        # Install basic dependencies first
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            'fastapi', 'uvicorn[standard]', 'python-multipart', 
            'pillow', 'pydantic', 'aiofiles'
        ], check=True)
        
        print("✅ Basic backend dependencies installed")
        
        # Try to install AI dependencies
        print("🤖 Installing AI dependencies (this may take a while)...")
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install',
                'torch', 'torchvision', 'torchaudio', '--index-url', 
                'https://download.pytorch.org/whl/cpu'
            ], check=True)
            
            subprocess.run([
                sys.executable, '-m', 'pip', 'install',
                'diffusers', 'transformers', 'accelerate'
            ], check=True)
            
            print("✅ AI dependencies installed")
        except subprocess.CalledProcessError:
            print("⚠️  AI dependencies installation failed, but basic functionality will work")
        
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Failed to install backend dependencies")
        return False

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    
    backend_dir = Path("backend")
    try:
        # Start backend in background
        process = subprocess.Popen([
            sys.executable, 'main.py'
        ], cwd=backend_dir)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Backend server started on http://localhost:8000")
            return process
        else:
            print("❌ Backend server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend development server"""
    print("\n🎨 Starting frontend server...")
    
    frontend_dir = Path("frontend")
    try:
        # Start frontend
        process = subprocess.Popen([
            'npm', 'run', 'dev'
        ], cwd=frontend_dir)
        
        # Wait a moment for server to start
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Frontend server started on http://localhost:3000")
            return process
        else:
            print("❌ Frontend server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        return
    
    # Install dependencies
    if not install_frontend_deps():
        return
    
    if not install_backend_deps():
        return
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    # Open browser
    print("\n🌐 Opening browser...")
    time.sleep(2)
    webbrowser.open('http://localhost:3000')
    
    print("\n" + "=" * 50)
    print("🎉 AI Image Generator is now running!")
    print("Frontend: http://localhost:3000")
    print("Backend API: http://localhost:8000")
    print("\n💡 Tips:")
    print("- Upload an image and describe the changes you want")
    print("- Try different models for different styles")
    print("- Adjust settings for better results")
    print("- All processing happens locally on your machine")
    print("\nPress Ctrl+C to stop the servers")
    print("=" * 50)
    
    try:
        # Keep running until user stops
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        frontend_process.terminate()
        backend_process.terminate()
        print("✅ Servers stopped. Thanks for using AI Image Generator!")

if __name__ == "__main__":
    main()
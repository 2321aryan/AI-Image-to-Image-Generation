#!/usr/bin/env python3
"""
Script to restart the frontend development server with clean cache
"""
import subprocess
import os
import shutil
import sys

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🧹 Cleaning frontend cache and restarting development server...")
    
    frontend_dir = "frontend"
    
    # Clean cache directories
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
    
    # Install dependencies if needed
    print("\n📦 Installing dependencies...")
    success, stdout, stderr = run_command("npm install", cwd=frontend_dir)
    if not success:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False
    
    print("✅ Dependencies installed successfully")
    
    # Start development server
    print("\n🚀 Starting development server...")
    print("The server will start on http://localhost:3000")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run("npm run dev", shell=True, cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n👋 Development server stopped")
    
    return True

if __name__ == "__main__":
    main()
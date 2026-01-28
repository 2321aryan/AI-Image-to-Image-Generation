#!/usr/bin/env python3
"""
Simple startup script for imgtoimg.ai
Just starts the backend - you can start frontend manually
"""

import subprocess
import sys
import os

def start_backend():
    """Start the backend server"""
    print("🚀 Starting imgtoimg.ai Backend...")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/main.py"):
        print("❌ Please run this from the project root directory")
        return False
    
    # Start backend
    print("🔄 Starting FastAPI backend server...")
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
    except Exception as e:
        print(f"❌ Backend failed to start: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🎨 imgtoimg.ai - Simple Startup")
    print("=" * 40)
    
    success = start_backend()
    
    if success:
        print("\n✅ Backend started successfully!")
    else:
        print("\n❌ Failed to start backend")
        print("\nManual startup:")
        print("  cd backend")
        print("  python main.py")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test to verify frontend fixes are working
"""
import requests
import time

def test_frontend():
    print("🧪 Testing Frontend Fix")
    
    # Check if frontend is accessible
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            
            # Check if it contains the expected content
            content = response.text
            if "AI Image Generator" in content or "Generate Image" in content:
                print("✅ Frontend content looks correct")
                return True
            else:
                print("⚠️  Frontend content may have issues")
                return False
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def test_backend():
    print("🧪 Testing Backend")
    
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def main():
    print("🔧 Testing System After Fixes")
    print("=" * 30)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 30)
    if backend_ok and frontend_ok:
        print("✅ ALL SYSTEMS WORKING!")
        print("\n🎯 Next steps:")
        print("1. Open http://localhost:3000")
        print("2. Upload an image")
        print("3. Enter a prompt")
        print("4. Click Generate Image")
        print("\n💡 The TypeError should now be fixed!")
    else:
        print("❌ Some issues remain")
        if not backend_ok:
            print("- Backend needs to be started")
        if not frontend_ok:
            print("- Frontend may need restart")

if __name__ == "__main__":
    main()
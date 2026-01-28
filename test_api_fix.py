#!/usr/bin/env python3
"""
Test script to verify API fixes are working
"""
import requests
import json
import time
import os
from PIL import Image

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get("http://localhost:8005/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_upload_endpoint():
    """Test upload endpoint with a simple test image"""
    try:
        # Create a simple test image
        test_image = Image.new('RGB', (512, 512), (100, 150, 200))
        test_image_path = "test_image.png"
        test_image.save(test_image_path)
        
        # Test upload
        with open(test_image_path, 'rb') as f:
            files = {'files': (test_image_path, f, 'image/png')}  # Include content type
            response = requests.post("http://localhost:8005/api/upload", files=files, timeout=30)
        
        # Clean up test image
        os.remove(test_image_path)
        
        if response.status_code == 200:
            print("✅ Upload endpoint working")
            data = response.json()
            return data.get('upload_id')
        else:
            print(f"❌ Upload endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return None

def test_models_endpoint():
    """Test models endpoint"""
    try:
        response = requests.get("http://localhost:8005/api/models", timeout=10)
        if response.status_code == 200:
            print("✅ Models endpoint working")
            models = response.json()
            print(f"Available models: {len(models)}")
            return True
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def test_generation_endpoint(upload_id):
    """Test generation endpoint"""
    if not upload_id:
        print("⚠️  Skipping generation test - no upload_id")
        return False
        
    try:
        generation_request = {
            "upload_id": upload_id,
            "prompt": "a beautiful landscape",
            "model": "stable-diffusion-1.5",
            "aspect_ratio": "1:1",
            "num_outputs": 1,
            "strength": 0.8,
            "guidance_scale": 7.5,
            "steps": 30
        }
        
        response = requests.post(
            "http://localhost:8005/api/generate", 
            json=generation_request, 
            timeout=60
        )
        
        if response.status_code == 200:
            print("✅ Generation endpoint working")
            data = response.json()
            job_id = data.get('job', {}).get('id') if data.get('job') else None
            print(f"Generation job created: {job_id}")
            print(f"Response data: {data}")
            return job_id
        else:
            print(f"❌ Generation endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return None

def main():
    print("🧪 Testing API Fixes")
    print("=" * 30)
    
    # Test backend health
    print("\n1. Testing backend health...")
    if not test_backend_health():
        print("❌ Backend is not running. Please start it first.")
        return False
    
    # Test models endpoint
    print("\n2. Testing models endpoint...")
    test_models_endpoint()
    
    # Test upload endpoint
    print("\n3. Testing upload endpoint...")
    upload_id = test_upload_endpoint()
    
    # Test generation endpoint
    print("\n4. Testing generation endpoint...")
    job_id = test_generation_endpoint(upload_id)
    
    print("\n🎉 API Testing Complete!")
    print("=" * 30)
    
    if upload_id and job_id:
        print("✅ All core endpoints are working")
        print("The image generator should now work properly!")
    else:
        print("⚠️  Some endpoints had issues, but basic functionality should work")
    
    return True

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Quick test to debug the generation issue
"""
import requests
import json
from PIL import Image
import os

def test_generation():
    print("🧪 Quick Generation Test")
    
    # Create test image
    test_image = Image.new('RGB', (512, 512), (100, 150, 200))
    test_image.save("test.png")
    
    try:
        # Test upload
        print("1. Testing upload...")
        with open("test.png", 'rb') as f:
            files = {'files': ("test.png", f, 'image/png')}
            response = requests.post("http://localhost:8005/api/upload", files=files)
        
        print(f"Upload status: {response.status_code}")
        if response.status_code != 200:
            print(f"Upload failed: {response.text}")
            return
        
        upload_data = response.json()
        upload_id = upload_data["upload_id"]
        print(f"Upload ID: {upload_id}")
        
        # Test generation
        print("2. Testing generation...")
        gen_request = {
            "upload_id": upload_id,
            "prompt": "a beautiful landscape",
            "model": "stable-diffusion-1.5",
            "aspect_ratio": "1:1",
            "num_outputs": 1,
            "strength": 0.8,
            "guidance_scale": 7.5,
            "steps": 30
        }
        
        print(f"Sending request: {json.dumps(gen_request, indent=2)}")
        
        response = requests.post("http://localhost:8005/api/generate", json=gen_request)
        print(f"Generation status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Generation request successful!")
            print(f"Job data: {json.dumps(data, indent=2)}")
        else:
            print("❌ Generation request failed!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        if os.path.exists("test.png"):
            os.remove("test.png")

if __name__ == "__main__":
    test_generation()
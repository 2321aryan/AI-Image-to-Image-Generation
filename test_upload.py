#!/usr/bin/env python3
"""
Test script to check upload functionality
"""

import requests
import io
from PIL import Image
import sys

def create_test_image():
    """Create a simple test image"""
    # Create a simple 512x512 RGB image
    img = Image.new('RGB', (512, 512), color='red')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def test_upload():
    """Test the upload/analyze endpoint"""
    base_url = "http://localhost:8004"
    
    print("Testing upload/analyze endpoint...")
    
    try:
        # Create test image
        test_image = create_test_image()
        
        # Prepare files for upload
        files = {
            'files': ('test_image.jpg', test_image, 'image/jpeg')
        }
        
        # Make upload request
        response = requests.post(
            f"{base_url}/api/upload/analyze", 
            files=files,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Upload successful!")
            print(f"  Upload ID: {data.get('upload_id')}")
            print(f"  Files processed: {len(data.get('files', []))}")
            print(f"  Message: {data.get('message')}")
            
            # Check analysis data
            if data.get('files'):
                for i, file_info in enumerate(data['files']):
                    print(f"  File {i+1}: {file_info.get('filename')}")
                    analysis = file_info.get('analysis', {})
                    persons = analysis.get('persons', [])
                    print(f"    Persons detected: {len(persons)}")
                    for j, person in enumerate(persons):
                        print(f"      Person {j+1}: ID={person.get('person_id')}, Confidence={person.get('confidence')}")
            
            return True
        else:
            print(f"✗ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Upload test failed: {e}")
        return False

if __name__ == "__main__":
    print("Upload Test")
    print("=" * 30)
    
    success = test_upload()
    
    print("\n" + "=" * 30)
    if success:
        print("Upload test passed!")
    else:
        print("Upload test failed!")
        sys.exit(1)
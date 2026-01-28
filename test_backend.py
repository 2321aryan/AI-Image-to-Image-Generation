#!/usr/bin/env python3
"""
Simple test script to check if the backend is running and accessible
"""

import requests
import sys
import json

def test_backend():
    """Test basic backend connectivity"""
    base_url = "http://localhost:8004"
    
    print("Testing backend connectivity...")
    
    try:
        # Test root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✓ Root endpoint accessible")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
            return False
            
        # Test health endpoint
        print("\n2. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Health endpoint accessible")
            health_data = response.json()
            print(f"  Status: {health_data.get('status')}")
            print(f"  CPU: {health_data.get('system_resources', {}).get('cpu_percent', 'N/A')}%")
            print(f"  Memory: {health_data.get('system_resources', {}).get('memory_percent', 'N/A')}%")
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            
        # Test upload capabilities
        print("\n3. Testing upload capabilities...")
        response = requests.get(f"{base_url}/api/upload/capabilities", timeout=5)
        if response.status_code == 200:
            print("✓ Upload capabilities accessible")
            caps = response.json()
            print(f"  Supported formats: {caps.get('supported_formats', [])}")
            print(f"  Max file size: {caps.get('max_file_size_mb', 'N/A')} MB")
            print(f"  Max files: {caps.get('max_files_per_upload', 'N/A')}")
        else:
            print(f"✗ Upload capabilities failed: {response.status_code}")
            
        print("\n✓ Backend is running and accessible!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend. Is it running on port 8004?")
        print("  Try running: python backend/main.py")
        return False
    except requests.exceptions.Timeout:
        print("✗ Backend request timed out")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_simple_upload():
    """Test a simple upload without files"""
    base_url = "http://localhost:8004"
    
    print("\n4. Testing upload endpoint (without files)...")
    try:
        # This should fail but give us info about the endpoint
        response = requests.post(f"{base_url}/api/upload", timeout=5)
        print(f"  Upload endpoint response: {response.status_code}")
        if response.status_code == 422:  # Validation error expected
            print("✓ Upload endpoint is accessible (validation error expected)")
        else:
            print(f"  Response: {response.text[:200]}...")
    except Exception as e:
        print(f"✗ Upload test failed: {e}")

if __name__ == "__main__":
    print("Backend Connectivity Test")
    print("=" * 50)
    
    success = test_backend()
    if success:
        test_simple_upload()
        print("\n" + "=" * 50)
        print("Backend test completed successfully!")
        print("If uploads are still failing, check:")
        print("1. File permissions in backend/temp/ directory")
        print("2. Browser console for detailed error messages")
        print("3. Backend logs for processing errors")
    else:
        print("\n" + "=" * 50)
        print("Backend test failed!")
        print("Please start the backend server first:")
        print("  cd backend && python main.py")
        sys.exit(1)
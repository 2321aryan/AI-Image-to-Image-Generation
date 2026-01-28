#!/usr/bin/env python3
"""
Simple AI Model Installation Script
This script installs the essential dependencies for real AI image generation.
"""

import subprocess
import sys
import os

def print_header():
    print("🤖 AI Image Generator - Model Installation")
    print("=" * 50)
    print("Installing Stable Diffusion for real image generation")
    print("=" * 50)

def install_pytorch():
    """Install PyTorch"""
    print("\n🔥 Installing PyTorch...")
    
    try:
        # Try CUDA version first
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            'torch', 'torchvision', 'torchaudio', 
            '--index-url', 'https://download.pytorch.org/whl/cu118'
        ], check=True)
        print("✅ PyTorch with CUDA support installed")
        return True
    except:
        try:
            # Fallback to CPU version
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                'torch', 'torchvision', 'torchaudio',
                '--index-url', 'https://download.pytorch.org/whl/cpu'
            ], check=True)
            print("✅ PyTorch (CPU version) installed")
            return True
        except:
            print("❌ Failed to install PyTorch")
            return False

def install_diffusers():
    """Install Diffusers and related packages"""
    print("\n🎨 Installing Diffusers (Stable Diffusion)...")
    
    packages = [
        'diffusers==0.24.0',
        'transformers==4.35.2',
        'accelerate==0.24.1',
        'safetensors==0.4.0'
    ]
    
    try:
        for package in packages:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        print("✅ Diffusers and AI packages installed")
        return True
    except:
        print("❌ Failed to install Diffusers")
        return False

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    
    packages = [
        'fastapi==0.104.1',
        'uvicorn[standard]==0.24.0',
        'python-multipart==0.0.6',
        'pillow==10.1.0',
        'pydantic==2.5.0',
        'aiofiles==23.2.1'
    ]
    
    try:
        for package in packages:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        print("✅ Backend dependencies installed")
        return True
    except:
        print("❌ Failed to install backend dependencies")
        return False

def test_installation():
    """Test if everything is working"""
    print("\n🧪 Testing installation...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        
        import diffusers
        print(f"✅ Diffusers: {diffusers.__version__}")
        
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
        
        # Test CUDA
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("ℹ️  CUDA not available, will use CPU")
        
        print("\n🎉 Installation successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print_header()
    
    success = True
    
    if not install_backend_deps():
        success = False
    
    if not install_pytorch():
        success = False
    
    if not install_diffusers():
        success = False
    
    if success:
        if test_installation():
            print("\n" + "=" * 50)
            print("🚀 Ready to generate AI images!")
            print("\nNext steps:")
            print("1. cd backend")
            print("2. python main.py")
            print("\nOr run: python start.py")
            print("=" * 50)
        else:
            print("\n❌ Installation completed but testing failed")
    else:
        print("\n❌ Installation failed")
        print("\n💡 Try running:")
        print("pip install torch diffusers transformers accelerate")

if __name__ == "__main__":
    main()
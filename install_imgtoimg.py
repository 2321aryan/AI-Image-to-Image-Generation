#!/usr/bin/env python3
"""
Installation script for imgtoimg.ai clone
Installs all necessary dependencies and sets up the environment
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_gpu():
    """Check for GPU availability"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU detected: {gpu_name}")
            return True
        else:
            print("⚠️  No GPU detected - will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet - GPU check will be done after installation")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    # Install PyTorch first (with CUDA support if available)
    system = platform.system().lower()
    if system == "windows":
        torch_command = "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    else:
        torch_command = "pip install torch torchvision torchaudio"
    
    if not run_command(torch_command, "Installing PyTorch"):
        return False
    
    # Install other dependencies
    if not run_command("pip install -r backend/requirements.txt", "Installing backend dependencies"):
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        "temp/uploads",
        "temp/results", 
        "temp/analysis",
        "temp/cache",
        "models"
    ]
    
    print("\n📁 Creating directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}")
    
    return True

def install_frontend():
    """Install frontend dependencies"""
    if not os.path.exists("frontend/package.json"):
        print("⚠️  Frontend package.json not found - skipping frontend installation")
        return True
    
    print("\n🌐 Installing frontend dependencies...")
    
    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found. Please install Node.js and npm first.")
        return False
    
    # Install dependencies
    if not run_command("cd frontend && npm install", "Installing frontend dependencies"):
        return False
    
    return True

def download_models():
    """Download initial models"""
    print("\n🤖 Downloading AI models...")
    print("Note: Models will be downloaded automatically on first use")
    print("This may take several minutes depending on your internet connection")
    
    # Create a simple test script to trigger model download
    test_script = """
import torch
from diffusers import StableDiffusionImg2ImgPipeline

print("Downloading Stable Diffusion 1.5...")
try:
    pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        safety_checker=None,
        requires_safety_checker=False
    )
    print("✅ Model downloaded successfully")
except Exception as e:
    print(f"⚠️  Model download will happen on first use: {e}")
"""
    
    with open("temp_model_download.py", "w") as f:
        f.write(test_script)
    
    try:
        run_command("python temp_model_download.py", "Downloading models")
    finally:
        if os.path.exists("temp_model_download.py"):
            os.remove("temp_model_download.py")
    
    return True

def main():
    """Main installation process"""
    print("🚀 imgtoimg.ai Installation Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup directories
    if not setup_directories():
        print("❌ Failed to setup directories")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check GPU after PyTorch installation
    check_gpu()
    
    # Install frontend
    if not install_frontend():
        print("❌ Failed to install frontend dependencies")
        sys.exit(1)
    
    # Download models (optional)
    download_models()
    
    print("\n" + "=" * 50)
    print("🎉 Installation completed successfully!")
    print("\nTo start the application:")
    print("1. Backend: python backend/main.py")
    print("2. Frontend: cd frontend && npm run dev")
    print("\nThen open http://localhost:3000 in your browser")
    print("\n⚠️  Note: First generation may take longer as models are loaded")

if __name__ == "__main__":
    main()
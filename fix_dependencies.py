#!/usr/bin/env python3
"""
Fix dependency conflicts for imgtoimg.ai
Resolves huggingface_hub and diffusers version conflicts
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def fix_dependencies():
    """Fix the dependency conflicts"""
    print("🔧 Fixing imgtoimg.ai Dependencies")
    print("=" * 40)
    
    # Navigate to backend directory
    if not os.path.exists("backend"):
        print("❌ Please run this from the project root directory")
        return False
    
    os.chdir("backend")
    
    # Step 1: Uninstall conflicting packages
    print("\n1. Removing conflicting packages...")
    packages_to_remove = [
        "diffusers", 
        "huggingface_hub", 
        "transformers", 
        "accelerate",
        "safetensors"
    ]
    
    for package in packages_to_remove:
        run_command(f"pip uninstall {package} -y", f"Removing {package}")
    
    # Step 2: Install PyTorch first (with CUDA support)
    print("\n2. Installing PyTorch with CUDA support...")
    if not run_command(
        "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118",
        "Installing PyTorch with CUDA"
    ):
        print("⚠️  CUDA installation failed, trying CPU version...")
        run_command(
            "pip install torch torchvision torchaudio",
            "Installing PyTorch (CPU)"
        )
    
    # Step 3: Install compatible AI packages in correct order
    print("\n3. Installing compatible AI packages...")
    ai_packages = [
        "huggingface_hub==0.19.4",
        "transformers==4.35.2", 
        "accelerate==0.24.1",
        "safetensors==0.4.0",
        "diffusers==0.24.0"
    ]
    
    for package in ai_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")
    
    # Step 4: Install remaining requirements
    print("\n4. Installing remaining requirements...")
    run_command("pip install -r requirements.txt", "Installing remaining packages")
    
    # Step 5: Verify installation
    print("\n5. Verifying installation...")
    try:
        import torch
        import diffusers
        import transformers
        import huggingface_hub
        
        print("✅ All packages imported successfully!")
        print(f"   PyTorch: {torch.__version__}")
        print(f"   Diffusers: {diffusers.__version__}")
        print(f"   Transformers: {transformers.__version__}")
        print(f"   CUDA Available: {torch.cuda.is_available()}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    """Main function"""
    success = fix_dependencies()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Dependencies fixed successfully!")
        print("\nNow you can start the backend:")
        print("   cd backend")
        print("   python main.py")
    else:
        print("❌ Some issues occurred during installation")
        print("\nTry manual installation:")
        print("   pip uninstall diffusers huggingface_hub transformers -y")
        print("   pip install huggingface_hub==0.19.4")
        print("   pip install diffusers==0.24.0")
        print("   pip install transformers==4.35.2")

if __name__ == "__main__":
    main()
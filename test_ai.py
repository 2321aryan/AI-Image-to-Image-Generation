#!/usr/bin/env python3
"""
Test script to verify AI image generation is working
"""

import sys
import os
sys.path.append('backend')

from backend.app.services.ai_service import ai_service
from PIL import Image
import tempfile

def test_ai_generation():
    print("🧪 Testing AI Image Generation")
    print("=" * 40)
    
    # Create a test image
    test_image = Image.new('RGB', (512, 512), color='blue')
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        test_image.save(tmp.name)
        
        try:
            print("📸 Generating test image...")
            
            # Test generation
            results = ai_service.generate_image(
                image_path=tmp.name,
                prompt="a beautiful landscape",
                num_images=1,
                num_inference_steps=20  # Faster for testing
            )
            
            if results and len(results) > 0:
                print(f"✅ Successfully generated {len(results)} images!")
                
                # Save result
                output_path = "test_output.png"
                results[0].save(output_path)
                print(f"💾 Saved test result to: {output_path}")
                
                if ai_service.model_loaded:
                    print("🤖 Real AI model is working!")
                else:
                    print("⚠️  Using demo mode (AI model not loaded)")
                
                return True
            else:
                print("❌ No images generated")
                return False
                
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return False
        finally:
            os.unlink(tmp.name)

def main():
    print("🚀 AI Image Generator Test")
    print("=" * 40)
    
    # Check if model is loaded
    if ai_service.model_loaded:
        print("✅ AI model loaded successfully")
    else:
        print("⚠️  AI model not loaded, will use demo mode")
    
    # Test generation
    if test_ai_generation():
        print("\n🎉 AI system is working!")
        print("\nYou can now run:")
        print("python start.py")
    else:
        print("\n❌ AI system test failed")
        print("\nTry running:")
        print("python install_ai.py")

if __name__ == "__main__":
    main()
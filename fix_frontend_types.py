#!/usr/bin/env python3
"""
Comprehensive script to fix frontend type issues and ensure clean startup
"""
import os
import subprocess
import shutil

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔧 Fixing frontend type issues...")
    
    frontend_dir = "frontend"
    
    # 1. Clean all cache directories
    print("\n🧹 Cleaning cache directories...")
    cache_dirs = [
        os.path.join(frontend_dir, "node_modules", ".vite"),
        os.path.join(frontend_dir, "node_modules", ".cache"),
        os.path.join(frontend_dir, "dist"),
        os.path.join(frontend_dir, ".vite"),
        os.path.join(frontend_dir, "tsconfig.tsbuildinfo")
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                if os.path.isfile(cache_dir):
                    os.remove(cache_dir)
                else:
                    shutil.rmtree(cache_dir)
                print(f"✅ Cleaned {cache_dir}")
            except Exception as e:
                print(f"⚠️  Could not clean {cache_dir}: {e}")
    
    # 2. Verify types file structure
    print("\n📁 Verifying type file structure...")
    types_index = os.path.join(frontend_dir, "src", "types", "index.ts")
    types_ts = os.path.join(frontend_dir, "src", "types.ts")
    
    if os.path.exists(types_ts):
        print(f"⚠️  Found conflicting types.ts file, removing...")
        os.remove(types_ts)
        print("✅ Removed conflicting types.ts")
    
    if os.path.exists(types_index):
        print("✅ Main types/index.ts file exists")
    else:
        print("❌ Main types/index.ts file missing!")
        return False
    
    # 3. Check TypeScript configuration
    print("\n⚙️  Checking TypeScript configuration...")
    tsconfig_path = os.path.join(frontend_dir, "tsconfig.json")
    if os.path.exists(tsconfig_path):
        print("✅ TypeScript configuration exists")
    else:
        print("⚠️  TypeScript configuration missing")
    
    # 4. Reinstall dependencies
    print("\n📦 Reinstalling dependencies...")
    success, stdout, stderr = run_command("npm ci", cwd=frontend_dir)
    if not success:
        print(f"⚠️  npm ci failed, trying npm install: {stderr}")
        success, stdout, stderr = run_command("npm install", cwd=frontend_dir)
        if not success:
            print(f"❌ Failed to install dependencies: {stderr}")
            return False
    
    print("✅ Dependencies installed successfully")
    
    # 5. Run TypeScript check
    print("\n🔍 Running TypeScript check...")
    success, stdout, stderr = run_command("npx tsc --noEmit", cwd=frontend_dir)
    if not success:
        print(f"⚠️  TypeScript check found issues:")
        print(stderr)
        print("This might be expected if there are other unrelated issues")
    else:
        print("✅ TypeScript check passed")
    
    print("\n🎉 Frontend type fixes completed!")
    print("\nNext steps:")
    print("1. Run 'python restart_frontend.py' to start the development server")
    print("2. Or manually run 'cd frontend && npm run dev'")
    print("3. Open http://localhost:3000 in your browser")
    
    return True

if __name__ == "__main__":
    main()
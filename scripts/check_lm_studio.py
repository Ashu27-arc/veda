"""
LM Studio API Status Checker and Helper
Checks if LM Studio is running and provides guidance
"""
import requests
import subprocess
import os
import sys

def check_lm_studio_status():
    """Check if LM Studio API is accessible"""
    print("🔍 Checking LM Studio API status...\n")
    
    try:
        # Try to connect to LM Studio API
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        
        if response.status_code == 200:
            models = response.json()
            print("✅ LM Studio API is RUNNING!")
            print(f"   URL: http://localhost:1234")
            
            if "data" in models and len(models["data"]) > 0:
                print(f"\n📦 Available Models ({len(models['data'])}):")
                for model in models["data"]:
                    print(f"   - {model.get('id', 'Unknown')}")
                return True
            else:
                print("\n⚠️  No models loaded!")
                print("   Please load a model in LM Studio")
                return False
        else:
            print(f"❌ LM Studio API returned error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ LM Studio API is NOT RUNNING")
        print("   Connection refused on http://localhost:1234\n")
        return False
    except Exception as e:
        print(f"❌ Error checking LM Studio: {e}")
        return False

def provide_fix_instructions():
    """Provide step-by-step instructions to fix LM Studio"""
    print("\n" + "="*60)
    print("📋 HOW TO FIX - LM Studio Setup")
    print("="*60)
    
    print("\n1️⃣  INSTALL LM Studio (if not installed)")
    print("   Download from: https://lmstudio.ai/")
    print("   Install and open the application")
    
    print("\n2️⃣  DOWNLOAD A MODEL")
    print("   - Click on 'Search' tab in LM Studio")
    print("   - Search for: 'Mistral 7B' or 'Llama 3'")
    print("   - Download any GGUF model (recommended: Q4 or Q5)")
    
    print("\n3️⃣  START THE LOCAL SERVER")
    print("   - Click on 'Local Server' tab")
    print("   - Select your downloaded model")
    print("   - Click 'Start Server' button")
    print("   - Wait for 'Server running on http://localhost:1234'")
    
    print("\n4️⃣  VERIFY IT'S WORKING")
    print("   - Run this script again: python scripts/check_lm_studio.py")
    print("   - Or start VEDA and test with a command")
    
    print("\n" + "="*60)
    print("💡 TIP: Keep LM Studio running in background for VEDA to work")
    print("="*60 + "\n")

def test_api_call():
    """Test actual API call with a sample prompt"""
    print("\n🧪 Testing API with sample prompt...\n")
    
    try:
        payload = {
            "model": "local-model",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in one sentence."}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {}).get("content", "")
                print(f"✅ API Response: {message}")
                print("\n🎉 LM Studio is working perfectly!")
                return True
        
        print(f"❌ API call failed: {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🤖 VEDA AI - LM Studio API Checker")
    print("="*60 + "\n")
    
    # Check if LM Studio is running
    is_running = check_lm_studio_status()
    
    if is_running:
        # Test actual API call
        test_api_call()
    else:
        # Provide fix instructions
        provide_fix_instructions()
        
        # Ask if user wants to try opening LM Studio
        print("\n❓ Do you want to try opening LM Studio? (y/n): ", end="")
        try:
            choice = input().lower().strip()
            if choice == 'y':
                print("\n🚀 Attempting to open LM Studio...")
                
                # Try common LM Studio paths
                possible_paths = [
                    r"C:\Users\{}\AppData\Local\LM Studio\LM Studio.exe".format(os.getenv('USERNAME')),
                    r"C:\Program Files\LM Studio\LM Studio.exe",
                    r"C:\Program Files (x86)\LM Studio\LM Studio.exe"
                ]
                
                opened = False
                for path in possible_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path])
                        print(f"✅ Opened LM Studio from: {path}")
                        print("\n⏳ Please:")
                        print("   1. Load a model")
                        print("   2. Start the local server")
                        print("   3. Run this script again to verify")
                        opened = True
                        break
                
                if not opened:
                    print("❌ Could not find LM Studio installation")
                    print("   Please open it manually from Start Menu")
        except:
            pass
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()

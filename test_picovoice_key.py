"""
Test Picovoice API Key
Quick script to verify if your Picovoice key is working
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_picovoice_key():
    """Test if Picovoice key is valid"""
    
    # Get the key
    access_key = os.getenv("PICOVOICE_ACCESS_KEY")
    
    print("=" * 60)
    print("🔑 PICOVOICE API KEY TEST")
    print("=" * 60)
    
    # Check if key exists
    if not access_key:
        print("❌ ERROR: PICOVOICE_ACCESS_KEY not found in .env file")
        return False
    
    # Check if key is placeholder
    if access_key in ["YOUR_PICOVOICE_ACCESS_KEY", "your_picovoice_access_key_here"]:
        print("❌ ERROR: Please replace placeholder with actual key")
        return False
    
    print(f"✅ Key found: {access_key[:20]}...{access_key[-10:]}")
    print(f"✅ Key length: {len(access_key)} characters")
    
    # Try to initialize Porcupine
    try:
        import pvporcupine
        print("\n🔄 Testing key with Porcupine...")
        
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=["computer"]
        )
        
        print("✅ SUCCESS! Porcupine initialized successfully")
        print(f"✅ Sample rate: {porcupine.sample_rate} Hz")
        print(f"✅ Frame length: {porcupine.frame_length}")
        print(f"✅ Version: {porcupine.version}")
        
        # Cleanup
        porcupine.delete()
        
        print("\n" + "=" * 60)
        print("🎉 YOUR PICOVOICE KEY IS WORKING PERFECTLY!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Possible issues:")
        print("   1. Invalid API key")
        print("   2. Key expired")
        print("   3. Network connection issue")
        print("   4. pvporcupine not installed (run: pip install pvporcupine)")
        return False

if __name__ == "__main__":
    test_picovoice_key()

"""
VEDA AI Training Script
Automatically train VEDA with your custom data
"""
import json
import os
from python_backend.self_learning import export_training_data, get_conversation_stats

def main():
    print("=" * 60)
    print("🤖 VEDA AI - Self-Training System")
    print("=" * 60)
    print()
    
    # Show stats
    stats = get_conversation_stats()
    print("📊 Current Stats:")
    print(f"   Total Conversations: {stats.get('total_conversations', 0)}")
    print(f"   Learned Responses: {stats.get('learned_responses', 0)}")
    print(f"   Positive Feedback: {stats.get('positive_feedback', 0)}")
    print(f"   Negative Feedback: {stats.get('negative_feedback', 0)}")
    print()
    
    print("🎯 Training Options:")
    print("1. Export learning data for Ollama training")
    print("2. Export learning data for Hugging Face fine-tuning")
    print("3. Train Ollama model with current data")
    print("4. View conversation history")
    print("5. Exit")
    print()
    
    choice = input("Select option (1-5): ").strip()
    
    if choice == "1":
        # Export for Ollama
        print("\n📤 Exporting data for Ollama...")
        result = export_training_data("ollama_training_data.txt")
        print(f"✅ {result}")
        print("\n📝 Next steps:")
        print("1. Run: ollama create veda-custom -f Modelfile")
        print("2. Update .env: OLLAMA_MODEL=veda-custom")
        
    elif choice == "2":
        # Export for Hugging Face
        print("\n📤 Exporting data for Hugging Face...")
        result = export_training_data("huggingface_training_data.json")
        print(f"✅ {result}")
        print("\n📝 Next steps:")
        print("1. Run: python")
        print("2. >>> from python_backend.huggingface_ai import fine_tune_model")
        print("3. >>> fine_tune_model('huggingface_training_data.json', './veda_model')")
        
    elif choice == "3":
        # Train Ollama
        print("\n🚀 Training Ollama model...")
        
        # Check if Ollama is installed
        import subprocess
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Ollama not found. Please install from https://ollama.ai")
                return
        except FileNotFoundError:
            print("❌ Ollama not found. Please install from https://ollama.ai")
            return
        
        # Export data
        export_training_data("ollama_training_data.txt")
        
        # Create Modelfile
        from python_backend.ollama_ai import train_ollama_model
        result = train_ollama_model("ollama_training_data.txt", "veda-custom")
        print(f"✅ {result}")
        
        # Train
        print("\n🔧 Creating custom model...")
        train_result = subprocess.run(
            ["ollama", "create", "veda-custom", "-f", "Modelfile"],
            capture_output=True,
            text=True
        )
        
        if train_result.returncode == 0:
            print("✅ Model trained successfully!")
            print("\n📝 Update .env file:")
            print("   OLLAMA_MODEL=veda-custom")
        else:
            print(f"❌ Training failed: {train_result.stderr}")
        
    elif choice == "4":
        # View history
        print("\n📜 Recent Conversations:")
        try:
            with open("data/conversation_history.json", 'r', encoding='utf-8') as f:
                conversations = json.load(f)
            
            # Show last 10
            for conv in conversations[-10:]:
                print(f"\n🗣️  User: {conv['user_input']}")
                print(f"🤖 VEDA: {conv['ai_response']}")
                if conv.get('feedback'):
                    print(f"   Feedback: {conv['feedback']}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif choice == "5":
        print("\n👋 Goodbye!")
        return
    
    else:
        print("\n❌ Invalid option")

if __name__ == "__main__":
    main()

"""
Hugging Face Transformers - Self-training AI
Install: pip install transformers torch
"""
from python_backend.logger import log_error, log_info

_model = None
_tokenizer = None

def load_model(model_name="microsoft/DialoGPT-medium"):
    """Load Hugging Face model (runs locally)"""
    global _model, _tokenizer
    
    if _model is None:
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            log_info(f"Loading model: {model_name}")
            _tokenizer = AutoTokenizer.from_pretrained(model_name)
            _model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Set pad token
            if _tokenizer.pad_token is None:
                _tokenizer.pad_token = _tokenizer.eos_token
            
            log_info("Model loaded successfully")
            return True
        except Exception as e:
            log_error(f"Model loading error: {e}")
            return False
    return True

def huggingface_response(prompt):
    """Get response from local Hugging Face model"""
    if not load_model():
        return None
    
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch
        
        # Encode input
        inputs = _tokenizer.encode(prompt + _tokenizer.eos_token, return_tensors="pt")
        
        # Generate response
        outputs = _model.generate(
            inputs,
            max_length=200,
            pad_token_id=_tokenizer.pad_token_id,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )
        
        # Decode response
        response = _tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove prompt from response
        if prompt in response:
            response = response.replace(prompt, "").strip()
        
        return response
        
    except Exception as e:
        log_error(f"Hugging Face error: {e}")
        return None

def fine_tune_model(training_data_file, output_model_path="./veda_finetuned"):
    """
    Fine-tune model with your custom data
    
    Args:
        training_data_file: Path to training data (JSON format)
        output_model_path: Where to save fine-tuned model
    
    Example training_data.json:
    [
        {"prompt": "Hello", "response": "Hi! How can I help?"},
        {"prompt": "Tum kaun ho", "response": "Main VEDA hoon"}
    ]
    """
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
        from datasets import Dataset
        import json
        
        # Load training data
        with open(training_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Prepare dataset
        texts = [f"User: {item['prompt']}\nVEDA: {item['response']}" for item in data]
        dataset = Dataset.from_dict({"text": texts})
        
        # Load base model
        model_name = "microsoft/DialoGPT-medium"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Tokenize dataset
        def tokenize_function(examples):
            return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_model_path,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            save_steps=100,
            save_total_limit=2,
            logging_steps=10
        )
        
        # Train
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset
        )
        
        log_info("Starting fine-tuning...")
        trainer.train()
        
        # Save model
        model.save_pretrained(output_model_path)
        tokenizer.save_pretrained(output_model_path)
        
        log_info(f"Model fine-tuned and saved to: {output_model_path}")
        return f"Success! Model saved to {output_model_path}"
        
    except Exception as e:
        log_error(f"Fine-tuning error: {e}")
        return f"Error: {e}"

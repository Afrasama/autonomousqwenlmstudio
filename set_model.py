#!/usr/bin/env python3
"""
Set the active LM Studio model for your robotics experiments
"""
import os

def set_model(model_choice):
    """Set the active model"""
    models = {
        "1": {
            "name": "Qwen2.5 7B Instruct",
            "model_id": "qwen2.5-7b-instruct-1m",
            "description": "General purpose instruction model"
        },
        "2": {
            "name": "Deepseek Coder 6.7B", 
            "model_id": "deepseek-coder-6.7b-kexer",
            "description": "Code generation and analysis model"
        }
    }
    
    if model_choice not in models:
        print("Invalid choice!")
        return False
    
    selected = models[model_choice]
    
    # Set environment variables
    env_vars = {
        "LLM_AGENT_BACKEND": "lmstudio",
        "LLM_AGENT_ENDPOINT": "http://localhost:1234/v1/chat/completions",
        "LLM_AGENT_MODEL": selected["model_id"],
        "LLM_AGENT_TIMEOUT_S": "60",
        "LLM_AGENT_USE_VISION": "0"
    }
    
    print(f"Setting model to: {selected['name']}")
    print(f"Model ID: {selected['model_id']}")
    print()
    
    for var, value in env_vars.items():
        os.environ[var] = value
        print(f"set {var}={value}")
    
    print(f"\n✅ Model configured: {selected['name']}")
    print("You can now run your robotics experiments!")
    
    return True

def main():
    print("Select Active Model for Robotics Experiments")
    print("=" * 50)
    print("1. Qwen2.5 7B Instruct - General purpose")
    print("2. Deepseek Coder 6.7B - Code focused")
    print()
    
    choice = input("Enter choice (1-2): ").strip()
    set_model(choice)

if __name__ == "__main__":
    main()

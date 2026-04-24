#!/usr/bin/env python3
"""
Configuration script for switching between different models in LM Studio
"""
import os
from pathlib import Path

def setup_lmstudio_config():
    """Setup environment variables for different LM Studio models"""
    
    print("LM Studio Model Configuration")
    print("=" * 40)
    print()
    
    # Available models
    models = {
        "1": {
            "name": "Qwen2.5 7B Instruct",
            "model_id": "qwen2.5-7b-instruct-q4_k_m.gguf",
            "description": "General purpose instruction model",
            "vision_capable": False
        },
        "2": {
            "name": "Deepseek Coder 6.7B", 
            "model_id": "deepseek-coder-6.7b-base-q4_k_m.gguf",
            "description": "Code generation and analysis model",
            "vision_capable": False
        },
        "3": {
            "name": "Custom Model",
            "model_id": "local-model",
            "description": "Use whatever model is loaded in LM Studio",
            "vision_capable": True
        }
    }
    
    print("Available models:")
    for key, model in models.items():
        vision_status = "✓ Vision" if model["vision_capable"] else "Text only"
        print(f"{key}. {model['name']} - {model['description']} ({vision_status})")
    
    print()
    choice = input("Select model (1-3): ").strip()
    
    if choice not in models:
        print("Invalid choice!")
        return
    
    selected_model = models[choice]
    
    # Environment configuration
    env_vars = {
        "LLM_AGENT_BACKEND": "lmstudio",
        "LLM_AGENT_ENDPOINT": "http://localhost:1234/v1/chat/completions", 
        "LLM_AGENT_MODEL": selected_model["model_id"],
        "LLM_AGENT_TIMEOUT_S": "60",
        "LLM_AGENT_USE_VISION": "1" if selected_model["vision_capable"] else "0"
    }
    
    print(f"\nConfiguring for: {selected_model['name']}")
    print("\nEnvironment variables to set:")
    
    for var, value in env_vars.items():
        print(f"set {var}={value}")
    
    # Create .env file for convenience
    env_file = Path(__file__).parent / ".env"
    with open(env_file, 'w') as f:
        f.write("# LM Studio Configuration\n")
        f.write(f"# Model: {selected_model['name']}\n")
        for var, value in env_vars.items():
            f.write(f"{var}={value}\n")
    
    print(f"\nConfiguration saved to: {env_file}")
    print("\nTo apply these variables in Windows Command Prompt:")
    print("  .env")
    print("\nTo apply these variables in PowerShell:")
    print("  Get-Content .env | ForEach-Object { Invoke-Expression $_ }")
    
    # Test configuration
    print(f"\nTesting configuration...")
    try:
        from reflection.llm_reflection_agent import LLMReflectionAgent
        
        agent = LLMReflectionAgent(
            backend=env_vars["LLM_AGENT_BACKEND"],
            endpoint=env_vars["LLM_AGENT_ENDPOINT"],
            model=env_vars["LLM_AGENT_MODEL"]
        )
        
        if agent.is_configured():
            print("✓ Agent configuration successful!")
            print(f"  Backend: {agent.backend}")
            print(f"  Model: {agent.model}")
            print(f"  Endpoint: {agent.endpoint}")
        else:
            print("⚠ Agent configuration incomplete - make sure LM Studio is running!")
            
    except ImportError as e:
        print(f"⚠ Could not test configuration: {e}")
        print("Make sure you're in the project directory with all dependencies installed")

if __name__ == "__main__":
    setup_lmstudio_config()

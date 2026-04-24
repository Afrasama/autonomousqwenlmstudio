#!/usr/bin/env python3
"""
Test the actual loaded models in LM Studio
"""
import requests
import json
from reflection.llm_reflection_agent import LLMReflectionAgent

def test_model_connection(model_name, model_id):
    """Test connection to a specific model"""
    print(f"\n{'='*50}")
    print(f"Testing {model_name}")
    print(f"Model ID: {model_id}")
    print('='*50)
    
    try:
        # Test basic connection first
        url = "http://localhost:1234/v1/chat/completions"
        payload = {
            "model": model_id,
            "messages": [
                {"role": "user", "content": "Say 'Hello, I am working!'"}
            ],
            "max_tokens": 10,
            "temperature": 0
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"[OK] Basic connection successful!")
            print(f"Response: {message}")
            
            # Now test with LLM Reflection Agent
            # Set environment variables for this test
            import os
            os.environ["LLM_AGENT_BACKEND"] = "lmstudio"
            os.environ["LLM_AGENT_ENDPOINT"] = "http://localhost:1234/v1/chat/completions"
            os.environ["LLM_AGENT_MODEL"] = model_id
            os.environ["LLM_AGENT_TIMEOUT_S"] = "60"
            os.environ["LLM_AGENT_USE_VISION"] = "0"
            
            agent = LLMReflectionAgent(
                backend="lmstudio",
                endpoint="http://localhost:1234/v1/chat/completions",
                model=model_id,
                timeout_s=60,
                use_vision=False
            )
            
            if agent.is_configured():
                print("[OK] LLM Reflection Agent configured!")
                
                # Test with simple robot scenario
                test_scene_info = {
                    "failure_type": "grasp_failure",
                    "pixel_error_x": 25.0,
                    "pixel_error_y": -15.0,
                    "retry_count": 2
                }
                
                test_policy = {
                    "x_offset": 0.0,
                    "y_offset": 0.0,
                    "grasp_height": 0.03,
                    "approach_height": 0.10,
                    "lift_height": 0.15,
                    "release_delay": 30
                }
                
                print("Testing robot reflection scenario...")
                decision = agent.reflect(test_scene_info, test_policy)
                
                print(f"Explanation: {decision.explanation}")
                print(f"Updates: {decision.updates}")
                print(f"Mode: {decision.mode}")
                
                return True
            else:
                print("[ERROR] LLM Reflection Agent not configured")
                return False
                
        else:
            print(f"[ERROR] Connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

def main():
    """Test all available models"""
    print("Testing Actual LM Studio Models")
    print("=" * 40)
    
    models_to_test = [
        ("Qwen2.5 7B Instruct", "qwen2.5-7b-instruct-1m"),
        ("Deepseek Coder 6.7B", "deepseek-coder-6.7b-kexer")
    ]
    
    results = {}
    
    for model_name, model_id in models_to_test:
        results[model_name] = test_model_connection(model_name, model_id)
    
    print(f"\n{'='*50}")
    print("Test Results Summary")
    print('='*50)
    
    for model_name, success in results.items():
        status = "[OK]" if success else "[FAIL]"
        print(f"{model_name}: {status}")
    
    # Create updated .env with correct model names
    print(f"\n{'='*50}")
    print("Creating updated configuration...")
    
    env_content = """# LM Studio Configuration - Updated with correct model names
LLM_AGENT_BACKEND=lmstudio
LLM_AGENT_ENDPOINT=http://localhost:1234/v1/chat/completions
LLM_AGENT_TIMEOUT_S=60
LLM_AGENT_USE_VISION=0

# Qwen2.5 7B Instruct
# LLM_AGENT_MODEL=qwen2.5-7b-instruct-1m

# Deepseek Coder 6.7B  
# LLM_AGENT_MODEL=deepseek-coder-6.7b-kexer
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("Configuration saved to .env")
    print("\nTo use a specific model, uncomment the corresponding LLM_AGENT_MODEL line")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Debug script for LM Studio connection issues
"""
import requests
import json
import time

def test_lmstudio_connection():
    """Test LM Studio server connection and model availability"""
    base_url = "http://localhost:1234"
    
    print("🔍 LM Studio Connection Debug")
    print("=" * 40)
    
    # Test 1: Server health
    print("1. Testing server health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"⚠️ Server responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return False
    
    # Test 2: Available models
    print("\n2. Checking available models...")
    try:
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            if models_data.get("data"):
                print("✅ Available models:")
                for i, model in enumerate(models_data["data"], 1):
                    model_id = model.get("id", "Unknown")
                    print(f"  {i}. {model_id}")
            else:
                print("❌ No models found - load a model in LM Studio")
                return False
        else:
            print(f"❌ Failed to get models: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Model check failed: {e}")
        return False
    
    # Test 3: Simple chat completion
    print("\n3. Testing chat completion...")
    try:
        payload = {
            "model": "local-model",
            "messages": [
                {"role": "user", "content": "Say 'Hello, I am working!'"}
            ],
            "max_tokens": 10,
            "temperature": 0
        }
        
        response = requests.post(f"{base_url}/v1/chat/completions", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ Chat completion successful!")
            print(f"Response: {message}")
        else:
            print(f"❌ Chat completion failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat completion error: {e}")
        return False
    
    # Test 4: JSON response format
    print("\n4. Testing JSON response format...")
    try:
        payload = {
            "model": "local-model",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Return only valid JSON."},
                {"role": "user", "content": 'Return {"status": "working", "message": "test successful"}'}
            ],
            "max_tokens": 50,
            "temperature": 0
        }
        
        response = requests.post(f"{base_url}/v1/chat/completions", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ JSON response received!")
            print(f"Response: {message}")
            
            # Try to parse as JSON
            try:
                parsed = json.loads(message)
                print(f"✅ JSON parsing successful!")
                print(f"Parsed: {parsed}")
            except json.JSONDecodeError:
                print(f"⚠️ JSON parsing failed - model may need better prompting")
        else:
            print(f"❌ JSON test failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ JSON test error: {e}")
    
    return True

def test_llm_reflection_agent():
    """Test the LLM Reflection Agent with LM Studio"""
    print("\n🤖 Testing LLM Reflection Agent")
    print("=" * 40)
    
    try:
        # Import the agent
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from reflection.llm_reflection_agent import LLMReflectionAgent
        
        # Create agent
        agent = LLMReflectionAgent(
            backend="lmstudio",
            endpoint="http://localhost:1234/v1/chat/completions",
            model="local-model",
            timeout_s=60,
            use_vision=False
        )
        
        if agent.is_configured():
            print("✅ LLM Reflection Agent configured!")
            print(f"Backend: {agent.backend}")
            print(f"Model: {agent.model}")
            print(f"Endpoint: {agent.endpoint}")
            
            # Test with simple scenario
            scene_info = {
                "failure_type": "grasp_failure",
                "pixel_error_x": 25.0,
                "pixel_error_y": -15.0,
                "retry_count": 1
            }
            
            policy = {
                "x_offset": 0.0,
                "y_offset": 0.0,
                "grasp_height": 0.03,
                "approach_height": 0.10,
                "lift_height": 0.15,
                "release_delay": 30
            }
            
            print("\n🧪 Testing reflection scenario...")
            start_time = time.time()
            decision = agent.reflect(scene_info, policy)
            elapsed = time.time() - start_time
            
            print(f"✅ Reflection completed in {elapsed:.2f}s")
            print(f"Explanation: {decision.explanation}")
            print(f"Updates: {decision.updates}")
            print(f"Mode: {decision.mode}")
            
        else:
            print("❌ LLM Reflection Agent not configured")
            return False
            
    except Exception as e:
        print(f"❌ LLM Reflection Agent test failed: {e}")
        return False
    
    return True

def main():
    """Main debug function"""
    print("🚀 LM Studio Debug Tool")
    print("This tool helps diagnose LM Studio connection issues")
    print()
    
    # Test basic connection
    if not test_lmstudio_connection():
        print("\n❌ Basic connection tests failed")
        print("Please check:")
        print("1. LM Studio is running")
        print("2. Server is enabled (port 1234)")
        print("3. A model is loaded")
        return
    
    # Test LLM Reflection Agent
    if test_llm_reflection_agent():
        print("\n🎉 All tests passed!")
        print("LM Studio integration is working correctly!")
    else:
        print("\n⚠️ Some tests failed")
        print("Check the error messages above for troubleshooting")

if __name__ == "__main__":
    main()

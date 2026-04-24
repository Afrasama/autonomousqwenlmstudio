#!/usr/bin/env python3
"""
Check LM Studio server status and available models
"""
import requests
import json
from urllib.parse import urljoin

def check_lmstudio_server():
    """Check if LM Studio server is running and get available models"""
    base_url = "http://localhost:1234"
    
    print("Checking LM Studio Server Status")
    print("=" * 40)
    
    try:
        # Check server health
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("[OK] LM Studio server is running")
        else:
            print(f"[WARN] LM Studio server responded with status {response.status_code}")
    except requests.exceptions.RequestException:
        print("[ERROR] LM Studio server is not running")
        print("Please start LM Studio and enable the server")
        return False
    
    try:
        # Get available models
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            print("\nAvailable Models:")
            
            if models_data.get("data"):
                for i, model in enumerate(models_data["data"], 1):
                    model_id = model.get("id", "Unknown")
                    print(f"{i}. {model_id}")
            else:
                print("No models found - make sure models are loaded in LM Studio")
                return False
        else:
            print(f"[ERROR] Failed to get models: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error checking models: {e}")
        return False
    
    return True

def test_connection():
    """Test basic connection with a simple request"""
    print("\nTesting Connection")
    print("=" * 40)
    
    try:
        url = "http://localhost:1234/v1/chat/completions"
        payload = {
            "model": "local-model",  # Use whatever model is loaded
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
            print("[OK] Connection test successful!")
            print(f"Response: {message}")
            return True
        else:
            print(f"[ERROR] Connection test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Connection test error: {e}")
        return False

def main():
    """Main status check"""
    print("LM Studio Status Checker")
    print("=" * 40)
    
    server_running = check_lmstudio_server()
    
    if server_running:
        test_connection()
    
    print("\nNext Steps:")
    print("1. Make sure LM Studio is running")
    print("2. Enable the server in LM Studio (Server tab)")
    print("3. Load your desired models in LM Studio")
    print("4. Run 'py setup_models.py' to configure")
    print("5. Run 'py test_new_models.py' to test")

if __name__ == "__main__":
    main()

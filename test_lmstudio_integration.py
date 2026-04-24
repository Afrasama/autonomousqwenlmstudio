#!/usr/bin/env python3
"""
Test LM Studio integration with the robotics system
"""
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reflection.llm_reflection_agent import LLMReflectionAgent

def test_lmstudio_integration():
    """Test LM Studio integration with the LLM Reflection Agent"""
    
    print("🧪 Testing LM Studio Integration")
    print("=" * 40)
    
    # Configure environment for LM Studio
    os.environ["LLM_AGENT_BACKEND"] = "lmstudio"
    os.environ["LLM_AGENT_ENDPOINT"] = "http://localhost:1234/v1/chat/completions"
    os.environ["LLM_AGENT_MODEL"] = "local-model"
    os.environ["LLM_AGENT_TIMEOUT_S"] = "60"
    os.environ["LLM_AGENT_USE_VISION"] = "0"
    
    try:
        # Create LLM Reflection Agent
        agent = LLMReflectionAgent()
        
        print(f"Backend: {agent.backend}")
        print(f"Model: {agent.model}")
        print(f"Endpoint: {agent.endpoint}")
        print(f"Configured: {agent.is_configured()}")
        
        if not agent.is_configured():
            print("❌ Agent not properly configured")
            print("Make sure LM Studio is running with a loaded model")
            return False
        
        # Test with a simple robotics scenario
        print("\n🤖 Testing robotics scenario...")
        
        scene_info = {
            "failure_type": "grasp_failure",
            "pixel_error_x": 25.0,
            "pixel_error_y": -15.0,
            "retry_count": 1,
            "cube_visible": True,
            "distance_to_goal": 0.15
        }
        
        policy = {
            "x_offset": 0.0,
            "y_offset": 0.0,
            "grasp_height": 0.03,
            "approach_height": 0.10,
            "lift_height": 0.15,
            "release_delay": 30
        }
        
        print("Scene info:")
        for key, value in scene_info.items():
            print(f"  {key}: {value}")
        
        print("\nCurrent policy:")
        for key, value in policy.items():
            print(f"  {key}: {value}")
        
        # Get decision from LM
        decision = agent.reflect(scene_info, policy)
        
        print(f"\n🧠 LLM Analysis:")
        print(f"Explanation: {decision.explanation}")
        print(f"Mode: {decision.mode}")
        print(f"Confidence: {decision.confidence}")
        
        if decision.updates:
            print(f"\n🔧 Suggested parameter updates:")
            for param, delta in decision.updates.items():
                old_value = policy.get(param, 0)
                new_value = old_value + delta
                print(f"  {param}: {old_value:+.3f} → {new_value:+.3f} (Δ{delta:+.3f})")
        else:
            print("\n🔧 No parameter updates suggested")
        
        print(f"\n✅ LM Studio integration test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_different_models():
    """Test different models if available"""
    print("\n🔄 Testing Different Models")
    print("=" * 40)
    
    # Common model names to try
    test_models = [
        "local-model",
        "qwen2.5-7b-instruct-1m",
        "deepseek-coder-6.7b-kexer"
    ]
    
    for model_name in test_models:
        print(f"\nTesting model: {model_name}")
        
        try:
            agent = LLMReflectionAgent(
                backend="lmstudio",
                model=model_name,
                timeout_s=30
            )
            
            if agent.is_configured():
                # Simple test
                scene_info = {"failure_type": "test", "retry_count": 0}
                policy = {"x_offset": 0.0}
                
                decision = agent.reflect(scene_info, policy)
                print(f"✅ {model_name}: {decision.explanation[:50]}...")
            else:
                print(f"❌ {model_name}: Not configured")
                
        except Exception as e:
            print(f"❌ {model_name}: {e}")

def main():
    """Main test function"""
    print("🚀 LM Studio Integration Test")
    print("This tests the LM Studio integration with your robotics system")
    print()
    
    # Basic integration test
    if test_lmstudio_integration():
        # Test different models
        test_different_models()
        
        print("\n🎉 Integration test completed!")
        print("\nYou can now run the full experiment:")
        print("python experiments/improved_kinematics_reflection.py")
    else:
        print("\n❌ Integration test failed")
        print("\nTroubleshooting:")
        print("1. Make sure LM Studio is running")
        print("2. Enable the server in LM Studio (port 1234)")
        print("3. Load a model in LM Studio")
        print("4. Run: python debug_lmstudio_connection.py")

if __name__ == "__main__":
    main()

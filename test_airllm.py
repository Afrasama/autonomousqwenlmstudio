import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from reflection.llm_reflection_agent import LLMReflectionAgent

def main():
    print("Testing LLMReflectionAgent with AirLLM backend...")
    
    # Initialize the agent with AirLLM backend
    agent = LLMReflectionAgent(backend="airllm")
    
    print(f"Backend set to: {agent.backend}")
    print(f"Model: {agent.model}")
    print(f"Endpoint: {agent.endpoint}")
    
    # Dummy scene info & policy
    scene_info = {
        "pixel_error_x": 10.0,
        "pixel_error_y": -5.0,
        "retry_count": 1,
        "failure_type": "placement_failure"
    }
    policy = {
        "x_offset": 0.0,
        "y_offset": 0.0,
        "grasp_height": 0.01,
        "approach_height": 0.1,
        "lift_height": 0.12,
        "release_delay": 0
    }
    
    print("\nCalling reflect()...")
    # This will trigger _query_airllm
    decision = agent.reflect(scene_info=scene_info, policy=policy)
    
    print("\nDecision Results:")
    print(f"Mode: {decision.mode}")
    print(f"Updates: {decision.updates}")
    print(f"Terminate: {decision.terminate}")
    print(f"Explanation: {decision.explanation}")

if __name__ == "__main__":
    main()

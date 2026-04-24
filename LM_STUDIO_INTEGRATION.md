# LM Studio Integration

This project supports **LM Studio** as a backend for the LLM reflection agent, allowing you to use local models for robotics error recovery.

## Quick Setup

### 1. Install and Configure LM Studio
1. Download and install [LM Studio](https://lmstudio.ai/)
2. Launch LM Studio and load a vision-capable model (recommended: LLaVA, Qwen-VL, or similar)
3. Enable the server in LM Studio:
   - Go to the "Server" tab
   - Ensure the server is running (default port: 1234)
   - Note the endpoint URL (usually `http://localhost:1234`)

### 2. Configure the Project
Run the setup script:
```bash
# Windows Command Prompt
setup_lmstudio.bat

# Windows PowerShell
.\setup_lmstudio.ps1
```

Or set environment variables manually:
```bash
export LLM_AGENT_BACKEND=lmstudio
export LLM_AGENT_ENDPOINT=http://localhost:1234/v1/chat/completions
export LLM_AGENT_MODEL=local-model
```

### 3. Test the Connection
```bash
python test_lmstudio_integration.py
```

### 4. Run Experiments
```bash
python experiments/improved_kinematics_reflection.py
```

## Supported Features

- **Vision Support**: Works with vision-capable models loaded in LM Studio
- **JSON Mode**: Uses structured responses for reliable parameter updates
- **Fallback Handling**: Automatically falls back to heuristic-based recovery if LM Studio is unavailable
- **Customizable**: Easy to adjust timeout, model selection, and other parameters

## Configuration Options

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `LLM_AGENT_BACKEND` | `lmstudio` | Backend to use (lmstudio, ollama, openai, airllm) |
| `LLM_AGENT_ENDPOINT` | `http://localhost:1234/v1/chat/completions` | LM Studio server endpoint |
| `LLM_AGENT_MODEL` | `local-model` | Model identifier (LM Studio uses loaded model) |
| `LLM_AGENT_TIMEOUT_S` | `60` | Request timeout in seconds |
| `LLM_AGENT_USE_VISION` | `1` | Enable vision processing (requires vision model) |

## Troubleshooting

### Connection Issues
- Ensure LM Studio server is running and accessible
- Check that the port (1234) is not blocked by firewall
- Verify a model is loaded in LM Studio

### Model Issues
- Use vision-capable models for best results (LLaVA, Qwen-VL, etc.)
- For text-only models, vision will be disabled automatically
- Larger models may require more VRAM and processing time

### Performance Tips
- Start with smaller models for testing
- Adjust timeout based on your hardware capabilities
- Consider using quantized models for faster inference

## Example Usage

```python
from reflection.llm_reflection_agent import LLMReflectionAgent

# Create LM Studio agent
agent = LLMReflectionAgent(
    backend="lmstudio",
    endpoint="http://localhost:1234/v1/chat/completions",
    model="local-model"
)

# Use in your robotics experiment
decision = agent.reflect(scene_info, policy, rgb=image_data)
print(f"Suggested updates: {decision.updates}")
```

## Integration with Existing Backends

LM Studio integration is fully compatible with existing backends. You can switch between backends by changing the `LLM_AGENT_BACKEND` environment variable:

- `lmstudio` - Use LM Studio (default when no API key is present)
- `ollama` - Use Ollama local server
- `openai` - Use OpenAI API (requires API key)
- `airllm` - Use AirLLM for large model inference

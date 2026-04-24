# Set up environment and run the AirLLM server
$env:AIRLLM_MODEL = "garage-bAInd/Platypus2-70B-instruct"
$env:AIRLLM_PORT = "8000"
$env:USE_CUDA = "1"  # Set to "0" for CPU if no GPU available

# Redirect HuggingFace cache to E: drive to resolve C: drive space issues
$env:HF_HOME = "E:\internship\hf_cache"

# Run with the virtual environment's python
.\airllm_env\Scripts\python.exe .\reflection\airllm_server.py

import json
import os
import sys
from flask import Flask, request, jsonify
from airllm import AutoModel

app = Flask(__name__)

# Configuration from environment variables
MODEL_NAME = os.getenv("AIRLLM_MODEL", "garage-bAInd/Platypus2-70B-instruct")
MAX_LENGTH = int(os.getenv("AIRLLM_MAX_LENGTH", "512"))
PORT = int(os.getenv("AIRLLM_PORT", "8000"))

print(f"Loading AirLLM model: {MODEL_NAME}...")
# AirLLM optimizes memory by loading layers one by one.
# This may take some time depending on your disk speed and model size.
try:
    model = AutoModel.from_pretrained(MODEL_NAME)
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    
    # Construct prompt from messages
    prompt = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        prompt += f"{role.upper()}: {content}\n"
    
    # We guide the model to start the JSON response
    prompt += "\nASSISTANT: {\n  \"explanation\": \""
    
    print(f"Generating response for prompt length: {len(prompt)}")
    
    try:
        input_tokens = model.tokenizer(
            [prompt],
            return_tensors="pt",
            return_attention_mask=False,
            truncation=True,
            max_length=MAX_LENGTH,
            padding=False
        )
        
        # Determine device
        device = "cuda" if os.getenv("USE_CUDA", "1") == "1" else "cpu"
        
        # Generation with AirLLM
        output = model.generate(
            input_tokens['input_ids'].to(device),
            max_new_tokens=256,
            use_cache=True,
            return_dict_in_generate=True
        )
        
        response_text = model.tokenizer.decode(output.sequences[0], skip_special_tokens=True)
        
        # Extract only the assistant's part
        if "ASSISTANT:" in response_text:
            response_text = response_text.split("ASSISTANT:")[-1].strip()
        
        # Ensure it's valid JSON (starts with {)
        if not response_text.startswith("{"):
            response_text = "{" + response_text
            
        print(f"Generated response: {response_text}")

        return jsonify({
            "message": {
                "role": "assistant",
                "content": response_text
            }
        })
    except Exception as e:
        print(f"Error during generation: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "running", "model": MODEL_NAME})

if __name__ == "__main__":
    print(f"AirLLM server listening on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT)

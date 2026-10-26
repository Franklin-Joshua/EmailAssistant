import os, requests
from datetime import datetime

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def ask_ollama(prompt, model="qwen3:4b", temperature=0.3):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False,
              "think": False, "options": {"temperature": temperature}},
        timeout=180
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()

def check_ollama(model="qwen3:4b"):
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        response.raise_for_status()
        models = [m.get("name", "") for m in response.json().get("models", [])]
        if any(m == model or m.startswith(model + ":") for m in models):
            return True, f"Connected. Model '{model}' is installed."
        return False, f"Ollama is running, but '{model}' is not installed. Run: ollama pull {model}"
    except Exception as e:
        return False, f"Cannot connect to Ollama at {OLLAMA_URL}. Start Ollama and retry. Details: {e}"

def save_reply(data):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "generated_reply.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write("\\n" + "="*70 + "\\n")
        f.write(f"Date: {data['date']}\\nCustomer Name: {data['name']}\\n")
        f.write(f"Subject: {data['subject']}\\nIntent: {data['intent']}\\n")
        f.write(f"Customer Email: {data['email']}\\n\\nGenerated Reply:\\n{data['reply']}\\n")
    return path

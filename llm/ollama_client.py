import requests

def ollama_generate(prompt: str, model: str = "mistral") -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 300  # cap output length so it doesn't run forever
        }
    }

    # Give the local model more time (5–10 minutes is normal on some machines)
    r = requests.post(url, json=payload, timeout=600)
    r.raise_for_status()
    return r.json()["response"]

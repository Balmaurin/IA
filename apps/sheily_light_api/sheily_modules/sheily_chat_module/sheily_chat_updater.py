import requests

OLLAMA_PULL_URL = "http://localhost:11434/api/pull"

def download_model(model_name: str) -> dict:
    payload = {"name": model_name}
    try:
        r = requests.post(OLLAMA_PULL_URL, json=payload, timeout=600)
        r.raise_for_status()
        return {"status": "downloaded", "model": model_name}
    except Exception as e:
        return {"error": str(e)}

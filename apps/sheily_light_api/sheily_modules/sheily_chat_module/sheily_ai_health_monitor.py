import requests

OLLAMA_URL = "http://localhost:11434/api/tags"

def check_ollama_health() -> bool:
    try:
        r = requests.get(OLLAMA_URL, timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def list_available_models() -> list:
    try:
        r = requests.get(OLLAMA_URL, timeout=5)
        if r.status_code == 200:
            return [model["name"] for model in r.json().get("models", [])]
    except Exception:
        pass
    return []

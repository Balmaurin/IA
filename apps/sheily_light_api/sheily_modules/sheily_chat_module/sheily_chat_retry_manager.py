import requests

CENTRAL_URL = "https://sheily-central.example.com/api/chat"


def chat_with_fallback(prompt: str, user: str) -> str:
    payload = {"message": prompt, "user": user}
    try:
        r = requests.post(CENTRAL_URL, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data.get("answer", "")
    except Exception as e:
        return f"Error: No se pudo obtener respuesta de la central ({e})"

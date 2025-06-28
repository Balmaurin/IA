import requests

CENTRAL_URL = "https://sheily-central.example.com/api"


def sync_user(user: str, data: dict) -> dict:
    try:
        r = requests.post(f"{CENTRAL_URL}/users/sync", json={"user": user, "data": data}, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def sync_tokens(user: str, tokens: int) -> dict:
    try:
        r = requests.post(f"{CENTRAL_URL}/tokens/report", json={"user": user, "tokens": tokens}, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

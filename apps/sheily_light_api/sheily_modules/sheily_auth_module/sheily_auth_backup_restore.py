import json
import base64
from typing import Dict


def export_backup(payload: Dict):
    # Simulación: exporta usuario y hash como backup cifrado (solo ejemplo)
    username = payload["username"]
    USERS_DB = payload.get("USERS_DB", {})
    if username not in USERS_DB:
        return {"error": "User not found"}
    backup = {"username": username, "hash": USERS_DB[username]}
    encoded = base64.b64encode(json.dumps(backup).encode()).decode()
    return {"backup": encoded}


def import_backup(payload: Dict):
    # Simulación: importa backup
    encoded = payload["backup"]
    backup = json.loads(base64.b64decode(encoded.encode()).decode())
    USERS_DB = payload.get("USERS_DB", {})
    USERS_DB[backup["username"]] = backup["hash"]
    return {"status": "restored"}

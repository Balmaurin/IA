import json
import base64

def export_tokens_backup(user: str):
    from .sheily_token_operations import TOKENS_DB
    backup = {"user": user, "balance": TOKENS_DB.get(user, 0)}
    encoded = base64.b64encode(json.dumps(backup).encode()).decode()
    return {"backup": encoded}

def import_tokens_backup(user: str, backup_file: str):
    from .sheily_token_operations import TOKENS_DB
    backup = json.loads(base64.b64decode(backup_file.encode()).decode())
    if backup["user"] != user:
        return {"error": "User mismatch"}
    TOKENS_DB[user] = backup["balance"]
    return {"status": "restored", "balance": TOKENS_DB[user]}

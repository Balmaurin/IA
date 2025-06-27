TOKENS_DB = {}

def add_token(user: str, amount: int):
    TOKENS_DB.setdefault(user, 0)
    TOKENS_DB[user] += amount
    return {"status": "added", "balance": TOKENS_DB[user]}

def get_balance(user: str):
    return {"user": user, "balance": TOKENS_DB.get(user, 0)}

def sync_tokens(user: str):
    # Simulación: sincroniza con la central (mock)
    return {"status": "synced", "user": user, "balance": TOKENS_DB.get(user, 0)}

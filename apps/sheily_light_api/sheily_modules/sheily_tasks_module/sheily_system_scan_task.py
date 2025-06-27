def run_system_scan(user: str, task: str = "scan"):
    # Simulación de escaneo: siempre retorna OK
    return {"user": user, "task": task, "status": "ok"}

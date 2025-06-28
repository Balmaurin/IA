"""SHEILY-light scaffold generator.
Creates missing directories, __init__.py and minimal stubs without touching existing code.
Run once with: python setup_scaffold.py
"""

import os
from pathlib import Path

aProjectRoot = Path(__file__).resolve().parent
apps_dir = aProjectRoot / "apps" / "sheily_light_api"
routers_dir = apps_dir / "sheily_routers"
core_dir = apps_dir / "sheily_core"
modules_base = apps_dir / "sheily_modules"


# ------------- helpers -----------------
def ensure_file(path: Path, content: str = ""):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[CREATE]", path.relative_to(aProjectRoot))


# ------------- main.py ------------------
main_py = apps_dir / "main.py"
main_py_content = (
    "from fastapi import FastAPI\n"
    "from sheily_core.orchestrator import orchestrator_boot\n"
    "from sheily_routers.sheily_status_router import router as status_router\n\n"
    'app = FastAPI(title="Shaley Orchestrator API")\n'
    'app.include_router(status_router, prefix="/status")\n\n'
    '@app.on_event("startup")\n'
    "async def startup_event():\n"
    "    orchestrator_boot()\n\n"
    '@app.get("/")\n'
    "async def root():\n"
    '    return {"message": "SHEILY-light API running"}\n'
)
ensure_file(main_py, main_py_content)

# ------------- core orchestrator ---------
ensure_file(core_dir / "__init__.py", "")
orc_py = core_dir / "orchestrator.py"
orc_content = "def orchestrator_boot():\n" "    print('Shaley Orchestrator arrancó correctamente.')\n"
ensure_file(orc_py, orc_content)

# ------------- routers -----------------
router_names = ["auth", "chat", "tokens", "tasks", "status", "config"]
for name in router_names:
    path = routers_dir / f"sheily_{name}_router.py"
    content = (
        "from fastapi import APIRouter\n\n"
        "router = APIRouter()\n\n"
        "@router.get('/ping')\n"
        "async def ping():\n"
        "    return {'ok': True}\n"
    )
    ensure_file(path, content)

ensure_file(routers_dir / "__init__.py", "\n")

# ------------- modules ------------------
module_groups = {
    "core": ["event_bus", "system_state", "config_manager"],
    "monitoring": ["sheily_node_status_monitor"],
    "config": ["sheily_user_config_manager"],
    "tokens": ["sheily_token_operations", "sheily_token_backup_restore"],
    "chat": ["sheily_chat_event_logger", "sheily_chat_retry_manager"],
    "tasks": ["sheily_system_scan_task"],
}
# Add extensive security/privacy stubs (short list for demo)
security_list = ["firewall_controller", "anti_tracking_module", "vpn_controller"]
module_groups["security_privacy"] = security_list

for group, mods in module_groups.items():
    group_dir = modules_base / group
    for mod in mods:
        # subdir path with module name directory
        mod_dir = group_dir / mod
        ensure_file(mod_dir / "__init__.py", "")
        ensure_file(mod_dir / "core.py", "def init():\n    pass\n")

print("✅ Scaffolding completado. Ejecuta: uvicorn apps.sheily_light_api.main:app --reload")

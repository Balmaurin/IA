"""Generate remaining SHEILY-light project scaffold.
Creates directories/files only if missing, with minimal placeholder content.
Run: python setup_full_scaffold.py
"""
from pathlib import Path
import textwrap
import yaml

ROOT = Path(__file__).resolve().parent

# Helper

def ensure(path: Path, content: str = ""):
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("[CREATE]", path.relative_to(ROOT))

# Root-level files
ensure(ROOT / "README.md", """# SHEILY-light\n\nLocal AI node with FastAPI backend, React/Vite frontend, and Ollama Llama3 integration.\n""")

docker_compose_prod = textwrap.dedent("""
version: '3.9'
services:
  api:
    build: ./apps/sheily_light_api
    command: uvicorn sheily_main_api:app --host 0.0.0.0 --port 8000
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - db
  web:
    build: ./web
    env_file: .env
    ports:
      - "3000:80"
    depends_on:
      - api
  db:
    image: postgres:15
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: sheily
    volumes:
      - pgdata:/var/lib/postgresql/data
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
volumes:
  pgdata:
  ollama_data:
""")
ensure(ROOT / "docker-compose.prod.yml", docker_compose_prod)

ensure(ROOT / ".env.example", "API_SECRET=changeme\nDATABASE_URL=postgresql://user:pass@db:5432/sheily\n")

# sheily_config
ensure(ROOT / "sheily_config/dev.yaml", "debug: true\n")
ensure(ROOT / "sheily_config/prod.yaml", "debug: false\n")

# sheily_docs
docs = {
    "SHEILY_SETUP.md": "## Instalación\n\n1. Requisitos...\n",
    "SHEILY_ARCHITECTURE.md": "## Arquitectura\n\nDescripción de módulos y flujo.\n",
    "SHEILY_API_REFERENCE.md": "## Endpoints\n\nDocumentación de la API REST.\n",
    "SHEILY_TEST_GUIDE.md": "## Pruebas\n\nCómo ejecutar la suite de tests.\n",
}
for name, content in docs.items():
    ensure(ROOT / "sheily_docs" / name, content)

# sheily_vault placeholder
ensure(ROOT / "sheily_vault/.gitkeep", "")

# sheily_tests E2E skeletons
for test in [
    "test_sheily_full_system.py",
    "test_sheily_end_to_end.py",
    "test_sheily_network_integration.py",
]:
    ensure(ROOT / "sheily_tests" / test, "def test_placeholder():\n    assert True\n")

# scripts
ensure(ROOT / "scripts/deploy.sh", "#!/usr/bin/env bash\nset -e\ndocker-compose -f docker-compose.prod.yml up -d --build\n")
ensure(ROOT / "scripts/init_project.sh", "#!/usr/bin/env bash\npython -m venv .venv && source .venv/bin/activate && pip install -r apps/sheily_light_api/requirements.txt\n")

# Backend core
api_root = ROOT / "apps" / "sheily_light_api"
ensure(api_root / "__init__.py", "")
ensure(api_root / "sheily_main_api.py", textwrap.dedent("""
from fastapi import FastAPI
from .sheily_routers import (
    sheily_auth_router,
    sheily_chat_router,
    sheily_tokens_router,
    sheily_backup_router,
    sheily_tasks_router,
    sheily_status_router,
    sheily_config_router,
)

app = FastAPI(title="SHEILY-light API")

routers = [
    sheily_auth_router.router,
    sheily_chat_router.router,
    sheily_tokens_router.router,
    sheily_backup_router.router,
    sheily_tasks_router.router,
    sheily_status_router.router,
    sheily_config_router.router,
]
for r in routers:
    app.include_router(r)

@app.get("/")
async def root():
    return {"message": "SHEILY-light API running"}
"""))

core_dir = api_root / "core"
ensure(core_dir / "__init__.py", "")
ensure(core_dir / "config.py", "SECRET_KEY = 'changeme'\n")
ensure(core_dir / "database.py", "from sqlalchemy import create_engine\nengine = create_engine('sqlite:///sheily.db', echo=False)\n")
ensure(core_dir / "logging_config.py", "import logging, sys\nlogging.basicConfig(stream=sys.stdout, level=logging.INFO)\n")

# Routers
backup_router_code = textwrap.dedent("""
from fastapi import APIRouter

router = APIRouter(prefix="/backup", tags=["backup"])

@router.post("/create")
async def create_backup():
    return {"detail": "backup created"}

@router.post("/restore")
async def restore_backup():
    return {"detail": "backup restored"}
""")
ensure(api_root / "sheily_routers" / "sheily_backup_router.py", backup_router_code)

# Helper to create stub module files
modules = {
    "sheily_auth_module": ["sheily_user_manager.py", "sheily_jwt_manager.py"],
    "sheily_chat_module": ["sheily_chat_service.py"],
    "sheily_tokens_module": ["sheily_token_vault_manager.py", "sheily_token_service.py"],
    "sheily_backup_module": ["sheily_backup_manager.py", "sheily_restore_service.py"],
    "sheily_orchestrator_module": ["sheily_node_orchestrator.py"],
    "sheily_comms_module": ["sheily_central_integration.py"],
    "sheily_tasks_module": ["sheily_scheduled_tasks.py"],
    "sheily_monitoring_module": ["sheily_monitoring_service.py"],
    "sheily_logs_module": ["sheily_logs_service.py"],
    "sheily_updater_module": ["sheily_auto_updater.py"],
    "sheily_audit_module": ["sheily_audit_manager.py"],
    "sheily_config_module": ["sheily_config_manager.py"],
}
for mod_dir, files in modules.items():
    base = api_root / "sheily_modules" / mod_dir
    ensure(base / "__init__.py", "")
    for f in files:
        ensure(base / f, f"""def placeholder():\n    return '{f} works'\n""")

# Backend tests skeleton
tests_dir = api_root / "sheily_tests"
unit_tests = [
    "test_sheily_auth_module.py",
    "test_sheily_chat_module.py",
    "test_sheily_tokens_module.py",
    "test_sheily_backup_module.py",
    "test_sheily_orchestrator_module.py",
    "test_sheily_comms_module.py",
    "test_sheily_tasks_module.py",
    "test_sheily_logs_module.py",
    "test_sheily_updater_module.py",
    "test_sheily_monitoring_module.py",
    "test_sheily_audit_module.py",
    "test_sheily_config_module.py",
    "test_sheily_main_api.py",
]
for t in unit_tests:
    ensure(tests_dir / t, "def test_placeholder():\n    assert True\n")

print("✅ Full project scaffold complete.")

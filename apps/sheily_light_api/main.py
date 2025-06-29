import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

# Importaciones de la aplicación
from sheily_light_api.sheily_core.orchestrator import orchestrator_boot
from sheily_light_api.sheily_routers.sheily_auth_router import router as auth_router
from sheily_light_api.sheily_routers.sheily_chat_router import router as chat_router
from sheily_light_api.sheily_routers.sheily_status_router import router as status_router

# Configuración de entorno
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

# Lista de orígenes permitidos para CORS
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite por defecto
    "http://127.0.0.1:5173",  # Alternativa local
    "http://localhost:8001",  # Backend
    "http://127.0.0.1:8001",  # Alternativa backend
]

# Configuración de Redis
REDIS_URL = "redis://localhost:6379"

app = FastAPI(
    title="Sheily Light API",
    version="0.1.0",
    debug=DEBUG,
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None,
)

# --- Middlewares ---
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Compresión GZIP
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Redirección HTTPS en producción
if not DEBUG:
    app.add_middleware(HTTPSRedirectMiddleware)


# Configuración de caché
@app.on_event("startup")
async def setup_redis_cache():
    """Configura la caché de Redis para la aplicación."""
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# Configuración de la aplicación
@app.on_event("startup")
async def startup():
    """Configuración inicial de la aplicación."""
    await setup_redis_cache()
    await orchestrator_boot()


# --- Fin Middlewares ---

# Configuración de rutas
# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(status_router, prefix="/api/status", tags=["status"])


# Eliminamos esta función duplicada ya que su lógica se movió a la función startup()


@app.get("/")
async def root():
    return {"message": "SHEILY-light API running"}


@app.get("/api/utils/time")
async def get_time():
    return {"time": datetime.now().isoformat()}

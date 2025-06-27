from fastapi import FastAPI
from sheily_light_api.sheily_core.orchestrator import orchestrator_boot
from sheily_routers.sheily_status_router import router as status_router
from sheily_routers.sheily_chat_router import router as chat_router
from sheily_routers.sheily_auth_router import router as auth_router

app = FastAPI(title="Shaley Orchestrator API")

# --- CORS Middleware ---
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia a ["http://localhost:3000"] si quieres restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Fin CORS ---

app.include_router(status_router, prefix="/status")
app.include_router(chat_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    orchestrator_boot()

@app.get("/")
async def root():
    return {"message": "SHEILY-light API running"}

from datetime import datetime

@app.get("/api/utils/time")
async def get_time():
    return {"time": datetime.now().isoformat()}

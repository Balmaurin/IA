# SHEILY-light Main API Entry Point
from fastapi import FastAPI
from sheily_light_api.sheily_routers.sheily_auth_router import router as auth_router
from sheily_light_api.sheily_routers.sheily_chat_router import router as chat_router
from sheily_light_api.sheily_routers.sheily_tokens_router import router as tokens_router
from sheily_light_api.sheily_routers.sheily_export_router import router as export_router
from sheily_light_api.sheily_routers.sheily_reward_router import router as reward_router
from sheily_light_api.sheily_routers.sheily_tasks_router import router as tasks_router
from sheily_light_api.sheily_routers.sheily_status_router import router as status_router
from sheily_light_api.sheily_routers.sheily_config_router import router as config_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SHEILY-light API", version="1.0.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(tokens_router, prefix="/api/tokens", tags=["tokens"])
app.include_router(export_router, prefix="/api/export", tags=["export"])
app.include_router(reward_router, prefix="/api/reward", tags=["reward"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(status_router, prefix="/api/status", tags=["status"])
app.include_router(config_router, prefix="/api/config", tags=["config"])
from sheily_light_api.sheily_routers.sheily_utils_router import router as utils_router
app.include_router(utils_router, prefix="/api", tags=["utils"])

@app.get("/")
def root():
    return {"message": "SHEILY-light API is running"}

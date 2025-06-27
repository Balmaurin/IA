from fastapi import APIRouter
from sheily_modules.sheily_config_module.sheily_user_config_manager import get_config, update_config

router = APIRouter()

@router.get("")
def config():
    return get_config()

@router.post("/update")
def update(payload: dict):
    return update_config(payload)

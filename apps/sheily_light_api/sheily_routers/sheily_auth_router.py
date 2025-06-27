from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sheily_light_api.dependencies import get_current_user
from sheily_light_api.models import User
from sheily_light_api.sheily_modules.sheily_auth_module \
    .sheily_user_manager import (
        register_user,
        login_user,
        logout_user
    )

router = APIRouter(prefix="/auth", tags=["auth"])

class Credentials(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(creds: Credentials):
    return register_user(creds.model_dump())


@router.post("/login")
def login(creds: Credentials):
    return login_user(creds.model_dump())


@router.post("/logout")
def logout(user: User = Depends(get_current_user)):
    return logout_user({"user": user.username})


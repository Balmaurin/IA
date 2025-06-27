from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..dependencies import get_current_user, get_db_dep
from ..models import User
from ..sheily_modules.sheily_tokens_module.sheily_token_service import get_balance, add_tokens

router = APIRouter(prefix="/tokens", tags=["tokens"])

@router.get("")
def balance(user: User = Depends(get_current_user), db: Session = Depends(get_db_dep)):
    return {"balance": get_balance(db, user)}

class TokenAmount(BaseModel):
    amount: int


@router.post("/add")
def add_tokens_endpoint(payload: TokenAmount, user: User = Depends(get_current_user), db: Session = Depends(get_db_dep)):
    new_balance = add_tokens(db, user, payload.amount)
    return {"balance": new_balance}

@router.post("/sync")
def sync(payload: dict):
    return sync_tokens(payload["user"])

@router.post("/backup")
def backup(payload: dict):
    return export_tokens_backup(payload["user"])

@router.post("/restore")
def restore(payload: dict):
    return import_tokens_backup(payload["user"], payload["backup_file"])

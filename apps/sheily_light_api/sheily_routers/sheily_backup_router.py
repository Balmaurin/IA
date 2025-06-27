
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..dependencies import get_current_user, get_db_dep
from ..models import User
from ..sheily_modules.sheily_backup_module.sheily_backup_manager import backup_manager

router = APIRouter(prefix="/backup", tags=["backup"])

class BackupRequest(BaseModel):
    password: str


@router.post("/create")
async def create_backup(req: BackupRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db_dep)):
    from ..sheily_modules.sheily_tokens_module.sheily_token_service import get_balance

    user_data = {
        "username": user.username,
        "tokens": get_balance(db, user),
    }
    path = backup_manager.create_backup(user_data, req.password)
    if not path:
        return {"detail": "backup error"}
    return {"backup_path": path}

class RestoreRequest(BaseModel):
    backup_path: str
    password: str


@router.post("/restore")
async def restore_backup(req: RestoreRequest, user: User = Depends(get_current_user)):
    data = backup_manager.restore_backup(req.backup_path, req.password)
    return {"data": data}

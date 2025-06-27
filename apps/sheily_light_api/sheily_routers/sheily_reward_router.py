"""Webhook to receive token rewards from SHEILY-CORE."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..dependencies import get_db_dep
from ..models import User
from ..sheily_modules.sheily_tokens_module.sheily_token_service import (
    add_tokens,
)

from ..sheily_modules.sheily_security.webhook_verifier import verify as verify_signature

SECRET = None  # legacy shared secret disabled

router = APIRouter(prefix="/reward", tags=["reward"])


class RewardPayload(BaseModel):
    user: str  # username
    amount: int
    tx_hash: str | None = None


@router.post("/notify")
async def notify_reward(request: Request, payload: RewardPayload, db: Session = Depends(get_db_dep)):
    raw_body = await request.body()
    verify_signature(request.headers, raw_body)
    user = db.query(User).filter(User.username == payload.user).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    new_balance = add_tokens(db, user, payload.amount)
    return {"balance": new_balance}
